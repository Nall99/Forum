from flask_login import UserMixin
from sqlalchemy.sql import func
from configuracao import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    nome = db.Column(db.String(150))
    senha = db.Column(db.String(150))

