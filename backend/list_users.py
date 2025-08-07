#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.models.user import db, User
from src.main import app

def list_users():
    """Lista todos os usuários cadastrados no banco de dados"""
    
    with app.app_context():
        print("📋 Usuários cadastrados no banco de dados:")
        print("=" * 50)
        
        users = User.query.all()
        
        if not users:
            print("❌ Nenhum usuário encontrado no banco de dados")
            return
        
        for user in users:
            print(f"\n👤 {user.name}")
            print(f"   📧 Email: {user.email}")
            print(f"   👥 Tipo: {user.user_type}")
            print(f"   📱 Telefone: {user.phone or 'N/A'}")
            print(f"   🏠 Cidade: {user.city or 'N/A'}")
            print(f"   ✅ Ativo: {'Sim' if user.is_active else 'Não'}")
            print(f"   🔐 Hash da senha: {user.password_hash[:50]}...")
            print(f"   📅 Criado em: {user.created_at}")
        
        print(f"\n📊 Total de usuários: {len(users)}")

if __name__ == "__main__":
    list_users()