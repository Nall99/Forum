from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from models import User, Reportar, db
from forms import CadastroForm

# Criação do Blueprint para a área administrativa
admin_route = Blueprint('admin', __name__)

@admin_route.route('/')
@login_required  # Apenas usuários logados podem acessar essa área
def dashboard():
    usuarios = User.query.all()
    return render_template('lista_usuarios.html', usuarios=usuarios, user=current_user)

@admin_route.route('/cadastrar_usuario', methods=['GET', 'POST'])
@login_required
def cadastrar_usuario():
    form = CadastroForm()
    

    if request.method == "POST":
        if form.validate_on_submit():
            hash_senha = generate_password_hash(form.senha.data, method='pbkdf2:sha256')
            new_user = User(nome=form.nome.data, email=form.email.data, senha=hash_senha, status=form.status.data)
            db.session.add(new_user)
            db.session.commit()
            flash('Usuario foi criada com sucesso!', category='success')

            usuarios = User.query.all()

            return render_template('lista_usuarios.html', usuarios=usuarios, user=current_user)
    return render_template('cadastrarUsuario.html', user=current_user, form=form)

@admin_route.route('/ver_denuncias')
@login_required
def ver_denuncias():
    denuncias = Reportar.query.all()
    
    return render_template('ver_denuncias.html', denuncias=denuncias, user=current_user)

@admin_route.route('/ver_usuarios')
@login_required
def ver_usuarios():

    usuarios = User.query.all()
    return render_template('lista_usuarios.html', usuarios=usuarios, user=current_user)

@admin_route.route('/ver_alunos')
@login_required
def ver_alunos():

    alunos = User.query.filter_by(status='Aluno').all()
    return render_template('lista_usuarios.html', usuarios=alunos, user=current_user)

@admin_route.route('/ver_professores')
@login_required
def ver_professores():

    professores = User.query.filter_by(status='Professor').all()
    return render_template('lista_usuarios.html', usuarios=professores, user=current_user)

@admin_route.route('deletar+usuario/<int:userID>', methods=['GET', 'POST'])
def deletar_usuario(userID):
    user = User.query.get_or_404(userID)
    usuarios = User.query.all()
    # Excluir o tópico e salvar as alterações
    try:
        db.session.delete(user)
        db.session.commit()
        flash("Usuário excluído com sucesso.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Erro ao excluir o tópico: {str(e)}", "error")
    return redirect(url_for('admin.dashboard', user=current_user))
