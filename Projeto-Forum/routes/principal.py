from flask import Blueprint, render_template, request
from werkzeug.utils import secure_filename
# from database.models.usuario import USUARIOS
# from database.models.topico import TOPICOS
# from main import app
import os

principal_route = Blueprint('principal', __name__)

# @principal_route.route('/<email>')
# def principalTemplate(email):
#     id = 0
#     for usuario in USUARIOS:
#         if usuario['email'].lower() == email.lower():
#             break
#         id += 1
#     try:
#         return render_template('principal.html', idUsuario=id)
#     except IndexError:
#         return render_template('login.html')


# @principal_route.route('/<int:idUsuario>/conteudoPrincipal')
# def conteudoPrincipal(idUsuario):
#     return render_template('conteudoPrincipal.html', idUsuario=idUsuario)

# @principal_route.route('/<int:idTopico>/detalhesTopico')
# def detalhesTopico(idTopico):
#     topico = list(filter(lambda t: t['id'] == idTopico, TOPICOS))[0]
#     return render_template('detalhesTopico.html', topico=topico)

# @principal_route.route('/listarTopicos')
# def listarTopicos():
#     return render_template('lista_topicos.html', topicos=TOPICOS)

# @principal_route.route('/<int:idUsuario>/criando-topico', methods=['POST'])
# def criandoTopico(idUsuario):
#     data = request.form
#     arq = request.files['arq']
#     topico = {
#         'id': len(TOPICOS),
#         'idUsuario': idUsuario,
#         'titulo': data['titulo'],
#         'categoria': data['list'],
#         'texto': data['texto'],
#     }
#     TOPICOS.append(topico)
#     # if arq:
#     #     filename = secure_filename(arq.filename)
#     #     file_path = os.path.normpath(os.path.join('./Projeto-Forum/static/files', filename))
#     #     arq.save(file_path)

    # return render_template('principal.html', idUsuario=idUsuario)

        

