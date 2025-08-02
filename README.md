# Serviço em Casa - MVP Marketplace de Serviços

## Introdução

O "Serviço em Casa" é um marketplace digital que conecta clientes que necessitam de serviços domiciliares com prestadores qualificados. Esta plataforma visa simplificar o processo de contratação de serviços como limpeza, manutenção, reparos e outros serviços domésticos, proporcionando uma experiência segura e eficiente para ambas as partes.

O MVP (Minimum Viable Product) foi projetado para validar o conceito de negócio com funcionalidades essenciais que permitem o funcionamento básico do marketplace, incluindo cadastro de usuários, busca de serviços, criação de pedidos, envio de propostas e sistema de avaliações.

## Visão Geral da Arquitetura

### Stack Tecnológico Selecionado

Para o desenvolvimento do MVP, optamos por uma stack moderna e eficiente que permite desenvolvimento rápido e escalabilidade futura:

**Backend:**
- Framework: Flask (Python) - Escolhido pela simplicidade, flexibilidade e rapidez de desenvolvimento
- Banco de Dados: SQLite (para MVP) com migração futura para PostgreSQL
- Autenticação: JWT (JSON Web Tokens) para sessões seguras
- APIs: RESTful seguindo padrões REST

**Frontend:**
- Framework: React.js - Interface moderna e responsiva
- Gerenciamento de Estado: Context API do React
- Estilização: CSS Modules com design responsivo
- Comunicação: Axios para requisições HTTP

**Infraestrutura:**
- Desenvolvimento: Ambiente local com hot-reload
- Deploy: Plataforma gratuita (Railway/Vercel) para demonstração
- Versionamento: Git com estrutura de branches organizada




## Tipos de Usuário

### Cliente (Contratante)

O cliente é o usuário que busca contratar serviços domiciliares. Suas principais características e funcionalidades incluem:

**Perfil e Cadastro:**
- Cadastro simplificado com dados básicos (nome, email, telefone, endereço)
- Verificação de email obrigatória para ativação da conta
- Possibilidade de adicionar foto de perfil
- Informações de localização para busca geolocalizada de prestadores

**Funcionalidades Principais:**
- Busca de prestadores por categoria de serviço (limpeza, elétrica, hidráulica, etc.)
- Filtros por distância, avaliação e disponibilidade
- Criação de pedidos detalhados com descrição, fotos e urgência
- Recebimento de propostas de múltiplos prestadores
- Sistema de chat para comunicação direta com prestadores
- Avaliação de prestadores após conclusão do serviço
- Histórico completo de serviços contratados

**Jornada do Cliente:**
1. Cadastro e verificação de email
2. Busca por categoria de serviço desejado
3. Criação de pedido com detalhes específicos
4. Recebimento e análise de propostas
5. Seleção do prestador e confirmação do serviço
6. Acompanhamento da execução via chat
7. Avaliação final do serviço prestado

### Prestador de Serviços

O prestador é o profissional que oferece serviços domiciliares através da plataforma. Suas características incluem:

**Perfil e Cadastro:**
- Cadastro detalhado com dados pessoais e profissionais
- Upload obrigatório de documentos (RG, CPF, comprovante de residência)
- Foto profissional para o perfil
- Seleção de categorias de serviço em que atua
- Definição de raio de atendimento ou cidades de atuação
- Portfólio com fotos de trabalhos anteriores

**Funcionalidades Principais:**
- Recebimento de notificações de novos pedidos na sua área
- Envio de propostas personalizadas com valor, prazo e observações
- Gestão de agenda e disponibilidade
- Sistema de chat para comunicação com clientes
- Acompanhamento de avaliações e reputação
- Histórico de serviços prestados e ganhos

**Processo de Verificação:**
- Análise de documentos enviados
- Verificação de antecedentes (futuramente)
- Aprovação manual para início das atividades
- Sistema de badges de verificação no perfil

**Jornada do Prestador:**
1. Cadastro com documentos e informações profissionais
2. Aguardo da verificação e aprovação
3. Configuração de perfil e categorias de atuação
4. Recebimento de notificações de pedidos
5. Envio de propostas competitivas
6. Execução do serviço contratado
7. Recebimento de avaliação e pagamento



## Módulos do Sistema

### 1. Cadastro e Autenticação

Este módulo é responsável por gerenciar o ciclo de vida dos usuários na plataforma, desde o registro até o acesso seguro.

**Funcionalidades:**
- **Registro de Usuário:** Permite que clientes e prestadores criem suas contas, fornecendo informações básicas como nome, e-mail e senha. Inclui validação de e-mail para garantir a autenticidade.
- **Login e Logout:** Gerencia o acesso dos usuários à plataforma, utilizando e-mail/senha e JWT para manter a sessão segura.
- **Recuperação de Senha:** Funcionalidade para usuários que esqueceram suas senhas, com envio de link de redefinição por e-mail.
- **Upload de Documentos:** Para prestadores, permite o upload de documentos de identificação (RG, CPF) e comprovante de residência, essenciais para o processo de verificação.
- **Classificação de Usuário:** Define se o usuário é um 'Cliente' ou 'Prestador', impactando as funcionalidades e a interface que ele terá acesso.

**Tecnologias:**
- Backend: Flask-JWT-Extended para autenticação JWT, Flask-Mail para envio de e-mails.
- Frontend: Formulários React com validação, Axios para comunicação com a API de autenticação.

### 2. Busca e Geolocalização

Este módulo permite que clientes encontrem prestadores de serviço com base em suas necessidades e localização.

**Funcionalidades:**
- **Busca por Categoria/Palavra-chave:** Clientes podem pesquisar serviços específicos (ex: 'eletricista', 'limpeza de sofá') ou navegar por categorias predefinidas.
- **Filtragem:** Resultados podem ser filtrados por distância do cliente, avaliação média do prestador e disponibilidade.
- **Integração com API de Mapas:** Utilização de uma API de geolocalização (Google Maps API ou OpenStreetMap) para exibir prestadores em um mapa e calcular distâncias.

**Tecnologias:**
- Backend: Funções para cálculo de distância (haversine formula), integração com APIs de geocodificação.
- Frontend: Componentes de busca React, integração com bibliotecas de mapas (ex: Leaflet para OpenStreetMap).

### 3. Pedidos de Serviço

Este módulo gerencia a criação e o ciclo de vida dos pedidos de serviço feitos pelos clientes.

**Funcionalidades:**
- **Criação de Pedido:** Formulário dinâmico onde o cliente descreve o serviço, adiciona imagens, informa o local e a urgência.
- **Notificação de Prestadores:** Após a criação de um pedido, prestadores qualificados e próximos são notificados em tempo real.
- **Gestão de Pedidos:** Clientes podem visualizar o status de seus pedidos (pendente, em andamento, concluído, cancelado).

**Tecnologias:**
- Backend: Modelos de dados para Pedidos, lógica de notificação (via WebSockets ou sistema de filas).
- Frontend: Formulários React para criação de pedidos, componentes para exibição do status.

### 4. Mensagens

Um sistema de comunicação interno para facilitar a interação entre clientes e prestadores.

**Funcionalidades:**
- **Chat Interno:** Permite que clientes e prestadores troquem mensagens em tempo real após um pedido ser criado ou uma proposta enviada.
- **Notificações:** Envio de notificações (push/e-mail) para novas mensagens ou atualizações importantes.
- **Histórico de Conversas:** Armazenamento de todas as conversas para referência futura.

**Tecnologias:**
- Backend: Flask-SocketIO para comunicação em tempo real via WebSockets.
- Frontend: Componentes de chat React, integração com Socket.IO client.

### 5. Orçamentos e Contratos

Este módulo permite que prestadores enviem propostas e que clientes as aceitem, formalizando o início do serviço.

**Funcionalidades:**
- **Envio de Propostas:** Prestadores podem enviar propostas detalhadas, incluindo valor, prazo de execução e observações adicionais.
- **Aceitação de Propostas:** Clientes podem aceitar ou recusar propostas recebidas.
- **Contrato Leve:** Geração de um 


“contrato leve” com as regras claras do serviço após a aceitação da proposta, garantindo transparência.

**Tecnologias:**
- Backend: Modelos de dados para Propostas, lógica de aceitação/recusa.
- Frontend: Interface para visualização e gestão de propostas.

### 6. Avaliações e Reputação

Essencial para construir confiança e qualidade na plataforma.

**Funcionalidades:**
- **Avaliação Mútua:** Após a conclusão de um serviço, tanto o cliente quanto o prestador podem se avaliar mutuamente (estrelas e comentários).
- **Sistema de Estrelas:** Avaliação de 1 a 5 estrelas para diferentes aspectos do serviço.
- **Comentários:** Campo para feedback detalhado.
- **Média de Avaliações:** Exibição da média de avaliações no perfil de cada usuário.

**Tecnologias:**
- Backend: Modelos de dados para Avaliações, lógica de cálculo de média.
- Frontend: Componentes de avaliação (estrelas), exibição de comentários.

### 7. Pagamentos (futuramente)

Este módulo será implementado em fases futuras do projeto, após a validação do MVP.

**Funcionalidades:**
- **Integração com Gateways de Pagamento:** Suporte a Pix, Cartão de Crédito/Débito (ex: Stripe, Pagar.me).
- **Garantia de Repasse:** Liberação do pagamento ao prestador somente após a confirmação da conclusão do serviço pelo cliente.
- **Carteira Digital:** Possibilidade de os prestadores terem uma carteira digital na plataforma para gerenciar seus recebimentos.

**Tecnologias:**
- Backend: Integração com APIs de gateways de pagamento.
- Frontend: Interfaces para checkout e gestão de pagamentos.

### 8. Segurança

Medidas para garantir a integridade e a privacidade dos dados.

**Funcionalidades:**
- **Criptografia de Senhas:** Utilização de algoritmos robustos (ex: BCrypt) para armazenar senhas de forma segura.
- **Validação de CNPJ/CPF:** Para prestadores, validação dos documentos para evitar fraudes.
- **Proteção contra Ameaças:** Mecanismos para prevenir spam, ataques de força bruta e bots.

**Tecnologias:**
- Backend: Bibliotecas de criptografia, validação de dados.
- Infraestrutura: Configurações de segurança de rede, firewalls.




## Regras de Negócio

As regras de negócio definem o comportamento e as restrições da plataforma, garantindo a integridade e a funcionalidade do marketplace.

- **Verificação de Prestadores:** Somente prestadores de serviço que tiveram seus documentos verificados e aprovados podem receber pedidos e enviar propostas.
- **Pausar Atendimento:** Prestadores têm a opção de pausar seu atendimento na plataforma, indicando que não estão disponíveis para novos serviços por um período.
- **Recusa de Propostas:** Clientes podem recusar propostas recebidas de prestadores sem qualquer penalidade.
- **Avaliações Negativas:** Um prestador que acumular 3 avaliações ruins (abaixo de uma pontuação definida, ex: 2 estrelas) entrará em análise pela equipe da plataforma, podendo ter seu perfil suspenso ou desativado.
- **Avaliação de Clientes (Opcional):** Em futuras versões, clientes também poderão ser avaliados pelos prestadores, incentivando um comportamento respeitoso e colaborativo.

## Funcionalidades Mobile Prioritárias (para futuras fases)

Embora o MVP inicial seja focado na versão web, as seguintes funcionalidades são prioritárias para o desenvolvimento mobile:

- **Notificações Push em Tempo Real:** Para alertar clientes sobre novas propostas e prestadores sobre novos pedidos ou mensagens.
- **Geolocalização Instantânea:** Utilização do GPS do dispositivo para localização precisa do usuário e dos serviços.
- **Interface Simplificada:** Design otimizado para aceitar/recusar pedidos e propostas com poucos toques.
- **Upload de Fotos do Serviço:** Permite que prestadores e clientes anexem fotos diretamente do celular para descrever melhor o serviço ou comprovar a execução.

## MVP (Mínimo Produto Viável)

O MVP do "Serviço em Casa" focará nas funcionalidades essenciais para validar o core do negócio:

- **Cadastro de Cliente e Prestador:** Permite que os dois tipos de usuários se registrem na plataforma.
- **Busca por Categoria e Localização:** Clientes podem encontrar prestadores com base no tipo de serviço e proximidade.
- **Criação e Envio de Pedido:** Clientes podem detalhar suas necessidades e enviar pedidos de serviço.
- **Proposta e Aceite:** Prestadores podem enviar propostas para os pedidos, e clientes podem aceitá-las.
- **Avaliação:** Sistema básico de avaliação para clientes avaliarem prestadores após a conclusão do serviço.
- **Painel Web de Admin:** Uma interface simples para a equipe da plataforma gerenciar usuários e serviços.

Este MVP será a base para futuras iterações e aprimoramentos da plataforma, incorporando mais funcionalidades e escalabilidade conforme o feedback dos usuários e as necessidades do mercado.

