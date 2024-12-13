from flask import render_template, Blueprint, request, flash, url_for, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user
from forms import CadastroForm, LoginForm, RecuperarForm
from models import User, db
from random import randint
from time import sleep
import email.message
import smtplib

auth_route = Blueprint('auth', __name__)

codRecuperacao = None

def mensagemDeRecuperacao(paraEmail):
    codRecuperacao = randint(0, 5000)
    corpo_email= f"""
    <p>Opa, tudo bem?</p>
    <p>Estou lhe enviando o código necessario para recuperação da sua conta</p>
    <p>Código de recuperação: {codRecuperacao}</p>
    """

    msg = email.message.Message()
    msg['Subject'] = 'Código de Recuperação'
    msg['From'] = 'nallxp98@gmail.com'
    msg['To'] = paraEmail
    senha = 'ecyiwsstgrfvhbme'

    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email)

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()

    # Login Credentials for sending the mail
    s.login(msg['From'], senha)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
    
    return codRecuperacao


@auth_route.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated and current_user.status != "Admin":
        print("rodando")
        return redirect(url_for('principal.principalTemplate', filtro='nada'))
    
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and check_password_hash(user.senha, form.senha.data):
                login_user(user, remember=form.lembrar.data)
                if user.status == "Admin":
                    return redirect(url_for('admin.dashboard', user=current_user))
                return redirect(url_for('principal.principalTemplate', filtro='nada'))
            else:
                flash("Falha no login. Email ou senha estão incorretos", "error")

    return render_template('login.html', user=current_user, form=form)

@auth_route.route('/cadastro/', methods=['GET', 'POST'])
def cadastro():
    if current_user.is_authenticated:
        return redirect(url_for('principal.principalTemplate', filtro='nada'))
    
    form = CadastroForm()
    if form.validate_on_submit():
        hash_senha = generate_password_hash(form.senha.data, method='pbkdf2:sha256')
        new_user = User(nome=form.nome.data, email=form.email.data, senha=hash_senha, status='Aluno')
        db.session.add(new_user)
        db.session.commit()
        flash('Sua conta foi criada com sucesso!', category='success')
        return redirect(url_for('auth.login'))

    return render_template('cadastro.html', user=current_user, form=form)

@auth_route.route('/recuperar/', methods=['GET', 'POST'])
def recuperar():
    form = RecuperarForm()
    if request.method == "POST":
        
        cod = mensagemDeRecuperacao(form.email.data)
        
        return redirect(url_for('auth.codRec', user=current_user, cod=cod))
    
    return render_template('recuperar.html', user=current_user, form=form)


@auth_route.route('/codRecuperacao/<int:cod>', methods=['GET', 'POST'])
def codRec(cod):
    
    flash('Código já foi enviado para o seu email', category='success')
    form = RecuperarForm()
    if request.method == "POST":
        if form.codigo.data == str(cod):
            return render_template('novasenha.html', user=current_user)
    return render_template('codigoRecuperar.html', user=current_user, form=form, cod=cod)