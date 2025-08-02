from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import db, User
from src.models.request import ServiceRequest
from src.models.service import ServiceCategory
from datetime import datetime
import logging

# Logger específico para rotas de request
request_logger = logging.getLogger('servico_em_casa.request')

request_bp = Blueprint('request', __name__)

@request_bp.route('/', methods=['POST'])
@jwt_required()
def create_request():
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()
        
        request_logger.info(f'Usuário {user_id} tentando criar pedido')
        request_logger.debug(f'Dados recebidos: {data}')
        
        # Validações básicas
        required_fields = ['category_id', 'title', 'description', 'address', 'city', 'state', 'zip_code']
        for field in required_fields:
            if not data.get(field):
                request_logger.warning(f'Campo obrigatório ausente: {field} - Usuário: {user_id}')
                return jsonify({'error': f'Campo {field} é obrigatório'}), 400
        
        # Verificar se a categoria existe
        category = ServiceCategory.query.get(data['category_id'])
        if not category:
            request_logger.warning(f'Categoria {data["category_id"]} não encontrada - Usuário: {user_id}')
            return jsonify({'error': 'Categoria não encontrada'}), 404
        
        # Verificar se o usuário é um cliente
        user = User.query.get(user_id)
        if user.user_type != 'client':
            request_logger.warning(f'Usuário {user_id} ({user.user_type}) tentou criar pedido sem permissão')
            return jsonify({'error': 'Apenas clientes podem criar pedidos'}), 403
        
        # Converter data preferida se fornecida
        preferred_date = None
        if data.get('preferred_date'):
            try:
                preferred_date = datetime.fromisoformat(data['preferred_date'].replace('Z', '+00:00'))
                request_logger.debug(f'Data preferida convertida: {preferred_date}')
            except ValueError:
                request_logger.warning(f'Formato de data inválido: {data.get("preferred_date")} - Usuário: {user_id}')
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
        
        request_logger.info(f'Pedido criado com sucesso - ID: {service_request.id} - Usuário: {user_id}')
        
        return jsonify({
            'message': 'Pedido criado com sucesso',
            'request': service_request.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        request_logger.error(f'Erro ao criar pedido - Usuário: {user_id} - Erro: {str(e)}', exc_info=True)
        return jsonify({
            'error': 'Erro ao criar pedido',
            'details': str(e) if current_app.debug else 'Erro interno do servidor'
        }), 500

@request_bp.route('/', methods=['GET'])
@jwt_required()
def get_requests():
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        request_logger.info(f'Usuário {user_id} buscando pedidos')
        
        if user.user_type == 'client':
            # Cliente vê seus próprios pedidos
            requests = ServiceRequest.query.filter_by(client_id=user_id).order_by(ServiceRequest.created_at.desc()).all()
            request_logger.debug(f'Cliente {user_id} encontrou {len(requests)} pedidos próprios')
        else:
            # Prestador vê pedidos disponíveis na sua área/categoria
            # Por simplicidade, mostrar todos os pedidos abertos
            requests = ServiceRequest.query.filter_by(status='open').order_by(ServiceRequest.created_at.desc()).limit(50).all()
            request_logger.debug(f'Prestador {user_id} encontrou {len(requests)} pedidos disponíveis')
        
        return jsonify({
            'requests': [req.to_dict() for req in requests]
        }), 200
        
    except Exception as e:
        request_logger.error(f'Erro ao buscar pedidos - Usuário: {user_id} - Erro: {str(e)}', exc_info=True)
        return jsonify({
            'error': 'Erro interno do servidor ao buscar pedidos',
            'details': str(e) if current_app.debug else 'Contate o suporte'
        }), 500

@request_bp.route('/<int:request_id>', methods=['GET'])
@jwt_required()
def get_request_detail(request_id):
    try:
        user_id = int(get_jwt_identity())
        request_logger.info(f'Usuário {user_id} buscando detalhes do pedido {request_id}')
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
        
        request_logger.debug(f'Detalhes do pedido {request_id} retornados para usuário {user_id}')
        return jsonify({'request': request_data}), 200
        
    except Exception as e:
        request_logger.error(f'Erro ao buscar detalhes do pedido {request_id} - Usuário: {user_id} - Erro: {str(e)}', exc_info=True)
        return jsonify({
            'error': 'Erro interno do servidor ao buscar detalhes do pedido',
            'details': str(e) if current_app.debug else 'Contate o suporte'
        }), 500

@request_bp.route('/<int:request_id>', methods=['PUT'])
@jwt_required()
def update_request(request_id):
    try:
        user_id = int(get_jwt_identity())
        request_logger.info(f'Usuário {user_id} tentando atualizar pedido {request_id}')
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
        
        request_logger.info(f'Pedido {request_id} atualizado com sucesso - Usuário: {user_id}')
        return jsonify({
            'message': 'Pedido atualizado com sucesso',
            'request': service_request.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        request_logger.error(f'Erro ao atualizar pedido {request_id} - Usuário: {user_id} - Erro: {str(e)}', exc_info=True)
        return jsonify({
            'error': 'Erro interno do servidor ao atualizar pedido',
            'details': str(e) if current_app.debug else 'Contate o suporte'
        }), 500

@request_bp.route('/<int:request_id>', methods=['DELETE'])
@jwt_required()
def delete_request(request_id):
    try:
        user_id = int(get_jwt_identity())
        request_logger.info(f'Usuário {user_id} tentando excluir pedido {request_id}')
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
        
        request_logger.info(f'Pedido {request_id} excluído com sucesso - Usuário: {user_id}')
        return jsonify({'message': 'Pedido excluído com sucesso'}), 200
        
    except Exception as e:
        db.session.rollback()
        request_logger.error(f'Erro ao excluir pedido {request_id} - Usuário: {user_id} - Erro: {str(e)}', exc_info=True)
        return jsonify({
            'error': 'Erro interno do servidor ao excluir pedido',
            'details': str(e) if current_app.debug else 'Contate o suporte'
        }), 500

