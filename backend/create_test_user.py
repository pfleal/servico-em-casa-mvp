#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.models.user import db, User
from src.main import app

def create_test_user():
    with app.app_context():
        # Verificar se o usuário já existe
        existing_user = User.query.filter_by(email='cliente@teste.com').first()
        if existing_user:
            print("Usuário já existe!")
            return
        
        # Criar usuário de teste
        user = User(
            name='Cliente Teste',
            email='cliente@teste.com',
            user_type='client'
        )
        user.set_password('123456')
        
        db.session.add(user)
        db.session.commit()
        
        print("Usuário de teste criado com sucesso!")
        print(f"Email: {user.email}")
        print(f"Senha: 123456")
        print(f"ID: {user.id}")

if __name__ == "__main__":
    create_test_user()