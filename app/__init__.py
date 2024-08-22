from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import json

db = SQLAlchemy()
migrate = Migrate()

from .models import Estudantes, Cursos, Inscricoes

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    db.init_app(app)
    migrate.init_app(app, db)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/cadastrar_estudante', methods=['GET', 'POST'])
    def cadastrar_estudante():
        if request.method == 'POST':
            nome = request.form['nome']
            cpf = request.form['cpf']
            estudante = Estudantes(nome=nome, cpf=cpf)
            db.session.add(estudante)
            db.session.commit()
            return redirect(url_for('index'))
        return render_template('cadastrar_estudante.html')

    @app.route('/cadastrar_curso', methods=['GET', 'POST'])
    def cadastrar_curso():
        if request.method == 'POST':
            nome = request.form['nome']
            duracao = request.form['duracao']
            preco = request.form['preco']
            curso = Cursos(nome=nome, duracao=duracao, preco=preco)
            db.session.add(curso)
            db.session.commit()
            return redirect(url_for('index'))
        return render_template('cadastrar_curso.html')

    @app.route('/cadastrar_inscricao', methods=['GET', 'POST'])
    def cadastrar_inscricao():
        if request.method == 'POST':
            id_estudante = request.form['estudante']
            id_curso = request.form['curso']
            data_inscricao = request.form['data_inscricao']
            inscricao = Inscricoes(id_estudante=id_estudante, id_curso=id_curso, data_inscricao=data_inscricao)
            db.session.add(inscricao)
            db.session.commit()
            return redirect(url_for('index'))
        estudantes = Estudantes.query.all()
        cursos = Cursos.query.all()
        return render_template('cadastrar_inscricao.html', estudantes=estudantes, cursos=cursos)

    @app.route('/usuarios')
    def usuarios():
        usuarios = Estudantes.query.all()
        html = '''
            <!DOCTYPE html>
            <html lang="pt-BR">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Lista de Estudantes</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        margin: 20px;
                        padding: 0;
                        background-color: #f4f4f4;
                    }
                    .container {
                        max-width: 800px;
                        margin: auto;
                        background: #fff;
                        padding: 20px;
                        border-radius: 8px;
                        box-shadow: 0 0 10px rgba(0,0,0,0.1);
                    }
                    h1 {
                        text-align: center;
                        color: #333;
                    }
                    ul {
                        list-style-type: none;
                        padding: 0;
                    }
                    li {
                        margin-bottom: 10px;
                        padding: 15px;
                        background: #f9f9f9;
                        border-radius: 4px;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    }
                    li:hover {
                        background: #e9e9e9;
                    }
                    .cpf {
                        font-size: 0.8em;
                        color: #666;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Lista de Estudantes</h1>
                    <ul>
        '''
        for usuario in usuarios:
            html += f'''
                        <li>
                            <strong>{usuario.nome}</strong>
                            <span class="cpf">CPF: {usuario.cpf}</span>
                        </li>
            '''
        html += '''
                    </ul>
                </div>
            </body>
            </html>
        '''
        return html

    with app.app_context():
        from . import models
    return app