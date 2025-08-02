from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from src.models.user import User, db
import re

auth_bp = Blueprint('auth', __name__)

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        current_app.logger.info(f'Tentativa de registro para email: {data.get("email", "N/A")}')
        
        # Validações básicas
        required_fields = ['name', 'email', 'password', 'user_type']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Campo {field} é obrigatório'}), 400
        
        if not validate_email(data['email']):
            return jsonify({'error': 'E-mail inválido'}), 400
        
        if data['user_type'] not in ['client', 'provider']:
            return jsonify({'error': 'Tipo de usuário inválido'}), 400
        
        if len(data['password']) < 6:
            return jsonify({'error': 'Senha deve ter pelo menos 6 caracteres'}), 400
        
        # Verificar se o e-mail já existe
        if User.query.filter_by(email=data['email']).first():
            current_app.logger.warning(f'Tentativa de registro com email já existente: {data["email"]}')
            return jsonify({'error': 'E-mail já cadastrado'}), 400
        
        # Criar novo usuário
        user = User(
            name=data['name'],
            email=data['email'],
            user_type=data['user_type'],
            phone=data.get('phone'),
            address=data.get('address'),
            city=data.get('city'),
            state=data.get('state'),
            zip_code=data.get('zip_code'),
            bio=data.get('bio'),
            experience_years=data.get('experience_years'),
            service_radius=data.get('service_radius')
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        current_app.logger.info(f'Usuário registrado com sucesso: {user.email} (ID: {user.id})')
        
        # Criar token de acesso
        access_token = create_access_token(identity=str(user.id))
        
        return jsonify({
            'message': 'Usuário criado com sucesso',
            'access_token': access_token,
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Erro no registro: {str(e)}')
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        current_app.logger.info(f'Tentativa de login para email: {data.get("email", "N/A")}')
        
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'E-mail e senha são obrigatórios'}), 400
        
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or not user.check_password(data['password']):
            current_app.logger.warning(f'Tentativa de login falhada para email: {data.get("email", "N/A")}')
            return jsonify({'error': 'E-mail ou senha incorretos'}), 401
        
        if not user.is_active:
            current_app.logger.warning(f'Tentativa de login com conta desativada: {user.email}')
            return jsonify({'error': 'Conta desativada'}), 401
        
        access_token = create_access_token(identity=str(user.id))
        
        current_app.logger.info(f'Login bem-sucedido para usuário: {user.email} (ID: {user.id})')
        
        return jsonify({
            'message': 'Login realizado com sucesso',
            'access_token': access_token,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        current_app.logger.error(f'Erro no login: {str(e)}')
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        return jsonify({'user': user.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        data = request.get_json()
        
        # Campos que podem ser atualizados
        updatable_fields = [
            'name', 'phone', 'address', 'city', 'state', 'zip_code',
            'bio', 'experience_years', 'service_radius', 'is_available'
        ]
        
        for field in updatable_fields:
            if field in data:
                setattr(user, field, data[field])
        
        db.session.commit()
        
        return jsonify({
            'message': 'Perfil atualizado com sucesso',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

