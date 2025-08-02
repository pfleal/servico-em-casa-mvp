from src.models.user import db
from datetime import datetime

class ServiceRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('service_category.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    zip_code = db.Column(db.String(10), nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    urgency = db.Column(db.String(20), default='normal')  # 'low', 'normal', 'high', 'urgent'
    budget_min = db.Column(db.Float, nullable=True)
    budget_max = db.Column(db.Float, nullable=True)
    preferred_date = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), default='open')  # 'open', 'in_progress', 'completed', 'cancelled'
    images = db.Column(db.Text, nullable=True)  # JSON string com URLs das imagens
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    proposals = db.relationship('Proposal', backref='service_request', lazy=True, cascade='all, delete-orphan')
    messages = db.relationship('Message', backref='service_request', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'client_id': self.client_id,
            'category_id': self.category_id,
            'title': self.title,
            'description': self.description,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'urgency': self.urgency,
            'budget_min': self.budget_min,
            'budget_max': self.budget_max,
            'preferred_date': self.preferred_date.isoformat() if self.preferred_date else None,
            'status': self.status,
            'images': self.images,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

