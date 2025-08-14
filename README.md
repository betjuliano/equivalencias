# Sistema de Equivalências - Curso de Administração UFSM

Sistema web para cadastro e consulta de equivalências de disciplinas do Curso de Administração da Universidade Federal de Santa Maria (UFSM).

## 🚀 Funcionalidades

### Área Pública
- **Consulta de Equivalências**: Visualização de todas as equivalências cadastradas
- **Sistema de Busca**: Busca por disciplina, código ou curso
- **Interface Responsiva**: Compatível com desktop, tablet e mobile
- **Ordenação**: Ordenação por qualquer coluna da tabela

### Área Administrativa
- **Autenticação Segura**: Sistema de login para administradores
- **CRUD Completo**: Criar, editar e excluir equivalências
- **Formulário Intuitivo**: Interface organizada para cadastro
- **Gerenciamento**: Tabela administrativa com ações rápidas

## 🛠️ Tecnologias Utilizadas

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript, Tailwind CSS
- **Banco de Dados**: SQLite (desenvolvimento) / PostgreSQL (produção)
- **Autenticação**: Flask-SQLAlchemy + Werkzeug
- **Design**: Tailwind CSS com gradientes e animações

## 📋 Estrutura de Dados

Cada equivalência contém:

### Disciplina da Administração (UFSM)
- Disciplina (nome completo)
- Código (código oficial)
- Carga Horária (ex: 60h)

### Disciplina Equivalente
- Disciplina Equivalente (nome)
- Código (código da disciplina)
- Curso (curso de origem)
- Carga Horária (ex: 60h)

### Informações Adicionais
- Justificativa (descrição detalhada)
- Data de Criação (automática)

## 🔧 Instalação e Configuração

### Pré-requisitos
- Python 3.8+
- pip (gerenciador de pacotes Python)

### Instalação Local

1. **Clone o repositório**
```bash
git clone https://github.com/seu-usuario/equivalencias.git
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
- Usuário: admin
- Senha: adm4125

## 🐘 Configuração com PostgreSQL/Supabase

### Variáveis de Ambiente

Crie um arquivo `.env` com:

```env
# Configuração do Banco de Dados
DATABASE_URL=postgresql://usuario:senha@host:porta/banco

# Configurações do Flask
SECRET_KEY=sua_chave_secreta_aqui
FLASK_ENV=production
PORT=5000
```

### Exemplo para Supabase

```env
DATABASE_URL=postgresql://postgres:[SUA_SENHA]@db.[SEU_PROJETO].supabase.co:5432/postgres
SECRET_KEY=ufsm_equivalencias_2025_secret_key
FLASK_ENV=production
```

### Migração de Dados

O sistema criará automaticamente as tabelas necessárias na primeira execução. Para migrar dados existentes:

1. Execute o sistema uma vez para criar as tabelas
2. Use ferramentas como pgAdmin ou scripts SQL para importar dados
3. O usuário administrador será criado automaticamente

## 🚀 Deploy

### Deploy Local
```bash
gunicorn -w 4 -b 0.0.0.0:5000 src.main:app
```

### Deploy com Docker

Crie um `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "src.main:app"]
```

### Deploy em Plataformas Cloud
- **Heroku**: Compatível com Procfile
- **Railway**: Deploy automático via GitHub
- **Render**: Suporte nativo para Flask
- **DigitalOcean App Platform**: Deploy direto do repositório

## 🔐 Credenciais Padrão

- **Usuário**: admin
- **Senha**: adm4125

> ⚠️ **Importante**: Altere as credenciais padrão em produção!

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
│   │   └── equivalencia.py # Rotas da API
│   └── main.py             # Aplicação principal
├── requirements.txt        # Dependências Python
├── .env.example           # Exemplo de variáveis de ambiente
├── .gitignore            # Arquivos ignorados pelo Git
└── README.md             # Este arquivo
```

## 🎨 Design e Interface

- **Paleta de Cores**: Azul UFSM institucional
- **Gradientes**: Modernos e profissionais
- **Responsividade**: Mobile-first design
- **Animações**: Transições suaves CSS
- **Tipografia**: Hierarquia clara e legível

## 🔄 API Endpoints

### Públicos
- `GET /api/equivalencias` - Lista todas as equivalências

### Administrativos (requer autenticação)
- `POST /api/login` - Fazer login
- `POST /api/logout` - Fazer logout
- `GET /api/check-auth` - Verificar autenticação
- `POST /api/equivalencias` - Criar equivalência
- `PUT /api/equivalencias/{id}` - Atualizar equivalência
- `DELETE /api/equivalencias/{id}` - Excluir equivalência

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

