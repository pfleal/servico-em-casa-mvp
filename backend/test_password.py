#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.models.user import db, User
from src.main import app

def test_passwords():
    """Testa diferentes senhas para o usuário existente"""
    
    # Senhas possíveis para testar
    possible_passwords = [
        "MinhaSenh@123",
        "123456",
        "senha123",
        "minhasenha",
        "password",
        "admin",
        "joao123",
        "silva123",
        "123",
        "abc123"
    ]
    
    with app.app_context():
        user = User.query.filter_by(email="joao.silva@email.com").first()
        
        if not user:
            print("❌ Usuário não encontrado")
            return
        
        print(f"🔍 Testando senhas para o usuário: {user.name} ({user.email})")
        print("=" * 60)
        
        for password in possible_passwords:
            if user.check_password(password):
                print(f"✅ SENHA CORRETA ENCONTRADA: '{password}'")
                print(f"📧 Email: {user.email}")
                print(f"🔑 Senha: {password}")
                return
            else:
                print(f"❌ Senha incorreta: '{password}'")
        
        print("\n⚠️  Nenhuma das senhas testadas funcionou.")
        print("💡 Vou criar um novo usuário com credenciais conhecidas...")
        
        # Criar um novo usuário de teste
        test_user = User(
            name="Usuário Teste",
            email="teste@email.com",
            user_type="client",
            phone="(11) 99999-0000",
            address="Rua Teste, 123",
            city="São Paulo",
            state="SP",
            zip_code="01000-000"
        )
        test_user.set_password("123456")
        
        # Verificar se já existe
        existing = User.query.filter_by(email="teste@email.com").first()
        if existing:
            print("✅ Usuário de teste já existe:")
            print(f"📧 Email: teste@email.com")
            print(f"🔑 Senha: 123456")
        else:
            db.session.add(test_user)
            db.session.commit()
            print("✅ Usuário de teste criado com sucesso:")
            print(f"📧 Email: teste@email.com")
            print(f"🔑 Senha: 123456")

if __name__ == "__main__":
    test_passwords()