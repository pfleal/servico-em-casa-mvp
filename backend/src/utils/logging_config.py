import logging
import os
from logging.handlers import RotatingFileHandler
from flask import request, g
import time

def setup_logging(app):
    """
    Configura o sistema de logging para a aplicação Flask
    """
    # Criar diretório de logs se não existir
    logs_dir = os.path.join(os.path.dirname(app.root_path), 'logs')
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    if not app.debug:
        # Configuração para produção
        # Log principal da aplicação
        file_handler = RotatingFileHandler(
            os.path.join(logs_dir, 'servico_em_casa.log'),
            maxBytes=10240000,  # 10MB
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        
        # Log de erros separado
        error_handler = RotatingFileHandler(
            os.path.join(logs_dir, 'errors.log'),
            maxBytes=10240000,  # 10MB
            backupCount=5
        )
        error_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        error_handler.setLevel(logging.ERROR)
        app.logger.addHandler(error_handler)
        
        # Log de acesso HTTP
        access_handler = RotatingFileHandler(
            os.path.join(logs_dir, 'access.log'),
            maxBytes=10240000,  # 10MB
            backupCount=5
        )
        access_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(message)s'
        ))
        access_handler.setLevel(logging.INFO)
        
        # Criar logger específico para acesso
        access_logger = logging.getLogger('access')
        access_logger.addHandler(access_handler)
        access_logger.setLevel(logging.INFO)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('Serviço em Casa startup')
    else:
        # Configuração para desenvolvimento
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]',
            handlers=[
                logging.StreamHandler()
            ]
        )
        app.logger.setLevel(logging.DEBUG)
        app.logger.info('Serviço em Casa startup')

def setup_request_logging(app):
    """
    Configura logging de requisições HTTP
    """
    @app.before_request
    def before_request():
        g.start_time = time.time()
        
        # Log da requisição recebida
        if not request.path.startswith('/static'):
            app.logger.debug(f'Requisição recebida: {request.method} {request.path} - IP: {request.remote_addr}')
    
    @app.after_request
    def after_request(response):
        # Calcular tempo de resposta
        if hasattr(g, 'start_time'):
            duration = time.time() - g.start_time
        else:
            duration = 0
        
        # Log da resposta (apenas para rotas da API)
        if not request.path.startswith('/static'):
            access_logger = logging.getLogger('access')
            log_message = f'{request.remote_addr} - "{request.method} {request.path}" {response.status_code} - {duration:.3f}s'
            
            if not app.debug:
                access_logger.info(log_message)
            else:
                app.logger.info(f'Resposta: {response.status_code} - {duration:.3f}s')
        
        return response
    
    @app.errorhandler(404)
    def not_found_error(error):
        app.logger.warning(f'Página não encontrada: {request.method} {request.path} - IP: {request.remote_addr}')
        return {'error': 'Página não encontrada'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f'Erro interno do servidor: {request.method} {request.path} - IP: {request.remote_addr} - Erro: {str(error)}')
        return {'error': 'Erro interno do servidor'}, 500

def log_user_action(user_id, action, details=None):
    """
    Função auxiliar para logar ações específicas do usuário
    """
    from flask import current_app
    
    message = f'Usuário {user_id}: {action}'
    if details:
        message += f' - {details}'
    
    current_app.logger.info(message)

def log_security_event(event_type, details, user_id=None):
    """
    Função auxiliar para logar eventos de segurança
    """
    from flask import current_app
    
    message = f'SEGURANÇA - {event_type}'
    if user_id:
        message += f' - Usuário: {user_id}'
    if details:
        message += f' - {details}'
    
    current_app.logger.warning(message)