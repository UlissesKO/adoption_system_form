from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from dotenv import load_dotenv
import os
from werkzeug.utils import secure_filename
from flask import session


load_dotenv(dotenv_path="C:\\tocadospeludos\\.env")

app = Flask(__name__, template_folder="C:\\tocadospeludos\\template")

app.secret_key = "chave-secreta"

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
    conn.close()
    return render_template("main_screen.html", adotantes=adotantes)

@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")

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

        conn.close()
        return redirect(url_for("preferencias"))


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
