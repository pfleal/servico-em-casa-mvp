#!/usr/bin/env python3
"""
Script para migrar dados do SQLite para PostgreSQL (Supabase)
"""

import os
import sys
import sqlite3
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from datetime import datetime

# Carrega as variáveis de ambiente
load_dotenv()

def convert_sqlite_to_postgres_value(value, column_name):
    """Converte valores do SQLite para PostgreSQL"""
    # Converte valores booleanos (SQLite usa 0/1, PostgreSQL usa true/false)
    if column_name in ['is_active', 'is_verified', 'is_available', 'materials_included', 'is_read']:
        return bool(value) if value is not None else None
    
    # Converte timestamps
    if column_name in ['created_at', 'updated_at', 'preferred_date'] and isinstance(value, str):
        try:
            return datetime.fromisoformat(value.replace('Z', '+00:00'))
        except:
            return value
    
    return value

def migrate_data():
    """Migra dados do SQLite para PostgreSQL"""
    
    # Configurações
    sqlite_db_path = os.path.join(os.path.dirname(__file__), 'src', 'database', 'app.db')
    postgres_url = os.environ.get('DATABASE_URL')
    
    if not postgres_url:
        print("❌ DATABASE_URL não encontrada no arquivo .env")
        return False
    
    if not os.path.exists(sqlite_db_path):
        print(f"❌ Banco SQLite não encontrado em: {sqlite_db_path}")
        print("ℹ️  Isso é normal se for a primeira execução. As tabelas serão criadas no PostgreSQL.")
        return True
    
    try:
        # Conecta ao SQLite
        sqlite_conn = sqlite3.connect(sqlite_db_path)
        sqlite_conn.row_factory = sqlite3.Row
        
        # Conecta ao PostgreSQL
        postgres_engine = create_engine(postgres_url)
        
        print("🔄 Iniciando migração dos dados...")
        
        # Lista de tabelas para migrar (na ordem correta devido às foreign keys)
        # Nota: 'user' é uma palavra reservada no PostgreSQL, então usamos aspas
        tables_to_migrate = [
            ('service_category', 'service_category'),
            ('user', '"user"'),  # Aspas para palavra reservada
            ('service_request', 'service_request'),
            ('provider_service', 'provider_service'),
            ('proposal', 'proposal'),
            ('evaluation', 'evaluation'),
            ('message', 'message')
        ]
        
        with postgres_engine.connect() as postgres_conn:
            # Inicia uma transação
            trans = postgres_conn.begin()
            
            try:
                for sqlite_table, postgres_table in tables_to_migrate:
                    try:
                        # Verifica se a tabela existe no SQLite
                        cursor = sqlite_conn.execute(
                            "SELECT name FROM sqlite_master WHERE type='table' AND name=?", 
                            (sqlite_table,)
                        )
                        if not cursor.fetchone():
                            print(f"⚠️  Tabela {sqlite_table} não encontrada no SQLite, pulando...")
                            continue
                        
                        # Busca dados do SQLite
                        cursor = sqlite_conn.execute(f"SELECT * FROM {sqlite_table}")
                        rows = cursor.fetchall()
                        
                        if not rows:
                            print(f"ℹ️  Tabela {sqlite_table} está vazia, pulando...")
                            continue
                        
                        # Prepara os dados para inserção
                        columns = [description[0] for description in cursor.description]
                        
                        # Limpa a tabela no PostgreSQL antes de inserir
                        postgres_conn.execute(text(f"TRUNCATE TABLE {postgres_table} RESTART IDENTITY CASCADE"))
                        
                        # Insere os dados no PostgreSQL
                        for row in rows:
                            placeholders = ', '.join([f':{col}' for col in columns])
                            query = f"INSERT INTO {postgres_table} ({', '.join(columns)}) VALUES ({placeholders})"
                            
                            # Converte Row para dict e ajusta os valores
                            row_dict = {}
                            for col in columns:
                                row_dict[col] = convert_sqlite_to_postgres_value(row[col], col)
                            
                            postgres_conn.execute(text(query), row_dict)
                        
                        print(f"✅ Migrados {len(rows)} registros da tabela {sqlite_table}")
                        
                    except Exception as e:
                        print(f"❌ Erro ao migrar tabela {sqlite_table}: {str(e)}")
                        continue
                
                # Confirma a transação
                trans.commit()
                
            except Exception as e:
                # Desfaz a transação em caso de erro
                trans.rollback()
                raise e
        
        sqlite_conn.close()
        print("🎉 Migração concluída com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro durante a migração: {str(e)}")
        return False

if __name__ == '__main__':
    print("🚀 Iniciando migração do SQLite para PostgreSQL...")
    success = migrate_data()
    
    if success:
        print("\n✅ Migração concluída! Agora você pode iniciar a aplicação com PostgreSQL.")
        sys.exit(0)
    else:
        print("\n❌ Migração falhou. Verifique os logs acima.")
        sys.exit(1)