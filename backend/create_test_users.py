#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.models.user import db, User
from src.main import app

def create_test_users():
    """Cria usuários de teste no banco de dados"""
    
    test_users = [
        {
            "name": "João Silva Santos",
            "email": "joao.silva@email.com",
            "password": "MinhaSenh@123",
            "user_type": "client",
            "phone": "(11) 99999-1234",
            "address": "Rua das Flores, 123",
            "city": "São Paulo",
            "state": "SP",
            "zip_code": "01234-567"
        },
        {
            "name": "Maria Oliveira",
            "email": "maria@email.com",
            "password": "123456",
            "user_type": "provider",
            "phone": "(11) 98888-5678",
            "address": "Av. Paulista, 456",
            "city": "São Paulo",
            "state": "SP",
            "zip_code": "01310-100",
            "bio": "Especialista em limpeza residencial com 5 anos de experiência",
            "experience_years": 5,
            "service_radius": 20
        },
        {
            "name": "Carlos Pereira",
            "email": "carlos@email.com",
            "password": "senha123",
            "user_type": "provider",
            "phone": "(11) 97777-9012",
            "address": "Rua Augusta, 789",
            "city": "São Paulo",
            "state": "SP",
            "zip_code": "01305-000",
            "bio": "Eletricista profissional, atendimento 24h",
            "experience_years": 8,
            "service_radius": 15
        },
        {
            "name": "Ana Costa",
            "email": "ana@email.com",
            "password": "minhasenha",
            "user_type": "client",
            "phone": "(11) 96666-3456",
            "address": "Rua da Consolação, 321",
            "city": "São Paulo",
            "state": "SP",
            "zip_code": "01302-000"
        }
    ]
    
    with app.app_context():
        print("🔄 Criando usuários de teste...")
        
        for user_data in test_users:
            # Verificar se o usuário já existe
            existing_user = User.query.filter_by(email=user_data["email"]).first()
            if existing_user:
                print(f"⚠️  Usuário {user_data['email']} já existe")
                continue
            
            # Criar novo usuário
            user = User(
                name=user_data["name"],
                email=user_data["email"],
                user_type=user_data["user_type"],
                phone=user_data.get("phone"),
                address=user_data.get("address"),
                city=user_data.get("city"),
                state=user_data.get("state"),
                zip_code=user_data.get("zip_code"),
                bio=user_data.get("bio"),
                experience_years=user_data.get("experience_years"),
                service_radius=user_data.get("service_radius")
            )
            user.set_password(user_data["password"])
            
            db.session.add(user)
            print(f"✅ Usuário criado: {user_data['name']} ({user_data['email']})")
        
        db.session.commit()
        print("\n🎉 Usuários de teste criados com sucesso!")
        
        # Listar todos os usuários
        print("\n📋 Usuários cadastrados:")
        users = User.query.all()
        for user in users:
            print(f"- {user.name} ({user.email}) - {user.user_type}")

if __name__ == "__main__":
    create_test_users()