# Sistema de Equivalências - Curso de Administração UFSM

## 🚀 Versão Corrigida - v2.0.1

Sistema web para cadastro e consulta de equivalências de disciplinas do Curso de Administração da Universidade Federal de Santa Maria (UFSM).

### ✅ Correções Implementadas

- **Login Administrativo**: Corrigido problema onde o login não funcionava
- **Configuração de Sessões**: Implementada configuração adequada do Flask
- **Logs de Debug**: Adicionado sistema de logging detalhado
- **Tratamento de Erros**: Melhorado tratamento de exceções
- **Validações**: Implementadas validações mais robustas

## 🚀 Funcionalidades

### Área Pública

- **Consulta de Equivalências**: Visualização de todas as equivalências cadastradas
- **Sistema de Busca**: Busca por disciplina, código ou curso
- **Interface Responsiva**: Compatível com desktop, tablet e mobile
- **Ordenação**: Ordenação por qualquer coluna da tabela

### Área Administrativa

- **Autenticação Segura**: Sistema de login para administradores ✅ **CORRIGIDO**
- **CRUD Completo**: Criar, editar e excluir equivalências
- **Formulário Intuitivo**: Interface organizada para cadastro
- **Gerenciamento**: Tabela administrativa com ações rápidas

## 🛠️ Tecnologias Utilizadas

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript, Tailwind CSS
- **Banco de Dados**: Supabase PostgreSQL (produção) / SQLite (desenvolvimento)
- **Supabase**: Cliente Python integrado para operações avançadas
- **Autenticação**: Flask-SQLAlchemy + Werkzeug + Sessions ✅ **CORRIGIDO**
- **Design**: Tailwind CSS com gradientes e animações

## 🔧 Instalação e Configuração

### Pré-requisitos

- Python 3.8+
- pip (gerenciador de pacotes Python)
- Acesso ao Supabase (opcional para produção)

### Instalação Rápida

1. **Clone o repositório corrigido**
   ```bash
   git clone <url-do-repositorio-corrigido>
   cd equivalencias
   ```

2. **Crie um ambiente virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\Scripts\activate  # Windows
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente**
   ```bash
   cp .env.example .env
   # Edite o arquivo .env com suas configurações
   ```

5. **Execute o aplicativo**
   ```bash
   python src/main.py
   ```

6. **Acesse o sistema**
   - URL: http://localhost:5000
   - Usuário: `admin`
   - Senha: `adm4125`

### 🧪 Teste da Correção

Execute o script de teste para verificar se tudo está funcionando:

```bash
python teste_login.py
```

Para testar em servidor remoto:
```bash
python teste_login.py http://seu-dominio.com
```

## 🐘 Configuração com PostgreSQL/Supabase

### Variáveis de Ambiente

Crie um arquivo `.env` com:

```dotenv
# Configuração do Banco de Dados
DATABASE_URL=postgresql://usuario:senha@host:porta/banco

# Configurações do Flask
SECRET_KEY=sua_chave_secreta_muito_segura_aqui
FLASK_ENV=production
PORT=5000
```

### Exemplo para Supabase

```dotenv
DATABASE_URL=postgresql://postgres:[SUA_SENHA]@db.[SEU_PROJETO].supabase.co:5432/postgres
SECRET_KEY=ufsm_equivalencias_2025_secret_key_super_segura
FLASK_ENV=production
```

## 🚀 Deploy

### Deploy Local

```bash
gunicorn -w 4 -b 0.0.0.0:5000 src.main:app
```

### Deploy com Docker

```bash
# Construir imagem
docker build -t equivalencias-ufsm .

# Executar container
docker run -p 5000:5000 --env-file .env equivalencias-ufsm
```

### Deploy com Docker Compose

```bash
docker-compose up -d
```

## 🔐 Credenciais Padrão

- **Usuário**: `admin`
- **Senha**: `adm4125`

> ⚠️ **IMPORTANTE**: Altere as credenciais padrão em produção!

## 📁 Estrutura do Projeto

```
equivalencias-ufsm/
├── src/
│   ├── static/
│   │   ├── index.html      # Interface principal
│   │   └── app.js          # JavaScript do frontend
│   ├── models/
│   │   └── equivalencia.py # Modelos do banco de dados
│   ├── routes/
│   │   └── equivalencia.py # Rotas da API ✅ CORRIGIDAS
│   ├── config/
│   │   └── supabase.py     # Configuração Supabase
│   └── main.py             # Aplicação principal ✅ CORRIGIDA
├── requirements.txt        # Dependências Python
├── .env.example           # Exemplo de variáveis de ambiente
├── Dockerfile            # Container Docker
├── docker-compose.yml    # Orquestração Docker
├── teste_login.py        # Script de teste ✅ NOVO
├── CORRECAO_LOGIN.md     # Documentação da correção ✅ NOVO
└── README.md             # Este arquivo
```

## 🔄 API Endpoints

### Públicos

- `GET /api/equivalencias` - Lista todas as equivalências
- `GET /api/info` - Informações do sistema

### Administrativos (requer autenticação)

- `POST /api/login` - Fazer login ✅ **CORRIGIDO**
- `POST /api/logout` - Fazer logout ✅ **CORRIGIDO**
- `GET /api/check-auth` - Verificar autenticação ✅ **CORRIGIDO**
- `POST /api/equivalencias` - Criar equivalência
- `PUT /api/equivalencias/{id}` - Atualizar equivalência
- `DELETE /api/equivalencias/{id}` - Excluir equivalência

## 🐛 Resolução de Problemas

### Login não funciona

1. **Verifique os logs do servidor**
2. **Execute o teste**: `python teste_login.py`
3. **Confirme as credenciais**: admin / adm4125
4. **Verifique se o SECRET_KEY está configurado**

### Erro de banco de dados

1. **Verifique a DATABASE_URL**
2. **Confirme conectividade com o banco**
3. **Execute**: `python src/main.py` e observe os logs

### Problemas de sessão

1. **Verifique se o SECRET_KEY está definido**
2. **Confirme se as configurações de sessão estão corretas**
3. **Limpe cookies do navegador**

## 📊 Logs e Monitoramento

O sistema agora inclui logs detalhados:

```bash
# Logs de login
INFO:src.routes.equivalencia:Tentativa de login recebida
INFO:src.routes.equivalencia:Login bem-sucedido para usuário: admin

# Logs de operações
INFO:src.routes.equivalencia:Criando nova equivalência
INFO:src.routes.equivalencia:Equivalência criada com sucesso: ID 1
```

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👨‍💼 Desenvolvedor

**Prof. Juliano Alves**  
Grupo de Pesquisa em IA - IA Projetos  
Universidade Federal de Santa Maria

## 📞 Suporte

Para dúvidas ou suporte técnico, entre em contato através dos canais oficiais da UFSM.

---

**© 2025 Universidade Federal de Santa Maria - Curso de Administração**

### 🔧 Versão Corrigida

Esta versão inclui correções importantes para o sistema de login administrativo. Todas as funcionalidades foram testadas e estão funcionando corretamente.

