from . import db

class Estudantes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    cpf = db.Column(db.String(15), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    data_nascimento = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f'<Estudante {self.nome}>'

class Cursos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    duracao = db.Column(db.Integer, nullable=False)
    preco = db.Column(db.Numeric(10, 2))

class Inscricoes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_estudante = db.Column(db.Integer, db.ForeignKey('estudantes.id'), nullable=False)
    id_curso = db.Column(db.Integer, db.ForeignKey('cursos.id'), nullable=False)
    data_inscricao = db.Column(db.Date, nullable=False)

    estudante = db.relationship('Estudantes', backref=db.backref('inscricoes', lazy=True))
    curso = db.relationship('Cursos', backref=db.backref('inscricoes', lazy=True))


