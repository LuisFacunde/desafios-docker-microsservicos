# Desafio 5: Microsserviços com API Gateway

## Objetivo

Criar uma arquitetura de microsserviços centralizada por um **API Gateway**. O Gateway atua como ponto único de entrada (Single Point of Entry) para o cliente externo, orquestrando as chamadas para os microsserviços de *backend* (`users-service` e `orders-service`) através de uma rede interna.

---

## Descrição da Solução, Arquitetura e Decisões Técnicas

A solução implementa três serviços em containers, todos interligados por uma rede Docker customizada, usando FastAPI para as APIs e Docker Compose para a orquestração.

### Arquitetura 

![API Gateway Architecture](./docs/gateway-architecture.png)


A arquitetura de Gateway consiste em:

| Serviço | Tecnologia | Função | Acesso |
| :--- | :--- | :--- | :--- |
| **`api-gateway`** | Python (FastAPI Proxy) | **Ponto Único de Entrada**. Roteia as requisições `/users` e `/orders` para os serviços internos. | Porta `8080` (Exposta para o Host). |
| **`users-service`** | Python (FastAPI) | Microsserviço de **Dados de Usuários**. | Apenas pela **rede interna** (`gateway_net`). |
| **`orders-service`** | Python (FastAPI) | Microsserviço de **Dados de Pedidos**. | Apenas pela **rede interna** (`gateway_net`). |

### Decisões Técnicas

1.  **Gateway como Proxy Reverso**: O `api-gateway` é um microsserviço que usa a biblioteca `requests` para se comportar como um proxy reverso, encaminhando requisições baseadas no caminho (`/users` ou `/orders`).
2.  **Isolamento de Backend**: Os microsserviços de `users` e `orders` não têm suas portas expostas ao host, sendo acessíveis **apenas** pelo `api-gateway` via rede interna (`gateway_net`).
3.  **Comunicação por Nome**: O Gateway acessa os *backends* utilizando seus **nomes de serviço** definidos no Compose (`users-service` e `orders-service`), tirando proveito do DNS interno do Docker.
4.  **Orquestração Completa**: O `docker-compose.yml` define os três serviços, a rede customizada e as dependências (`depends_on`), garantindo que a arquitetura suba de forma correta e previsível.

---

## Explicação Detalhada do Funcionamento e Fluxos

O principal fluxo de funcionamento demonstra a orquestração e a separação de responsabilidades.

### Fluxo de Requisição (Exemplo: `/users`)

1.  **Requisição do Cliente**: O cliente externo faz uma requisição para `http://localhost:8080/users`.
2.  **Roteamento no Gateway**: O `api-gateway` recebe a requisição no *endpoint* `/users` e executa a lógica de *proxy*.
3.  **Chamada Interna**: O Gateway cria uma nova requisição HTTP para o endereço interno `http://users-service:8000/api/v1/users`.
    * O nome `users-service` é resolvido pelo Docker para o IP do container correspondente.
4.  **Processamento no Backend**: O `users-service` processa a requisição e retorna os dados de usuários (JSON) para o Gateway.
5.  **Resposta Final**: O Gateway recebe os dados do *backend* e os repassa, sem modificação, de volta para o cliente externo.

Este fluxo comprova que o **Gateway é o ponto único de entrada** e que a **integração correta** entre os serviços está funcionando.

---

## Instruções de Execução Passo a Passo

### Pré-requisitos

* Docker e Docker Compose instalados.
* A pasta `desafio5/` deve conter as três pastas de serviço e o arquivo `docker-compose.yml`.

### 1. Subir a Arquitetura Completa

Navegue até o diretório `desafio5/` e inicie todos os serviços:

```bash
docker-compose up --build -d
```

Resultado esperado:

Três containers (`api_gateway_service`, `ms_users`, `ms_orders`) serão iniciados.

Apenas a porta `8080` do Gateway será mapeada para o host.

### 2. Testar o Roteamento para Usuários
Execute o curl para acessar o endpoint `/users` através do Gateway (porta 8080):

```bash
curl http://localhost:8080/users
```

Saída Esperada (Comprova que o Gateway acessou o users-service):

```json
[{"id": 101, "name": "Luis", "service": "Users"}, {"id": 102, "name": "Facunde", "service": "Users"}]
```

### 3. Testar o Roteamento para Pedidos
Execute o curl para acessar o endpoint `/orders` através do Gateway (porta 8080):

```bash
curl http://localhost:8080/orders
```

Saída Esperada (Comprova que o Gateway acessou o orders-service):

```json
[{"order_id": "O001", "item": "Laptop", "service": "Orders"}, {"order_id": "O002", "item": "Mouse", "service": "Orders"}]
```

### 4. Limpeza Final
Para remover todos os containers e a rede customizada:

```bash
docker-compose down
```
