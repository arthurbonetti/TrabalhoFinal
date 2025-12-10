"""
Conexão e operações com MongoDB
"""
from pymongo import MongoClient
from config.databases import MONGO_CONFIG


class MongoDB:
    def __init__(self):
        self.config = MONGO_CONFIG
        self.client = None
        self.db = None
    
    def connect(self):
        """Conecta ao MongoDB"""
        try:
            self.client = MongoClient(
                f"mongodb://{self.config['host']}:{self.config['port']}/"
            )
            self.db = self.client[self.config['database']]
            # Testa a conexão
            self.db.command('ping')
            print("✓ Conectado ao MongoDB")
            return True
        except Exception as e:
            print(f"✗ Erro ao conectar MongoDB: {e}")
            return False
    
    def disconnect(self):
        """Desconecta do MongoDB"""
        if self.client:
            self.client.close()
            print("✓ Desconectado do MongoDB")
    
    def insert_cliente_interesses(self, cliente_id, cpf, nome, interesses):
        """Insere dados de cliente com interesses"""
        try:
            collection = self.db['clientes_interesses']
            documento = {
                'cliente_id': cliente_id,
                'cpf': cpf,
                'nome': nome,
                'interesses': interesses
            }
            result = collection.insert_one(documento)
            print(f"✓ Interesses do cliente {nome} inseridos")
            return str(result.inserted_id)
        except Exception as e:
            print(f"✗ Erro ao inserir interesses: {e}")
            return None
    
    def update_cliente_interesses(self, cliente_id, interesses):
        """Atualiza interesses de um cliente"""
        try:
            collection = self.db['clientes_interesses']
            collection.update_one(
                {'cliente_id': cliente_id},
                {'$set': {'interesses': interesses}}
            )
            print(f"✓ Interesses do cliente {cliente_id} atualizados")
            return True
        except Exception as e:
            print(f"✗ Erro ao atualizar interesses: {e}")
            return False
    
    def get_cliente_interesses(self, cliente_id):
        """Retorna interesses de um cliente"""
        try:
            collection = self.db['clientes_interesses']
            return collection.find_one({'cliente_id': cliente_id})
        except Exception as e:
            print(f"✗ Erro ao buscar interesses: {e}")
            return None
    
    def get_all_clientes_interesses(self):
        """Retorna todos os clientes com interesses"""
        try:
            collection = self.db['clientes_interesses']
            return list(collection.find())
        except Exception as e:
            print(f"✗ Erro ao buscar clientes: {e}")
            return []
    
    def delete_collection(self, collection_name):
        """Deleta uma coleção"""
        try:
            self.db[collection_name].drop()
            print(f"✓ Coleção {collection_name} deletada")
            return True
        except Exception as e:
            print(f"✗ Erro ao deletar coleção: {e}")
            return False
