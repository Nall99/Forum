from flask import Blueprint, render_template, request
from database.models.usuario import USUARIOS

cadastro_route = Blueprint('cadastro', __name__)

@cadastro_route.route('/')
def cadastroTemplate():
    return render_template('cadastro.html')

@cadastro_route.route('/cadastrando', methods=['POST'])
def cadastro():
    data = request.form
    new_user = {
        'id': len(USUARIOS),
        'nome': data['nome'],
        'email': data['email'],
        'senha': data['senha']
    }
    USUARIOS.append(new_user)
    return render_template('principal.html')
