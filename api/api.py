"""
API de integração entre todas as bases de dados
"""
from database.postgres_db import PostgresDB
from database.mongo_db import MongoDB
from database.neo4j_db import Neo4jDB
from database.redis_db import RedisDB


class RecommendationAPI:
    def __init__(self):
        self.postgres = PostgresDB()
        self.mongo = MongoDB()
        self.neo4j = Neo4jDB()
        self.redis = RedisDB()
    
    def conectar_todos(self):
        """Conecta em todos os bancos de dados"""
        print("\n=== Conectando aos bancos de dados ===")
        resultado = True
        resultado &= self.postgres.connect()
        resultado &= self.mongo.connect()
        resultado &= self.neo4j.connect()
        resultado &= self.redis.connect()
        return resultado
    
    def desconectar_todos(self):
        """Desconecta de todos os bancos de dados"""
        print("\n=== Desconectando dos bancos de dados ===")
        self.postgres.disconnect()
        self.mongo.disconnect()
        self.neo4j.disconnect()
        self.redis.disconnect()
    
    def inicializar_bancos(self):
        """Inicializa as tabelas e estruturas nos bancos"""
        print("\n=== Inicializando estruturas ===")
        self.postgres.create_tables()
        self.neo4j.delete_all()  # Limpa dados anteriores
        self.mongo.delete_collection('clientes_interesses')
        self.redis.clear_cache()
    
    def adicionar_cliente(self, cpf, nome, endereco, cidade, uf, email, interesses=[]):
        """Adiciona um cliente em todos os bancos"""
        print(f"\n=== Adicionando cliente {nome} ===")
        
        # PostgreSQL
        cliente_id = self.postgres.insert_cliente(cpf, nome, endereco, cidade, uf, email)
        if not cliente_id:
            return None
        
        # MongoDB
        self.mongo.insert_cliente_interesses(cliente_id, cpf, nome, interesses)
        
        # Neo4j
        self.neo4j.create_cliente(cliente_id, cpf, nome)
        
        return cliente_id
    
    def adicionar_amizade(self, cliente_id1, cliente_id2):
        """Adiciona uma relação de amizade entre dois clientes"""
        print(f"\n=== Criando amizade entre {cliente_id1} e {cliente_id2} ===")
        self.neo4j.create_amizade(cliente_id1, cliente_id2)
    
    def adicionar_produto(self, produto, valor, quantidade, tipo):
        """Adiciona um produto"""
        return self.postgres.insert_produto(produto, valor, quantidade, tipo)
    
    def registrar_compra(self, cliente_id, produto_id):
        """Registra uma compra e atualiza o cache"""
        print(f"\n=== Registrando compra ===")
        compra_id = self.postgres.insert_compra(cliente_id, produto_id)
        if compra_id:
            self.sincronizar_cache()
        return compra_id
    
    def sincronizar_cache(self):
        """Sincroniza todos os dados com Redis"""
        print("\n=== Sincronizando cache ===")
        self.redis.clear_cache()
        
        # Sincronizar clientes
        clientes = self.postgres.get_all_clientes()
        self.redis.store_clientes(clientes)
        
        # Sincronizar compras
        compras = self.postgres.get_all_compras()
        self.redis.store_compras(compras)
        
        # Sincronizar amigos
        for cliente in clientes:
            amigos = self.neo4j.get_amigos(cliente['id'])
            self.redis.store_amigos(cliente['id'], amigos)
        
        # Sincronizar recomendações
        for cliente in clientes:
            recomendacoes = self.neo4j.get_recomendacoes_para_amigo(cliente['id'])
            self.redis.store_recomendacoes(cliente['id'], recomendacoes)
    
    def atualizar_interesses(self, cliente_id, interesses):
        """Atualiza os interesses de um cliente"""
        print(f"\n=== Atualizando interesses do cliente {cliente_id} ===")
        self.mongo.update_cliente_interesses(cliente_id, interesses)
    
    def get_dados_consolidados(self):
        """Retorna todos os dados consolidados do Redis"""
        dados = {
            'clientes': self.redis.get_clientes(),
            'compras': self.redis.get_compras(),
            'amigos': {},
            'recomendacoes': {}
        }
        
        for cliente in dados['clientes']:
            cliente_id = int(cliente['id'])
            dados['amigos'][cliente_id] = self.redis.get_amigos(cliente_id)
            dados['recomendacoes'][cliente_id] = self.redis.get_recomendacoes(cliente_id)
        
        return dados
