#!/usr/bin/env python3
"""Ferramenta de verificação do fluxo de autenticação."""

from __future__ import annotations

import sys
from typing import Any

import requests


def check_server(session: requests.Session, base_url: str) -> bool:
    """Verifica se o servidor está respondendo e se a sessão está configurada."""

    print("1. Testando conectividade com o servidor...")
    try:
        response = session.get(f"{base_url}/api/info", timeout=5)
    except requests.exceptions.RequestException as exc:
        print(f"❌ Erro de conectividade: {exc}")
        print("   Certifique-se de que o servidor está rodando em", base_url)
        return False

    if response.status_code != 200:
        print(f"❌ Servidor retornou status {response.status_code}")
        return False

    info: dict[str, Any] = response.json()
    print(f"✅ Servidor online - {info.get('name', 'Sistema')}")
    print(f"   Versão: {info.get('version', 'N/A')}")
    print(f"   Sessões: {'✅' if info.get('session_configured') else '❌'}")
    return True


def check_authentication(session: requests.Session, base_url: str) -> None:
    """Exibe o estado de autenticação da sessão atual."""

    print("\n2. Verificando status de autenticação...")
    try:
        response = session.get(f"{base_url}/api/check-auth")
    except requests.exceptions.RequestException as exc:
        print(f"❌ Erro na verificação: {exc}")
        return

    if response.status_code == 200:
        auth_data = response.json()
        if auth_data.get("authenticated"):
            print(f"✅ Usuário já autenticado: {auth_data.get('username')}")
        else:
            print("✅ Usuário não autenticado (esperado)")
    else:
        print(f"❌ Erro ao verificar autenticação: {response.status_code}")


def login(session: requests.Session, base_url: str, username: str, password: str) -> bool:
    """Realiza o login e confirma se a sessão foi criada."""

    print("\n3. Testando login com credenciais corretas...")
    payload = {"username": username, "password": password}
    try:
        response = session.post(
            f"{base_url}/api/login",
            json=payload,
            headers={"Content-Type": "application/json"},
        )
    except requests.exceptions.RequestException as exc:
        print(f"❌ Erro na requisição de login: {exc}")
        return False

    if response.status_code != 200:
        print(f"❌ Login falhou com status {response.status_code}")
        try:
            error_data = response.json()
            print(f"   Erro: {error_data.get('error', 'Erro desconhecido')}")
        except Exception:
            print(f"   Resposta: {response.text}")
        return False

    result = response.json()
    print("✅ Login bem-sucedido!")
    print(f"   Usuário: {result.get('username')}")
    print(f"   Mensagem: {result.get('message')}")

    print("\n4. Verificando se a sessão foi criada...")
    auth_response = session.get(f"{base_url}/api/check-auth")
    if auth_response.status_code == 200:
        auth_data = auth_response.json()
        if auth_data.get("authenticated"):
            print(f"✅ Sessão criada com sucesso para: {auth_data.get('username')}")
            return True
        print("❌ Sessão não foi criada")
    else:
        print(f"❌ Erro ao verificar sessão: {auth_response.status_code}")
    return False


def login_incorreto(session: requests.Session, base_url: str) -> None:
    """Verifica o comportamento do login com credenciais inválidas."""

    print("\n5. Testando login com credenciais incorretas...")
    wrong_payload = {"username": "admin", "password": "senha_errada"}
    try:
        response = session.post(
            f"{base_url}/api/login",
            json=wrong_payload,
            headers={"Content-Type": "application/json"},
        )
    except requests.exceptions.RequestException as exc:
        print(f"❌ Erro no teste de credenciais incorretas: {exc}")
        return

    if response.status_code == 401:
        print("✅ Credenciais incorretas rejeitadas corretamente")
    else:
        print(f"❌ Resposta inesperada para credenciais incorretas: {response.status_code}")


def logout(session: requests.Session, base_url: str) -> None:
    """Efetua logout e confirma a remoção da sessão."""

    print("\n6. Testando logout...")
    try:
        response = session.post(f"{base_url}/api/logout")
    except requests.exceptions.RequestException as exc:
        print(f"❌ Erro no teste de logout: {exc}")
        return

    if response.status_code == 200:
        print("✅ Logout realizado com sucesso")
        auth_response = session.get(f"{base_url}/api/check-auth")
        if auth_response.status_code == 200:
            auth_data = auth_response.json()
            if not auth_data.get("authenticated"):
                print("✅ Sessão removida com sucesso")
            else:
                print("❌ Sessão ainda ativa após logout")
    else:
        print(f"❌ Erro no logout: {response.status_code}")


def testar_login(base_url: str = "http://localhost:5000") -> bool:
    """Executa todos os testes de login."""

    session = requests.Session()

    print("🧪 Testando Sistema de Login - Equivalências UFSM")
    print("=" * 50)

    if not check_server(session, base_url):
        return False
    check_authentication(session, base_url)
    if not login(session, base_url, "admin", "adm4125"):
        return False
    login_incorreto(session, base_url)
    logout(session, base_url)

    print("\n" + "=" * 50)
    print("🎉 Teste concluído! Se todos os itens estão ✅, a correção funcionou.")
    return True


if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5000"
    testar_login(url)

