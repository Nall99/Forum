from flask import Flask
from configuracao import *

# inicialização
app = Flask(__name__)

# configurações
configurarTudo(app)

# execução
app.run(debug=True)

