# Integracao de Funcionarios

## Caso de uso

Este microservico sera responsavel pelo controle cadastral de funcionarios de uma empresa.

A API deve permitir cadastrar, consultar, atualizar e inativar funcionarios armazenados em um banco MongoDB. Outros sistemas internos poderao consumir esse microservico para validar se um funcionario existe, se esta ativo e quais sao seus dados basicos de cadastro.

## Objetivo

Centralizar os dados principais dos funcionarios em uma API propria, simples e independente, usando MongoDB como banco de dados.

Esse servico pode ser usado por sistemas como:

- sistema de RH;
- sistema de folha de pagamento;
- sistema de ponto;
- controle de acesso;
- dashboards administrativos;
- outros microservicos internos.

## Entidade principal

### Funcionario

Exemplo de documento salvo no MongoDB:

```json
{
  "nome": "Ana Souza",
  "documento": "12345678900",
  "email": "ana.souza@empresa.com",
  "cargo": "Desenvolvedora Backend",
  "departamento": "Tecnologia",
  "data_admissao": "2026-06-15",
  "ativo": true
}
```

## Regras de negocio

- Todo funcionario deve possuir `nome` e `documento`.
- O campo `documento` deve ser unico.
- A busca de funcionarios deve permitir pesquisar por `documento` ou por `nome`.
- A busca por `documento` deve retornar o funcionario exato quando encontrado.
- A busca por `nome` pode retornar um ou mais funcionarios com nomes parecidos.
- Um funcionario inativo deve continuar salvo no banco, mas com `ativo` igual a `false`.
- A remocao fisica do funcionario deve ser evitada no fluxo principal.

## Endpoints sugeridos

### Criar funcionario

```http
POST /funcionarios
```

Cria um novo funcionario no MongoDB.

Exemplo de entrada:

```json
{
  "nome": "Ana Souza",
  "documento": "12345678900",
  "email": "ana.souza@empresa.com",
  "cargo": "Desenvolvedora Backend",
  "departamento": "Tecnologia",
  "data_admissao": "2026-06-15"
}
```

### Listar funcionarios

```http
GET /funcionarios
```

Retorna os funcionarios cadastrados.

### Buscar funcionario por documento ou nome

```http
GET /funcionarios/buscar?documento=12345678900
```

Busca um funcionario pelo documento.

```http
GET /funcionarios/buscar?nome=ana
```

Busca funcionarios pelo nome.

Regras da busca:

- se `documento` for informado, a API deve priorizar a busca por documento;
- se `nome` for informado, a API deve buscar funcionarios cujo nome contenha o texto enviado;
- se nenhum parametro for informado, a API deve retornar erro de requisicao invalida.

### Buscar funcionario por ID

```http
GET /funcionarios/{id}
```

Retorna um funcionario especifico pelo identificador do MongoDB.

### Atualizar funcionario

```http
PUT /funcionarios/{id}
```

Atualiza os dados cadastrais de um funcionario.

### Inativar funcionario

```http
PATCH /funcionarios/{id}/inativar
```

Marca o funcionario como inativo.

Exemplo de alteracao no documento:

```json
{
  "ativo": false
}
```

## Fluxo principal

1. O sistema de RH envia os dados de um novo funcionario para `POST /funcionarios`.
2. A API valida se ja existe funcionario com o mesmo `documento`.
3. Se nao existir, a API salva o funcionario no MongoDB.
4. Outros sistemas podem consultar o funcionario usando `GET /funcionarios/buscar?documento=...`.
5. Usuarios administrativos tambem podem localizar funcionarios pelo nome usando `GET /funcionarios/buscar?nome=...`.
6. Quando o funcionario sai da empresa, a API recebe `PATCH /funcionarios/{id}/inativar`.
7. O funcionario permanece no banco para historico, mas deixa de ser considerado ativo.

## Nome do banco e colecao

Sugestao inicial:

```text
Banco: app_db
Colecao: funcionarios
```
