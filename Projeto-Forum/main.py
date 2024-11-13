from flask import Flask
from configuracao import *

# inicialização
app = Flask(__name__)
UPLOAD_FOLDER = './Projeto-Forum/static/files'
ALLOWED_EXTESIONS = {'txt', 'pdf', 'png', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

#configuração
configurarTudo(app)

# execução
app.run(debug=True)