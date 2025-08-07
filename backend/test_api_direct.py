#!/usr/bin/env python3
import requests
import json

def test_api_direct():
    """Testa a API diretamente usando requests"""
    
    url = "https://beautiful-thread-production.up.railway.app/api/auth/login"
    
    # Dados de login
    data = {
        "email": "joao.silva@email.com",
        "password": "MinhaSenh@123"
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    print(f"🌐 Testando API diretamente...")
    print(f"URL: {url}")
    print(f"Dados: {json.dumps(data, indent=2)}")
    print(f"Headers: {json.dumps(headers, indent=2)}")
    print("=" * 50)
    
    try:
        # Fazer a requisição
        response = requests.post(url, json=data, headers=headers, timeout=30)
        
        print(f"📊 Resposta:")
        print(f"   Status Code: {response.status_code}")
        print(f"   Headers: {dict(response.headers)}")
        
        try:
            response_json = response.json()
            print(f"   Body: {json.dumps(response_json, indent=2)}")
        except:
            print(f"   Body (text): {response.text}")
        
        if response.status_code == 200:
            print(f"\n✅ LOGIN FUNCIONOU!")
        elif response.status_code == 401:
            print(f"\n❌ LOGIN FALHOU - Credenciais incorretas")
        else:
            print(f"\n⚠️  Status inesperado: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro na requisição: {e}")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
    
    # Testar também com outras senhas
    print(f"\n🔍 Testando outras senhas...")
    test_passwords = ["123456", "senha123", "password"]
    
    for pwd in test_passwords:
        test_data = {"email": "joao.silva@email.com", "password": pwd}
        try:
            resp = requests.post(url, json=test_data, headers=headers, timeout=10)
            print(f"   '{pwd}': {resp.status_code}")
            if resp.status_code == 200:
                print(f"   ✅ SENHA CORRETA: {pwd}")
                break
        except:
            print(f"   '{pwd}': erro")

if __name__ == "__main__":
    test_api_direct()