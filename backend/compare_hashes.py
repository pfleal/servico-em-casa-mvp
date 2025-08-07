#!/usr/bin/env python3
from werkzeug.security import generate_password_hash, check_password_hash

def compare_hashes():
    """Compara hashes de senha para debug"""
    
    password = "MinhaSenh@123"
    
    # Hash atual do banco (do script anterior)
    current_hash = "scrypt:32768:8:1$z0Mm1Gmzr2jtRcQu$e624d8b4decd078579984603ef26be87bc81f12bab424420e68a6cccd72a471c2131acf28a7dec9c8a85f38433400552e0b23367a62c646c7b4ed2a23fdce6d5"
    
    print(f"🔐 Testando senha: {password}")
    print(f"📝 Hash atual: {current_hash}")
    print()
    
    # Testar o hash atual
    print("1️⃣ Testando hash atual...")
    result1 = check_password_hash(current_hash, password)
    print(f"   check_password_hash(current_hash, password): {result1}")
    
    # Gerar um novo hash
    print("\n2️⃣ Gerando novo hash...")
    new_hash = generate_password_hash(password)
    print(f"   Novo hash: {new_hash}")
    
    # Testar o novo hash
    result2 = check_password_hash(new_hash, password)
    print(f"   check_password_hash(new_hash, password): {result2}")
    
    # Comparar estruturas
    print("\n3️⃣ Comparando estruturas...")
    print(f"   Hash atual começa com: {current_hash[:20]}...")
    print(f"   Novo hash começa com: {new_hash[:20]}...")
    print(f"   Tamanho hash atual: {len(current_hash)}")
    print(f"   Tamanho novo hash: {len(new_hash)}")
    
    # Testar outras senhas comuns
    print("\n4️⃣ Testando outras senhas...")
    test_passwords = [
        "MinhaSenh@123",
        "123456",
        "senha123",
        "minhasenha",
        "password",
        "joao123",
        "silva123"
    ]
    
    for test_pwd in test_passwords:
        result = check_password_hash(current_hash, test_pwd)
        print(f"   '{test_pwd}': {result}")
    
    print("\n📊 RESUMO:")
    if result1:
        print("   ✅ Hash atual está correto para a senha 'MinhaSenh@123'")
        print("   🤔 O problema pode estar na aplicação ou na requisição")
    else:
        print("   ❌ Hash atual NÃO funciona com a senha 'MinhaSenh@123'")
        print("   💡 Precisa atualizar o hash no banco de dados")
        print(f"   🔄 Use este comando SQL:")
        print(f"   UPDATE \"user\" SET password_hash = '{new_hash}' WHERE email = 'joao.silva@email.com';")

if __name__ == "__main__":
    compare_hashes()