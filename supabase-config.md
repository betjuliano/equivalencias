# Configuração Supabase Self-Hosted

## Credenciais PostgreSQL Externo

Baseado nas preferências do usuário, use as seguintes configurações:

### Variáveis de Ambiente (.env)

```env
# Configuração do Banco de Dados PostgreSQL Externo
DATABASE_URL=postgresql://postgres:5100a23f8d3196cfce339c43d475b3e0@207.180.254.250:5432/equivalencias_ufsm

# Configurações do Flask
SECRET_KEY=ufsm_equivalencias_2025_secret_key_admin
FLASK_ENV=production
PORT=5000
```

## Passos para Configuração

### 1. Criar Banco de Dados

Conecte-se ao PostgreSQL e crie um banco específico para o projeto:

```sql
-- Conectar como postgres
psql -h 207.180.254.250 -U postgres -d postgres

-- Criar banco de dados para o projeto
CREATE DATABASE equivalencias_ufsm;

-- Conceder permissões (se necessário)
GRANT ALL PRIVILEGES ON DATABASE equivalencias_ufsm TO postgres;
```

### 2. Configurar Aplicação

1. **Copie o arquivo de exemplo**:
   ```bash
   cp .env.example .env
   ```

2. **Edite o arquivo .env** com as credenciais acima

3. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute a aplicação**:
   ```bash
   python src/main.py
   ```

### 3. Deploy com Docker

```bash
# Build da imagem
docker build -t equivalencias-ufsm .

# Executar com variáveis de ambiente
docker run -p 5000:5000 \
  -e DATABASE_URL="postgresql://postgres:5100a23f8d3196cfce339c43d475b3e0@207.180.254.250:5432/equivalencias_ufsm" \
  -e SECRET_KEY="ufsm_equivalencias_2025_secret_key_admin" \
  -e FLASK_ENV="production" \
  equivalencias-ufsm
```

### 4. Deploy com Docker Compose

Edite o `docker-compose.yml` para usar o PostgreSQL externo:

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://postgres:5100a23f8d3196cfce339c43d475b3e0@207.180.254.250:5432/equivalencias_ufsm
      - SECRET_KEY=ufsm_equivalencias_2025_secret_key_admin
      - FLASK_ENV=production
```

## Verificação da Conexão

Para testar a conexão com o banco:

```python
import psycopg2

try:
    conn = psycopg2.connect(
        host="207.180.254.250",
        database="equivalencias_ufsm",
        user="postgres",
        password="5100a23f8d3196cfce339c43d475b3e0"
    )
    print("Conexão com PostgreSQL estabelecida com sucesso!")
    conn.close()
except Exception as e:
    print(f"Erro na conexão: {e}")
```

## Migração de Dados

O sistema criará automaticamente as tabelas necessárias na primeira execução. As tabelas criadas serão:

- `admin` - Usuários administrativos
- `equivalencia` - Dados das equivalências

## Backup e Restauração

### Backup
```bash
pg_dump -h 207.180.254.250 -U postgres -d equivalencias_ufsm > backup.sql
```

### Restauração
```bash
psql -h 207.180.254.250 -U postgres -d equivalencias_ufsm < backup.sql
```

## Monitoramento

Para monitorar a aplicação em produção, considere:

- **Logs**: Configure logging adequado
- **Métricas**: Use ferramentas como Prometheus
- **Alertas**: Configure alertas para falhas
- **Backup**: Automatize backups regulares

## Segurança

- ✅ Credenciais via variáveis de ambiente
- ✅ Conexão SSL com PostgreSQL (recomendado)
- ✅ Senhas hasheadas com Werkzeug
- ✅ Validação de entrada de dados
- ✅ Proteção contra SQL injection (SQLAlchemy ORM)

