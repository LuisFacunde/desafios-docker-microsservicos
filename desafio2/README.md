## Desafio 2: Volumes e Persistência

### Objetivo

Demonstrar a **persistência de dados** de um banco de dados PostgreSQL utilizando um **Volume Nomeado** do Docker.

### Arquitetura da Solução

- **Serviço `db` (PostgreSQL)**  
  - Imagem: `postgres:15-alpine`
  - Função: banco de dados responsável por armazenar os dados da aplicação.

- **Volume Nomeado `postgres_data`**  
  - Tipo: Volume gerenciado pelo Docker.  
  - Finalidade: garantir que os dados do banco persistam mesmo após a remoção do container.

- **Mapeamento de Diretório**  
  - Diretório interno do container: `/var/lib/postgresql/data`  
  - É o diretório padrão onde o PostgreSQL armazena fisicamente os dados.  
  - Esse diretório é montado no volume nomeado `postgres_data`.

### Decisões Técnicas

- **Uso de `docker-compose.yml`**  
  - Definição declarativa da arquitetura.  
  - Facilita a reprodutibilidade do ambiente e a orquestração do serviço de forma simples (`docker-compose up/down`).

- **Diretório de Dados**  
  - O volume `postgres_data` é mapeado para `/var/lib/postgresql/data`.  
  - Isso garante que todos os arquivos de dados do PostgreSQL sejam escritos no volume persistente.

---

### Funcionamento da Persistência

Fluxo para demonstrar a persistência:

1. **Criação do Volume e do Container**
   - Ao executar `docker-compose up`, o Docker:
     - Verifica se o volume nomeado `postgres_data` existe.  
     - Caso não exista, cria o volume no sistema de arquivos do host.  
     - Sobe o container do PostgreSQL e monta o volume em `/var/lib/postgresql/data`.

2. **Criação e Armazenamento de Dados**
   - Dentro do banco, é criado um registro de teste.  
   - Esse registro é gravado fisicamente no volume `postgres_data`, que fica fora do ciclo de vida do container.

3. **Remoção do Container (mantendo o volume)**
   - Ao executar `docker-compose down`, o container é parado e removido.  
   - O volume nomeado `postgres_data` não é apagado e permanece com todos os dados.

4. **Recriação do Container e Prova da Persistência**
   - Ao executar `docker-compose up -d` novamente:
     - Um novo container é criado.  
     - O Docker monta o mesmo volume existente `postgres_data` no novo container.  
     - O PostgreSQL lê os dados do volume e o registro criado anteriormente continua disponível.
   - Isso comprova que os dados sobrevivem à destruição e recriação do container.

---

### Pré-requisitos

- Docker instalado  
- Docker Compose instalado  
- Porta do PostgreSQL (normalmente `5432`) disponível na máquina host

---

### Passo a Passo de Execução

#### 1. Subir o serviço

No diretório `desafio2/`, execute:

```bash
docker-compose up -d
```

**Resultado esperado:**
- O serviço PostgreSQL será iniciado.  
- O volume nomeado `postgres_data` será criado automaticamente (caso ainda não exista).

---

#### 2. Criar e salvar dados no banco

Acesse o container do PostgreSQL e o cliente `psql`:

```bash
docker exec -it desafio2_postgres_db psql -U user -d persisted_data
```

Dentro do `psql`, execute em ordem um de cada vez:

```sql
CREATE TABLE pessoas (id SERIAL PRIMARY KEY, nome VARCHAR(100));

INSERT INTO pessoas (nome) VALUES ('Luis Facunde');

SELECT * FROM pessoas;
```

Saída esperada:

```text
 id |    nome
----+--------------
  1 | Luis Facunde
(1 row)
```

Para sair do `psql`:

```text
\q
```

---

#### 3. Remover o container (mantendo o volume)

Este passo simula uma falha, atualização ou recriação do serviço.

```bash
docker-compose down
```

**Resultado esperado:**
- O container `desafio2_postgres_db` será removido.  
- O volume `postgres_data` continuará existindo com os dados gravados.

---

#### 4. Recriar o container e comprovar a persistência

Suba novamente o serviço:

```bash
docker-compose up -d
```

Acesse o NOVO container e o banco:

```bash
docker exec -it desafio2_postgres_db psql -U user -d persisted_data
```

Dentro do `psql`, consulte os dados:

```sql
SELECT * FROM pessoas;
```

Saída esperada (prova de persistência):

```text
 id |    nome
----+--------------
  1 | Luis Facunde
(1 row)
```

Saia do `psql`:

```text
\q
```

---

#### 5. Limpeza final (opcional)

Para remover containers, rede e também o volume (apagando os dados persistidos):

```bash
docker-compose down -v
```

Após esse comando, o volume `postgres_data` será removido e os dados serão perdidos, deixando o ambiente limpo para um novo teste.