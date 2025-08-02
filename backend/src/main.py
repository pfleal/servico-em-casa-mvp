import os
import sys
import logging
from datetime import datetime
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, request, make_response
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from src.models.user import db
from src.models.service import ServiceCategory, ProviderService
from src.models.request import ServiceRequest
from src.models.proposal import Proposal
from src.models.evaluation import Evaluation
from src.models.message import Message
from src.routes.user import user_bp
from src.routes.auth import auth_bp
from src.routes.service import service_bp
from src.routes.request import request_bp
from src.routes.proposal import proposal_bp
from src.routes.evaluation import evaluation_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'

# Criar diretório de logs se não existir
log_dir = os.path.join(os.path.dirname(__file__), 'logs')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Configuração de Logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Console output
        logging.FileHandler(os.path.join(log_dir, 'app.log'), encoding='utf-8')
    ]
)

# Logger específico para a aplicação
app_logger = logging.getLogger('servico_em_casa')
app_logger.setLevel(logging.DEBUG)

app_logger.info('Aplicação iniciada')

# Configurações CORS
CORS(app, 
     origins=["http://localhost:5173", "http://127.0.0.1:5173"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization"],
     supports_credentials=True)

# Configurações JWT
jwt = JWTManager(app)

# Configurações SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

# Handler para requisições OPTIONS (preflight) - deve vir primeiro
@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        app_logger.debug(f'Requisição OPTIONS (preflight) para: {request.url}')
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "http://localhost:5173")
        response.headers.add('Access-Control-Allow-Headers', "Content-Type,Authorization")
        response.headers.add('Access-Control-Allow-Methods', "GET,PUT,POST,DELETE,OPTIONS")
        response.headers.add('Access-Control-Allow-Credentials', "true")
        return response

# Middleware de logging para requisições
@app.before_request
def log_request_info():
    # Não logar requisições OPTIONS para evitar spam
    if request.method != "OPTIONS":
        app_logger.info(f'Requisição: {request.method} {request.url} - IP: {request.remote_addr}')
        try:
            if request.json:
                app_logger.debug(f'Dados da requisição: {request.json}')
        except Exception:
            # Ignorar erros de parsing JSON para requisições que não são JSON
            pass

@app.after_request
def log_response_info(response):
    # Não logar respostas OPTIONS para evitar spam
    if request.method != "OPTIONS":
        app_logger.info(f'Resposta: {response.status_code} para {request.method} {request.url}')
    return response

# Handlers de erro globais com logging
@app.errorhandler(404)
def not_found_error(error):
    app_logger.warning(f'Erro 404: Rota não encontrada - {request.method} {request.url}')
    return {'error': 'Rota não encontrada'}, 404

@app.errorhandler(500)
def internal_error(error):
    app_logger.error(f'Erro interno do servidor: {str(error)}', exc_info=True)
    return {'error': 'Erro interno do servidor', 'details': str(error) if app.debug else None}, 500

@app.errorhandler(Exception)
def handle_exception(error):
    app_logger.error(f'Exceção não tratada: {str(error)}', exc_info=True)
    return {'error': 'Erro inesperado', 'details': str(error) if app.debug else None}, 500

# Registrar blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(service_bp, url_prefix='/api/services')
app.register_blueprint(request_bp, url_prefix='/api/requests')
app.register_blueprint(proposal_bp, url_prefix='/api/proposals')
app.register_blueprint(evaluation_bp, url_prefix='/api/evaluations')

app_logger.info('Blueprints registrados com sucesso')

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app_logger.info('Configurando banco de dados SQLite')
db.init_app(app)
with app.app_context():
    try:
        db.create_all()
        app_logger.info('Banco de dados inicializado com sucesso')
    except Exception as e:
        app_logger.error(f'Erro ao inicializar banco de dados: {str(e)}', exc_info=True)
        raise

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    app_logger.info('Iniciando servidor Flask em http://0.0.0.0:5000')
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    except Exception as e:
        app_logger.error(f'Erro ao iniciar servidor: {str(e)}', exc_info=True)
        raise
