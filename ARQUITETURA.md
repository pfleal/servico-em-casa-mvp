# Serviço em Casa MVP - Arquitetura do Projeto

## 📋 Visão Geral

Este é um marketplace de serviços domésticos com frontend React e backend Flask, integrado ao Supabase (PostgreSQL) e deployado no Railway.

## 🏗️ Estrutura do Projeto

```mermaid
graph TD
    A[Serviço em Casa MVP] --> B[Frontend - React/Vite]
    A --> C[Backend - Flask/Python]
    A --> D[Banco de Dados - Supabase]
    A --> E[Deploy - Railway]
    
    B --> B1[src/components]
    B --> B2[src/hooks]
    B --> B3[src/lib]
    B --> B4[Tailwind CSS + shadcn/ui]
    
    C --> C1[src/routes]
    C --> C2[src/models]
    C --> C3[src/database]
    C --> C4[src/utils]
    
    D --> D1[PostgreSQL]
    D --> D2[Autenticação]
    D --> D3[Storage]
    
    E --> E1[https://beautiful-thread-production.up.railway.app]
```

## 🌐 Arquitetura de Sistema

```mermaid
sequenceDiagram
    participant U as Usuário
    participant F as Frontend (React)
    participant B as Backend (Flask)
    participant S as Supabase (PostgreSQL)
    participant R as Railway (Deploy)
    
    U->>F: Acessa aplicação
    F->>B: Requisições API
    B->>S: Consultas SQL
    S-->>B: Dados
    B-->>F: Resposta JSON
    F-->>U: Interface atualizada
    
    Note over R: Backend deployado em produção
    Note over F: Frontend local (desenvolvimento)
```

## 📁 Estrutura de Diretórios

```
servico-em-casa-mvp/
├── frontend/                 # Aplicação React
│   ├── src/
│   │   ├── components/      # Componentes reutilizáveis
│   │   ├── hooks/          # Custom hooks
│   │   ├── lib/            # Utilitários
│   │   └── App.jsx         # Componente principal
│   ├── package.json
│   └── vite.config.js
├── backend/                 # API Flask
│   ├── src/
│   │   ├── routes/         # Endpoints da API
│   │   ├── models/         # Modelos de dados
│   │   ├── database/       # Configuração do banco
│   │   └── main.py         # Aplicação principal
│   ├── requirements.txt
│   └── Procfile           # Configuração Railway
└── ARQUITETURA.md          # Este arquivo
```

## 🔗 URLs e Endpoints

### Backend em Produção (Railway)
- **URL Base**: `https://beautiful-thread-production.up.railway.app`
- **API Base**: `https://beautiful-thread-production.up.railway.app/api`

### Principais Endpoints

```mermaid
graph LR
    A[API Base] --> B[/auth]
    A --> C[/users]
    A --> D[/services]
    A --> E[/requests]
    
    B --> B1[POST /login]
    B --> B2[POST /register]
    B --> B3[GET /profile]
    
    C --> C1[GET /users]
    C --> C2[POST /users]
    C --> C3[PUT /users/:id]
    
    D --> D1[GET /services]
    D --> D2[POST /services]
    
    E --> E1[GET /requests]
    E --> E2[POST /requests]
```

## 🔐 Autenticação

```mermaid
sequenceDiagram
    participant C as Cliente
    participant A as API Auth
    participant DB as Supabase
    
    C->>A: POST /api/auth/register
    A->>DB: Criar usuário
    DB-->>A: Usuário criado
    A-->>C: Sucesso
    
    C->>A: POST /api/auth/login
    A->>DB: Verificar credenciais
    DB-->>A: Usuário válido
    A-->>C: JWT Token
    
    C->>A: GET /api/auth/profile (com token)
    A->>A: Validar JWT
    A->>DB: Buscar dados do usuário
    DB-->>A: Dados do usuário
    A-->>C: Perfil do usuário
```

## 🚀 Como Conectar ao Backend em Nuvem

### 1. Configuração do Frontend

No arquivo `frontend/src/lib/api.js`, configure a URL base:

```javascript
const API_BASE_URL = 'https://beautiful-thread-production.up.railway.app/api';
```

### 2. Credenciais de Teste

```
E-mail: joao.silva@email.com
Senha: MinhaSenh@123
```

### 3. Variáveis de Ambiente (Backend)

```env
DATABASE_URL=postgresql://postgres:[password]@db.fhksnwlygqdwnrdymwlz.supabase.co:5432/postgres
SUPABASE_URL=https://fhksnwlygqdwnrdymwlz.supabase.co
SUPABASE_ANON_KEY=[key]
SUPABASE_SERVICE_ROLE_KEY=[key]
```

## 🛠️ Comandos de Desenvolvimento

### Frontend
```bash
cd frontend
npm install
npm run dev
# Acesse: http://localhost:5173
```

### Backend (Local)
```bash
cd backend
pip install -r requirements.txt
python src/main.py
# Acesse: http://localhost:5000
```

## 🎨 Sistema de Temas

O frontend possui um sistema de temas avançado:

```mermaid
graph TD
    A[Sistema de Temas] --> B[Light Themes]
    A --> C[Dark Themes]
    A --> D[Pastel Themes]
    
    B --> B1[light]
    B --> B2[gray]
    
    C --> C1[dark]
    C --> C2[blue-dark]
    C --> C3[red-dark]
    C --> C4[green-dark]
    
    D --> D1[rose-pastel]
    D --> D2[blue-pastel]
    D --> D3[mint-pastel]
    
    A --> E[localStorage]
    E --> F[servico-em-casa-theme]
```

## 📊 Modelos de Dados

```mermaid
erDiagram
    USERS {
        int id PK
        string name
        string email UK
        string password_hash
        string phone
        string address
        string city
        string state
        string zip_code
        string user_type
        boolean is_active
        boolean is_verified
        datetime created_at
        datetime updated_at
    }
    
    SERVICES {
        int id PK
        string name
        text description
        decimal base_price
        string category
        boolean is_active
        datetime created_at
        datetime updated_at
    }
    
    SERVICE_REQUESTS {
        int id PK
        int client_id FK
        int service_id FK
        text description
        string status
        decimal proposed_price
        datetime scheduled_date
        datetime created_at
        datetime updated_at
    }
    
    USERS ||--o{ SERVICE_REQUESTS : creates
    SERVICES ||--o{ SERVICE_REQUESTS : requested
```

## 🔄 Fluxo de Desenvolvimento

```mermaid
flowchart TD
    A[Início] --> B[Clonar Repositório]
    B --> C[Instalar Dependências]
    C --> D[Configurar Variáveis]
    D --> E[Iniciar Frontend]
    E --> F[Conectar ao Backend em Nuvem]
    F --> G[Testar Funcionalidades]
    G --> H[Desenvolvimento]
    
    H --> I{Mudanças no Backend?}
    I -->|Sim| J[Deploy no Railway]
    I -->|Não| K[Continuar Frontend]
    
    J --> L[Testar em Produção]
    K --> M[Testar Localmente]
    
    L --> N[Finalizado]
    M --> N
```

## 📝 Notas Importantes

1. **Backend em Produção**: O backend está sempre disponível no Railway
2. **Banco de Dados**: Supabase PostgreSQL configurado e populado
3. **Autenticação**: JWT implementado e funcionando
4. **CORS**: Configurado para aceitar requisições do frontend
5. **Temas**: Sistema completo com persistência no localStorage
6. **Responsivo**: Interface adaptada para mobile e desktop

## 🆘 Troubleshooting

### Erro de CORS
```javascript
// Verificar se a URL da API está correta
const API_BASE_URL = 'https://beautiful-thread-production.up.railway.app/api';
```

### Erro de Autenticação
```javascript
// Verificar se o token está sendo enviado
headers: {
  'Authorization': `Bearer ${token}`,
  'Content-Type': 'application/json'
}
```

### Erro de Conexão
```bash
# Verificar se o backend está online
curl https://beautiful-thread-production.up.railway.app/api/health
```

---

**Última atualização**: Janeiro 2025  
**Versão**: 1.0.0  
**Status**: ✅ Produção Ativa