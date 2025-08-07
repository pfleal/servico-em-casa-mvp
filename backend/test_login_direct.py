#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.main import app
from src.models.user import User, db
from werkzeug.security import check_password_hash

def test_login_direct():
    """Testa o login diretamente usando o contexto da aplicação"""
    
    with app.app_context():
        print("🔍 Testando login diretamente no contexto da aplicação...")
        print("=" * 60)
        
        # Verificar configuração do banco
        print(f"📊 Configuração do banco: {app.config['SQLALCHEMY_DATABASE_URI']}")
        
        # Buscar o usuário
        email = "joao.silva@email.com"
        user = User.query.filter_by(email=email).first()
        
        if not user:
            print(f"❌ Usuário '{email}' não encontrado no banco!")
            
            # Listar todos os usuários
            print("\n📋 Usuários existentes no banco:")
            all_users = User.query.all()
            if all_users:
                for u in all_users:
                    print(f"   📧 {u.email} - {u.name} (ID: {u.id})")
            else:
                print("   ❌ Nenhum usuário encontrado!")
            return
        
        print(f"✅ Usuário encontrado:")
        print(f"   📧 Email: {user.email}")
        print(f"   👤 Nome: {user.name}")
        print(f"   🆔 ID: {user.id}")
        print(f"   🔐 Hash: {user.password_hash[:50]}...")
        print(f"   ✅ Ativo: {user.is_active}")
        print(f"   ✅ Verificado: {user.is_verified}")
        
        # Testar senhas
        test_passwords = ["MinhaSenh@123", "123456", "senha123", "password"]
        
        print(f"\n🔍 Testando senhas:")
        for pwd in test_passwords:
            # Testar com o método do usuário
            result_user = user.check_password(pwd)
            
            # Testar diretamente com check_password_hash
            result_direct = check_password_hash(user.password_hash, pwd)
            
            status = "✅" if result_user else "❌"
            print(f"   {status} '{pwd}': user.check_password() = {result_user}, check_password_hash() = {result_direct}")
            
            if result_user:
                print(f"   🎉 SENHA CORRETA ENCONTRADA: '{pwd}'")
                break
        
        # Simular o processo de login completo
        print(f"\n🔄 Simulando processo de login completo:")
        login_password = "MinhaSenh@123"
        
        print(f"   1. Buscar usuário por email '{email}'...")
        login_user = User.query.filter_by(email=email).first()
        print(f"      Resultado: {'✅ Encontrado' if login_user else '❌ Não encontrado'}")
        
        if login_user:
            print(f"   2. Verificar senha '{login_password}'...")
            password_ok = login_user.check_password(login_password)
            print(f"      Resultado: {'✅ Senha correta' if password_ok else '❌ Senha incorreta'}")
            
            print(f"   3. Verificar se conta está ativa...")
            print(f"      Resultado: {'✅ Conta ativa' if login_user.is_active else '❌ Conta inativa'}")
            
            # Resultado final
            if login_user and password_ok and login_user.is_active:
                print(f"\n🎉 LOGIN DEVERIA FUNCIONAR!")
            else:
                print(f"\n❌ LOGIN DEVERIA FALHAR")
                if not password_ok:
                    print(f"   Motivo: Senha incorreta")
                if not login_user.is_active:
                    print(f"   Motivo: Conta inativa")

if __name__ == "__main__":
    test_login_direct()