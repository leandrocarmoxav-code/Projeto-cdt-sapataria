from flask import Flask, render_template

app = Flask(__name__)

estoque = [

    {
        "marca": "Nike",
        "modelo": "Air Max 90",
        "preco": 799.90
    },

    {
        "marca": "Adidas",
        "modelo": "Ultraboost",
        "preco": 699.90
    },

    {
        "marca": "Jordan",
        "modelo": "Jordan 4 Retro",
        "preco": 1799.90
    }

]

@app.route("/")
def inicio():

    return render_template(
        "index.html",
        estoque=estoque
    )

@app.route("/teste")
def teste():

    return "Flask funcionando!"

# IMPORTANTE PARA O VERCEL
app = app