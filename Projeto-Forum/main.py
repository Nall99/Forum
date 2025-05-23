from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_ckeditor import CKEditor
from models import db, User
from flask import Flask

# Importação das Rotas
from routes.principal import principal_route
from routes.auth import auth_route
from routes.admin import admin_route

# Criando app
app = Flask(__name__)
ckeditor = CKEditor(app) 

csrf = CSRFProtect()

# Configurar o aplicativo e o banco de dados
app.config['SECRET_KEY'] = 'hifsehifjsd fhisehfsd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)
csrf.init_app(app)

# Login
loginManager = LoginManager()
loginManager.init_app(app)

# FUNÇÕES
@loginManager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def configurarRotas(app):
    app.register_blueprint(auth_route)
    app.register_blueprint(principal_route, url_prefix='/principal')
    app.register_blueprint(admin_route, url_prefix='/admin')

# Executando a config das rotas
configurarRotas(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
