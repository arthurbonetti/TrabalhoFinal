"""neo4j_demo.py
Exemplo simples de conexão ao Neo4j usando a biblioteca oficial neo4j.

Requisitos:
- Defina as variáveis de ambiente NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD
- Instale dependências: pip install -r requirements.txt

Este script demonstra: criar driver, abrir sessão, executar uma query e fechar o driver.
"""
import os
from neo4j import GraphDatabase


def get_driver():
    uri = os.environ.get("NEO4J_URI")
    user = os.environ.get("NEO4J_USER")
    password = os.environ.get("NEO4J_PASSWORD")
    if not uri or not user or not password:
        raise RuntimeError("Defina NEO4J_URI, NEO4J_USER e NEO4J_PASSWORD como variáveis de ambiente")
    driver = GraphDatabase.driver(uri, auth=(user, password))
    return driver


def create_person(driver, name):
    with driver.session() as session:
        result = session.run("CREATE (p:Person {name: $name}) RETURN p", name=name)
        return [record[0] for record in result]


def list_people(driver):
    with driver.session() as session:
        result = session.run("MATCH (p:Person) RETURN p.name AS name")
        return [record["name"] for record in result]


def query_pessoa_names(driver):
    """Exemplo baseado no trecho enviado: verifica conectividade, abre sessão no database 'neo4j' e lista p.nome de nós :Pessoa."""
    # Verifica conectividade (lança exceção se não conseguir)
    driver.verify_connectivity()

    with driver.session(database="neo4j") as session:
        result = session.run("MATCH (p:Pessoa) RETURN p.nome AS nome")
        for record in result:
            print(record["nome"])


def main():
    driver = get_driver()
    try:
        print("Verificando conectividade com Neo4j...")
        try:
            driver.verify_connectivity()
            print("Conectividade OK")
        except Exception as e:
            print("Falha ao verificar conectividade:", e)

        # Exemplo de criação (opcional)
        print("Criando pessoa de exemplo: Alice")
        create_person(driver, "Alice")

        # Listagem genérica (label Person)
        print("Pessoas (label Person):")
        people = list_people(driver)
        for p in people:
            print(" -", p)

        # Exemplo específico do enunciado (label Pessoa e propriedade nome)
        print("Pessoas (label Pessoa, propriedade nome):")
        try:
            query_pessoa_names(driver)
        except Exception as e:
            print("Não foi possível executar query_pessoa_names:", e)
    finally:
        # driver.close() fecha conexões e libera recursos
        driver.close()


if __name__ == "__main__":
    main()
