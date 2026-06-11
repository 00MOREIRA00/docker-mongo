# Docker Compose do MongoDB local

## O que esse Docker Compose faz?

Esse arquivo `docker-compose.yml` sobe um ambiente local com dois containers:

- um container com o MongoDB;
- um container com o Mongo Express, uma interface web simples para visualizar e administrar o MongoDB pelo navegador.

Na prática, ele permite executar um banco MongoDB local sem precisar instalar o MongoDB diretamente na máquina. Tudo roda em containers Docker, com configuração pronta para desenvolvimento e testes.

---

## Estrutura geral

O Compose está dividido em duas partes principais:

- `services`: define os containers que serão executados;
- `volumes`: define o volume usado para persistir os dados do MongoDB.

O arquivo possui dois serviços:

- `mongo`;
- `mongo-express`.

E um volume:

- `mongodb_data`.

---

## Serviço mongo

O serviço `mongo` é responsável por subir o banco de dados MongoDB.

```yaml
mongo:
  image: mongo:7
  container_name: mongodb-local
  restart: unless-stopped
  ports:
    - "27017:27017"
  environment:
    MONGO_INITDB_ROOT_USERNAME: admin
    MONGO_INITDB_ROOT_PASSWORD: admin123
    MONGO_INITDB_DATABASE: app_db
  volumes:
    - mongodb_data:/data/db
```

### Imagem utilizada

```yaml
image: mongo:7
```

Essa linha informa que o container será criado a partir da imagem oficial do MongoDB na versão 7.

Usar uma versão fixa, como `mongo:7`, é melhor do que usar apenas `latest`, porque evita mudanças inesperadas quando uma nova versão do MongoDB for publicada.

### Nome do container

```yaml
container_name: mongodb-local
```

Define o nome do container como `mongodb-local`.

Isso facilita identificar o container quando você rodar comandos como:

```bash
docker ps
```

### Política de reinicialização

```yaml
restart: unless-stopped
```

Essa configuração faz o container reiniciar automaticamente caso ele pare por erro ou caso o Docker seja reiniciado.

Ele só não será reiniciado automaticamente se for parado manualmente pelo usuário.

### Porta do MongoDB

```yaml
ports:
  - "27017:27017"
```

Essa configuração expõe a porta padrão do MongoDB.

O primeiro `27017` representa a porta da máquina local. O segundo `27017` representa a porta dentro do container.

Com isso, aplicações rodando na sua máquina podem acessar o MongoDB usando:

```text
localhost:27017
```

### Variáveis de ambiente

```yaml
environment:
  MONGO_INITDB_ROOT_USERNAME: admin
  MONGO_INITDB_ROOT_PASSWORD: admin123
  MONGO_INITDB_DATABASE: app_db
```

Essas variáveis configuram o usuário inicial, a senha e o banco criado na inicialização do MongoDB.

Neste Compose:

- usuário administrador: `admin`;
- senha: `admin123`;
- banco inicial: `app_db`.

O usuário criado é um usuário root do MongoDB. Ele deve ser usado com cuidado em ambientes reais.

### Volume de dados

```yaml
volumes:
  - mongodb_data:/data/db
```

Essa linha conecta o volume `mongodb_data` ao diretório `/data/db` dentro do container.

O diretório `/data/db` é onde o MongoDB armazena seus dados.

Isso significa que, mesmo se o container for removido e criado novamente, os dados continuarão salvos no volume Docker, desde que o volume não seja apagado.

---

## Serviço mongo-express

O serviço `mongo-express` sobe uma interface web para administrar o MongoDB.

```yaml
mongo-express:
  image: mongo-express:latest
  container_name: mongodb-express-local
  restart: unless-stopped
  ports:
    - "8081:8081"
  environment:
    ME_CONFIG_MONGODB_URL: mongodb://admin:admin123@mongo:27017/?authSource=admin
    ME_CONFIG_BASICAUTH_USERNAME: admin
    ME_CONFIG_BASICAUTH_PASSWORD: admin123
  depends_on:
    - mongo
```

### Imagem utilizada

```yaml
image: mongo-express:latest
```

Essa linha usa a imagem do Mongo Express.

O Mongo Express é uma ferramenta web leve para visualizar bancos, coleções e documentos do MongoDB.

### Nome do container

```yaml
container_name: mongodb-express-local
```

Define o nome do container como `mongodb-express-local`.

Esse nome ajuda a identificar rapidamente que o container é a interface web do MongoDB local.

### Porta do Mongo Express

```yaml
ports:
  - "8081:8081"
```

Essa configuração expõe a interface web na porta `8081`.

Depois que o ambiente estiver rodando, o Mongo Express pode ser acessado pelo navegador em:

```text
http://localhost:8081
```

### Conexão com o MongoDB

```yaml
ME_CONFIG_MONGODB_URL: mongodb://admin:admin123@mongo:27017/?authSource=admin
```

Essa variável informa ao Mongo Express como se conectar ao MongoDB.

A URL possui algumas partes importantes:

- `admin`: usuário do MongoDB;
- `admin123`: senha do MongoDB;
- `mongo`: nome do serviço do MongoDB dentro da rede do Docker Compose;
- `27017`: porta interna do MongoDB;
- `authSource=admin`: indica que a autenticação deve ser feita no banco `admin`.

Dentro do Docker Compose, os serviços conseguem se comunicar pelo nome definido no arquivo. Por isso o Mongo Express usa `mongo` em vez de `localhost`.

### Autenticação do Mongo Express

```yaml
ME_CONFIG_BASICAUTH_USERNAME: admin
ME_CONFIG_BASICAUTH_PASSWORD: admin123
```

Essas variáveis configuram o login para acessar a interface web do Mongo Express.

Neste projeto:

- usuário da interface: `admin`;
- senha da interface: `admin123`.

Esse login protege o acesso ao painel web.

### Dependência entre serviços

```yaml
depends_on:
  - mongo
```

Essa configuração informa que o serviço `mongo-express` depende do serviço `mongo`.

Assim, o Docker Compose tenta iniciar o MongoDB antes de iniciar o Mongo Express.

É importante entender que `depends_on` controla a ordem de inicialização, mas não garante que o MongoDB já esteja totalmente pronto para receber conexões no primeiro segundo.

---

## Volume mongodb_data

```yaml
volumes:
  mongodb_data:
```

Esse trecho cria um volume Docker chamado `mongodb_data`.

Ele é usado para guardar os dados do banco MongoDB fora do ciclo de vida do container.

Sem esse volume, ao remover o container, os dados poderiam ser perdidos. Com o volume, os dados permanecem salvos enquanto o volume existir.

---

## Como subir o ambiente

Para iniciar os containers, execute:

```bash
docker compose up -d
```

O parâmetro `-d` executa os containers em segundo plano.

Depois disso, é possível verificar se tudo está rodando com:

```bash
docker ps
```

---

## Como acessar

### MongoDB

Para conectar uma aplicação local ao MongoDB, use:

```text
mongodb://admin:admin123@localhost:27017/app_db?authSource=admin
```

### Mongo Express

Para acessar a interface web, abra:

```text
http://localhost:8081
```

Login:

- usuário: `admin`;
- senha: `admin123`.

---

## Como parar o ambiente

Para parar os containers sem remover os dados, execute:

```bash
docker compose down
```

Esse comando remove os containers e a rede criada pelo Compose, mas mantém o volume `mongodb_data`.

---

## Como apagar os dados

Se quiser remover também os dados armazenados no volume, execute:

```bash
docker compose down -v
```

O parâmetro `-v` remove os volumes associados ao Compose.

Use esse comando com cuidado, porque ele apaga os dados persistidos do MongoDB.

---

## Pontos de atenção

Esse Compose é adequado para ambiente local de desenvolvimento e estudos.

Alguns cuidados importantes:

- as credenciais estão expostas diretamente no arquivo;
- a senha `admin123` é simples e não deve ser usada em produção;
- a porta `27017` fica disponível na máquina local;
- o Mongo Express também fica exposto na porta `8081`;
- `mongo-express:latest` pode mudar de versão sem aviso.

Para um ambiente de produção, o ideal seria usar senhas fortes, variáveis de ambiente externas, controle de rede, versões fixas das imagens e políticas mais rígidas de segurança.

---

## Resumindo

Esse `docker-compose.yml` cria um ambiente MongoDB local completo, com banco de dados persistente e painel web de administração.

O serviço `mongo` executa o banco de dados, enquanto o serviço `mongo-express` fornece uma interface visual para consultar e administrar os dados.

É uma configuração simples, útil para desenvolvimento, testes e aprendizado com MongoDB em containers.
