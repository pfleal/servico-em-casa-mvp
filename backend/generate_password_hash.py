#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from werkzeug.security import generate_password_hash

def generate_hash():
    """Gera o hash da senha para update direto no banco"""
    
    password = "MinhaSenh@123"
    
    # Usar o mesmo método que a aplicação usa
    password_hash = generate_password_hash(password)
    
    print("🔐 Hash da senha gerado:")
    print("=" * 50)
    print(f"Senha original: {password}")
    print(f"Hash gerado: {password_hash}")
    print("\n📝 SQL para update no banco:")
    print("=" * 50)
    print(f"UPDATE users SET password_hash = '{password_hash}' WHERE email = 'joao.silva@email.com';")
    print("\n💡 Copie o hash acima e use no seu update SQL.")

if __name__ == "__main__":
    generate_hash()