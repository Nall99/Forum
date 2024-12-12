from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required, logout_user
from forms import TopicoForm, UpdateForm, RespostaForm
from models import Topico, User, Resposta, db
from datetime import datetime
from PIL import Image
import secrets
import os

principal_route = Blueprint('principal', __name__)


def tempo_relativo(data_envio):
    agora = datetime.now()
    delta = agora - data_envio

    if delta.days > 0:
        return f"{delta.days} dias atrás"
    elif delta.seconds >= 3600:
        horas = delta.seconds // 3600
        return f"{horas} horas atrás"
    elif delta.seconds >= 60:
        minutos = delta.seconds // 60
        return f"{minutos} minutos atrás"
    else:
        return "Agora mesmo"

@principal_route.route('/')
def principalTemplate():
    return render_template('conteudoPrincipal.html', user=current_user.is_authenticated)

@principal_route.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    foto_fn = random_hex + f_ext
    foto_path = os.path.join(principal_route.root_path,'..', 'static/profile-pics', foto_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(foto_path)

    return foto_fn

@principal_route.route('/criando+topico', methods=['GET', 'POST'])
def criando_topico():
    form = TopicoForm()
    if request.method == 'POST':
        novo_topico = Topico(titulo=form.titulo.data,
                             categoria=form.categoria.data,
                             texto=form.texto.data,
                             etiqueta="nada ainda",
                             autor_id=current_user.id)
        db.session.add(novo_topico)
        db.session.commit()
        return redirect(url_for('principal.principalTemplate'))
    return render_template('criarTopico.html', form=form, user=not current_user.is_authenticated)

@principal_route.route('/lista+topicos')
def lista_topicos():
    topicos = Topico.query.all()

    for topico in topicos:
        # Atividade
        ultima_resposta = Resposta.query.filter_by(topico_id=topico.id).order_by(Resposta.data.desc()).first()
        if ultima_resposta:
            topico.ultima_resposta_data = ultima_resposta.data
        else:
            topico.ultima_resposta_data = None  # Se não houver resposta, atribui None
        # Cria uma lista com os autor_id únicos de cada resposta
        autores_unicos = list(set([resposta.autor_id for resposta in topico.respostas]))
        topico.quantidade_de_autores_unicos = len(autores_unicos)

    return render_template('lista_topicos.html', topicos=topicos, tempo_relativo=tempo_relativo)

@principal_route.route('/perfil', methods=['GET', 'POST'])
@login_required
def perfil():
    form = UpdateForm()
    if form.validate_on_submit():
        if form.foto.data:
            arq_foto = save_picture(form.foto.data)
            current_user.arq_imagem = arq_foto
        current_user.nome = form.nome.data
        current_user.email = form.email.data
        db.session.commit()
        return redirect(url_for('principal.perfil'))
    elif request.method == 'GET':
        form.nome.data = current_user.nome
        form.email.data = current_user.email
    arq_imagem = url_for('static', filename='profile-pics/' + current_user.arq_imagem)
    return render_template('perfil.html', imagem=arq_imagem, form=form)

@principal_route.route('/<int:topicoID>', methods=['GET', 'POST'])
def detalhe_topico(topicoID):
    form = RespostaForm()
    topico = Topico.query.filter_by(id=topicoID).first()
    autor = User.query.filter_by(id=topico.autor_id).first()
    autor_imagem = url_for('static', filename='profile-pics/' + autor.arq_imagem)

    if request.method == 'POST':
        nova_resposta =  Resposta(texto=form.texto.data,
                             autor_id=current_user.id,
                             topico_id=topicoID)
        db.session.add(nova_resposta)
        db.session.commit()

        return redirect(url_for('principal.detalhe_topico', topicoID=topico.id))
    
    return render_template('detalhesTopico.html', topico=topico, autor=autor, imagem=autor_imagem, form=form, user=current_user.is_authenticated)

@principal_route.route('/lista+respostas/<int:topicoID>')
def lista_respostas(topicoID):
    respostas = Resposta.query.filter_by(topico_id=topicoID)
    return render_template('lista_respostas.html', respostas=respostas, tempo_relativo=tempo_relativo)

@principal_route.route('/user+resposta/<int:userID>')
def user_resposta(userID):
    user = User.query.filter_by(id=userID).first()
    return render_template('user_resposta.html', user=user)