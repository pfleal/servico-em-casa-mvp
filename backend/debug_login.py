#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.models.user import db, User
from src.main import app
from werkzeug.security import check_password_hash
import json

def debug_login():
    """Debug detalhado do processo de login"""
    
    with app.app_context():
        print("🔍 DEBUG DETALHADO DO LOGIN")
        print("=" * 50)
        
        email = "joao.silva@email.com"
        password = "MinhaSenh@123"
        
        print(f"📧 Email testado: {email}")
        print(f"🔐 Senha testada: {password}")
        print()
        
        # 1. Buscar usuário
        print("1️⃣ Buscando usuário...")
        user = User.query.filter_by(email=email).first()
        
        if not user:
            print(f"❌ ERRO: Usuário '{email}' não encontrado!")
            return
        
        print(f"✅ Usuário encontrado:")
        print(f"   ID: {user.id}")
        print(f"   Nome: {user.name}")
        print(f"   Email: {user.email}")
        print(f"   Tipo: {user.user_type}")
        print(f"   Ativo: {user.is_active}")
        print(f"   Verificado: {user.is_verified}")
        print()
        
        # 2. Verificar hash da senha
        print("2️⃣ Verificando hash da senha...")
        print(f"   Hash armazenado: {user.password_hash}")
        print(f"   Tamanho do hash: {len(user.password_hash)} caracteres")
        print(f"   Tipo do hash: {type(user.password_hash)}")
        print()
        
        # 3. Testar verificação da senha
        print("3️⃣ Testando verificação da senha...")
        
        # Método 1: user.check_password()
        try:
            result1 = user.check_password(password)
            print(f"   user.check_password('{password}'): {result1}")
        except Exception as e:
            print(f"   ❌ ERRO em user.check_password(): {e}")
            result1 = False
        
        # Método 2: check_password_hash diretamente
        try:
            result2 = check_password_hash(user.password_hash, password)
            print(f"   check_password_hash(hash, '{password}'): {result2}")
        except Exception as e:
            print(f"   ❌ ERRO em check_password_hash(): {e}")
            result2 = False
        
        print()
        
        # 4. Verificar condições de login
        print("4️⃣ Verificando condições de login...")
        print(f"   Usuário existe: {user is not None}")
        print(f"   Senha correta (método 1): {result1}")
        print(f"   Senha correta (método 2): {result2}")
        print(f"   Conta ativa: {user.is_active}")
        print()
        
        # 5. Simular lógica do auth.py
        print("5️⃣ Simulando lógica do auth.py...")
        
        # Condição do auth.py: if not user or not user.check_password(data['password']):
        auth_condition = not user or not user.check_password(password)
        print(f"   Condição de falha: not user or not user.check_password(password)")
        print(f"   not user: {not user}")
        print(f"   not user.check_password(password): {not user.check_password(password)}")
        print(f"   Resultado da condição: {auth_condition}")
        
        if auth_condition:
            print(f"   ❌ LOGIN FALHARIA: E-mail ou senha incorretos")
        else:
            if not user.is_active:
                print(f"   ❌ LOGIN FALHARIA: Conta desativada")
            else:
                print(f"   ✅ LOGIN DEVERIA FUNCIONAR!")
        
        print()
        
        # 6. Testar outras senhas
        print("6️⃣ Testando outras senhas possíveis...")
        test_passwords = [
            "123456",
            "senha123", 
            "MinhaSenh@123",
            "minhasenha",
            "password",
            "joao123",
            "silva123"
        ]
        
        for test_pwd in test_passwords:
            try:
                if user.check_password(test_pwd):
                    print(f"   ✅ SENHA CORRETA ENCONTRADA: '{test_pwd}'")
                    break
                else:
                    print(f"   ❌ '{test_pwd}' - incorreta")
            except Exception as e:
                print(f"   ❌ '{test_pwd}' - erro: {e}")
        
        print()
        print("🔍 DEBUG CONCLUÍDO")

if __name__ == "__main__":
    debug_login()