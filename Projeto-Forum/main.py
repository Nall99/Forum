from flask import Flask
from configuracao import *

app = Flask(__name__)

configurarRotas(app)
db = configurarBancoDeDados(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)