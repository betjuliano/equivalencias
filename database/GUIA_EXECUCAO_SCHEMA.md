# 🐘 Guia de Execução do Schema no Supabase

## 📋 Resumo

Este guia contém as instruções completas para criar o schema do **Sistema de Equivalências UFSM** no seu Supabase self-hosted.

## 🎯 Objetivo

Criar as tabelas `admin` e `equivalencia` no Supabase com:
- ✅ Estrutura completa das tabelas
- ✅ Índices para performance
- ✅ Políticas de segurança (RLS)
- ✅ Triggers automáticos
- ✅ Dados de exemplo
- ✅ Usuário administrador

## 🚀 Passo a Passo

### **1. Acessar o Painel do Supabase**

1. Abra seu navegador
2. Acesse: **https://supabases.iaprojetos.com.br**
3. Faça login com suas credenciais de administrador

### **2. Abrir o SQL Editor**

1. No painel lateral, clique em **"SQL Editor"**
2. Clique em **"New Query"** ou **"Nova Consulta"**
3. Você verá um editor de SQL em branco

### **3. Executar o Script SQL**

1. **Copie todo o conteúdo** do arquivo `supabase_schema_complete.sql`
2. **Cole no editor SQL** do Supabase
3. Clique em **"Run"** ou **"Executar"**
4. Aguarde a execução (pode levar alguns segundos)

### **4. Verificar Execução**

Após a execução, você deve ver:

```
✅ Tabelas criadas: admin, equivalencia
✅ Índices criados: 5 índices
✅ Triggers criados: 2 triggers
✅ Políticas RLS: 3 políticas
✅ Dados inseridos: 1 admin + 5 equivalências
```

### **5. Verificar Tabelas Criadas**

1. No painel lateral, clique em **"Table Editor"**
2. Você deve ver as tabelas:
   - **admin** (1 registro)
   - **equivalencia** (5 registros)

## 📊 Estrutura Criada

### **Tabela: admin**
```sql
id (BIGSERIAL PRIMARY KEY)
username (VARCHAR(80) UNIQUE)
password_hash (VARCHAR(255))
created_at (TIMESTAMP)
updated_at (TIMESTAMP)
```

### **Tabela: equivalencia**
```sql
id (BIGSERIAL PRIMARY KEY)
disciplina_adm (VARCHAR(200))
codigo_adm (VARCHAR(20))
carga_horaria_adm (VARCHAR(10))
disciplina_equivalente (VARCHAR(200))
codigo_equivalente (VARCHAR(20))
curso (VARCHAR(100))
carga_horaria_equivalente (VARCHAR(10))
justificativa (TEXT)
created_at (TIMESTAMP)
updated_at (TIMESTAMP)
```

## 🔐 Credenciais Criadas

### **Usuário Administrador:**
- **Usuário:** admin
- **Senha:** adm4125

> **Nota:** A senha será automaticamente atualizada pelo sistema Flask na primeira execução.

## 📝 Dados de Exemplo

O script cria **5 equivalências de exemplo**:

1. **Introdução à Administração** ↔ **Fundamentos de Administração** (Ciências Econômicas)
2. **Matemática Financeira** ↔ **Matemática Aplicada às Finanças** (Matemática)
3. **Contabilidade Geral** ↔ **Princípios de Contabilidade** (Ciências Contábeis)
4. **Estatística Aplicada** ↔ **Estatística Básica** (Estatística)
5. **Direito Empresarial** ↔ **Direito Comercial** (Direito)

## 🔧 Recursos Implementados

### **Segurança (RLS)**
- ✅ Row Level Security habilitado
- ✅ Políticas para leitura pública
- ✅ Políticas para escrita administrativa

### **Performance**
- ✅ Índices em campos de busca
- ✅ Índices em chaves estrangeiras
- ✅ Índices em timestamps

### **Automação**
- ✅ Triggers para `updated_at`
- ✅ Valores padrão para timestamps
- ✅ Validações de integridade

## 🧪 Testar o Schema

### **Via SQL Editor:**
```sql
-- Verificar admin
SELECT username, created_at FROM admin;

-- Verificar equivalências
SELECT 
    disciplina_adm, 
    disciplina_equivalente, 
    curso 
FROM equivalencia 
LIMIT 5;

-- Contar registros
SELECT 
    'admin' as tabela, COUNT(*) as total FROM admin
UNION ALL
SELECT 
    'equivalencia' as tabela, COUNT(*) as total FROM equivalencia;
```

### **Via Sistema Web:**
1. Execute o sistema Flask
2. Acesse: `http://localhost:5000`
3. Teste login: admin / adm4125
4. Verifique se os dados aparecem

## ❌ Solução de Problemas

### **Erro: "relation already exists"**
- **Causa:** Tabelas já existem
- **Solução:** Execute o `DROP TABLE` no início do script

### **Erro: "permission denied"**
- **Causa:** Usuário sem permissões
- **Solução:** Use credenciais de administrador do Supabase

### **Erro: "function does not exist"**
- **Causa:** Extensões não instaladas
- **Solução:** Execute `CREATE EXTENSION` primeiro

## 📞 Suporte

Se encontrar problemas:

1. **Verifique logs** no painel do Supabase
2. **Execute comandos** um por vez
3. **Confirme permissões** de administrador
4. **Teste conexão** com o banco

## ✅ Checklist Final

Após execução bem-sucedida:

- [ ] Tabela `admin` criada com 1 registro
- [ ] Tabela `equivalencia` criada com 5 registros
- [ ] Índices criados (5 índices)
- [ ] Triggers funcionando (updated_at)
- [ ] Políticas RLS ativas
- [ ] Login admin/adm4125 funcionando
- [ ] Sistema Flask conectando ao Supabase

---

**🎉 Schema pronto para o Sistema de Equivalências UFSM!**

