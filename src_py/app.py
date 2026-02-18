from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from dotenv import load_dotenv
import os
from werkzeug.utils import secure_filename

load_dotenv(dotenv_path="C:\\tocadospeludos\\.env")

app = Flask(__name__, template_folder="C:\\tocadospeludos\\template")

UPLOAD_FOLDER = "C:\\tocadospeludos\\static\\uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM adotantes WHERE email=%s AND senha=%s", (email, senha))
        usuario = cursor.fetchone()
        conn.close()

        if usuario:
            # Login válido → vai para tela de preferências
            return redirect(url_for("preferencias"))
        else:
            # Login inválido → volta para login com mensagem
            return render_template("login.html", erro="Email ou senha incorretos")

    # Se for GET, apenas renderiza o formulário
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
    conn.close()
    return render_template("main_screen.html", adotantes=adotantes)

@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")

@app.route("/preferencias", methods=["GET", "POST"])
def preferencias():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM pets")
    pets = cursor.fetchall()
    conn.close()

    if request.method == "POST":
        pet_id = request.form.get("pet_id")
        # Aqui você pode salvar a preferência do usuário no banco
        # Exemplo: inserir em uma tabela preferencias
        return redirect(url_for("main_screen"))

    return render_template("preferencias.html", pets=pets)


@app.route("/salvar", methods=["POST"])
def salvar():
    nome = request.form["nome"]
    email = request.form["email"]
    senha = request.form["senha"]
    telefone = request.form["telefone"]
    endereco = request.form["endereco"]
    ambiente = request.form["ambiente"]

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO adotantes (nome, email, senha,  telefone, endereco, ambiente) VALUES (%s, %s, %s, %s, %s, %s)",
        (nome, email, senha, telefone, endereco, ambiente)
    )
    conn.commit()
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
    app.run(debug=True)
