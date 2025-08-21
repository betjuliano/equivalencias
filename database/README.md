# 🐘 Database Schema - Sistema de Equivalências UFSM

Esta pasta contém todos os arquivos necessários para criar e configurar o banco de dados do Sistema de Equivalências UFSM no Supabase.

## 📁 Arquivos Incluídos

### **🎯 Para Execução Direta**

#### **`supabase_schema_complete.sql`**
- **Script SQL completo** para execução no painel do Supabase
- **Uso:** Copie e cole no SQL Editor do Supabase
- **Cria:** Tabelas, índices, triggers, políticas RLS e dados de exemplo
- **Recomendado:** Use este arquivo para configuração inicial

#### **`GUIA_EXECUCAO_SCHEMA.md`**
- **Guia passo a passo** detalhado
- **Instruções completas** de execução
- **Solução de problemas** e verificações
- **Checklist** de validação

### **🔧 Scripts Auxiliares**

#### **`create_schema.sql`**
- **Versão alternativa** do schema
- **Mais detalhado** com comentários extensivos
- **Para referência** técnica

#### **`create_supabase_schema.py`**
- **Script Python** para criação via PostgreSQL direto
- **Uso:** Quando há acesso direto ao PostgreSQL
- **Requer:** psycopg2-binary, werkzeug

#### **`create_supabase_schema_api.py`**
- **Script Python** para criação via API REST
- **Uso:** Quando há acesso apenas à API do Supabase
- **Requer:** requests, werkzeug

## 🚀 Execução Recomendada

### **Método 1: SQL Editor (Recomendado)**
1. Acesse: https://supabases.iaprojetos.com.br
2. Vá para **SQL Editor**
3. Copie o conteúdo de `supabase_schema_complete.sql`
4. Cole e execute no editor
5. Siga o `GUIA_EXECUCAO_SCHEMA.md`

### **Método 2: Script Python**
```bash
# Via PostgreSQL direto
python database/create_supabase_schema.py

# Via API REST
python database/create_supabase_schema_api.py
```

## 📊 Estrutura Criada

### **Tabelas**
- **`admin`**: Usuários administrativos (1 registro)
- **`equivalencia`**: Dados das equivalências (5 registros de exemplo)

### **Recursos**
- **5 índices** para performance
- **2 triggers** para updated_at automático
- **3 políticas RLS** para segurança
- **Extensão uuid-ossp** habilitada

### **Dados Iniciais**
- **Usuário admin**: admin / adm4125
- **5 equivalências** de exemplo entre cursos

## 🔐 Credenciais

- **Usuário:** admin
- **Senha:** adm4125
- **Nota:** A senha será atualizada automaticamente pelo sistema Flask

## 🧪 Verificação

Após execução, teste:

```sql
-- Verificar tabelas criadas
SELECT COUNT(*) FROM admin;        -- Deve retornar: 1
SELECT COUNT(*) FROM equivalencia; -- Deve retornar: 5

-- Ver estrutura
\d admin
\d equivalencia
```

## 📞 Suporte

Para problemas na execução:
1. Consulte o `GUIA_EXECUCAO_SCHEMA.md`
2. Verifique permissões de administrador
3. Confirme credenciais do Supabase
4. Execute comandos um por vez

---

**🎯 Use `supabase_schema_complete.sql` + `GUIA_EXECUCAO_SCHEMA.md` para configuração rápida e completa!**

