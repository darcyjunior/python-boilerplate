# Boilerplate Python

Um template moderno para projetos Python seguindo as melhores práticas de desenvolvimento, pronto para ser utilizado como base em novos projetos.

## 📚 Sumário

- [Quickstart](#-quickstart)
- [Recursos](#-recursos)
- [Testes](#-testes)
- [Ambiente (Python 3.11)](#-ambiente-python-311)
- [Variáveis de Ambiente](#-variáveis-de-ambiente-env)
- [Scripts úteis](#-scripts-úteis)
- [Exemplo Prático](#-exemplo-prático)
- [Interface Web](#-interface-web-para-o-exemplo-de-tarefas)
- [Executando localmente](#-executando-localmente)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Ferramentas de Desenvolvimento](#-ferramentas-de-desenvolvimento)
- [Contribuindo](#-contribuindo)

## ⚡ Quickstart

```bash
# 1) Clonar o repositório
git clone https://github.com/darcyjunior/python-boilerplate.git
cd python-boilerplate

# 2) Criar e ativar venv (Python 3.11)
python3.11 -m venv .venv
source .venv/bin/activate
python3 -m pip install -U pip
pip install -e ".[dev]"

# 3) Rodar o servidor (porta 8010)
uvicorn boilerplate.main:app --reload --port 8010

# 4) Abrir a documentação
xdg-open http://localhost:8010/docs || open http://localhost:8010/docs
```

## 🚀 Recursos

- ✅ Estrutura de projeto Python moderna e organizada
- ✅ Configuração com `pyproject.toml` (PEP 621)
- ✅ Suporte a Docker e Docker Compose
- ✅ Configuração de ambiente com variáveis de ambiente
- ✅ Documentação automática da API com Swagger UI e ReDoc
- ✅ Testes unitários e de integração com cobertura de código
- ✅ Linting e formatação de código (Black, isort, flake8, mypy)
- ✅ Suporte a banco de dados (SQLAlchemy)
- ✅ Autenticação JWT
- ✅ Logging configurável
- ✅ Tratamento de erros global
- ✅ CORS configurável

## 🧪 Testes

O projeto inclui testes unitários e de integração para garantir a qualidade do código. Os testes estão organizados da seguinte forma:

```
tests/
├── unit/                 # Testes unitários
│   └── test_todo_service.py  # Testes para o serviço de Tarefas
└── integration/          # Testes de integração
    └── test_todo_api.py      # Testes para a API de Tarefas
```

### Como executar os testes

1. Instale as dependências de desenvolvimento:
   ```bash
   pip install -e ".[dev]"
   ```

2. Execute todos os testes com cobertura:
   ```bash
   pytest
   ```

3. Execute apenas testes unitários:
   ```bash
   pytest tests/unit/
   ```

4. Execute apenas testes de integração:
   ```bash
   pytest tests/integration/
   ```

5. Gere um relatório de cobertura em HTML:
   ```bash
   pytest --cov=boilerplate --cov-report=html
   ```
   O relatório estará disponível em `htmlcov/index.html`

### O que está sendo testado

- **Testes Unitários**:
  - Criação, leitura, atualização e exclusão de tarefas
  - Filtros de busca (tarefas concluídas/pendentes)
  - Validação de dados
  - Comportamento do serviço em casos de erro

- **Testes de Integração**:
  - Endpoints da API REST
  - Respostas HTTP corretas
  - Validação de esquemas de dados
  - Comportamento da API em casos de erro

## 🚀 Exemplo Prático

## 🧰 Ambiente (Python 3.11)

- Requer Python 3.11 (veja `pyproject.toml: requires-python = ">=3.11,<3.12"`).
- Criar e ativar o ambiente virtual:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python3 -m pip install -U pip
pip install -e ".[dev]"
```

## 🔐 Variáveis de Ambiente (.env)

Crie um arquivo `.env` na raiz (baseado em `.env.example`).

| Variável | Default | Descrição |
|---|---|---|
| ENVIRONMENT | development | Ambiente da aplicação (development/production) |
| DEBUG | False | Ativa logs de debug |
| SECRET_KEY | your-secret-key-here | Em produção é obrigatório alterar |
| ALLOWED_ORIGINS | * | CORS |
| TIMEZONE | America/Sao_Paulo | Timezone padrão |

Observação: Em produção, `SECRET_KEY` não pode ficar no default; validado em runtime.

## 🧾 Scripts úteis

### 🚀 Iniciar o servidor

```bash
uvicorn boilerplate.main:app --reload --port 8010
```

### 🧹 Limpar exemplo prático

Visualizar o que será removido (sem deletar):
```bash
python scripts/cleanup_example.py --dry-run
```

Remoção com confirmação interativa:
```bash
python scripts/cleanup_example.py
```

Remover tudo sem confirmação (útil para CI/automação):
```bash
python scripts/cleanup_example.py --yes
```

> **Nota**: O script verifica se os caminhos são seguros (dentro do projeto) antes de remover qualquer arquivo.

Vamos criar um exemplo prático de uma API de tarefas (To-Do) para demonstrar como utilizar este boilerplate.

### Onde está o exemplo no código

- Modelos: `src/boilerplate/models/todo.py`
- Serviço: `src/boilerplate/services/todo.py`
- Endpoints: `src/boilerplate/api/v1/endpoints/todos.py`

### Endpoints principais

- `GET /api/v1/todos/` — Lista todas as tarefas
- `POST /api/v1/todos/` — Cria uma nova tarefa (201)
- `GET /api/v1/todos/{todo_id}` — Obtém uma tarefa específica
- `PUT /api/v1/todos/{todo_id}` — Atualiza uma tarefa
- `DELETE /api/v1/todos/{todo_id}` — Remove uma tarefa (204)

Exemplo para criar uma tarefa:

```bash
curl -X POST 'http://localhost:8010/api/v1/todos/' \
  -H 'Content-Type: application/json' \
  -d '{"title": "Minha primeira tarefa", "description": "Exemplo"}'
```

## 🌐 Interface Web para o Exemplo de Tarefas

Além da API RESTful, este projeto inclui uma interface web amigável para gerenciar suas tarefas. A interface foi construída com HTML, JavaScript puro e estilizada com Tailwind CSS e Flowbite.

### Acessando a Interface

1. Certifique-se de que o servidor está em execução:
   ```bash
   uvicorn boilerplate.main:app --reload
   ```

2. Acesse a interface web em seu navegador:
   ```
   http://localhost:8010/todos
   ```

### Recursos da Interface

- ✅ Listagem de todas as tarefas
- ✅ Adicionar nova tarefa
- ✅ Marcar tarefa como concluída
- ✅ Editar tarefa existente
- ✅ Excluir tarefa
- ✅ Interface responsiva que funciona em dispositivos móveis
- ✅ Atualização em tempo real

### Estrutura dos Arquivos

A interface web consiste nos seguintes arquivos:

- `templates/base.html` - Layout base com cabeçalho e rodapé
- `templates/todos.html` - Página principal da lista de tarefas
- `static/css/styles.css` - Estilos personalizados
- `static/js/todos.js` - Lógica JavaScript para interação com a API

### Personalização

Você pode personalizar facilmente a interface modificando os arquivos na pasta `templates` e `static`:

1. **Cores**: Edite as classes do Tailwind no `base.html`
2. **Layout**: Modifique a estrutura em `todos.html`
3. **Comportamento**: Ajuste a lógica em `todos.js`
4. **Estilos**: Adicione estilos personalizados em `styles.css`

## 🧹 Removendo o Exemplo Prático

Se você deseja remover o exemplo prático de API de Tarefas após usá-lo como referência, siga estes passos:

1. Execute o script de limpeza:
   ```bash
   python scripts/cleanup_example.py
   ```

2. O script irá remover automaticamente:
   - `src/boilerplate/models/todo.py`
   - `src/boilerplate/services/todo.py`
   - `src/boilerplate/api/v1/endpoints/todos.py`
   - `src/boilerplate/api/v1/api.py`
   - `src/boilerplate/templates/todos.html`
   - `src/boilerplate/static/js/todos.js`
   - `src/boilerplate/static/css/styles.css`
   - Diretórios vazios resultantes

3. Após a execução do script, você precisará fazer as seguintes alterações manuais:
   - Remova as rotas relacionadas ao exemplo do arquivo `main.py`
   - Remova as importações não utilizadas no `main.py`
   - Remova a seção "Exemplo Prático" do `README.md` se desejar
   - Remova a seção "Interface Web" do `README.md`

4. Se estiver usando controle de versão, não se esqueça de fazer commit das alterações:
   ```bash
   git add .
   git commit -m "Remove exemplo prático e interface web"
   ```

5. Dica: Limpe o cache do seu navegador para garantir que as alterações tenham efeito completo.

## 📦 Pré-requisitos

- Python 3.11+
- Docker e Docker Compose (opcional, para desenvolvimento com containers)
- Git

## 🛠️ Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/python-boilerplate.git
   cd python-boilerplate
   ```

2. Crie e ative um ambiente virtual (recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. Instale as dependências:
   ```bash
   pip install -e ".[dev]"
   ```

4. Crie um arquivo `.env` baseado no `.env.example` e configure conforme necessário:
   ```bash
   cp .env.example .env
   ```

## 🚀 Executando localmente

### Sem Docker

1. Inicie o servidor de desenvolvimento:
   ```bash
   uvicorn boilerplate.main:app --reload --port 8010
   ```

2. Acesse a documentação interativa da API em:
   - Swagger UI: http://localhost:8010/docs
   - ReDoc: http://localhost:8010/redoc

### Com Docker

1. Construa e inicie os contêineres:
   ```bash
   docker-compose up --build
   ```

2. Acesse a aplicação em http://localhost:8010

<!-- Seção de testes consolidada no topo (🧪 Testes). Removida duplicação. -->

## 🛠️ Ferramentas de Desenvolvimento

- **Formatação de código**:
  ```bash
  black src/
  isort src/
  ```

- **Verificação de código**:
  ```bash
  flake8 src/
  mypy src/
  ```

- **Atualizar dependências**:
  ```bash
  pip install -U pip
  pip freeze > requirements.txt
  ```

## 📦 Estrutura do Projeto

```
.
├── .github/               # Configurações do GitHub (CI/CD, templates de issues, etc.)
├── docker/                # Arquivos de configuração do Docker
├── docs/                  # Documentação do projeto
├── scripts/               # Scripts úteis para desenvolvimento
├── src/                   # Código-fonte da aplicação
│   └── boilerplate/       # Pacote principal
│       ├── api/           # Rotas da API
│       ├── core/          # Configurações e lógica principal
│       ├── models/        # Modelos de dados
│       ├── services/      # Lógica de negócios
│       ├── utils/         # Utilitários e helpers
│       ├── __init__.py
│       ├── config.py      # Configurações da aplicação
│       └── main.py        # Ponto de entrada da aplicação
├── tests/                 # Testes automatizados
│   ├── integration/       # Testes de integração
│   └── unit/              # Testes unitários
├── .env.example           # Exemplo de variáveis de ambiente
├── .gitignore
├── .dockerignore
├── docker-compose.yml     # Configuração do Docker Compose
├── Dockerfile             # Configuração do Docker
├── pyproject.toml         # Configuração do projeto e dependências
└── README.md              # Este arquivo
```

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Faça commit das suas alterações (`git commit -m 'Add some AmazingFeature'`)
4. Faça push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.

## 📧 Contato

Darcy Junior - [@darcyjunior](https://github.com/darcyjunior)

Link do Projeto: [https://github.com/darcyjunior/python-boilerplate](https://github.com/darcyjunior/python-boilerplate)