#!/usr/bin/env python3
"""
Script para criar o schema do Sistema de Equivalências UFSM no Supabase
"""

import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from werkzeug.security import generate_password_hash

# Configurações do Supabase
SUPABASE_HOST = "207.180.254.250"
SUPABASE_PORT = "5432"
SUPABASE_USER = "postgres"
SUPABASE_PASSWORD = "5100a23f8d3196cfce339c43d475b3e0"
SUPABASE_DATABASE = "postgres"

def create_database_if_not_exists():
    """Criar banco de dados equivalencias_ufsm se não existir"""
    try:
        # Conectar ao banco postgres padrão
        conn = psycopg2.connect(
            host=SUPABASE_HOST,
            port=SUPABASE_PORT,
            user=SUPABASE_USER,
            password=SUPABASE_PASSWORD,
            database=SUPABASE_DATABASE
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Verificar se o banco já existe
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'equivalencias_ufsm'")
        exists = cursor.fetchone()
        
        if not exists:
            print("📦 Criando banco de dados 'equivalencias_ufsm'...")
            cursor.execute("CREATE DATABASE equivalencias_ufsm")
            print("✅ Banco de dados criado com sucesso!")
        else:
            print("✅ Banco de dados 'equivalencias_ufsm' já existe")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar banco de dados: {e}")
        return False

def execute_schema_sql():
    """Executar o script SQL para criar o schema"""
    try:
        # Conectar ao banco equivalencias_ufsm
        conn = psycopg2.connect(
            host=SUPABASE_HOST,
            port=SUPABASE_PORT,
            user=SUPABASE_USER,
            password=SUPABASE_PASSWORD,
            database="equivalencias_ufsm"
        )
        cursor = conn.cursor()
        
        print("🔧 Executando script de criação do schema...")
        
        # Ler e executar o arquivo SQL
        with open('/home/ubuntu/create_schema.sql', 'r', encoding='utf-8') as file:
            sql_script = file.read()
        
        # Dividir o script em comandos individuais
        commands = [cmd.strip() for cmd in sql_script.split(';') if cmd.strip()]
        
        for i, command in enumerate(commands, 1):
            if command:
                try:
                    cursor.execute(command)
                    print(f"✅ Comando {i}/{len(commands)} executado")
                except Exception as e:
                    print(f"⚠️  Aviso no comando {i}: {e}")
        
        # Criar usuário admin com senha correta
        print("👤 Criando usuário administrador...")
        admin_password_hash = generate_password_hash('adm4125')
        
        cursor.execute("""
            INSERT INTO admin (username, password_hash) 
            VALUES (%s, %s)
            ON CONFLICT (username) 
            DO UPDATE SET password_hash = EXCLUDED.password_hash
        """, ('admin', admin_password_hash))
        
        conn.commit()
        print("✅ Usuário admin criado/atualizado com sucesso!")
        
        # Verificar tabelas criadas
        cursor.execute("""
            SELECT table_name, table_type 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name IN ('admin', 'equivalencia')
            ORDER BY table_name
        """)
        
        tables = cursor.fetchall()
        print("\n📊 Tabelas criadas:")
        for table_name, table_type in tables:
            print(f"  ✅ {table_name} ({table_type})")
        
        # Verificar dados de exemplo
        cursor.execute("SELECT COUNT(*) FROM equivalencia")
        equiv_count = cursor.fetchone()[0]
        print(f"\n📝 Registros de equivalência: {equiv_count}")
        
        cursor.execute("SELECT COUNT(*) FROM admin")
        admin_count = cursor.fetchone()[0]
        print(f"👤 Usuários admin: {admin_count}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erro ao executar schema SQL: {e}")
        return False

def test_connection():
    """Testar conexão com o Supabase"""
    try:
        print("🔍 Testando conexão com Supabase...")
        conn = psycopg2.connect(
            host=SUPABASE_HOST,
            port=SUPABASE_PORT,
            user=SUPABASE_USER,
            password=SUPABASE_PASSWORD,
            database="equivalencias_ufsm"
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT version()")
        version = cursor.fetchone()[0]
        print(f"✅ Conexão estabelecida! PostgreSQL: {version}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
        return False

def main():
    """Função principal"""
    print("🚀 Iniciando criação do schema no Supabase...")
    print("=" * 60)
    
    # Passo 1: Criar banco de dados
    if not create_database_if_not_exists():
        print("❌ Falha ao criar banco de dados. Abortando.")
        return
    
    print()
    
    # Passo 2: Executar schema SQL
    if not execute_schema_sql():
        print("❌ Falha ao criar schema. Abortando.")
        return
    
    print()
    
    # Passo 3: Testar conexão final
    if test_connection():
        print("\n🎉 Schema criado com sucesso no Supabase!")
        print("=" * 60)
        print("📋 Resumo:")
        print("  🐘 Banco: equivalencias_ufsm")
        print("  📊 Tabelas: admin, equivalencia")
        print("  👤 Usuário: admin")
        print("  🔐 Senha: adm4125")
        print("  🌐 Host: 207.180.254.250:5432")
        print("=" * 60)
    else:
        print("❌ Falha no teste de conexão final.")

if __name__ == "__main__":
    main()

