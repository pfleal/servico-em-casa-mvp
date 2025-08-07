#!/usr/bin/env python3
import os
import psycopg2
from werkzeug.security import check_password_hash

def check_user_password():
    """Conecta diretamente ao PostgreSQL para verificar a senha"""
    
    # URL do banco de dados do Railway
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        print("❌ DATABASE_URL não encontrada nas variáveis de ambiente")
        return
    
    print(f"🔗 Conectando ao banco: {database_url[:50]}...")
    
    try:
        # Conectar ao banco
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        # Buscar o usuário
        email = "joao.silva@email.com"
        cursor.execute("SELECT id, name, email, password_hash, is_active, is_verified FROM \"user\" WHERE email = %s", (email,))
        
        result = cursor.fetchone()
        
        if not result:
            print(f"❌ Usuário '{email}' não encontrado!")
            return
        
        user_id, name, user_email, password_hash, is_active, is_verified = result
        
        print(f"✅ Usuário encontrado:")
        print(f"   ID: {user_id}")
        print(f"   Nome: {name}")
        print(f"   Email: {user_email}")
        print(f"   Hash: {password_hash}")
        print(f"   Ativo: {is_active}")
        print(f"   Verificado: {is_verified}")
        print()
        
        # Testar a senha
        password = "MinhaSenh@123"
        print(f"🔐 Testando senha: {password}")
        
        # Verificar senha
        is_valid = check_password_hash(password_hash, password)
        print(f"   Resultado: {is_valid}")
        
        if is_valid:
            print(f"✅ SENHA CORRETA!")
            if is_active:
                print(f"✅ CONTA ATIVA - LOGIN DEVERIA FUNCIONAR!")
            else:
                print(f"❌ CONTA DESATIVADA")
        else:
            print(f"❌ SENHA INCORRETA")
            
            # Testar outras senhas
            print(f"\n🔍 Testando outras senhas...")
            test_passwords = ["123456", "senha123", "minhasenha", "password", "joao123"]
            
            for test_pwd in test_passwords:
                if check_password_hash(password_hash, test_pwd):
                    print(f"   ✅ Senha correta encontrada: '{test_pwd}'")
                    break
                else:
                    print(f"   ❌ '{test_pwd}' - incorreta")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Erro ao conectar ao banco: {e}")

if __name__ == "__main__":
    check_user_password()