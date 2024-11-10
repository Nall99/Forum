from flask import Blueprint, render_template

recuperar_route = Blueprint('recuperarConta', __name__)

@recuperar_route.route('/')
def recuperarTemplate():
    return render_template('recuperar.html')