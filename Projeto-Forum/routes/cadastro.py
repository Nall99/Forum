from flask import Blueprint, render_template, request, flash
from database.models.usuario import USUARIOS

cadastro_route = Blueprint('cadastro', __name__)

@cadastro_route.route('/')
def cadastroTemplate():
    return render_template('cadastro.html')

@cadastro_route.route('/cadastrando', methods=['GET', 'POST'])
def cadastro():
    data = request.form
    if request.method == 'POST':
        email = request.form.get('email')
        nome = request.form.get('nome')
        senha1 = request.form.get('senha1')
        senha2 = request.form.get('senha2')
        
        if len(nome) < 2:
            flash('Seu nome precisa ser maior que 1 único caracter', category='erro')
        elif senha1 != senha2:
            flash('As senhas estão diferentes', category='error')
        elif len(senha1) < 7:
            flash('Sua senha deve ser maior que 8 caracteres', category='error')
        else:
            flash('Sua conta foi criada com sucesso!', category='success')
            pass


    # new_user = {
    #     'id': len(USUARIOS),
    #     'nome': data['nome'],
    #     'email': data['email'],
    #     'senha': data['senha']
    # }
    USUARIOS.append(new_user)
    return render_template('login.html')
