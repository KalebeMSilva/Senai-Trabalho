from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

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
        estudantes = Estudantes.query.all()
        cursos = Cursos.query.all()
        return render_template('index.html', estudantes=estudantes, cursos=cursos)

    @app.route('/cadastrar_estudante', methods=['GET', 'POST'])
    @app.route('/editar_estudante/<int:id>', methods=['GET', 'POST'])
    def manage_estudante(id=None):
        if id:
            estudante = Estudantes.query.get_or_404(id)
        else:
            estudante = None

        if request.method == 'POST':
            nome = request.form['nome']
            cpf = request.form['cpf']
            email = request.form['email']
            data_nascimento = datetime.strptime(request.form['data_nascimento'], '%Y-%m-%d').date()
            
            if estudante:
                estudante.nome = nome
                estudante.cpf = cpf
                estudante.email = email
                estudante.data_nascimento = data_nascimento
            else:
                estudante = Estudantes(nome=nome, cpf=cpf, email=email, data_nascimento=data_nascimento)
                db.session.add(estudante)
            db.session.commit()
            return redirect(url_for('index'))

        return render_template('cadastrar_estudante.html', estudante=estudante)

    @app.route('/remover_estudante/<int:id>', methods=['POST'])
    def remover_estudante(id):
        estudante = Estudantes.query.get_or_404(id)
        db.session.delete(estudante)
        db.session.commit()
        return redirect(url_for('index'))

    @app.route('/cadastrar_curso', methods=['GET', 'POST'])
    @app.route('/editar_curso/<int:id>', methods=['GET', 'POST'])
    def manage_curso(id=None):
        if id:
            curso = Cursos.query.get_or_404(id)
        else:
            curso = None

        if request.method == 'POST':
            nome = request.form['nome']
            duracao = request.form['duracao']
            preco = request.form['preco']
            if curso:
                curso.nome = nome
                curso.duracao = duracao
                curso.preco = preco
            else:
                curso = Cursos(nome=nome, duracao=duracao, preco=preco)
                db.session.add(curso)
            db.session.commit()
            return redirect(url_for('index'))

        return render_template('cadastrar_curso.html', curso=curso)

    @app.route('/remover_curso/<int:id>', methods=['POST'])
    def remover_curso(id):
        curso = Cursos.query.get_or_404(id)
        db.session.delete(curso)
        db.session.commit()
        return redirect(url_for('index'))

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

    @app.route('/remover_inscricao/<int:id>', methods=['POST'])
    def remover_inscricao(id):
        inscricao = Inscricoes.query.get_or_404(id)
        db.session.delete(inscricao)
        db.session.commit()
        return redirect(url_for('index'))

    return app
