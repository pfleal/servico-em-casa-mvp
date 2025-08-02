from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import db
from src.models.service import ServiceCategory, ProviderService
from sqlalchemy import or_

service_bp = Blueprint('service', __name__)

@service_bp.route('/categories', methods=['GET'])
def get_categories():
    try:
        categories = ServiceCategory.query.filter_by(is_active=True).all()
        return jsonify({
            'categories': [category.to_dict() for category in categories]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@service_bp.route('/categories', methods=['POST'])
@jwt_required()
def create_category():
    try:
        data = request.get_json()
        
        if not data.get('name'):
            return jsonify({'error': 'Nome da categoria é obrigatório'}), 400
        
        # Verificar se já existe
        existing = ServiceCategory.query.filter_by(name=data['name']).first()
        if existing:
            return jsonify({'error': 'Categoria já existe'}), 400
        
        category = ServiceCategory(
            name=data['name'],
            description=data.get('description'),
            icon=data.get('icon')
        )
        
        db.session.add(category)
        db.session.commit()
        
        return jsonify({
            'message': 'Categoria criada com sucesso',
            'category': category.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@service_bp.route('/provider-services', methods=['POST'])
@jwt_required()
def add_provider_service():
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()
        
        if not data.get('category_id'):
            return jsonify({'error': 'ID da categoria é obrigatório'}), 400
        
        # Verificar se a categoria existe
        category = ServiceCategory.query.get(data['category_id'])
        if not category:
            return jsonify({'error': 'Categoria não encontrada'}), 404
        
        # Verificar se o prestador já oferece este serviço
        existing = ProviderService.query.filter_by(
            provider_id=user_id,
            category_id=data['category_id']
        ).first()
        
        if existing:
            return jsonify({'error': 'Você já oferece este serviço'}), 400
        
        provider_service = ProviderService(
            provider_id=user_id,
            category_id=data['category_id'],
            description=data.get('description'),
            base_price=data.get('base_price')
        )
        
        db.session.add(provider_service)
        db.session.commit()
        
        return jsonify({
            'message': 'Serviço adicionado com sucesso',
            'service': provider_service.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@service_bp.route('/provider-services', methods=['GET'])
@jwt_required()
def get_provider_services():
    try:
        user_id = get_jwt_identity()
        services = ProviderService.query.filter_by(provider_id=user_id, is_active=True).all()
        
        return jsonify({
            'services': [service.to_dict() for service in services]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@service_bp.route('/search', methods=['GET'])
def search_providers():
    try:
        # Parâmetros de busca
        category_id = request.args.get('category_id', type=int)
        city = request.args.get('city')
        state = request.args.get('state')
        keyword = request.args.get('keyword')
        min_rating = request.args.get('min_rating', type=float)
        
        # Query base
        from src.models.user import User
        query = User.query.filter_by(user_type='provider', is_active=True, is_verified=True)
        
        # Filtros
        if city:
            query = query.filter(User.city.ilike(f'%{city}%'))
        
        if state:
            query = query.filter(User.state.ilike(f'%{state}%'))
        
        if min_rating:
            query = query.filter(User.average_rating >= min_rating)
        
        if keyword:
            query = query.filter(or_(
                User.name.ilike(f'%{keyword}%'),
                User.bio.ilike(f'%{keyword}%')
            ))
        
        # Se categoria específica foi solicitada
        if category_id:
            provider_ids = db.session.query(ProviderService.provider_id).filter_by(
                category_id=category_id,
                is_active=True
            ).subquery()
            query = query.filter(User.id.in_(provider_ids))
        
        providers = query.limit(50).all()
        
        return jsonify({
            'providers': [provider.to_dict() for provider in providers]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

