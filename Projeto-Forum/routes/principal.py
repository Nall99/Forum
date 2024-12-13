from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import current_user, login_required, logout_user
from forms import TopicoForm, UpdateForm, RespostaForm, DenunciaForm
from models import Topico, User, Resposta, Categoria, Etiqueta, Reportar, db
from datetime import datetime
from sqlalchemy import func
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

@principal_route.route('/<filtro>')
def principalTemplate(filtro):
    if filtro == "nada":
        filtro = None
    categorias = Categoria.query.all()
    etiquetas = Etiqueta.query.all()
    return render_template('conteudoPrincipal.html', filtro=filtro, user=current_user, categorias=categorias, etiquetas=etiquetas)

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
    form.categoria.choices = [categoria.nome for categoria in Categoria.query.all()]
    form.etiqueta.choices = [etiqueta.nome for etiqueta in Etiqueta.query.all()]
    if request.method == 'POST':
        novo_topico = Topico(titulo=form.titulo.data,
                             categoria=form.categoria.data,
                             texto=form.texto.data,
                             etiqueta=form.etiqueta.data,
                             autor_id=current_user.id,
                             data=datetime.now())
        db.session.add(novo_topico)
        db.session.commit()
        return redirect(url_for('principal.principalTemplate', filtro='nada'))
    return render_template('formulario.html', form=form, user=current_user)

@principal_route.route('/lista+topicos/<filtro>')
def lista_topicos(filtro):

    user_id = current_user.id  # Presumindo que você está usando Flask-Login para autenticação

    categorias = [categoria.nome for categoria in Categoria.query.all()]
    etiquetas = [etiqueta.nome for etiqueta in Etiqueta.query.all()]

    # Base da consulta
    query = Topico.query
    topicos = []  # Inicializa topicos como uma lista vazia

    # Filtrar por categoria
    if filtro in categorias:
        query = query.filter(Topico.categoria.ilike(filtro))
    
    # Filtrar por etiqueta
    elif filtro in etiquetas:
        query = query.filter(Topico.etiqueta.ilike(filtro))
    
    # Filtrar pelos tópicos criados pelo usuário atual
    elif filtro.lower() == "meus topicos":
        query = query.filter(Topico.autor_id == user_id)
    
    # Filtrar por nome de usuário
    elif User.query.filter_by(nome=filtro).first():
        usuario = User.query.filter_by(nome=filtro).first()
        query = query.filter(Topico.autor_id == usuario.id)
    
    # Filtrar por tópicos mais recentes
    elif filtro.lower() == "mais recentes":
        query = query.order_by(Topico.data.desc())
    
    # Filtrar por tópicos mais populares (baseado em respostas e visualizações)
    if filtro.lower() == "mais popular":
        # Consulta com contagem de respostas
        query = (
            db.session.query(Topico, func.count(Resposta.id).label('num_respostas'))
            .join(Resposta, Resposta.topico_id == Topico.id, isouter=True)
            .group_by(Topico.id)
            .order_by(func.count(Resposta.id).desc())  # Ordena pela contagem de respostas
        )

        # Retorna apenas os tópicos (primeiro item de cada resultado da consulta)
        topicos = [item[0] for item in query.all()]

    else:
        topicos = query.all()

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
    return render_template('perfil.html', imagem=arq_imagem, form=form, user=None)

@principal_route.route('/<int:topicoID>', methods=['GET', 'POST'])
def detalhe_topico(topicoID):

    categorias = Categoria.query.all()
    etiquetas = Etiqueta.query.all()

    form = RespostaForm()
    topico = Topico.query.filter_by(id=topicoID).first()
    autor = User.query.filter_by(id=topico.autor_id).first()
    autor_imagem = url_for('static', filename='profile-pics/' + autor.arq_imagem)

    if request.method == 'POST':
        nova_resposta =  Resposta(texto=form.texto.data,
                             autor_id=current_user.id,
                             topico_id=topicoID,
                             data=datetime.now())
        db.session.add(nova_resposta)
        db.session.commit()

        return redirect(url_for('principal.detalhe_topico', topicoID=topico.id))
    
    return render_template('detalhesTopico.html', topico=topico, autor=autor, imagem=autor_imagem, form=form, user=current_user, categorias=categorias, etiquetas=etiquetas)

@principal_route.route('/lista+respostas/<int:topicoID>')
def lista_respostas(topicoID):
    respostas = Resposta.query.filter_by(topico_id=topicoID)
    return render_template('lista_respostas.html', respostas=respostas, tempo_relativo=tempo_relativo)

@principal_route.route('/lista+usuarios/<status>')
def lista_usuarios(status:str):
    usuarios = User.query.filter_by(status=status).all()
    categorias = Categoria.query.all()
    etiquetas = Etiqueta.query.all()
    
    return render_template('lista_usuarios.html', usuarios=usuarios, categorias=categorias, etiquetas=etiquetas, user=current_user)

@principal_route.route('/denunca/<int:targetID>/<int:topicoID>', methods=['GET', 'POST'])
def denuncia(targetID, topicoID):
    form = DenunciaForm()
    if request.method == 'POST':
        novo_reporte = Reportar(
        autor_id=current_user.id, 
        target_id=targetID, 
        motivo=form.motivo.data,
        data=datetime.now()
        )
        db.session.add(novo_reporte)
        db.session.commit()
        return redirect(url_for('principal.detalhe_topico', topicoID=topicoID))
    return render_template('report.html', form=form, targetID=targetID, topicoID=topicoID, user=current_user)

@principal_route.route('/excluir_topico/<int:topicoID>', methods=['GET'])
@login_required
def excluir_topico(topicoID):
    # Buscar o tópico no banco de dados
    topico = Topico.query.get_or_404(topicoID)

    # Verificar se o tópico pertence ao usuário atual
    if topico.autor_id != current_user.id:
        flash("Você não tem permissão para excluir este tópico.", "error")
        return redirect(url_for('principal.principalTemplate', filtro='Meus topicos'))

    # Excluir o tópico e salvar as alterações
    try:
        db.session.delete(topico)
        db.session.commit()
        flash("Tópico excluído com sucesso.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Erro ao excluir o tópico: {str(e)}", "error")
    
    # Redirecionar para a lista de tópicos
    return redirect(url_for('principal.principalTemplate', filtro='nada'))
