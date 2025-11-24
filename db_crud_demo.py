"""db_crud_demo.py
Exemplo de CRUD para Redis e PostgreSQL.

Configuração esperada por variáveis de ambiente:
REDIS_HOST, REDIS_PORT (opcional), REDIS_DB (opcional)
POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD

Instalar dependências: pip install -r requirements.txt
"""
import os
import json

import redis
import psycopg2
from psycopg2.extras import RealDictCursor


# ---------------- Redis CRUD (chave-valor simples) ----------------
def get_redis_client():
    host = os.environ.get("REDIS_HOST", "localhost")
    port = int(os.environ.get("REDIS_PORT", "6379"))
    db = int(os.environ.get("REDIS_DB", "0"))
    return redis.Redis(host=host, port=port, db=db, decode_responses=True)


def redis_create(client, key, value):
    return client.set(key, json.dumps(value))


def redis_read(client, key):
    v = client.get(key)
    return json.loads(v) if v is not None else None


def redis_update(client, key, value):
    if client.exists(key):
        return client.set(key, json.dumps(value))
    return False


def redis_delete(client, key):
    return client.delete(key)


# ---------------- PostgreSQL CRUD (tabela simples) ----------------
def get_postgres_conn():
    host = os.environ.get("POSTGRES_HOST", "localhost")
    port = os.environ.get("POSTGRES_PORT", "5432")
    db = os.environ.get("POSTGRES_DB", "testdb")
    user = os.environ.get("POSTGRES_USER", "postgres")
    pwd = os.environ.get("POSTGRES_PASSWORD", "")
    conn = psycopg2.connect(host=host, port=port, dbname=db, user=user, password=pwd)
    return conn


def postgres_init(conn):
    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS pessoa (
                id SERIAL PRIMARY KEY,
                nome TEXT NOT NULL,
                idade INT
            )
            """
        )
        conn.commit()


def postgres_create(conn, nome, idade):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("INSERT INTO pessoa (nome, idade) VALUES (%s, %s) RETURNING id, nome, idade", (nome, idade))
        row = cur.fetchone()
        conn.commit()
        return row


def postgres_read(conn, pessoa_id):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT id, nome, idade FROM pessoa WHERE id = %s", (pessoa_id,))
        return cur.fetchone()


def postgres_update(conn, pessoa_id, nome=None, idade=None):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        # build a minimal update
        updates = []
        params = []
        if nome is not None:
            updates.append("nome = %s")
            params.append(nome)
        if idade is not None:
            updates.append("idade = %s")
            params.append(idade)
        if not updates:
            return None
        params.append(pessoa_id)
        sql = f"UPDATE pessoa SET {', '.join(updates)} WHERE id = %s RETURNING id, nome, idade"
        cur.execute(sql, params)
        row = cur.fetchone()
        conn.commit()
        return row


def postgres_delete(conn, pessoa_id):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM pessoa WHERE id = %s", (pessoa_id,))
        conn.commit()
        return cur.rowcount


def main():
    print("=== Redis demo ===")
    r = get_redis_client()
    redis_create(r, "pessoa:1", {"nome": "João", "idade": 30})
    print("Read from redis:", redis_read(r, "pessoa:1"))
    redis_update(r, "pessoa:1", {"nome": "João", "idade": 31})
    print("After update:", redis_read(r, "pessoa:1"))
    redis_delete(r, "pessoa:1")
    print("After delete:", redis_read(r, "pessoa:1"))

    print("\n=== PostgreSQL demo ===")
    conn = get_postgres_conn()
    try:
        postgres_init(conn)
        new = postgres_create(conn, "Maria", 28)
        print("Created:", new)
        read = postgres_read(conn, new["id"]) if new else None
        print("Read:", read)
        updated = postgres_update(conn, new["id"], idade=29)
        print("Updated:", updated)
        deleted = postgres_delete(conn, new["id"])
        print("Rows deleted:", deleted)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
