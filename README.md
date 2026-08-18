# Email Worker Compose

Aplicação distribuída de processamento de mensagens utilizando **Docker Compose**, **Python**, **PostgreSQL**, **Redis** e **Nginx**.

O projeto foi desenvolvido durante os estudos de Docker com o objetivo de praticar a criação e integração de múltiplos containers, comunicação entre serviços, persistência de dados, processamento assíncrono por filas e escalabilidade horizontal de workers.

## 📌 Sobre o projeto

A aplicação simula um sistema de envio de e-mails.

Quando uma mensagem é recebida pela aplicação:

1. Os dados da mensagem são registrados no PostgreSQL.
2. A mensagem é adicionada a uma fila no Redis.
3. Um worker consome a mensagem da fila.
4. O worker simula o processamento/envio do e-mail.
5. Múltiplos workers podem processar mensagens simultaneamente.

A arquitetura foi organizada em diferentes serviços Docker, permitindo que cada componente tenha uma responsabilidade específica.

## 🏗️ Arquitetura

```text
                         ┌───────────────┐
                         │    Cliente    │
                         └───────┬───────┘
                                 │
                                 ▼
                         ┌───────────────┐
                         │     Nginx     │
                         │ Reverse Proxy │
                         └───────┬───────┘
                                 │
                                 ▼
                         ┌───────────────┐
                         │      App      │
                         │ Python/Bottle │
                         └───────┬───────┘
                                 │
                  ┌──────────────┴──────────────┐
                  │                             │
                  ▼                             ▼
          ┌───────────────┐              ┌───────────────┐
          │  PostgreSQL   │              │     Redis     │
          │  Persistência │              │     Fila      │
          └───────────────┘              └───────┬───────┘
                                                 │
                                    ┌────────────┼────────────┐
                                    ▼            ▼            ▼
                              ┌──────────┐ ┌──────────┐ ┌──────────┐
                              │ Worker 1 │ │ Worker 2 │ │ Worker 3 │
                              └──────────┘ └──────────┘ └──────────┘
```

## 🐳 Serviços

### Nginx

Responsável pelo acesso HTTP e pelo funcionamento como **proxy reverso** para a aplicação.

### App

Aplicação desenvolvida em Python utilizando o framework Bottle.

Responsabilidades:

* Receber as mensagens;
* Registrar mensagens no PostgreSQL;
* Enfileirar mensagens no Redis;
* Disponibilizar endpoints HTTP para envio.

### PostgreSQL

Banco de dados responsável pela persistência das mensagens recebidas.

Os dados são armazenados através de um volume Docker:

```text
dados:/var/lib/postgresql/data
```

### Redis

Utilizado como sistema de filas.

A aplicação adiciona mensagens à fila:

```text
sender
```

Os workers retiram as mensagens dessa fila para processamento.

### Workers

Processos responsáveis pelo consumo da fila e processamento das mensagens.

A arquitetura permite executar múltiplas instâncias dos workers, possibilitando **escala horizontal**.

## 📁 Estrutura do projeto

```text
email-worker-compose/
├── app/
│   ├── Dockerfile
│   ├── app.sh
│   ├── requirements.txt
│   └── sender.py
├── nginx/
│   └── default.config
├── scripts/
│   ├── cheack.sql
│   └── init.sql
├── web/
│   └── index.html
├── worker/
│   ├── Dockerfile
│   ├── app.sh
│   ├── requirements.txt
│   └── worker.py
├── comandos.txt
├── docker-compose.yml
├── docker-compose-override.yml
├── run_workers.sh
├── .env.example
└── .gitignore
```

## ⚙️ Tecnologias utilizadas

* Docker
* Docker Compose
* Python
* Bottle
* PostgreSQL
* Redis
* Nginx
* Shell Script
* Git/GitHub

## 🚀 Como executar

Clone o repositório:

```bash
git clone git@github.com:Eduardbo/email-worker-compose.git
cd email-worker-compose
```

Crie o arquivo de variáveis de ambiente:

```bash
cp .env.example .env
```

Edite o arquivo `.env` e defina as configurações necessárias.

Depois inicie os serviços:

```bash
docker compose up -d
```

Verifique os containers:

```bash
docker compose ps
```

Visualize os logs:

```bash
docker compose logs -f
```

## 📬 Processamento das mensagens

A aplicação recebe uma requisição contendo o assunto e o conteúdo da mensagem.

A mensagem é então:

```text
Requisição HTTP
      ↓
    Nginx
      ↓
     App
      ↓
 PostgreSQL
      ↓
    Redis
      ↓
    Worker
      ↓
 Processamento
```

O Redis desacopla o recebimento da mensagem do processamento realizado pelos workers.

Isso permite que a aplicação continue recebendo novas mensagens mesmo quando o processamento de uma mensagem individual demora mais tempo.

## 📈 Escalabilidade

Um dos objetivos do projeto foi praticar a execução de múltiplas instâncias dos workers.

Exemplo:

```bash
docker compose up -d --scale workers=3
```

Com isso, múltiplos workers podem consumir mensagens da mesma fila Redis.

```text
             Redis
               │
       ┌───────┼───────┐
       ▼       ▼       ▼
    Worker 1 Worker 2 Worker 3
```

Esse modelo permite aumentar a capacidade de processamento adicionando novas instâncias.

## 🌐 Redes Docker

O projeto utiliza redes separadas para organizar a comunicação entre os serviços:

```text
banco
web
fila
```

Isso permite controlar quais serviços precisam se comunicar entre si.

Exemplo:

```text
App ─────── PostgreSQL
 │
 ├───────── Redis
 │
 └───────── Nginx
```

Os workers participam da rede responsável pela comunicação com o Redis.

## 🔐 Variáveis de ambiente

As configurações sensíveis não são armazenadas diretamente no código.

O projeto utiliza variáveis de ambiente, como:

```text
POSTGRES_PASSWORD
DB_PASSWORD
DB_NAME
DB_USER
DB_HOST
REDIS_HOST
```

O arquivo `.env` deve permanecer apenas no ambiente local e está incluído no `.gitignore`.

Para facilitar a configuração de novos ambientes, o projeto possui:

```text
.env.example
```

## 📚 Conceitos praticados

Durante o desenvolvimento foram praticados conceitos de:

* Criação e gerenciamento de containers;
* Construção de imagens com Dockerfile;
* Docker Compose;
* Bind mounts;
* Volumes Docker;
* Redes Docker;
* Comunicação entre containers;
* PostgreSQL em container;
* Redis;
* Filas de mensagens;
* Processamento assíncrono;
* Workers;
* Escalabilidade horizontal;
* Nginx como proxy reverso;
* Variáveis de ambiente;
* Configuração baseada em ambiente;
* Docker Compose Override;
* Logs de containers;
* Shell Script;
* Versionamento com Git.

## 🎯 Objetivo de aprendizado

O principal objetivo deste projeto foi consolidar conhecimentos de **containerização e arquitetura de aplicações distribuídas**, passando desde a criação de containers individuais até a integração de múltiplos serviços através do Docker Compose.

O projeto também serviu para compreender, na prática, conceitos como **filas de mensagens, processamento assíncrono, separação de responsabilidades e escalabilidade horizontal**.

## 📌 Observação

Este projeto foi desenvolvido como parte dos estudos práticos de Docker e posteriormente organizado para documentação e portfólio.

## 👨‍💻 Autor

**Eduardo Braga**

Estudante de Ciência da Computação com interesse em infraestrutura, segurança da informação, sistemas distribuídos e tecnologias de containerização.
