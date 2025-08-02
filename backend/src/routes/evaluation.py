from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import db, User
from src.models.request import ServiceRequest
from src.models.proposal import Proposal
from src.models.evaluation import Evaluation
from sqlalchemy import func

evaluation_bp = Blueprint('evaluation', __name__)

@evaluation_bp.route('/', methods=['POST'])
@jwt_required()
def create_evaluation():
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()
        
        # Validações básicas
        required_fields = ['service_request_id', 'evaluated_id', 'rating']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Campo {field} é obrigatório'}), 400
        
        # Validar rating
        if not isinstance(data['rating'], int) or data['rating'] < 1 or data['rating'] > 5:
            return jsonify({'error': 'Rating deve ser um número entre 1 e 5'}), 400
        
        # Verificar se o pedido existe
        service_request = ServiceRequest.query.get(data['service_request_id'])
        if not service_request:
            return jsonify({'error': 'Pedido não encontrado'}), 404
        
        # Verificar se o serviço foi concluído
        if service_request.status != 'completed':
            return jsonify({'error': 'Só é possível avaliar serviços concluídos'}), 400
        
        # Verificar se o usuário tem permissão para avaliar
        evaluated_user = User.query.get(data['evaluated_id'])
        if not evaluated_user:
            return jsonify({'error': 'Usuário avaliado não encontrado'}), 404
        
        # Verificar se o usuário está envolvido no pedido
        is_client = service_request.client_id == user_id
        
        # Se é cliente, deve avaliar o prestador
        if is_client:
            # Verificar se existe proposta aceita do prestador avaliado
            accepted_proposal = Proposal.query.filter_by(
                service_request_id=data['service_request_id'],
                provider_id=data['evaluated_id'],
                status='accepted'
            ).first()
            
            if not accepted_proposal:
                return jsonify({'error': 'Prestador não trabalhou neste pedido'}), 400
        else:
            # Se é prestador, deve avaliar o cliente
            # Verificar se o prestador tem proposta aceita neste pedido
            accepted_proposal = Proposal.query.filter_by(
                service_request_id=data['service_request_id'],
                provider_id=user_id,
                status='accepted'
            ).first()
            
            if not accepted_proposal:
                return jsonify({'error': 'Você não trabalhou neste pedido'}), 400
            
            # Verificar se está avaliando o cliente correto
            if data['evaluated_id'] != service_request.client_id:
                return jsonify({'error': 'Você só pode avaliar o cliente deste pedido'}), 400
        
        # Verificar se já existe avaliação
        existing_evaluation = Evaluation.query.filter_by(
            service_request_id=data['service_request_id'],
            evaluator_id=user_id,
            evaluated_id=data['evaluated_id']
        ).first()
        
        if existing_evaluation:
            return jsonify({'error': 'Você já avaliou este usuário para este serviço'}), 400
        
        evaluation = Evaluation(
            service_request_id=data['service_request_id'],
            evaluator_id=user_id,
            evaluated_id=data['evaluated_id'],
            rating=data['rating'],
            comment=data.get('comment'),
            punctuality=data.get('punctuality'),
            quality=data.get('quality'),
            communication=data.get('communication')
        )
        
        db.session.add(evaluation)
        
        # Atualizar média de avaliações do usuário avaliado
        avg_rating = db.session.query(func.avg(Evaluation.rating)).filter_by(
            evaluated_id=data['evaluated_id']
        ).scalar()
        
        total_evaluations = Evaluation.query.filter_by(
            evaluated_id=data['evaluated_id']
        ).count() + 1
        
        evaluated_user.average_rating = round(avg_rating, 2) if avg_rating else data['rating']
        
        # Se é prestador sendo avaliado, atualizar total de serviços
        if evaluated_user.user_type == 'provider':
            evaluated_user.total_services = total_evaluations
        
        db.session.commit()
        
        return jsonify({
            'message': 'Avaliação criada com sucesso',
            'evaluation': evaluation.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao criar avaliação: {str(e)}")
        return jsonify({
            'error': 'Erro interno do servidor ao criar avaliação',
            'details': str(e) if current_app.debug else 'Contate o suporte'
        }), 500

@evaluation_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_evaluations(user_id):
    try:
        # Verificar se o usuário existe
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        evaluations = Evaluation.query.filter_by(evaluated_id=user_id).order_by(Evaluation.created_at.desc()).all()
        
        # Incluir informações do avaliador
        evaluations_data = []
        for evaluation in evaluations:
            evaluator = User.query.get(evaluation.evaluator_id)
            evaluation_data = evaluation.to_dict()
            evaluation_data['evaluator'] = {
                'id': evaluator.id,
                'name': evaluator.name,
                'user_type': evaluator.user_type
            }
            evaluations_data.append(evaluation_data)
        
        return jsonify({
            'evaluations': evaluations_data,
            'average_rating': user.average_rating,
            'total_evaluations': len(evaluations)
        }), 200
        
    except Exception as e:
        print(f"Erro ao buscar avaliações do usuário: {str(e)}")
        return jsonify({
            'error': 'Erro interno do servidor ao buscar avaliações do usuário',
            'details': str(e) if current_app.debug else 'Contate o suporte'
        }), 500

@evaluation_bp.route('/request/<int:request_id>', methods=['GET'])
@jwt_required()
def get_request_evaluations(request_id):
    try:
        user_id = int(get_jwt_identity())
        
        # Verificar se o pedido existe
        service_request = ServiceRequest.query.get(request_id)
        if not service_request:
            return jsonify({'error': 'Pedido não encontrado'}), 404
        
        # Verificar se o usuário está envolvido no pedido
        is_client = service_request.client_id == user_id
        is_provider = False
        
        if not is_client:
            # Verificar se é o prestador que trabalhou no pedido
            accepted_proposal = Proposal.query.filter_by(
                service_request_id=request_id,
                provider_id=user_id,
                status='accepted'
            ).first()
            is_provider = bool(accepted_proposal)
        
        if not is_client and not is_provider:
            return jsonify({'error': 'Não autorizado'}), 403
        
        evaluations = Evaluation.query.filter_by(service_request_id=request_id).all()
        
        evaluations_data = []
        for evaluation in evaluations:
            evaluator = User.query.get(evaluation.evaluator_id)
            evaluated = User.query.get(evaluation.evaluated_id)
            
            evaluation_data = evaluation.to_dict()
            evaluation_data['evaluator'] = {
                'id': evaluator.id,
                'name': evaluator.name,
                'user_type': evaluator.user_type
            }
            evaluation_data['evaluated'] = {
                'id': evaluated.id,
                'name': evaluated.name,
                'user_type': evaluated.user_type
            }
            evaluations_data.append(evaluation_data)
        
        return jsonify({'evaluations': evaluations_data}), 200
        
    except Exception as e:
        print(f"Erro ao buscar avaliações do pedido: {str(e)}")
        return jsonify({
            'error': 'Erro interno do servidor ao buscar avaliações do pedido',
            'details': str(e) if current_app.debug else 'Contate o suporte'
        }), 500

@evaluation_bp.route('/my-evaluations', methods=['GET'])
@jwt_required()
def get_my_evaluations():
    try:
        user_id = int(get_jwt_identity())
        
        # Avaliações recebidas
        received = Evaluation.query.filter_by(evaluated_id=user_id).order_by(Evaluation.created_at.desc()).all()
        
        # Avaliações dadas
        given = Evaluation.query.filter_by(evaluator_id=user_id).order_by(Evaluation.created_at.desc()).all()
        
        received_data = []
        for evaluation in received:
            evaluator = User.query.get(evaluation.evaluator_id)
            evaluation_data = evaluation.to_dict()
            evaluation_data['evaluator'] = {
                'id': evaluator.id,
                'name': evaluator.name,
                'user_type': evaluator.user_type
            }
            received_data.append(evaluation_data)
        
        given_data = []
        for evaluation in given:
            evaluated = User.query.get(evaluation.evaluated_id)
            evaluation_data = evaluation.to_dict()
            evaluation_data['evaluated'] = {
                'id': evaluated.id,
                'name': evaluated.name,
                'user_type': evaluated.user_type
            }
            given_data.append(evaluation_data)
        
        return jsonify({
            'received': received_data,
            'given': given_data
        }), 200
        
    except Exception as e:
        print(f"Erro ao buscar minhas avaliações: {str(e)}")
        return jsonify({
            'error': 'Erro interno do servidor ao buscar suas avaliações',
            'details': str(e) if current_app.debug else 'Contate o suporte'
        }), 500

