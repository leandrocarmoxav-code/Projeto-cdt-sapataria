from flask import Flask, render_template, request, redirect, jsonify
import sqlite3
import json
import os

app = Flask(__name__)

# ==========================================
# BANCO DE DADOS
# ==========================================

DATABASE = "central_tenis.db"

def conectar():

    conexao = sqlite3.connect(DATABASE)

    conexao.row_factory = sqlite3.Row

    return conexao

def criar_tabelas():

    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS usuarios (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        nome TEXT NOT NULL,

        email TEXT NOT NULL,

        usuario TEXT UNIQUE NOT NULL,

        senha TEXT NOT NULL

    )

    """)

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS pedidos (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        usuario TEXT,

        produto TEXT,

        preco REAL

    )

    """)

    conexao.commit()

    conexao.close()

criar_tabelas()

# ==========================================
# ESTOQUE
# ==========================================

estoque = [

    {
        "marca": "Nike",
        "modelo": "Air Max 90",
        "preco": 799.90
    },

    {
        "marca": "Nike",
        "modelo": "Jordan 1",
        "preco": 999.90
    },

    {
        "marca": "Adidas",
        "modelo": "Ultraboost",
        "preco": 699.90
    },

    {
        "marca": "Puma",
        "modelo": "RS-X",
        "preco": 450.00
    },

    {
        "marca": "Vans",
        "modelo": "Old Skool",
        "preco": 399.90
    },

    {
        "marca": "New Balance",
        "modelo": "9060",
        "preco": 950.00
    },

    {
        "marca": "Asics",
        "modelo": "Gel Kayano",
        "preco": 850.00
    },

    {
        "marca": "Converse",
        "modelo": "Chuck Taylor",
        "preco": 320.00
    },

    {
        "marca": "Jordan",
        "modelo": "Jordan 4 Retro",
        "preco": 1799.90
    }

]

# ==========================================
# HOME
# ==========================================

@app.route("/")
def inicio():

    return render_template(

        "index.html",

        estoque=estoque

    )

# ==========================================
# CADASTRAR USUÁRIO
# ==========================================

@app.route("/cadastrar", methods=["POST"])
def cadastrar():

    nome = request.form.get("nome")
    email = request.form.get("email")
    usuario = request.form.get("usuario")
    senha = request.form.get("senha")

    if not nome or not email or not usuario or not senha:

        return "Preencha todos os campos!"

    conexao = conectar()

    cursor = conexao.cursor()

    try:

        cursor.execute("""

        INSERT INTO usuarios

        (nome, email, usuario, senha)

        VALUES (?, ?, ?, ?)

        """, (nome, email, usuario, senha))

        conexao.commit()

    except sqlite3.IntegrityError:

        conexao.close()

        return "Usuário já existe!"

    conexao.close()

    return redirect("/")

# ==========================================
# LOGIN
# ==========================================

@app.route("/login", methods=["POST"])
def login():

    usuario = request.form.get("usuario")
    senha = request.form.get("senha")

    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute("""

    SELECT * FROM usuarios

    WHERE usuario = ? AND senha = ?

    """, (usuario, senha))

    resultado = cursor.fetchone()

    conexao.close()

    if resultado:

        return f"""

        Login realizado!

        Bem-vindo {resultado['nome']}

        """

    return "Usuário ou senha incorretos!"

# ==========================================
# EXPORTAR JSON
# ==========================================

@app.route("/exportar")
def exportar():

    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM usuarios")

    usuarios = cursor.fetchall()

    cursor.execute("SELECT * FROM pedidos")

    pedidos = cursor.fetchall()

    lista_usuarios = []

    for u in usuarios:

        lista_usuarios.append({

            "id": u["id"],
            "nome": u["nome"],
            "email": u["email"],
            "usuario": u["usuario"],
            "senha": u["senha"]

        })

    lista_pedidos = []

    for p in pedidos:

        lista_pedidos.append({

            "id": p["id"],
            "usuario": p["usuario"],
            "produto": p["produto"],
            "preco": p["preco"]

        })

    dados = {

        "usuarios": lista_usuarios,

        "pedidos": lista_pedidos

    }

    with open(

        "backup_loja.json",

        "w",

        encoding="utf-8"

    ) as arquivo:

        json.dump(

            dados,

            arquivo,

            indent=4,

            ensure_ascii=False

        )

    conexao.close()

    return jsonify({

        "mensagem":

        "JSON exportado com sucesso!"

    })

# ==========================================
# TESTE VERCEL
# ==========================================

@app.route("/teste")
def teste():

    return "Servidor Flask funcionando!"

# ==========================================
# INICIAR SERVIDOR
# ==========================================

if __name__ == "__main__":

    porta = int(

        os.environ.get(

            "PORT",

            5000

        )

    )

    app.run(

        host="0.0.0.0",

        port=porta,

        debug=True

    )