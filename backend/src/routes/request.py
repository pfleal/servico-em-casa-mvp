from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import db, User
from src.models.request import ServiceRequest
from src.models.service import ServiceCategory
from datetime import datetime

request_bp = Blueprint('request', __name__)

@request_bp.route('/', methods=['POST'])
@jwt_required()
def create_request():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validações básicas
        required_fields = ['category_id', 'title', 'description', 'address', 'city', 'state', 'zip_code']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Campo {field} é obrigatório'}), 400
        
        # Verificar se a categoria existe
        category = ServiceCategory.query.get(data['category_id'])
        if not category:
            return jsonify({'error': 'Categoria não encontrada'}), 404
        
        # Verificar se o usuário é um cliente
        user = User.query.get(user_id)
        if user.user_type != 'client':
            return jsonify({'error': 'Apenas clientes podem criar pedidos'}), 403
        
        # Converter data preferida se fornecida
        preferred_date = None
        if data.get('preferred_date'):
            try:
                preferred_date = datetime.fromisoformat(data['preferred_date'].replace('Z', '+00:00'))
            except ValueError:
                return jsonify({'error': 'Formato de data inválido'}), 400
        
        service_request = ServiceRequest(
            client_id=user_id,
            category_id=data['category_id'],
            title=data['title'],
            description=data['description'],
            address=data['address'],
            city=data['city'],
            state=data['state'],
            zip_code=data['zip_code'],
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            urgency=data.get('urgency', 'normal'),
            budget_min=data.get('budget_min'),
            budget_max=data.get('budget_max'),
            preferred_date=preferred_date,
            images=data.get('images')
        )
        
        db.session.add(service_request)
        db.session.commit()
        
        return jsonify({
            'message': 'Pedido criado com sucesso',
            'request': service_request.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@request_bp.route('/', methods=['GET'])
@jwt_required()
def get_requests():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if user.user_type == 'client':
            # Cliente vê seus próprios pedidos
            requests = ServiceRequest.query.filter_by(client_id=user_id).order_by(ServiceRequest.created_at.desc()).all()
        else:
            # Prestador vê pedidos disponíveis na sua área/categoria
            # Por simplicidade, mostrar todos os pedidos abertos
            requests = ServiceRequest.query.filter_by(status='open').order_by(ServiceRequest.created_at.desc()).limit(50).all()
        
        return jsonify({
            'requests': [req.to_dict() for req in requests]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@request_bp.route('/<int:request_id>', methods=['GET'])
@jwt_required()
def get_request_detail(request_id):
    try:
        service_request = ServiceRequest.query.get(request_id)
        
        if not service_request:
            return jsonify({'error': 'Pedido não encontrado'}), 404
        
        # Incluir informações do cliente
        client = User.query.get(service_request.client_id)
        category = ServiceCategory.query.get(service_request.category_id)
        
        request_data = service_request.to_dict()
        request_data['client'] = {
            'id': client.id,
            'name': client.name,
            'average_rating': client.average_rating,
            'total_services': client.total_services
        }
        request_data['category'] = category.to_dict() if category else None
        
        return jsonify({'request': request_data}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@request_bp.route('/<int:request_id>', methods=['PUT'])
@jwt_required()
def update_request(request_id):
    try:
        user_id = get_jwt_identity()
        service_request = ServiceRequest.query.get(request_id)
        
        if not service_request:
            return jsonify({'error': 'Pedido não encontrado'}), 404
        
        # Verificar se o usuário é o dono do pedido
        if service_request.client_id != user_id:
            return jsonify({'error': 'Não autorizado'}), 403
        
        data = request.get_json()
        
        # Campos que podem ser atualizados
        updatable_fields = [
            'title', 'description', 'urgency', 'budget_min', 'budget_max',
            'preferred_date', 'status'
        ]
        
        for field in updatable_fields:
            if field in data:
                if field == 'preferred_date' and data[field]:
                    try:
                        setattr(service_request, field, datetime.fromisoformat(data[field].replace('Z', '+00:00')))
                    except ValueError:
                        return jsonify({'error': 'Formato de data inválido'}), 400
                else:
                    setattr(service_request, field, data[field])
        
        db.session.commit()
        
        return jsonify({
            'message': 'Pedido atualizado com sucesso',
            'request': service_request.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@request_bp.route('/<int:request_id>', methods=['DELETE'])
@jwt_required()
def delete_request(request_id):
    try:
        user_id = get_jwt_identity()
        service_request = ServiceRequest.query.get(request_id)
        
        if not service_request:
            return jsonify({'error': 'Pedido não encontrado'}), 404
        
        # Verificar se o usuário é o dono do pedido
        if service_request.client_id != user_id:
            return jsonify({'error': 'Não autorizado'}), 403
        
        # Só permitir exclusão se não houver propostas aceitas
        from src.models.proposal import Proposal
        accepted_proposals = Proposal.query.filter_by(
            service_request_id=request_id,
            status='accepted'
        ).first()
        
        if accepted_proposals:
            return jsonify({'error': 'Não é possível excluir pedido com proposta aceita'}), 400
        
        db.session.delete(service_request)
        db.session.commit()
        
        return jsonify({'message': 'Pedido excluído com sucesso'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

