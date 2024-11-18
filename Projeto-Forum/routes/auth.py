from flask import render_template, Blueprint, request, flash, url_for, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth_route = Blueprint('auth', __name__)

@auth_route.route('/', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@auth_route.route('/cadastro/', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        email = request.form.get('email')
        nome = request.form.get('nome')
        senha1 = request.form.get('senha1')
        senha2 = request.form.get('senha2')

        if len(nome) < 2:
            flash('Seu nome precisa ser maior que 1 único caracter', category='error')
        elif senha1 != senha2:
            flash('As senhas estão diferentes', category='error')
        elif len(senha1) < 7:
            flash('Sua senha deve ser maior que 8 caracteres', category='error')
        else:
            flash('Sua conta foi criada com sucesso!', category='success')
            pass
    
    return render_template('cadastro.html')