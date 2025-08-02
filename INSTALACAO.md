# Guia de Instalação - Serviço em Casa MVP

## Pré-requisitos

- Python 3.11+
- Node.js 20+
- Git

## Instalação do Backend (Flask)

1. **Navegue para o diretório do backend:**
   ```bash
   cd backend
   ```

2. **Crie e ative o ambiente virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\Scripts\activate     # Windows
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure o banco de dados:**
   ```bash
   python populate_db.py
   ```

5. **Execute o backend:**
   ```bash
   python src/main.py
   ```

   O backend estará disponível em: `http://localhost:5000`

## Instalação do Frontend (React)

1. **Navegue para o diretório do frontend:**
   ```bash
   cd frontend
   ```

2. **Instale as dependências:**
   ```bash
   pnpm install
   # ou
   npm install
   ```

3. **Execute o frontend:**
   ```bash
   pnpm run dev
   # ou
   npm run dev
   ```

   O frontend estará disponível em: `http://localhost:5173`

## Configuração da API

O frontend está configurado para se conectar ao backend em `http://localhost:5000`. Se você alterar a porta do backend, atualize o arquivo `frontend/src/lib/api.js`.

## Estrutura do Projeto

```
servico-em-casa-mvp/
├── backend/                 # API Flask
│   ├── src/                # Código fonte
│   │   ├── models/         # Modelos de dados
│   │   ├── routes/         # Rotas da API
│   │   └── main.py         # Arquivo principal
│   ├── venv/               # Ambiente virtual Python
│   ├── requirements.txt    # Dependências Python
│   └── populate_db.py      # Script para popular o banco
├── frontend/               # Interface React
│   ├── src/                # Código fonte
│   │   ├── components/     # Componentes React
│   │   ├── hooks/          # Hooks customizados
│   │   └── lib/            # Utilitários
│   ├── package.json        # Dependências Node.js
│   └── vite.config.js      # Configuração do Vite
├── README.md               # Documentação principal
├── TESTES.md               # Relatório de testes
└── INSTALACAO.md           # Este arquivo
```

## Funcionalidades Implementadas

### ✅ Funcionando
- Interface responsiva com design moderno
- Páginas de cadastro e login
- Dashboard para clientes e prestadores
- Busca de serviços por categoria e localização
- Criação de pedidos de serviço
- Visualização de propostas
- Sistema de avaliações
- Perfil de usuário

### ⚠️ Necessita Ajustes
- Integração completa entre frontend e backend
- Correção do modelo de banco de dados
- Sistema de autenticação JWT
- Upload de imagens
- Notificações em tempo real

## Próximos Passos

1. **Corrigir modelo de banco de dados**
2. **Implementar autenticação completa**
3. **Adicionar sistema de pagamentos**
4. **Implementar chat em tempo real**
5. **Adicionar testes automatizados**
6. **Fazer deploy em produção**

## Suporte

Para dúvidas ou problemas, consulte a documentação no README.md ou os testes realizados no TESTES.md.

