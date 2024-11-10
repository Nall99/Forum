from flask import Blueprint, render_template

cadastro_route = Blueprint('cadastro', __name__)

@cadastro_route.route('/')
def cadastroTemplate():
    return render_template('cadastro.html')