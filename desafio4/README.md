# Desafio 4: Microsserviços Independentes

## Objetivo

O objetivo deste desafio é criar dois microsserviços totalmente independentes (cada um com seu próprio Dockerfile e código) e demonstrar a comunicação direta entre eles via **requisições HTTP**, utilizando a rede interna do Docker Compose.

---

## Arquitetura da Solução e Decisões Técnicas

A arquitetura consiste em dois microsserviços Python/FastAPI que se comunicam diretamente através de uma rede bridge customizada.

### Componentes

| Serviço | Função | Porta Interna | Acesso Externo |
| :--- | :--- | :--- | :--- |
| **`users-service` (MS A)** | **Produtor de Dados**. Retorna uma lista estática de usuários (JSON). | `8000` | Não Exposto |
| **`consumer-service` (MS B)** | **Consumidor de Dados**. Faz uma requisição HTTP para o MS A, combina os dados e retorna o resultado. | `8001` | Mapeado para `8001` no host |

### Decisões Técnicas

1.  **Isolamento Total**: Cada microsserviço possui seu próprio `Dockerfile` e seu próprio código-fonte (`app.py`), conforme o requisito de serem executáveis via Docker separadamente.
2.  **Comunicação via Nome do Serviço**: O Serviço B acessa o Serviço A utilizando o **nome do serviço** (`users-service`) no seu URL de requisição (`http://users-service:8000/users`). O Docker Compose gerencia a resolução de DNS dentro da rede.
3.  **Rede Interna Exclusiva**: O Serviço A não tem sua porta (8000) exposta para o host, sendo acessível **apenas** pelo Serviço B na rede interna (`microservice_net`), garantindo o isolamento.
4.  **Uso de Variáveis de Ambiente**: O Microsserviço B utiliza a variável de ambiente `MS_A_HOST` (`users-service`) para construir seu URL de requisição, permitindo que a configuração de rede seja gerenciada pelo `docker-compose.yml`.

---

## Explicação Detalhada do Funcionamento

O fluxo demonstra como o Serviço B orquestra a obtenção e o processamento de dados do Serviço A. 

### Fluxo de Comunicação

1.  **Requisição Inicial**: O cliente externo acessa o endpoint `/status` do **Serviço B** (`http://localhost:8001/status`).
2.  **Requisição HTTP**: O código do Serviço B executa uma requisição GET para `http://users-service:8000/users`.
3.  **Resolução de DNS**: O *driver* de rede do Docker intercepta o nome `users-service` e o resolve para o IP interno do container `ms_a_users_service`.
4.  **Processamento no A**: O Serviço A recebe a requisição, retorna a lista de usuários (JSON) e encerra a conexão.
5.  **Combinação no B**: O Serviço B recebe o JSON, itera sobre a lista e combina a informação original (`nome`, `cadastro`) com uma *string* de status local (`ativo desde... (Processado em B)`).
6.  **Resposta Final**: O Serviço B retorna o JSON com o resultado combinado para o cliente externo, comprovando a comunicação funcional.

---

## Instruções de Execução Passo a Passo

### Pré-requisitos

* Docker e Docker Compose instalados.
* A pasta `desafio4/` deve conter as subpastas `microservice_a/`, `microservice_b/` e o arquivo `docker-compose.yml`.

### 1. Subir os Microsserviços

Navegue até o diretório `desafio4/` e execute:

```bash
docker-compose up --build -d
```

**Resultado esperado:**

* Dois containers (ms_a_users_service e ms_b_consumer_service) serão criados.
* A porta 8001 será mapeada para o Serviço B.

### 2. Testar a Comunicação (Prova do Requisito)

Execute o curl para acessar o Serviço B. A resposta JSON abaixo comprova que o Serviço B consumiu os dados do Serviço A via HTTP e os processou.

```bash
curl http://localhost:8001/status
```

**Saída Esperada (Comunicação HTTP entre microsserviços funcional):**

```bash
{
  "status": "Processamento concluído com sucesso",
  "timestamp_b": "YYYY-MM-DDTHH:MM:SS.000000+00:00",
  "info_combinada": [
    "Usuário João Silva ativo desde 2024-01-10 (Processado em B)",
    "Usuário Maria Santos ativo desde 2024-03-25 (Processado em B)",
    "Usuário Pedro Oliveira ativo desde 2024-05-18 (Processado em B)"
  ]
}
```

### 3. Limpeza Final

Para parar e remover os containers e a rede customizada:

```bash
docker-compose down
```
