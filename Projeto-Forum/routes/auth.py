from flask import render_template, Blueprint, request, flash, url_for, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user
from models import User, db
from forms import CadastroForm, LoginForm

auth_route = Blueprint('auth', __name__)

@auth_route.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('principal.principalTemplate'))
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and check_password_hash(user.senha, form.senha.data):
                print(form.lembrar.data)
                login_user(user, remember=form.lembrar.data)
                return redirect(url_for('principal.principalTemplate'))
            else:
                flash("Falha no login. Email ou senha estão incorretos", "error")

    return render_template('login.html', user=current_user.is_authenticated, form=form)

@auth_route.route('/cadastro/', methods=['GET', 'POST'])
def cadastro():
    if current_user.is_authenticated:
        return redirect(url_for('principal.principalTemplate'))
    
    form = CadastroForm()
    if form.validate_on_submit():
        hash_senha = generate_password_hash(form.senha.data, method='pbkdf2:sha256')
        new_user = User(nome=form.nome.data, email=form.email.data, senha=hash_senha, status='Aluno')
        db.session.add(new_user)
        db.session.commit()
        flash('Sua conta foi criada com sucesso!', category='success')
        return redirect(url_for('auth.login'))

    return render_template('cadastro.html', user=current_user.is_authenticated, form=form)
