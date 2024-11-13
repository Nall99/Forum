from flask import Blueprint, render_template, request
from database.models.usuario import USUARIOS
from database.models.topico import TOPICOS

principal_route = Blueprint('principal', __name__)

@principal_route.route('/<email>')
def principalTemplate(email):
    id = 0
    for usuario in USUARIOS:
        if usuario['email'].lower() == email.lower():
            break
        id += 1
    
    try:
        return render_template('principal.html', idUsuario=id)
    except IndexError:
        return render_template('login.html')

@principal_route.route('/<int:idUsuario>/criando-topico', methods=['POST'])
def criandoTopico(idUsuario):
    data = request.form
    topico = {
        'id': len(TOPICOS),
        'idUsuario': idUsuario,
        'titulo': data['titulo'],
        'categoria': data['list'],
        'texto': data['texto']
    }
    TOPICOS.append(topico)
    return render_template('principal.html', idUsuario=idUsuario)