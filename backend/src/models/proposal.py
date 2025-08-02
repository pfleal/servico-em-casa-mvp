from src.models.user import db
from datetime import datetime

class Proposal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_request_id = db.Column(db.Integer, db.ForeignKey('service_request.id'), nullable=False)
    provider_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)
    estimated_duration = db.Column(db.String(100), nullable=True)  # ex: "2 horas", "1 dia"
    description = db.Column(db.Text, nullable=True)
    materials_included = db.Column(db.Boolean, default=False)
    availability = db.Column(db.String(200), nullable=True)
    status = db.Column(db.String(20), default='pending')  # 'pending', 'accepted', 'rejected', 'cancelled'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'service_request_id': self.service_request_id,
            'provider_id': self.provider_id,
            'price': self.price,
            'estimated_duration': self.estimated_duration,
            'description': self.description,
            'materials_included': self.materials_included,
            'availability': self.availability,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

