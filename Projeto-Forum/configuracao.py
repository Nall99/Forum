from routes.login import login_route
from routes.cadastro import cadastro_route
from routes.recuperarConta import recuperar_route

def configurarTudo(app):
    configurarRotas(app)

def configurarRotas(app):
    app.register_blueprint(login_route)
    app.register_blueprint(cadastro_route, url_prefix='/cadastro')
    app.register_blueprint(recuperar_route, url_prefix='/recuperar')


def configurarBancoDeDados():
    # ToDo
    pass