#!/usr/bin/env python3
import os
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import sessionmaker

def check_database_structure():
    """Verifica a estrutura do banco de dados"""
    
    # URL do banco de dados do Railway
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        # Tentar construir a URL a partir das variáveis individuais do Railway
        pg_host = os.getenv('PGHOST')
        pg_port = os.getenv('PGPORT', '5432')
        pg_database = os.getenv('PGDATABASE')
        pg_user = os.getenv('PGUSER')
        pg_password = os.getenv('PGPASSWORD')
        
        if all([pg_host, pg_database, pg_user, pg_password]):
            database_url = f"postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_database}"
            print(f"🔧 Construindo URL do banco a partir das variáveis individuais")
        else:
            print("❌ Variáveis do banco de dados não encontradas")
            print(f"PGHOST: {pg_host}")
            print(f"PGPORT: {pg_port}")
            print(f"PGDATABASE: {pg_database}")
            print(f"PGUSER: {pg_user}")
            print(f"PGPASSWORD: {'***' if pg_password else None}")
            return
    
    print(f"🔍 Conectando ao banco de dados...")
    print(f"URL: {database_url[:50]}...")
    
    try:
        # Criar engine
        engine = create_engine(database_url)
        
        # Criar inspector
        inspector = inspect(engine)
        
        # Listar todas as tabelas
        tables = inspector.get_table_names()
        print(f"\n📋 Tabelas encontradas: {len(tables)}")
        
        for table_name in tables:
            print(f"\n🗂️  Tabela: {table_name}")
            
            # Obter colunas da tabela
            columns = inspector.get_columns(table_name)
            print(f"   Colunas ({len(columns)}):")
            
            for column in columns:
                nullable = "NULL" if column['nullable'] else "NOT NULL"
                default = f" DEFAULT {column['default']}" if column['default'] else ""
                print(f"     - {column['name']}: {column['type']} {nullable}{default}")
            
            # Se for uma tabela de usuários, mostrar alguns dados
            if 'user' in table_name.lower() or 'usuario' in table_name.lower():
                print(f"\n   📊 Dados da tabela {table_name}:")
                try:
                    with engine.connect() as conn:
                        result = conn.execute(text(f"SELECT * FROM {table_name} LIMIT 5"))
                        rows = result.fetchall()
                        
                        if rows:
                            # Mostrar cabeçalhos
                            headers = result.keys()
                            print(f"     Headers: {list(headers)}")
                            
                            # Mostrar dados
                            for i, row in enumerate(rows):
                                print(f"     Row {i+1}: {dict(row._mapping)}")
                        else:
                            print(f"     (Tabela vazia)")
                except Exception as e:
                    print(f"     ❌ Erro ao consultar dados: {e}")
        
        # Verificar especificamente por usuários com email joao.silva@email.com
        print(f"\n🔍 Procurando usuário 'joao.silva@email.com' em todas as tabelas...")
        
        for table_name in tables:
            try:
                columns = inspector.get_columns(table_name)
                email_columns = [col['name'] for col in columns if 'email' in col['name'].lower()]
                
                if email_columns:
                    for email_col in email_columns:
                        with engine.connect() as conn:
                            query = text(f"SELECT * FROM {table_name} WHERE {email_col} = :email")
                            result = conn.execute(query, {"email": "joao.silva@email.com"})
                            rows = result.fetchall()
                            
                            if rows:
                                print(f"\n   ✅ Usuário encontrado na tabela '{table_name}':")
                                for row in rows:
                                    print(f"      {dict(row._mapping)}")
            except Exception as e:
                print(f"   ❌ Erro ao verificar tabela {table_name}: {e}")
        
    except Exception as e:
        print(f"❌ Erro ao conectar ao banco: {e}")

if __name__ == "__main__":
    check_database_structure()