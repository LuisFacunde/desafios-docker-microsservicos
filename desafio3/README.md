# Desafio 3: Docker Compose Orquestrando Serviços

## Objetivo

Usar **Docker Compose** para orquestrar e gerenciar três serviços dependentes (`web`, `db`, `cache`), configurando dependências, variáveis de ambiente e comunicação via **rede interna**.

---

## Arquitetura da Solução, Decisões Técnicas e Funcionamento

A solução implementa uma arquitetura de três camadas clássica orquestrada pelo `docker-compose.yml`, simulando um sistema que precisa de uma API, um banco de dados persistente e um cache rápido.

### Componentes

| Serviço | Tecnologia | Função | Acesso |
| :--- | :--- | :--- | :--- |
| **`web`** | Python (FastAPI) | Microsserviço principal, *entrypoint* do sistema. | Porta `8000` (Exposta para o Host). |
| **`db`** | PostgreSQL (15-alpine) | Serviço de Banco de Dados. | Apenas pela **rede interna** (`app_network`). |
| **`cache`** | Redis (7-alpine) | Serviço de Cache de alta velocidade. | Apenas pela **rede interna** (`app_network`). |

### Decisões Técnicas

1.  **Orquestração e Redes**: Utilizamos o `docker-compose.yml` para definir e iniciar todos os serviços simultaneamente. [cite_start]Uma **rede bridge customizada** (`app_network`) é criada automaticamente, o que permite a comunicação por **nomes de serviço** (DNS interno)[cite: 52].
2.  [cite_start]**Configuração de Dependências**: O campo `depends_on: [db, cache]` é configurado no serviço `web`[cite: 52]. Isso garante que os serviços de dados estejam em processo de inicialização antes que a API `web` tente se conectar, prevenindo falhas de *startup*.
3.  [cite_start]**Variáveis de Ambiente**: As credenciais de conexão do PostgreSQL e os *hostnames* internos (ex: `DB_HOST: db`) são passados para a aplicação `web` via `environment`, garantindo boas práticas de configuração[cite: 50].

### Fluxo de Funcionamento

O funcionamento é comprovado quando uma requisição ao Serviço `web` força a comunicação interna:

1.  **Requisição Externa**: O cliente acessa `http://localhost:8000/`.
2.  [cite_start]**Comunicação Inter-serviço**: A aplicação `web` (FastAPI) tenta estabelecer conexões com o `db` e o `cache` usando os nomes dos serviços (`db` e `cache`)[cite: 51].
3.  **Resolução de Nomes**: O Docker resolve esses nomes para os IPs internos dos containers, e a conexão é realizada com sucesso dentro da rede `app_network`.
4.  [cite_start]**Prova Funcional**: A API `web` retorna um JSON indicando o status `Conectado com sucesso` para ambos os serviços, provando que a **comunicação entre os serviços está funcionando**[cite: 56].

---

## Instruções de Execução Passo a Passo

### Pré-requisitos

* Docker e Docker Compose instalados.
* A pasta `desafio3/` deve conter as subpastas `web/` e o arquivo `docker-compose.yml`.

### 1. Subir os Containers

Navegue até o diretório `desafio3/` e inicie a arquitetura. O *build* garante que a imagem do serviço `web` seja criada corretamente.

```bash
docker-compose up --build -d
```

### 2. Testar a Comunicação (Prova do Requisito)

Execute o curl para acessar o endpoint principal. A resposta comprova que o serviço web conseguiu se conectar com sucesso ao db e ao cache.

```Bash
curl http://localhost:8000/
```

**Saída Esperada (Comunicação funcional):**
```Bash
JSON

{
  "web_status": "Serviço Web rodando.",
  "db_check": "Conectado com sucesso ao PostgreSQL.",
  "cache_check": "Conectado com sucesso ao Redis. Valor salvo: YYYY-MM-DD HH:MM:SS" 
}
```

### 3. Limpeza Final
Para parar e remover todos os containers, a rede e o volume de dados (do PostgreSQL):

```Bash
docker-compose down -v
```