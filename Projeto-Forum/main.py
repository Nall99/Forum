from flask import Flask
from configuracao import *

# inicialização 
app = Flask(__name__)

#configuração
configurarTudo(app)

# execução
app.run(debug=True)