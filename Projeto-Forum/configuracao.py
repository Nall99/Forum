from routes.principal import principal_route
from routes.auth import auth_route
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def configurarRotas(app):
    app.register_blueprint(auth_route)
    app.register_blueprint(principal_route, url_prefix='/principal')


def configurarBancoDeDados(app):
    DB_NOME = 'database.db'

    app.config['SECRET_KEY'] = 'hifsehifjsd fhisehfsd'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NOME}'
    
    db.init_app(app)
    
    return db
    