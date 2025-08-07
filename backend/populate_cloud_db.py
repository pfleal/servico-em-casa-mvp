#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.models.user import db, User
from src.main import app

def populate_cloud_db():
    """Popula o banco de dados da nuvem com usuários de teste"""
    
    with app.app_context():
        print("🌐 Populando banco de dados da nuvem...")
        print("=" * 50)
        
        # Verificar se já existem usuários
        existing_users = User.query.all()
        print(f"📊 Usuários existentes: {len(existing_users)}")
        
        # Usuários para criar
        users_to_create = [
            {
                "name": "João Silva Santos",
                "email": "joao.silva@email.com",
                "password": "MinhaSenh@123",
                "user_type": "client",
                "phone": "(11) 99999-8888",
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
                "phone": "(11) 98888-7777",
                "address": "Av. Paulista, 456",
                "city": "São Paulo",
                "state": "SP",
                "zip_code": "01310-100"
            },
            {
                "name": "Usuário Teste",
                "email": "teste@email.com",
                "password": "123456",
                "user_type": "client",
                "phone": "(11) 99999-0000",
                "address": "Rua Teste, 123",
                "city": "São Paulo",
                "state": "SP",
                "zip_code": "01000-000"
            }
        ]
        
        created_count = 0
        
        for user_data in users_to_create:
            # Verificar se o usuário já existe
            existing = User.query.filter_by(email=user_data["email"]).first()
            
            if existing:
                print(f"⚠️  Usuário já existe: {user_data['email']}")
                continue
            
            # Criar novo usuário
            user = User(
                name=user_data["name"],
                email=user_data["email"],
                user_type=user_data["user_type"],
                phone=user_data["phone"],
                address=user_data["address"],
                city=user_data["city"],
                state=user_data["state"],
                zip_code=user_data["zip_code"]
            )
            user.set_password(user_data["password"])
            
            try:
                db.session.add(user)
                db.session.commit()
                print(f"✅ Usuário criado: {user_data['name']} ({user_data['email']})")
                print(f"   🔑 Senha: {user_data['password']}")
                created_count += 1
            except Exception as e:
                db.session.rollback()
                print(f"❌ Erro ao criar usuário {user_data['email']}: {str(e)}")
        
        print(f"\n📊 Resumo:")
        print(f"   👥 Usuários criados: {created_count}")
        print(f"   📋 Total de usuários no banco: {len(User.query.all())}")
        
        # Listar todos os usuários
        print("\n👤 Usuários disponíveis para login:")
        all_users = User.query.all()
        for user in all_users:
            print(f"   📧 {user.email} - {user.name} ({user.user_type})")

if __name__ == "__main__":
    populate_cloud_db()