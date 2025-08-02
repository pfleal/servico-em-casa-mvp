from src.models.user import db
from datetime import datetime

class Evaluation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_request_id = db.Column(db.Integer, db.ForeignKey('service_request.id'), nullable=False)
    evaluator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # quem avalia
    evaluated_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # quem é avaliado
    rating = db.Column(db.Integer, nullable=False)  # 1 a 5 estrelas
    comment = db.Column(db.Text, nullable=True)
    punctuality = db.Column(db.Integer, nullable=True)  # 1 a 5
    quality = db.Column(db.Integer, nullable=True)  # 1 a 5
    communication = db.Column(db.Integer, nullable=True)  # 1 a 5
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'service_request_id': self.service_request_id,
            'evaluator_id': self.evaluator_id,
            'evaluated_id': self.evaluated_id,
            'rating': self.rating,
            'comment': self.comment,
            'punctuality': self.punctuality,
            'quality': self.quality,
            'communication': self.communication,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

