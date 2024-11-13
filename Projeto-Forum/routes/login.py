from flask import Blueprint, render_template, request, redirect, url_for
from database.models.usuario import USUARIOS

login_route = Blueprint('login', __name__)

@login_route.route('/')
def loginTemplate():
    return render_template('login.html')

@login_route.route('/logando', methods=['POST', 'GET'])
def login():
    data = request.form
    id = 0
    for usuario in USUARIOS:
        if usuario['email'].lower() == data['email'].lower():
            if usuario['senha'] == data['senha']:
                print('Login realizado com sucesso')
                break
        id += 1
    
    try:
        return redirect(url_for("principal.principalTemplate", email=data['email']))
    except IndexError:
        return render_template('login.html')
        
