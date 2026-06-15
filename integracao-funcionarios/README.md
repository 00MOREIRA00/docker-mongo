# Integracao de Funcionarios

API FastAPI para controle cadastral de funcionarios de uma empresa.

## Requisitos

- Python compativel com o projeto
- uv
- Docker
- Docker Compose

## Subir o MongoDB

Na raiz do repositorio, execute:

```bash
docker compose up -d
```

Esse comando sobe:

- MongoDB em `localhost:27017`
- Mongo Express em `http://localhost:8081`

Credenciais locais:

```text
Usuario: admin
Senha: admin123
Banco: app_db
```

## Rodar a API

Entre na pasta do microservico:

```bash
cd integracao-funcionarios
```

Instale/sincronize as dependencias:

```bash
uv sync
```

Suba a API em modo desenvolvimento:

```bash
uv run uvicorn main:app --reload
```

A API ficara disponivel em:

```text
http://127.0.0.1:8000
```

## Documentacao interativa

Com a API rodando, acesse:

```text
http://127.0.0.1:8000/docs
```

## Health check

Endpoint inicial:

```http
GET /
```

Resposta esperada:

```json
{
  "mensage": "Is up"
}
```

## Parar o ambiente local

Na raiz do repositorio, execute:

```bash
docker compose down
```
