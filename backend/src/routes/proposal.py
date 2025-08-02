from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import db, User
from src.models.request import ServiceRequest
from src.models.proposal import Proposal

proposal_bp = Blueprint('proposal', __name__)

@proposal_bp.route('/', methods=['POST'])
@jwt_required()
def create_proposal():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validações básicas
        required_fields = ['service_request_id', 'price']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Campo {field} é obrigatório'}), 400
        
        # Verificar se o pedido existe
        service_request = ServiceRequest.query.get(data['service_request_id'])
        if not service_request:
            return jsonify({'error': 'Pedido não encontrado'}), 404
        
        # Verificar se o pedido está aberto
        if service_request.status != 'open':
            return jsonify({'error': 'Pedido não está mais disponível'}), 400
        
        # Verificar se o usuário é um prestador
        user = User.query.get(user_id)
        if user.user_type != 'provider':
            return jsonify({'error': 'Apenas prestadores podem enviar propostas'}), 403
        
        # Verificar se o prestador não é o mesmo cliente do pedido
        if service_request.client_id == user_id:
            return jsonify({'error': 'Você não pode enviar proposta para seu próprio pedido'}), 400
        
        # Verificar se já existe uma proposta deste prestador para este pedido
        existing_proposal = Proposal.query.filter_by(
            service_request_id=data['service_request_id'],
            provider_id=user_id
        ).first()
        
        if existing_proposal:
            return jsonify({'error': 'Você já enviou uma proposta para este pedido'}), 400
        
        proposal = Proposal(
            service_request_id=data['service_request_id'],
            provider_id=user_id,
            price=data['price'],
            estimated_duration=data.get('estimated_duration'),
            description=data.get('description'),
            materials_included=data.get('materials_included', False),
            availability=data.get('availability')
        )
        
        db.session.add(proposal)
        db.session.commit()
        
        return jsonify({
            'message': 'Proposta enviada com sucesso',
            'proposal': proposal.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao criar proposta: {str(e)}")
        return jsonify({
            'error': 'Erro interno do servidor ao criar proposta',
            'details': str(e) if current_app.debug else 'Contate o suporte'
        }), 500

@proposal_bp.route('/request/<int:request_id>', methods=['GET'])
@jwt_required()
def get_proposals_by_request(request_id):
    try:
        user_id = int(get_jwt_identity())
        
        # Verificar se o pedido existe
        service_request = ServiceRequest.query.get(request_id)
        if not service_request:
            return jsonify({'error': 'Pedido não encontrado'}), 404
        
        # Verificar se o usuário é o dono do pedido
        if service_request.client_id != user_id:
            return jsonify({'error': 'Não autorizado'}), 403
        
        proposals = Proposal.query.filter_by(service_request_id=request_id).all()
        
        # Incluir informações do prestador em cada proposta
        proposals_data = []
        for proposal in proposals:
            provider = User.query.get(proposal.provider_id)
            proposal_data = proposal.to_dict()
            proposal_data['provider'] = {
                'id': provider.id,
                'name': provider.name,
                'average_rating': provider.average_rating,
                'total_services': provider.total_services,
                'profile_picture': provider.profile_picture,
                'bio': provider.bio,
                'experience_years': provider.experience_years
            }
            proposals_data.append(proposal_data)
        
        return jsonify({'proposals': proposals_data}), 200
        
    except Exception as e:
        print(f"Erro ao buscar propostas: {str(e)}")
        return jsonify({
            'error': 'Erro interno do servidor ao buscar propostas',
            'details': str(e) if current_app.debug else 'Contate o suporte'
        }), 500

@proposal_bp.route('/<int:proposal_id>/accept', methods=['POST'])
@jwt_required()
def accept_proposal(proposal_id):
    try:
        user_id = int(get_jwt_identity())
        
        proposal = Proposal.query.get(proposal_id)
        if not proposal:
            return jsonify({'error': 'Proposta não encontrada'}), 404
        
        # Verificar se o usuário é o dono do pedido
        service_request = ServiceRequest.query.get(proposal.service_request_id)
        if service_request.client_id != user_id:
            return jsonify({'error': 'Não autorizado'}), 403
        
        # Verificar se a proposta ainda está pendente
        if proposal.status != 'pending':
            return jsonify({'error': 'Proposta não está mais disponível'}), 400
        
        # Aceitar a proposta
        proposal.status = 'accepted'
        
        # Atualizar status do pedido
        service_request.status = 'in_progress'
        
        # Rejeitar todas as outras propostas
        other_proposals = Proposal.query.filter_by(
            service_request_id=proposal.service_request_id
        ).filter(Proposal.id != proposal_id).all()
        
        for other_proposal in other_proposals:
            if other_proposal.status == 'pending':
                other_proposal.status = 'rejected'
        
        db.session.commit()
        
        return jsonify({
            'message': 'Proposta aceita com sucesso',
            'proposal': proposal.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao aceitar proposta: {str(e)}")
        return jsonify({
            'error': 'Erro interno do servidor ao aceitar proposta',
            'details': str(e) if current_app.debug else 'Contate o suporte'
        }), 500

@proposal_bp.route('/<int:proposal_id>/reject', methods=['POST'])
@jwt_required()
def reject_proposal(proposal_id):
    try:
        user_id = int(get_jwt_identity())
        
        proposal = Proposal.query.get(proposal_id)
        if not proposal:
            return jsonify({'error': 'Proposta não encontrada'}), 404
        
        # Verificar se o usuário é o dono do pedido
        service_request = ServiceRequest.query.get(proposal.service_request_id)
        if service_request.client_id != user_id:
            return jsonify({'error': 'Não autorizado'}), 403
        
        # Verificar se a proposta ainda está pendente
        if proposal.status != 'pending':
            return jsonify({'error': 'Proposta não pode ser rejeitada'}), 400
        
        proposal.status = 'rejected'
        db.session.commit()
        
        return jsonify({
            'message': 'Proposta rejeitada',
            'proposal': proposal.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao rejeitar proposta: {str(e)}")
        return jsonify({
            'error': 'Erro interno do servidor ao rejeitar proposta',
            'details': str(e) if current_app.debug else 'Contate o suporte'
        }), 500

@proposal_bp.route('/my-proposals', methods=['GET'])
@jwt_required()
def get_my_proposals():
    try:
        user_id = int(get_jwt_identity())
        
        proposals = Proposal.query.filter_by(provider_id=user_id).order_by(Proposal.created_at.desc()).all()
        
        # Incluir informações do pedido em cada proposta
        proposals_data = []
        for proposal in proposals:
            service_request = ServiceRequest.query.get(proposal.service_request_id)
            client = User.query.get(service_request.client_id)
            
            proposal_data = proposal.to_dict()
            proposal_data['service_request'] = {
                'id': service_request.id,
                'title': service_request.title,
                'description': service_request.description,
                'city': service_request.city,
                'state': service_request.state,
                'status': service_request.status
            }
            proposal_data['client'] = {
                'id': client.id,
                'name': client.name,
                'average_rating': client.average_rating
            }
            proposals_data.append(proposal_data)
        
        return jsonify({'proposals': proposals_data}), 200
        
    except Exception as e:
        print(f"Erro ao buscar minhas propostas: {str(e)}")
        return jsonify({
            'error': 'Erro interno do servidor ao buscar minhas propostas',
            'details': str(e) if current_app.debug else 'Contate o suporte'
        }), 500

