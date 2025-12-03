# Desafio 1: Cliente e Servidor com Docker Compose

## Objetivo

Montar uma aplicação simples composta por um **servidor** (FastAPI) e um **cliente** que realiza chamadas periódicas ao servidor, ambos orquestrados via Docker Compose.

---

## Descrição da Solução, Arquitetura e Decisões Técnicas

A solução contém dois containers conectados por uma rede Docker definida no `docker-compose.yml`:

### Arquitetura

| Serviço | Tecnologia | Função | Acesso |
| :--- | :--- | :--- | :--- |
| **`servidor`** | Python (FastAPI) | Servidor HTTP que responde em `/` com mensagem, timestamp e IP do cliente. | Porta `8080` mapeada para o host (`8080:8080`). |
| **`cliente`** | Shell script (curl) em container | Cliente que periodicamente chama o servidor via nome de serviço Docker (`servidor`). | Executa internamente; não precisa de porta exposta. |

### Decisões Técnicas

1. **FastAPI no servidor**: fornece um endpoint simples em `/` que devolve JSON com `mensagem`, `timestamp` e o `ip_cliente_requisitante`.
2. **Cliente como script**: o `client/script.sh` usa `curl` em loop para demonstrar chamadas periódicas e logs.
3. **Comunicação por nome de serviço**: o cliente usa a URL `http://servidor:8080` para se conectar, aproveitando o DNS interno do Docker Compose.
4. **Orquestração com Docker Compose**: o `docker-compose.yml` define os serviços e a rede, permitindo levantar tudo com um único comando.

---

## Explicação Detalhada do Funcionamento e Fluxos

### Fluxo de Requisição (Exemplo: cliente → servidor)

1. O container `cliente` executa `script.sh`, que faz `curl` para `http://servidor:8080` repetidamente.
2. O Docker resolve `servidor` para o IP do container `servidor` na rede interna.
3. O `servidor` (FastAPI) recebe a requisição, registra o IP do cliente e retorna um JSON contendo `mensagem`, `timestamp` e `ip_cliente_requisitante`.
4. O `cliente` exibe o JSON recebido no seu output (logs do container), demonstrando comunicação interna entre containers.

---

## Instruções de Execução Passo a Passo

### Pré-requisitos

* Docker e Docker Compose instalados.
* Estar no diretório que contém `docker-compose.yml` (a raiz `desafio1/`).

### 1. Subir os containers

```bash
cd "$(pwd | sed 's/\/desafios-docker-microsservicos.*//')/desafios-docker-microsservicos/desafio1" || cd desafio1
docker-compose up --build -d
```

Resultado esperado:

- Dois containers serão iniciados: `servidor_web` (expondo a porta 8080) e `cliente_requisitante`.

### 2. Verificar se o servidor está respondendo pelo host

```bash
curl http://localhost:8080/
```

Saída Esperada (exemplo):

```json
{
  "mensagem": "Olá do Servidor FastAPI!",
  "timestamp": "2025-12-02 12:34:56",
  "ip_cliente_requisitante": "172.18.0.5"
}
```

Observação: o `timestamp` e o `ip_cliente_requisitante` variam conforme a execução.

### 3. Ver os logs do cliente (requisições periódicas)

```bash
docker logs -f cliente_requisitante
```

Você verá repetidas chamadas e as respostas JSON do servidor sendo exibidas.

### 4. Limpeza

Para parar e remover containers e a rede criada:

```bash
docker-compose down
```
