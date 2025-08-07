#!/usr/bin/env python3
import psycopg2
from werkzeug.security import check_password_hash

def test_supabase_login():
    """Testa o login diretamente no banco PostgreSQL do Supabase"""
    
    # Configurações do Supabase (mesmas do config.py)
    connection_string = "postgresql://postgres:peixebolagato@db.fhksnwlygqdwnrdymwlz.supabase.co:5432/postgres"
    
    print("🔍 Testando login diretamente no Supabase PostgreSQL...")
    print("=" * 60)
    
    try:
        # Conectar ao banco
        conn = psycopg2.connect(connection_string)
        cursor = conn.cursor()
        
        print("✅ Conectado ao banco PostgreSQL")
        
        # Listar todas as tabelas
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = cursor.fetchall()
        print(f"\n📋 Tabelas encontradas: {[t[0] for t in tables]}")
        
        # Verificar se existe tabela 'user'
        table_name = 'user'
        if (table_name,) not in tables:
            print(f"❌ Tabela '{table_name}' não encontrada!")
            # Tentar outras variações
            possible_names = ['users', 'User', 'Users', 'usuario', 'usuarios']
            for name in possible_names:
                if (name,) in tables:
                    table_name = name
                    print(f"✅ Usando tabela '{table_name}' em vez disso")
                    break
            else:
                print("❌ Nenhuma tabela de usuários encontrada!")
                return
        
        # Verificar estrutura da tabela primeiro
        cursor.execute(f"""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = '{table_name}'
            ORDER BY ordinal_position
        """)
        columns = cursor.fetchall()
        column_names = [col[0] for col in columns]
        
        print(f"\n📊 Colunas da tabela '{table_name}': {column_names}")
        
        # Buscar o usuário específico (usando aspas duplas para a tabela)
        email = "joao.silva@email.com"
        cursor.execute(f'SELECT * FROM "{table_name}" WHERE email = %s', (email,))
        user_data = cursor.fetchone()
        
        if not user_data:
            print(f"❌ Usuário '{email}' não encontrado!")
            
            # Listar todos os usuários
            cursor.execute(f'SELECT id, email, name FROM "{table_name}" LIMIT 10')
            all_users = cursor.fetchall()
            print(f"\n📋 Usuários existentes (primeiros 10):")
            for user in all_users:
                print(f"   ID: {user[0]}, Email: {user[1]}, Nome: {user[2]}")
            return
        
        print(f"\n📊 Colunas da tabela '{table_name}': {column_names}")
        
        # Criar dicionário com os dados do usuário
        user_dict = dict(zip(column_names, user_data))
        
        print(f"\n✅ Usuário encontrado:")
        print(f"   📧 Email: {user_dict.get('email')}")
        print(f"   👤 Nome: {user_dict.get('name')}")
        print(f"   🆔 ID: {user_dict.get('id')}")
        
        # Verificar hash da senha
        password_hash = user_dict.get('password_hash')
        if password_hash:
            print(f"   🔐 Hash: {password_hash[:50]}...")
            
            # Testar senhas
            test_passwords = ["MinhaSenh@123", "123456", "senha123", "password"]
            
            print(f"\n🔍 Testando senhas:")
            for pwd in test_passwords:
                result = check_password_hash(password_hash, pwd)
                status = "✅" if result else "❌"
                print(f"   {status} '{pwd}': {result}")
                
                if result:
                    print(f"   🎉 SENHA CORRETA: '{pwd}'")
                    break
        else:
            print(f"   ❌ Campo password_hash não encontrado!")
        
        # Verificar status da conta
        is_active = user_dict.get('is_active', True)
        is_verified = user_dict.get('is_verified', False)
        
        print(f"\n📊 Status da conta:")
        print(f"   ✅ Ativo: {is_active}")
        print(f"   ✅ Verificado: {is_verified}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    test_supabase_login()