from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    user_type = db.Column(db.String(20), nullable=False)  # 'client' ou 'provider'
    address = db.Column(db.String(255), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(50), nullable=True)
    zip_code = db.Column(db.String(10), nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    profile_picture = db.Column(db.String(255), nullable=True)
    is_verified = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    service_requests = db.relationship('ServiceRequest', backref='client', lazy=True, foreign_keys='ServiceRequest.client_id')
    proposals = db.relationship('Proposal', backref='provider', lazy=True, foreign_keys='Proposal.provider_id')
    evaluations_given = db.relationship('Evaluation', backref='evaluator', lazy=True, foreign_keys='Evaluation.evaluator_id')
    evaluations_received = db.relationship('Evaluation', backref='evaluated', lazy=True, foreign_keys='Evaluation.evaluated_id')
    
    # Campos específicos para prestadores
    bio = db.Column(db.Text, nullable=True)
    experience_years = db.Column(db.Integer, nullable=True)
    service_radius = db.Column(db.Integer, nullable=True)  # raio em km
    is_available = db.Column(db.Boolean, default=True)
    average_rating = db.Column(db.Float, default=0.0)
    total_services = db.Column(db.Integer, default=0)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'user_type': self.user_type,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'profile_picture': self.profile_picture,
            'is_verified': self.is_verified,
            'is_active': self.is_active,
            'bio': self.bio,
            'experience_years': self.experience_years,
            'service_radius': self.service_radius,
            'is_available': self.is_available,
            'average_rating': self.average_rating,
            'total_services': self.total_services,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
