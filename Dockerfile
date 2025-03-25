# Adicionando dependências no Dockerfile
# Criação do ambiente e instalação de pacotes necessários
FROM python:3.13

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

RUN echo "fastapi\nuvicorn\nsqlalchemy\nalembic\npymongo\nsqlite" > requirements.txt
