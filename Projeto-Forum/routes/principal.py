from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required, logout_user
from models import Topico, User, db
from forms import TopicoForm, UpdateForm
from PIL import Image
import secrets
import os

principal_route = Blueprint('principal', __name__)

@principal_route.route('/')
def principalTemplate():
    return render_template('principal.html')

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
    return render_template('criarTopico.html', form=form)

@principal_route.route('/lista+topicos')
def lista_topicos():
    topicos = Topico.query.all()
    return render_template('lista_topicos.html', topicos=topicos)

@principal_route.route('/perfil', methods=['GET','POST'])
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

