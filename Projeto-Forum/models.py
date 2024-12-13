from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy() 

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    nome = db.Column(db.String(150), nullable=False)
    senha = db.Column(db.String(40), nullable=False)
    arq_imagem = db.Column(db.String(20), nullable=False, default='default.jpg')
    status = db.Column(db.String(20), nullable=False)
    topicos = db.relationship('Topico', backref='autor', cascade='all, delete-orphan', lazy=True)
    respostas = db.relationship('Resposta', backref='autor', cascade='all, delete-orphan', lazy=True)

    # Relacionamento com a tabela Reportar
    reportes_feitos = db.relationship(
        'Reportar', 
        foreign_keys='Reportar.autor_id', 
        cascade='all, delete-orphan',
        backref='autor_do_reporte', 
        lazy=True
    )
    reportes_recebidos = db.relationship(
        'Reportar', 
        foreign_keys='Reportar.target_id',
        cascade='all, delete-orphan', 
        backref='usuario_reportado', 
        lazy=True
    )

    def __repr__(self) -> str:
        return f"Usuario('{self.nome}', '{self.email}', '{self.arq_imagem}')"

class Reportar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    autor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    target_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    motivo = db.Column(db.String(255), nullable=False)
    data = db.Column(db.DateTime, nullable=False)
    def __repr__(self):
        return f"Reportar(Autor: {self.autor_id}, Alvo: {self.target_id}, Motivo: {self.motivo})"

class Topico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime)
    titulo = db.Column(db.String(50))
    categoria = db.Column(db.String(150))
    etiqueta = db.Column(db.String(150))
    autor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    texto = db.Column(db.String(400))
    respostas = db.relationship('Resposta', backref='topico', cascade='all, delete-orphan', lazy=True)

    def __repr__(self) -> str:
        return f"(Topico'{self.titulo}', '{self.categoria}', '{self.etiqueta}', '{self.data}')"

class Resposta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime)
    texto = db.Column(db.String(400))
    autor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    topico_id = db.Column(db.Integer, db.ForeignKey('topico.id'))

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(25))

class Etiqueta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(25))