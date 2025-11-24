# Trabalho Final — Banco de Dados (Etapas selecionadas)

Este diretório contém os artefatos criados a partir das instruções das etapas do trabalho final.

Arquivos adicionados:
- `requirements.txt` — dependências necessárias (neo4j, redis, psycopg2-binary)
- `neo4j_demo.py` — exemplo de conexão e criação simples de nó no Neo4j
- `db_crud_demo.py` — exemplo de CRUD para Redis e PostgreSQL

Como reproduzir (local):

1. Criar e ativar venv (no Linux/macOS):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Instalar dependências:

```bash
pip install -r "./requirements.txt"
```

3. Configurar variáveis de ambiente necessárias:

- Para o `neo4j_demo.py`:
  - `NEO4J_URI` (ex: bolt://localhost:7687)
  - `NEO4J_USER`
  - `NEO4J_PASSWORD`

- Para o `db_crud_demo.py` (Redis):
  - `REDIS_HOST` (opcional, default localhost)
  - `REDIS_PORT` (opcional, default 6379)
  - `REDIS_DB` (opcional, default 0)

- Para o `db_crud_demo.py` (PostgreSQL):
  - `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`

4. Executar os exemplos:

```bash
python3 neo4j_demo.py
python3 db_crud_demo.py
```

Observações e limitações:
- Não iniciamos nem configuramos uma instância do Neo4j, Redis ou PostgreSQL neste repositório; os scripts assumem que os serviços já estão acessíveis nas URIs/hosts configurados.
- Os exemplos são minimalistas e destinados a demonstração. Em produção, trate conexões, retries, timeouts, e credenciais com mais cuidado.

---

Documentação gerada por assistente de IA (pergunta pedida na etapa 1)

Pergunta: "Quais são os métodos da classe driver usados na biblioteca neo4j em Python? Dê exemplos."

Resumo das operações/métodos úteis (biblioteca neo4j Python):

- GraphDatabase.driver(uri, auth=...)
  - Cria um driver (objetos de cliente) para se conectar ao banco.
  - Exemplo: driver = GraphDatabase.driver("bolt://localhost:7687", auth=("user","pwd"))

- driver.session()
  - Abre uma sessão para executar queries.
  - Pode-se usar em bloco with: with driver.session() as session: session.run(...)

- session.run(cypher_query, **params)
  - Executa uma query Cypher e retorna um iterador de registros.
  - Exemplo: result = session.run("MATCH (n) RETURN n LIMIT 10")

- session.execute_write(func, *args, **kwargs)
  - Executa uma função de escrita dentro de uma transação, garantindo retry quando apropriado.
  - Exemplo: session.execute_write(lambda tx: tx.run("CREATE (p:Person {name:$name})", name="Ana"))

- session.execute_read(func, *args, **kwargs)
  - Executa uma função de leitura dentro de uma transação, separando intenção de leitura/escrita.

- driver.close()
  - Fecha o driver e libera recursos de conexão.

- Transações explícitas: session.begin_transaction(), tx.run(...), tx.commit(), tx.rollback()

Exemplo curto (pseudocódigo):

```py
from neo4j import GraphDatabase
driver = GraphDatabase.driver(uri, auth=(user, pwd))
with driver.session() as session:
    session.run("CREATE (p:Person {name:$name})", name="Exemplo")
driver.close()
```

Como referenciar o texto gerado por uma IA na documentação do projeto

Sugestão de referência (formato livre):

"Trecho de apoio técnico gerado por um assistente de IA em 17/11/2025. Utilizado para descrever os métodos disponíveis na biblioteca neo4j Python e exemplos de uso. O texto foi revisto e adaptado pelos autores do projeto." 

Incluímos esta referência no documento para cumprir a solicitação de documentação da origem do texto gerado por IA.

---

Próximos passos recomendados (não realizados aqui):
- Iniciar/Configurar instâncias locais de Neo4j, Redis e PostgreSQL, ou usar serviços remotos e ajustar variáveis de ambiente.
- Testes unitários e de integração automatizados para os scripts de CRUD.
- Se desejar, posso gerar um pequeno arquivo docker-compose que levante Neo4j, Redis e Postgres para testes locais.
