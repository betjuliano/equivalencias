# Configuração Supabase Self-Hosted - IA Projetos

## Credenciais Configuradas

O sistema está configurado para usar o Supabase self-hosted da IA Projetos:

### Variáveis de Ambiente (.env)

```env
# Configurações do Supabase
SUPABASE_URL=https://supabases.iaprojetos.com.br
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.ewogICJyb2xlIjogImFub24iLAogICJpc3MiOiAic3VwYWJhc2UiLAogICJpYXQiOiAxNzE1MDUwODAwLAogICJleHAiOiAxODcyODE3MjAwCn0.TKsuZpcWuZTmGvi2ZihI_xNTTWKdGUJ_9jpf49rIHLE
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.ewogICJyb2xlIjogInNlcnZpY2Vfcm9sZSIsCiAgImlzcyI6ICJzdXBhYmFzZSIsCiAgImlhdCI6IDE3MTUwNTA4MDAsCiAgImV4cCI6IDE4NzI4MTcyMDAKfQ.3HrXvFpCTuI8a9NPJjNY-frjGSx0iwMbhO9Gah9RkVs

# Configuração do Banco de Dados PostgreSQL (via Supabase)
DATABASE_URL=postgresql://postgres:5100a23f8d3196cfce339c43d475b3e0@207.180.254.250:5432/equivalencias_ufsm

# Configurações do Flask
SECRET_KEY=ufsm_equivalencias_2025_secret_key_admin
FLASK_ENV=production

# Configurações de Deploy
PORT=5000
NODE_ENV=development
```

## Funcionalidades Integradas

### 1. Cliente Supabase Configurado

O sistema agora inclui um cliente Supabase totalmente configurado em `src/config/supabase.py`:

- **Cliente Público**: Para operações de leitura
- **Cliente Admin**: Para operações administrativas
- **Teste de Conexão**: Endpoint `/api/supabase/test`

### 2. Endpoints de Monitoramento

#### Testar Supabase
```
GET /api/supabase/test
```
Retorna status da conexão com Supabase.

#### Informações do Sistema
```
GET /api/info
```
Retorna informações completas do sistema.

### 3. Estrutura de Banco de Dados

O sistema criará automaticamente as seguintes tabelas no PostgreSQL:

#### Tabela: `admin`
```sql
CREATE TABLE admin (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Tabela: `equivalencia`
```sql
CREATE TABLE equivalencia (
    id SERIAL PRIMARY KEY,
    disciplina_adm VARCHAR(200) NOT NULL,
    codigo_adm VARCHAR(20) NOT NULL,
    carga_horaria_adm VARCHAR(10) NOT NULL,
    disciplina_equivalente VARCHAR(200) NOT NULL,
    codigo_equivalente VARCHAR(20) NOT NULL,
    curso VARCHAR(100) NOT NULL,
    carga_horaria_equivalente VARCHAR(10) NOT NULL,
    justificativa TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Configuração e Deploy

### 1. Instalação Local

```bash
# Clonar repositório
git clone https://github.com/betjuliano/equivalencias.git
cd equivalencias

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp .env.example .env
# Editar .env com as credenciais (já configuradas)

# Executar aplicação
python src/main.py
```

### 2. Deploy com Docker

```bash
# Build da imagem
docker build -t equivalencias-ufsm .

# Executar container
docker run -p 5000:5000 \
  --env-file .env \
  equivalencias-ufsm
```

### 3. Deploy com Docker Compose

```bash
# Executar em desenvolvimento
docker-compose up -d

# Executar em produção
docker-compose -f docker-compose.prod.yml up -d
```

## Verificação da Configuração

### 1. Teste de Conexão

Após iniciar o sistema, acesse:
- `http://localhost:5000/api/supabase/test` - Testar Supabase
- `http://localhost:5000/api/info` - Informações do sistema

### 2. Logs do Sistema

O sistema exibirá logs informativos:
```
🚀 Iniciando Sistema de Equivalências UFSM
📍 Porta: 5000
🐘 Banco: Supabase PostgreSQL
🔧 Debug: False
Usuário administrador criado: admin / adm4125
Supabase: Conexão com Supabase estabelecida com sucesso!
```

## Segurança e Boas Práticas

### 1. Chaves de API
- ✅ **Anon Key**: Usada para operações públicas
- ✅ **Service Role Key**: Usada para operações administrativas
- ✅ **Credenciais via variáveis de ambiente**

### 2. Banco de Dados
- ✅ **PostgreSQL via Supabase**
- ✅ **Conexão SSL automática**
- ✅ **Backup automático do Supabase**

### 3. Autenticação
- ✅ **Senhas hasheadas com Werkzeug**
- ✅ **Sessões seguras do Flask**
- ✅ **Validação de entrada**

## Monitoramento e Manutenção

### 1. Logs
```bash
# Logs do container
docker logs equivalencias-ufsm

# Logs da aplicação
tail -f app.log
```

### 2. Backup
O Supabase já possui backup automático configurado. Para backup manual:
```bash
pg_dump -h 207.180.254.250 -U postgres equivalencias_ufsm > backup.sql
```

### 3. Atualizações
```bash
# Atualizar código
git pull origin main

# Reinstalar dependências
pip install -r requirements.txt

# Reiniciar aplicação
systemctl restart equivalencias-ufsm
```

## Suporte Técnico

**Desenvolvedor:** Prof. Juliano Alves  
**Grupo:** Pesquisa em IA - IA Projetos  
**Instituição:** UFSM  
**Supabase:** https://supabases.iaprojetos.com.br

---

**Sistema totalmente integrado com Supabase self-hosted! 🚀**

