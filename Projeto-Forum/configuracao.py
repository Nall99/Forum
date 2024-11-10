from routes.login import login_route
<<<<<<< HEAD
from routes.cadastro import cadastro_route
from routes.recuperarConta import recuperar_route
=======
>>>>>>> 8ce7265 (Estrutura das pastas e Flask)

def configurarTudo(app):
    configurarRotas(app)

def configurarRotas(app):
    app.register_blueprint(login_route)
<<<<<<< HEAD
    app.register_blueprint(cadastro_route, url_prefix='/cadastro')
    app.register_blueprint(recuperar_route, url_prefix='/recuperar')


def configurarBancoDeDados():
=======

def configurarBD():
>>>>>>> 8ce7265 (Estrutura das pastas e Flask)
    # ToDo
    pass