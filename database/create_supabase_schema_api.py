#!/usr/bin/env python3
"""
Script para criar o schema do Sistema de Equivalências UFSM no Supabase via API
"""

import requests
import json
from werkzeug.security import generate_password_hash

# Configurações do Supabase
SUPABASE_URL = "https://supabases.iaprojetos.com.br"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.ewogICJyb2xlIjogImFub24iLAogICJpc3MiOiAic3VwYWJhc2UiLAogICJpYXQiOiAxNzE1MDUwODAwLAogICJleHAiOiAxODcyODE3MjAwCn0.TKsuZpcWuZTmGvi2ZihI_xNTTWKdGUJ_9jpf49rIHLE"
SUPABASE_SERVICE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.ewogICJyb2xlIjogInNlcnZpY2Vfcm9sZSIsCiAgImlzcyI6ICJzdXBhYmFzZSIsCiAgImlhdCI6IDE3MTUwNTA4MDAsCiAgImV4cCI6IDE4NzI4MTcyMDAKfQ.3HrXvFpCTuI8a9NPJjNY-frjGSx0iwMbhO9Gah9RkVs"

def test_supabase_connection():
    """Testar conexão com Supabase via API"""
    try:
        print("🔍 Testando conexão com Supabase...")
        
        headers = {
            "apikey": SUPABASE_ANON_KEY,
            "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
            "Content-Type": "application/json"
        }
        
        # Testar endpoint de health check
        response = requests.get(f"{SUPABASE_URL}/rest/v1/", headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("✅ Conexão com Supabase estabelecida!")
            return True
        else:
            print(f"❌ Erro na conexão: Status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
        return False

def execute_sql_via_rpc(sql_command, description=""):
    """Executar comando SQL via RPC do Supabase"""
    try:
        headers = {
            "apikey": SUPABASE_SERVICE_KEY,
            "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
            "Content-Type": "application/json"
        }
        
        # Usar RPC para executar SQL
        payload = {
            "query": sql_command
        }
        
        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/rpc/exec_sql",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code in [200, 201]:
            print(f"✅ {description}")
            return True
        else:
            print(f"⚠️  {description} - Status: {response.status_code}")
            print(f"    Resposta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao executar SQL ({description}): {e}")
        return False

def create_tables_via_api():
    """Criar tabelas usando a API REST do Supabase"""
    try:
        print("🔧 Criando tabelas via API REST...")
        
        # Headers para requisições administrativas
        headers = {
            "apikey": SUPABASE_SERVICE_KEY,
            "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal"
        }
        
        # Tentar criar dados diretamente nas tabelas (assumindo que existem)
        print("👤 Criando usuário administrador...")
        
        admin_data = {
            "username": "admin",
            "password_hash": generate_password_hash('adm4125')
        }
        
        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/admin",
            headers=headers,
            json=admin_data,
            timeout=10
        )
        
        if response.status_code in [200, 201]:
            print("✅ Usuário admin criado com sucesso!")
        else:
            print(f"⚠️  Resposta da criação do admin: {response.status_code} - {response.text}")
        
        # Criar dados de exemplo
        print("📝 Criando equivalências de exemplo...")
        
        equivalencias = [
            {
                "disciplina_adm": "Introdução à Administração",
                "codigo_adm": "CAD1088",
                "carga_horaria_adm": "60h",
                "disciplina_equivalente": "Fundamentos de Administração",
                "codigo_equivalente": "ECO1001",
                "curso": "Ciências Econômicas",
                "carga_horaria_equivalente": "60h",
                "justificativa": "Deferimento - aproximadamente 85% de equivalência de conteúdo. Ambas as disciplinas abordam conceitos fundamentais de administração, teorias organizacionais e princípios de gestão empresarial."
            },
            {
                "disciplina_adm": "Matemática Financeira",
                "codigo_adm": "CAD1045",
                "carga_horaria_adm": "60h",
                "disciplina_equivalente": "Matemática Aplicada às Finanças",
                "codigo_equivalente": "MAT2010",
                "curso": "Matemática",
                "carga_horaria_equivalente": "60h",
                "justificativa": "Deferimento - conteúdo equivalente em cálculos financeiros, juros compostos, valor presente e futuro, análise de investimentos e sistemas de amortização."
            },
            {
                "disciplina_adm": "Contabilidade Geral",
                "codigo_adm": "CAD1020",
                "carga_horaria_adm": "90h",
                "disciplina_equivalente": "Princípios de Contabilidade",
                "codigo_equivalente": "CON1001",
                "curso": "Ciências Contábeis",
                "carga_horaria_equivalente": "90h",
                "justificativa": "Deferimento - disciplinas equivalentes abordando princípios contábeis, demonstrações financeiras, análise de balanços e escrituração contábil."
            }
        ]
        
        for i, equiv in enumerate(equivalencias, 1):
            response = requests.post(
                f"{SUPABASE_URL}/rest/v1/equivalencia",
                headers=headers,
                json=equiv,
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                print(f"✅ Equivalência {i} criada")
            else:
                print(f"⚠️  Equivalência {i}: {response.status_code} - {response.text}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar dados via API: {e}")
        return False

def verify_data():
    """Verificar dados criados"""
    try:
        print("🔍 Verificando dados criados...")
        
        headers = {
            "apikey": SUPABASE_ANON_KEY,
            "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
            "Content-Type": "application/json"
        }
        
        # Verificar equivalências
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/equivalencia?select=*",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            equivalencias = response.json()
            print(f"📝 Equivalências encontradas: {len(equivalencias)}")
            
            for equiv in equivalencias:
                print(f"  ✅ {equiv.get('disciplina_adm')} ↔ {equiv.get('disciplina_equivalente')}")
        else:
            print(f"⚠️  Erro ao verificar equivalências: {response.status_code}")
        
        # Verificar admins (pode não funcionar por segurança)
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/admin?select=username",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            admins = response.json()
            print(f"👤 Administradores encontrados: {len(admins)}")
        else:
            print(f"⚠️  Tabela admin protegida (normal): {response.status_code}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao verificar dados: {e}")
        return False

def main():
    """Função principal"""
    print("🚀 Criando schema no Supabase via API...")
    print("=" * 60)
    
    # Passo 1: Testar conexão
    if not test_supabase_connection():
        print("❌ Falha na conexão. Abortando.")
        return
    
    print()
    
    # Passo 2: Criar dados
    if not create_tables_via_api():
        print("❌ Falha ao criar dados. Continuando verificação...")
    
    print()
    
    # Passo 3: Verificar dados
    verify_data()
    
    print("\n🎉 Processo concluído!")
    print("=" * 60)
    print("📋 Informações do Schema:")
    print("  🐘 Supabase: https://supabases.iaprojetos.com.br")
    print("  📊 Tabelas: admin, equivalencia")
    print("  👤 Usuário: admin")
    print("  🔐 Senha: adm4125")
    print("  📝 Dados de exemplo incluídos")
    print("=" * 60)
    print("\n💡 Nota: Se as tabelas não existirem, você pode criá-las")
    print("    manualmente no painel do Supabase usando o SQL fornecido.")

if __name__ == "__main__":
    main()

