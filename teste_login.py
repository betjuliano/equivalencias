#!/usr/bin/env python3
"""
Script de teste para verificar se a correção do login está funcionando
"""

import requests
import json
import sys

def testar_login(base_url="http://localhost:5000"):
    """Testa o sistema de login"""

    session = requests.Session()

    print("🧪 Testando Sistema de Login - Equivalências UFSM")
    print("=" * 50)

    # Teste 1: Verificar se o servidor está rodando
    print("1. Testando conectividade com o servidor...")
    try:
        response = session.get(f"{base_url}/api/info", timeout=5)
        if response.status_code == 200:
            info = response.json()
            print(f"✅ Servidor online - {info.get('name', 'Sistema')}")
            print(f"   Versão: {info.get('version', 'N/A')}")
            print(f"   Sessões: {'✅' if info.get('session_configured') else '❌'}")
        else:
            print(f"❌ Servidor retornou status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro de conectividade: {e}")
        print("   Certifique-se de que o servidor está rodando em", base_url)
        return False
    
    # Teste 2: Verificar autenticação inicial
    print("\n2. Verificando status de autenticação...")
    try:
        response = session.get(f"{base_url}/api/check-auth")
        if response.status_code == 200:
            auth_data = response.json()
            if auth_data.get('authenticated'):
                print(f"✅ Usuário já autenticado: {auth_data.get('username')}")
            else:
                print("✅ Usuário não autenticado (esperado)")
        else:
            print(f"❌ Erro ao verificar autenticação: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro na verificação: {e}")
    
    # Teste 3: Testar login com credenciais corretas
    print("\n3. Testando login com credenciais corretas...")
    login_data = {
        "username": "admin",
        "password": "adm4125"
    }
    
    try:
        response = session.post(
            f"{base_url}/api/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Login bem-sucedido!")
            print(f"   Usuário: {result.get('username')}")
            print(f"   Mensagem: {result.get('message')}")
            
            # Verificar se a sessão foi criada
            print("\n4. Verificando se a sessão foi criada...")
            auth_response = session.get(f"{base_url}/api/check-auth")
            if auth_response.status_code == 200:
                auth_data = auth_response.json()
                if auth_data.get('authenticated'):
                    print(f"✅ Sessão criada com sucesso para: {auth_data.get('username')}")
                else:
                    print("❌ Sessão não foi criada")
                    return False
            
        else:
            print(f"❌ Login falhou com status {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Erro: {error_data.get('error', 'Erro desconhecido')}")
            except:
                print(f"   Resposta: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro na requisição de login: {e}")
        return False
    
    # Teste 4: Testar login com credenciais incorretas
    print("\n5. Testando login com credenciais incorretas...")
    wrong_login_data = {
        "username": "admin",
        "password": "senha_errada"
    }
    
    try:
        response = session.post(
            f"{base_url}/api/login",
            json=wrong_login_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 401:
            print("✅ Credenciais incorretas rejeitadas corretamente")
        else:
            print(f"❌ Resposta inesperada para credenciais incorretas: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro no teste de credenciais incorretas: {e}")
    
    # Teste 5: Testar logout
    print("\n6. Testando logout...")
    try:
        response = session.post(f"{base_url}/api/logout")
        if response.status_code == 200:
            print("✅ Logout realizado com sucesso")
            
            # Verificar se a sessão foi removida
            auth_response = session.get(f"{base_url}/api/check-auth")
            if auth_response.status_code == 200:
                auth_data = auth_response.json()
                if not auth_data.get('authenticated'):
                    print("✅ Sessão removida com sucesso")
                else:
                    print("❌ Sessão ainda ativa após logout")
        else:
            print(f"❌ Erro no logout: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro no teste de logout: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Teste concluído! Se todos os itens estão ✅, a correção funcionou.")
    return True

if __name__ == "__main__":
    # Permitir URL customizada como argumento
    url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5000"
    testar_login(url)

