from app import app
from flask import render_template, request, flash, redirect, make_response, url_for

mensagens = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/autenticar", methods=['POST'])
def autenticar():
    usuario = request.form.get("usuario")
    if usuario:
        resp = make_response(redirect(url_for('usuario_page', usuario=usuario)))
        resp.set_cookie('usuario', usuario)
        return resp
    else:
        return redirect(url_for('login'))

@app.route("/autenticar/<usuario>", methods=['GET', 'POST'])
def usuario_page(usuario):
    if request.method == 'POST':
        mensagem = request.form.get("mensagem")
        if mensagem:
            mensagens = request.cookies.get(f'mensagens_{usuario}', '')
            if mensagens:
                mensagens += ',' + mensagem
            else:
                mensagens = mensagem
            resp = make_response(render_template("usuario.html", usuario=usuario, mensagens=mensagens.split(',')))
            resp.set_cookie(f'mensagens_{usuario}', mensagens)
            return resp
    else:
        mensagens = request.cookies.get(f'mensagens_{usuario}', '')
        mensagens = mensagens.split(',') if mensagens else []
        return render_template("usuario.html", usuario=usuario, mensagens=mensagens)

@app.route("/mensagens")
def listar_mensagens():
    usuario = request.args.get('usuario')
    if not usuario:
        return "Por favor, forneça um usuário na string de consulta.", 400
    
    mensagens = request.cookies.get(f'mensagens_{usuario}', '')
    mensagens = mensagens.split(',') if mensagens else []

    return render_template("listar_mensagens.html", usuario=usuario, mensagens=mensagens)