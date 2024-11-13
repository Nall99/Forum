from flask import Blueprint, render_template, request
import smtplib
import email.message
from random import randint


def topicoDeRecuperacao(paraEmail):
    CodRecuperacao = randint(0, 5000)
    CodRecuperacao_str = str(CodRecuperacao).zfill(3)
    corpo_email= f"""
    <p>Opa, tudo bem?</p>
    <p>Estou lhe enviando o código necessario para recuperação da sua conta</p>
    <p>Código de recuperação: {CodRecuperacao_str}</p>
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
    print('Email enviado')

recuperar_route = Blueprint('recuperarConta', __name__)

@recuperar_route.route('/')
def recuperarTemplate():
    return render_template('recuperar.html')

@recuperar_route.route('/recuperando', methods=['POST'])
def recuperar():
    data = request.form
    topicoDeRecuperacao(data['email'])
    return render_template('login.html')