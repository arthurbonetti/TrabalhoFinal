"""
Conexão e operações com Neo4j
"""
from neo4j import GraphDatabase
from config.databases import NEO4J_CONFIG


class Neo4jDB:
    def __init__(self):
        self.config = NEO4J_CONFIG
        self.driver = None
    
    def connect(self):
        """Conecta ao Neo4j"""
        try:
            self.driver = GraphDatabase.driver(
                self.config['uri'],
                auth=(self.config['username'], self.config['password'])
            )
            # Testa a conexão
            with self.driver.session() as session:
                session.run("RETURN 1")
            print("✓ Conectado ao Neo4j")
            return True
        except Exception as e:
            print(f"✗ Erro ao conectar Neo4j: {e}")
            return False
    
    def disconnect(self):
        """Desconecta do Neo4j"""
        if self.driver:
            self.driver.close()
            print("✓ Desconectado do Neo4j")
    
    def create_cliente(self, cliente_id, cpf, nome):
        """Cria um nó de cliente"""
        try:
            with self.driver.session() as session:
                session.run(
                    "CREATE (c:Cliente {id: $id, cpf: $cpf, nome: $nome})",
                    id=cliente_id, cpf=cpf, nome=nome
                )
            print(f"✓ Cliente {nome} criado no Neo4j")
            return True
        except Exception as e:
            print(f"✗ Erro ao criar cliente: {e}")
            return False
    
    def create_amizade(self, cliente_id1, cliente_id2):
        """Cria uma relação de amizade entre dois clientes"""
        try:
            with self.driver.session() as session:
                session.run(
                    """
                    MATCH (c1:Cliente {id: $id1}), (c2:Cliente {id: $id2})
                    CREATE (c1)-[:AMIGO]->(c2)
                    """,
                    id1=cliente_id1, id2=cliente_id2
                )
            print(f"✓ Amizade criada entre {cliente_id1} e {cliente_id2}")
            return True
        except Exception as e:
            print(f"✗ Erro ao criar amizade: {e}")
            return False
    
    def get_amigos(self, cliente_id):
        """Retorna os amigos de um cliente"""
        try:
            with self.driver.session() as session:
                result = session.run(
                    """
                    MATCH (c:Cliente {id: $id})-[:AMIGO]->(amigo:Cliente)
                    RETURN amigo.id as id, amigo.cpf as cpf, amigo.nome as nome
                    """,
                    id=cliente_id
                )
                return [dict(record) for record in result]
        except Exception as e:
            print(f"✗ Erro ao buscar amigos: {e}")
            return []
    
    def get_all_clientes(self):
        """Retorna todos os clientes"""
        try:
            with self.driver.session() as session:
                result = session.run(
                    "MATCH (c:Cliente) RETURN c.id as id, c.cpf as cpf, c.nome as nome"
                )
                return [dict(record) for record in result]
        except Exception as e:
            print(f"✗ Erro ao buscar clientes: {e}")
            return []
    
    def delete_all(self):
        """Deleta todos os nós e relações"""
        try:
            with self.driver.session() as session:
                session.run("MATCH (n) DETACH DELETE n")
            print("✓ Todos os dados deletados do Neo4j")
            return True
        except Exception as e:
            print(f"✗ Erro ao deletar dados: {e}")
            return False
    
    def get_recomendacoes_para_amigo(self, amigo_id):
        """Retorna clientes que compraram produtos e seus amigos"""
        try:
            with self.driver.session() as session:
                result = session.run(
                    """
                    MATCH (amigo:Cliente {id: $id})<-[:AMIGO]-(cliente:Cliente)
                    RETURN cliente.id as cliente_id, cliente.nome as cliente_nome,
                           amigo.id as amigo_id, amigo.nome as amigo_nome
                    """,
                    id=amigo_id
                )
                return [dict(record) for record in result]
        except Exception as e:
            print(f"✗ Erro ao buscar recomendações: {e}")
            return []
