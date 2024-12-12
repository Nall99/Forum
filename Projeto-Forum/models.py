from flask_login import UserMixin
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy() 

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    nome = db.Column(db.String(150), nullable=False)
    senha = db.Column(db.String(40), nullable=False)
    arq_imagem = db.Column(db.String(20), nullable=False, default='default.jpg')
    topicos = db.relationship('Topico', backref='autor', lazy=True)
    respostas = db.relationship('Resposta', backref='autor', lazy=True)

    def __repr__(self) -> str:
        return f"Usuario('{self.nome}', '{self.email}', '{self.arq_imagem}')"

class Topico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime, default=datetime.now())
    titulo = db.Column(db.String(50))
    categoria = db.Column(db.String(150))
    etiqueta = db.Column(db.String(150))
    autor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    texto = db.Column(db.String(400))
    respostas = db.relationship('Resposta', backref='respostas', lazy=True)

    def __repr__(self) -> str:
        return f"(Topico'{self.titulo}', '{self.categoria}', '{self.data}')"

class Resposta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime, default=datetime.now())
    texto = db.Column(db.String(400))
    autor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    topico_id = db.Column(db.Integer, db.ForeignKey('topico.id'))
