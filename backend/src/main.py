import os
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from src.models.user import db
from src.config import config
from src.models.service import ServiceCategory, ProviderService
from src.models.request import ServiceRequest
from src.models.proposal import Proposal
from src.models.evaluation import Evaluation
from src.models.message import Message
from src.routes.user import user_bp
from src.routes.auth import auth_bp
from src.routes.service import service_bp
from src.routes.order import order_bp
from src.routes.proposal import proposal_bp
from src.routes.evaluation import evaluation_bp
from src.utils.logging_config import setup_logging, setup_request_logging

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))

# Configuração da aplicação
config_name = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config[config_name])

# Configuração de Logging
setup_logging(app)
setup_request_logging(app)

# Configurações CORS
CORS(app, origins="*")

# Configurações JWT
jwt = JWTManager(app)



# Configurações SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

# Registrar blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(service_bp, url_prefix='/api/services')
app.register_blueprint(order_bp, url_prefix='/api/orders')
app.register_blueprint(proposal_bp, url_prefix='/api/proposals')
app.register_blueprint(evaluation_bp, url_prefix='/api/evaluations')

# Configuração do banco de dados
db.init_app(app)
with app.app_context():
    db.create_all()

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
    app.run(host='0.0.0.0', port=5000, debug=True)
