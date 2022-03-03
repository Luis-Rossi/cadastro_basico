from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'

db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column('ID', db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column('Nome', db.String(150), nullable=False)
    email = db.Column('Email', db.String(150), nullable=False)
    senha = db.Column('Senha', db.String(150), nullable=False)

    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = senha

@app.route('/')
def index():
    usuario = Usuario.query.all()
    return render_template("cadastro.html", usuarios=usuario)

@app.route('/adiciona', methods=['GET', 'POST'])
def adiciona_usuario():
    if request.method == 'POST':
        usuario = Usuario(request.form['nome'], request.form['email'], request.form['senha'])
        if usuario.nome == '' or usuario.email == '' or usuario.senha == '':
            mensagem = 'Não deixe campos em branco!'
            return render_template('adiciona.html', mensagem = mensagem)
        else:
            db.session.add(usuario)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('adiciona.html')

@app.route('/delete/<int:id>')
def deletar_usuario(id):
    usuario = Usuario.query.get(id)
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    usuario = Usuario.query.get(id)
    if request.method == 'POST':
        usuario.nome = request.form['nome']
        usuario.email = request.form['email']
        usuario.senha = request.form['senha']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', usuario = usuario)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)






















'''
from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)
banco = sqlite3.connect('usuarios.db')
cursor = banco.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS usuarios (usuario text, email text, senha password)")

class Informacoes:
    def __init__(self, usuario, email, senha):
        self.usuario = usuario
        self.email = email
        self.senha = senha

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/login.html", methods=["GET", "POST"])
def recebe_valores():
    usuario = request.form['usuario']
    email = request.form['email']
    senha = request.form['senha']
    cursor.execute("INSERT INTO usuarios VALUES(usuario, email, senha)")
    banco.commit()

def mostra_valores():
    cursor.execute("SELECT * FROM usuarios")
    return render_template("login.html"), banco.fetchall()



app.run(debug=True)
'''