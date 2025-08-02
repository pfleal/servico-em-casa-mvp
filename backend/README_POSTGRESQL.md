# Migração para PostgreSQL (Supabase)

Este documento descreve a migração do banco de dados SQLite para PostgreSQL usando o Supabase.

## 🚀 Configuração Realizada

### 1. Dependências Adicionadas
- `psycopg2-binary==2.9.9` - Driver PostgreSQL para Python
- `python-dotenv==1.0.0` - Carregamento de variáveis de ambiente

### 2. Arquivos Criados/Modificados

#### `.env` - Variáveis de Ambiente
```env
# Configurações do Supabase PostgreSQL
SUPABASE_URL=https://fhksnwlygqdwnrdymwlz.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_SERVICE_ROLE_KEY=sbp_f7466e28e6bb632ccce762c102b5ff19260a07e0

# Configuração do banco PostgreSQL
DATABASE_URL=postgresql://postgres:peixebolagato@db.fhksnwlygqdwnrdymwlz.supabase.co:5432/postgres

# Configurações da aplicação
FLASK_ENV=development
SECRET_KEY=asdf#FGSgvasgf$5$WGT
JWT_SECRET_KEY=jwt-secret-string
```

#### `src/config.py` - Configurações Centralizadas
- Configurações para desenvolvimento, produção e testes
- Carregamento automático de variáveis de ambiente
- Configurações específicas do Supabase

#### `migrate_to_postgres.py` - Script de Migração
- Migra dados do SQLite para PostgreSQL
- Trata diferenças de tipos de dados (booleanos, timestamps)
- Lida com palavras reservadas do PostgreSQL ("user")
- Transações seguras com rollback em caso de erro

### 3. Modificações no `main.py`
- Importação do sistema de configuração
- Remoção de configurações hardcoded
- Uso de configurações baseadas em ambiente

## 📊 Dados Migrados

A migração foi executada com sucesso, transferindo:
- ✅ 10 registros da tabela `service_category`
- ✅ 1 registro da tabela `user`
- ✅ 3 registros da tabela `service_request`
- ℹ️ Tabelas vazias: `provider_service`, `proposal`, `evaluation`, `message`

## 🔧 Como Usar

### Primeira Execução
1. Certifique-se de que o ambiente virtual está ativo
2. Instale as dependências: `pip install -r requirements.txt`
3. Execute a migração: `python migrate_to_postgres.py`
4. Inicie a aplicação: `python src/main.py`

### Execuções Subsequentes
1. Ative o ambiente virtual
2. Inicie a aplicação: `python src/main.py`

## 🌟 Benefícios da Migração

### Performance
- PostgreSQL oferece melhor performance para consultas complexas
- Suporte nativo a índices avançados
- Melhor handling de conexões concorrentes

### Escalabilidade
- Supabase oferece escalabilidade automática
- Backup automático e recuperação de desastres
- Monitoramento integrado

### Recursos Avançados
- Suporte a JSON nativo
- Full-text search
- Extensões PostgreSQL
- APIs REST automáticas via Supabase

### Produção
- Ambiente de produção profissional
- SSL/TLS por padrão
- Autenticação e autorização integradas
- Dashboard de administração

## 🔒 Segurança

- Todas as credenciais estão no arquivo `.env` (não commitado)
- Conexões SSL/TLS obrigatórias
- Autenticação via tokens do Supabase
- Isolamento de ambiente (dev/prod)

## 📝 Logs

O sistema de logging continua funcionando normalmente, registrando:
- Conexões de banco de dados
- Operações CRUD
- Erros e exceções
- Performance de queries

## 🚨 Importante

- **Nunca commite o arquivo `.env`** - ele contém credenciais sensíveis
- Mantenha backups regulares dos dados
- Use diferentes bancos para desenvolvimento e produção
- Monitore o uso de recursos no dashboard do Supabase

## 🆘 Troubleshooting

### Erro de Conexão
- Verifique se a `DATABASE_URL` está correta no `.env`
- Confirme se o Supabase está acessível
- Verifique as credenciais de acesso

### Erro de Migração
- Execute `python migrate_to_postgres.py` novamente
- Verifique se o SQLite original existe
- Confirme se as tabelas foram criadas no PostgreSQL

### Performance Lenta
- Verifique o plano do Supabase
- Analise queries no dashboard
- Considere adicionar índices específicos