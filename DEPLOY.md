# 🚀 Instruções de Deploy - Sistema de Equivalências UFSM

## 📋 Repositório Preparado

O projeto está completamente preparado para deploy no GitHub com:

- ✅ Código fonte completo e organizado
- ✅ Configuração para PostgreSQL/Supabase
- ✅ Docker e Docker Compose
- ✅ Documentação completa
- ✅ Variáveis de ambiente configuradas
- ✅ Credenciais atualizadas (admin/adm4125)

## 🐙 Deploy no GitHub

### 1. Criar Repositório no GitHub

1. Acesse [GitHub](https://github.com)
2. Clique em "New repository"
3. Nome: `equivalencias`
4. Descrição: `Sistema de Equivalências - Curso de Administração UFSM`
5. Marque como **Público** (para facilitar colaboração)
6. **NÃO** inicialize com README (já temos um)

### 2. Conectar Repositório Local

```bash
# Navegar para o diretório do projeto
cd /caminho/para/equivalencias-ufsm

# Adicionar origem remota (substitua SEU_USUARIO)
git remote add origin https://github.com/SEU_USUARIO/equivalencias.git

# Fazer push do código
git branch -M main
git push -u origin main
```

### 3. Configurar GitHub Pages (Opcional)

Para documentação:
1. Vá em Settings > Pages
2. Source: Deploy from a branch
3. Branch: main / docs

## 🐘 Integração com Supabase Self-Hosted

### Configuração Automática

O sistema já está preparado para Supabase com:

**Credenciais PostgreSQL Configuradas:**
- Host: `207.180.254.250`
- Usuário: `postgres`
- Senha: `5100a23f8d3196cfce339c43d475b3e0`
- Banco: `equivalencias_ufsm` (será criado automaticamente)

### Passos para Ativação

1. **Criar arquivo .env**:
```bash
cp .env.example .env
```

2. **Editar .env** com:
```env
DATABASE_URL=postgresql://postgres:5100a23f8d3196cfce339c43d475b3e0@207.180.254.250:5432/equivalencias_ufsm
SECRET_KEY=ufsm_equivalencias_2025_secret_key_admin
FLASK_ENV=production
```

3. **Executar aplicação**:
```bash
python src/main.py
```

## 🐳 Deploy com Docker

### Desenvolvimento Local
```bash
docker-compose up -d
```

### Produção
```bash
# Build
docker build -t equivalencias-ufsm .

# Run
docker run -p 5000:5000 \
  -e DATABASE_URL="postgresql://postgres:5100a23f8d3196cfce339c43d475b3e0@207.180.254.250:5432/equivalencias_ufsm" \
  equivalencias-ufsm
```

## ☁️ Deploy em Plataformas Cloud

### Railway
1. Conecte o repositório GitHub
2. Configure variáveis de ambiente
3. Deploy automático

### Render
1. New Web Service
2. Connect GitHub repository
3. Configure environment variables

### Heroku
```bash
# Instalar Heroku CLI
heroku create equivalencias-ufsm
heroku config:set DATABASE_URL="postgresql://postgres:5100a23f8d3196cfce339c43d475b3e0@207.180.254.250:5432/equivalencias_ufsm"
git push heroku main
```

## 🔧 Configuração com Portainer + Traefik

Para deploy em VPS com Docker:

### docker-compose.prod.yml
```yaml
version: '3.8'

services:
  equivalencias:
    build: .
    environment:
      - DATABASE_URL=postgresql://postgres:5100a23f8d3196cfce339c43d475b3e0@207.180.254.250:5432/equivalencias_ufsm
      - SECRET_KEY=ufsm_equivalencias_2025_secret_key_admin
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.equivalencias.rule=Host(`equivalencias.seudominio.com`)"
      - "traefik.http.routers.equivalencias.tls.certresolver=letsencrypt"
    networks:
      - traefik

networks:
  traefik:
    external: true
```

## 📊 Monitoramento

### Logs
```bash
# Docker logs
docker logs equivalencias-ufsm

# Aplicação logs
tail -f app.log
```

### Health Check
```bash
curl http://localhost:5000/api/equivalencias
```

## 🔐 Segurança em Produção

### Checklist
- [ ] Alterar SECRET_KEY para valor único
- [ ] Configurar HTTPS/SSL
- [ ] Backup automático do banco
- [ ] Monitoramento de logs
- [ ] Rate limiting (se necessário)
- [ ] Firewall configurado

### Backup Automático
```bash
# Script de backup (crontab)
0 2 * * * pg_dump -h 207.180.254.250 -U postgres equivalencias_ufsm > /backups/equivalencias_$(date +\%Y\%m\%d).sql
```

## 📞 Suporte

**Desenvolvedor:** Prof. Juliano Alves  
**Grupo:** Pesquisa em IA - IA Projetos  
**Instituição:** UFSM

## 🎯 Próximos Passos

1. **Criar repositório no GitHub**
2. **Fazer push do código**
3. **Configurar variáveis de ambiente**
4. **Testar conexão com PostgreSQL**
5. **Deploy em produção**
6. **Configurar domínio (se necessário)**
7. **Implementar backup automático**

---

**Sistema pronto para produção! 🚀**

