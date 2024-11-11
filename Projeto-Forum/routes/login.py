from flask import Blueprint, render_template, request
from database.models.usuario import USUARIOS

login_route = Blueprint('login', __name__)

@login_route.route('/')
def loginTemplate():
    return render_template('login.html')

@login_route.route('/logando', methods=['POST', 'GET'])
def login():
    data = request.form
    return verificando(data['email'], data['senha'])

def verificando(email, senha):
    id = 0
    for usuario in USUARIOS:
        if usuario['email'].lower() == email.lower():
            if usuario['senha'] == senha:
                print('Login realizado com sucesso')
                break
        id += 1
    
    try:
        return render_template('principal.html', user=USUARIOS[id])
    except IndexError:
        return render_template('login.html')
        
