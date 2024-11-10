from routes.login import login_route

def configurarTudo(app):
    configurarRotas(app)

def configurarRotas(app):
    app.register_blueprint(login_route)

def configurarBD():
    # ToDo
    pass