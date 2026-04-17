from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from dotenv import load_dotenv
import os
from werkzeug.utils import secure_filename
from flask import session
from re import match #Validação de senha
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from uuid import uuid4 #Renomeio do arquivo (Evita colisão de nomes)


load_dotenv(dotenv_path="C:\\tocadospeludos\\.env") #Alterado para rodar no linux

app = Flask(
    __name__, 
    template_folder="C:\\tocadospeludos\\template",
    static_folder="C:\\tocadospeludos\\static"
    ) #Alterado para rodar no linux

app.secret_key = "chave-secreta"

UPLOAD_FOLDER = "C:\\tocadospeludos\\static\\uploads" #Alterado para rodar no linux

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"} #Extensões válidas para upload de imagem
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        connection_timeout=5
    )

def valida_extensao(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM adotantes WHERE email=%s", (email,))
        usuario = cursor.fetchone()
        cursor.close()
        conn.close()

        if usuario and check_password_hash(usuario["senha"], senha):
            session["id_adotante"] = usuario["id_adotante"]  # guarda na sessão
            return redirect(url_for("preferencias"))
        else:
            return render_template("login.html", erro="Email ou senha incorretos")

    return render_template("login.html")


@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/main_screen")
def main_screen():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM adotantes")
    adotantes = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("main_screen.html", adotantes=adotantes)

@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")

@app.route("/contato", methods=["GET", "POST"])
def contato():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        mensagem = request.form.get("mensagem")
        if not nome or not email or not mensagem:
            return render_template("contato.html", erro="Todos os campos são obrigatórios")

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "INSERT INTO contato (email, mensagem) VALUES (%s, %s)",
            (email, mensagem)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return render_template("contato.html", sucesso="Mensagem registrada com sucesso!")
    
    return render_template("contato.html")

@app.route("/preferencias", methods=["GET", "POST"])
def preferencias():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # GET → carregar raças filtradas
    if request.method == "GET":
        animal = request.args.get("animal")
        sexo = request.args.get("sexo")

        if animal and sexo:
            cursor.execute("SELECT DISTINCT raca FROM pets WHERE animal=%s AND sexo=%s", (animal, sexo))
            racas = cursor.fetchall()
        else:
            racas = []

        cursor.close()
        conn.close()
        return render_template("preferencias.html", racas=racas, animal=animal, sexo=sexo)

    # POST → salvar adoção
    if request.method == "POST":
        animal = request.form.get("animal")
        sexo = request.form.get("sexo")
        raca = request.form.get("raca")
        id_adotante = session.get("id_adotante")

        cursor.execute(
            "SELECT id_pet FROM pets WHERE animal=%s AND sexo=%s AND raca=%s LIMIT 1",
            (animal, sexo, raca)
        )
        pet = cursor.fetchone()

        if pet:
            cursor.execute(
                "INSERT INTO adocoes (id_adotante, id_pet) VALUES (%s, %s)",
                (id_adotante, pet["id_pet"])
            )
            conn.commit()

        cursor.close()
        conn.close()
        return redirect(url_for("preferencias"))


@app.route("/salvar", methods=["POST"])
def salvar():
    nome = request.form["nome"]

    #Validação se o e-mail existe
    email = request.form["email"]
    if not match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.(com|edu)(\.[a-zA-Z]{2})?$", email):
        return "Email fora do padrão", 400
    else:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM adotantes WHERE email=%s", (email,))
        email_existe = cursor.fetchone()

        if email_existe:
            return "Email já cadastrado", 400

    #Validação dos requisitos de segurança da senha
    senha = request.form["senha"]
    if not match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).+$", senha):
        return "Senha não atende aos requisitos de segurança", 400
    
    telefone = request.form["telefone"]
    endereco = request.form["endereco"]
    ambiente = request.form["ambiente"]
    if ambiente not in ["Casa sem quintal", "Casa com quintal", "Apartamento"]:
        return "Ambiente inválido", 400

    #Envia a foto para o servidor (Vai precisar alterar o banco de dados com o path da foto)
    #Falta validações de extensão do arquivo
    #Renomear para um nome aleatorio (Evita sobreescrita)
    foto = request.files.get("foto")
    if foto and foto.filename != "":
        if valida_extensao(foto.filename): #Valida se é realmente uma foto
            extensao = secure_filename(foto.filename).rsplit(".", 1)[1].lower()
            #Altera o nome, para evitar colisões
            file_path = os.path.join(UPLOAD_FOLDER, f"{uuid4().hex}.{extensao}")
            foto.save(file_path)
        else:
            return "Tipo de arquivo não permitido", 400

    hash_senha = generate_password_hash(senha) #Gera uma hash para armazenar no banco

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO adotantes (nome, email, senha,  telefone, endereco, ambiente) VALUES (%s, %s, %s, %s, %s, %s)",
        (nome, email, hash_senha, telefone, endereco, ambiente)
    ) #Guarda a hash da senha ao invés do texto puro. (Mais seguro)
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for("main_screen"))

# Rota separada para upload de foto
@app.route("/upload_foto", methods=["POST"])
def upload_foto():
    foto = request.files.get("foto")
    if foto and foto.filename != "":
        filename = secure_filename(foto.filename)
        foto.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        # Retorna o caminho relativo para ser usado no front
        return f"static/uploads/{filename}"
    return "Nenhum arquivo enviado"

if __name__ == "__main__":
    app.run()
