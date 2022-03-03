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