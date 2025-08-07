#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.models.user import db, User
from src.main import app
from werkzeug.security import check_password_hash

def test_cloud_login():
    """Testa o login diretamente no banco da nuvem"""
    
    with app.app_context():
        print("🔍 Testando login no banco da nuvem...")
        print("=" * 50)
        
        email = "joao.silva@email.com"
        password = "MinhaSenh@123"
        
        # Buscar usuário
        user = User.query.filter_by(email=email).first()
        
        if not user:
            print(f"❌ Usuário '{email}' não encontrado!")
            return
        
        print(f"✅ Usuário encontrado:")
        print(f"   📧 Email: {user.email}")
        print(f"   👤 Nome: {user.name}")
        print(f"   🔐 Hash: {user.password_hash}")
        print(f"   ✅ Ativo: {user.is_active}")
        
        # Testar senha usando o método da classe
        print(f"\n🔐 Testando senha '{password}':")
        
        # Método 1: usando user.check_password()
        result1 = user.check_password(password)
        print(f"   user.check_password(): {result1}")
        
        # Método 2: usando check_password_hash diretamente
        result2 = check_password_hash(user.password_hash, password)
        print(f"   check_password_hash(): {result2}")
        
        # Verificar se a conta está ativa
        print(f"\n👤 Status da conta:")
        print(f"   is_active: {user.is_active}")
        print(f"   is_verified: {user.is_verified}")
        
        if result1 and result2:
            print(f"\n✅ SENHA CORRETA! O login deveria funcionar.")
            if not user.is_active:
                print(f"⚠️  Mas a conta está DESATIVADA!")
        else:
            print(f"\n❌ SENHA INCORRETA!")
            print(f"\n💡 Vou tentar outras senhas comuns:")
            
            test_passwords = [
                "123456",
                "senha123",
                "MinhaSenh@123",
                "minhasenha",
                "password"
            ]
            
            for test_pwd in test_passwords:
                if user.check_password(test_pwd):
                    print(f"   ✅ Senha correta encontrada: '{test_pwd}'")
                    break
                else:
                    print(f"   ❌ '{test_pwd}' - incorreta")

if __name__ == "__main__":
    test_cloud_login()