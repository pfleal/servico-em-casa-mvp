#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.models.user import db
from src.models.service import ServiceCategory
from src.main import app

def populate_categories():
    categories = [
        {"name": "Limpeza", "description": "Serviços de limpeza doméstica e comercial"},
        {"name": "Elétrica", "description": "Instalações e reparos elétricos"},
        {"name": "Hidráulica", "description": "Instalações e reparos hidráulicos"},
        {"name": "Pintura", "description": "Pintura residencial e comercial"},
        {"name": "Jardinagem", "description": "Cuidados com jardins e plantas"},
        {"name": "Marcenaria", "description": "Móveis sob medida e reparos"},
        {"name": "Pedreiro", "description": "Construção e reformas"},
        {"name": "Ar Condicionado", "description": "Instalação e manutenção de ar condicionado"},
        {"name": "Informática", "description": "Suporte técnico e reparos em computadores"},
        {"name": "Mudanças", "description": "Serviços de mudança e transporte"}
    ]
    
    with app.app_context():
        for cat_data in categories:
            # Verificar se já existe
            existing = ServiceCategory.query.filter_by(name=cat_data["name"]).first()
            if not existing:
                category = ServiceCategory(**cat_data)
                db.session.add(category)
        
        db.session.commit()
        print("Categorias criadas com sucesso!")

if __name__ == "__main__":
    populate_categories()

