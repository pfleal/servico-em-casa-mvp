# Deploy do Backend no Railway

## 📋 Pré-requisitos

1. Conta no [Railway.app](https://railway.app)
2. Repositório GitHub com o código do backend
3. Variáveis de ambiente do Supabase

## 🚀 Passos para Deploy

### 1. Preparação dos Arquivos

Os seguintes arquivos já foram criados:
- ✅ `Procfile` - Comando para iniciar a aplicação
- ✅ `railway.json` - Configurações do Railway
- ✅ `requirements.txt` - Dependências Python

### 2. Deploy no Railway

1. **Acesse o Railway**: https://railway.app
2. **Faça login** com sua conta GitHub
3. **Clique em "New Project"**
4. **Selecione "Deploy from GitHub repo"**
5. **Escolha o repositório** do seu projeto
6. **Selecione a pasta `backend`** como diretório raiz

### 3. Configurar Variáveis de Ambiente

No painel do Railway, vá em **Variables** e adicione:

```env
FLASK_ENV=production
SECRET_KEY=asdf#FGSgvasgf$5$WGT
JWT_SECRET_KEY=jwt-secret-string
SUPABASE_URL=https://fhksnwlygqdwnrdymwlz.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZoa3Nud2x5Z3Fkd25yZHltd2x6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQxNjExOTgsImV4cCI6MjA2OTczNzE5OH0.DesiS550vbiH0TpLdQ66BW9KFjLvLNlIsPihYg2cLUg
SUPABASE_SERVICE_ROLE_KEY=sbp_f7466e28e6bb632ccce762c102b5ff19260a07e0
DATABASE_URL=postgresql://postgres:peixebolagato@db.fhksnwlygqdwnrdymwlz.supabase.co:5432/postgres
```

### 4. Deploy Automático

O Railway irá:
1. Detectar automaticamente que é uma aplicação Python
2. Instalar as dependências do `requirements.txt`
3. Executar o comando do `Procfile`
4. Gerar uma URL pública para sua API

### 5. Verificar o Deploy

1. **Aguarde o build** terminar (geralmente 2-5 minutos)
2. **Clique em "Generate Domain"** para obter a URL pública
3. **Teste a API** acessando: `https://seu-dominio.railway.app/`

## 🔧 Comandos Úteis

### Testar localmente antes do deploy:
```bash
cd backend
pip install -r requirements.txt
gunicorn src.main:app --host 0.0.0.0 --port 8000
```

### Ver logs no Railway:
- Acesse o painel do projeto
- Clique na aba "Deployments"
- Clique no deployment ativo
- Veja os logs em tempo real

## 🌐 Integração com Frontend

Após o deploy, atualize a URL da API no frontend:

```javascript
// No arquivo de configuração do frontend
const API_BASE_URL = 'https://seu-dominio.railway.app/api'
```

## 🔍 Troubleshooting

### Erro de Conexão com Banco:
- Verifique se as variáveis `DATABASE_URL` estão corretas
- Confirme se o Supabase permite conexões externas

### Erro 500 na API:
- Verifique os logs no Railway
- Confirme se todas as variáveis de ambiente estão configuradas

### Build Falha:
- Verifique se o `requirements.txt` está correto
- Confirme se não há dependências conflitantes

## 📞 Suporte

Se precisar de ajuda:
1. Verifique os logs no Railway
2. Teste a aplicação localmente primeiro
3. Confirme se todas as variáveis estão configuradas

---

**✨ Pronto! Seu backend Flask estará rodando no Railway integrado com o Supabase!**