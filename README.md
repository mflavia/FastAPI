# FastAPI Products API 🚀

API para gerenciamento de produtos, construída com FastAPI, SQLAlchemy e MongoDB para logs de visualização.

## 🛠 Tecnologias Utilizadas

- **FastAPI** - Framework web para APIs rápidas
- **SQLAlchemy** - ORM para interação com SQLite
- **Alembic** - Gerenciamento de migrações do banco de dados
- **MongoDB** - Armazenamento de logs de visualização
- **Docker** - Contêineres para ambiente de desenvolvimento

## 📦 Configuração e Execução

### 📌 Pré-requisitos

- **Docker e Docker Compose** instalados
- **Python 3.10+** (se for rodar fora do Docker)

### 🚀 Rodando com Docker

1. Clone o repositório:

   ```bash
   git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
   cd SEU_REPOSITORIO

2. Suba os containers
   ```bash
   docker-compose up --build


3. Acesse a API do navegador
   ```
   http://localhost:8000/docs


📌 Rotas da API
| Método  | Rota             | Descrição                 |
|---------|-----------------|---------------------------|
| `POST`  | `/products/`     | Criar um novo produto    |
| `GET`   | `/products/`     | Listar todos os produtos |
| `GET`   | `/products/{id}` | Obter um produto por ID  |
| `PUT`   | `/products/{id}` | Atualizar um produto     |
| `DELETE`| `/products/{id}` | Remover um produto       |

