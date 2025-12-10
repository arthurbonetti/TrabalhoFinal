"""
Conexão e operações com Redis
"""
import json
import redis
from config.databases import REDIS_CONFIG


class RedisDB:
    def __init__(self):
        self.config = REDIS_CONFIG
        self.client = None
    
    def connect(self):
        """Conecta ao Redis"""
        try:
            self.client = redis.Redis(
                host=self.config['host'],
                port=self.config['port'],
                db=self.config['db'],
                decode_responses=True
            )
            self.client.ping()
            print("✓ Conectado ao Redis")
            return True
        except Exception as e:
            print(f"✗ Erro ao conectar Redis: {e}")
            return False
    
    def disconnect(self):
        """Desconecta do Redis"""
        if self.client:
            self.client.close()
            print("✓ Desconectado do Redis")
    
    def clear_cache(self):
        """Limpa todo o cache"""
        try:
            self.client.flushdb()
            print("✓ Cache limpo")
            return True
        except Exception as e:
            print(f"✗ Erro ao limpar cache: {e}")
            return False
    
    def store_clientes(self, clientes):
        """Armazena lista de clientes"""
        try:
            self.client.delete('clientes')
            for cliente in clientes:
                key = f"cliente:{cliente['id']}"
                self.client.hset(key, mapping={
                    'id': cliente['id'],
                    'cpf': cliente['cpf'],
                    'nome': cliente['nome'],
                    'email': cliente.get('email', ''),
                    'endereco': cliente.get('endereco', ''),
                    'cidade': cliente.get('cidade', ''),
                    'uf': cliente.get('uf', '')
                })
                self.client.lpush('clientes', key)
            print(f"✓ {len(clientes)} clientes armazenados no Redis")
            return True
        except Exception as e:
            print(f"✗ Erro ao armazenar clientes: {e}")
            return False
    
    def store_compras(self, compras):
        """Armazena lista de compras"""
        try:
            self.client.delete('compras')
            for compra in compras:
                key = f"compra:{compra['id']}"
                self.client.hset(key, mapping={
                    'id': compra['id'],
                    'cliente_id': compra['cliente_id'],
                    'cliente_nome': compra['cliente_nome'],
                    'produto': compra['produto'],
                    'valor': str(compra['valor']),
                    'data': str(compra['data'])
                })
                self.client.lpush('compras', key)
            print(f"✓ {len(compras)} compras armazenadas no Redis")
            return True
        except Exception as e:
            print(f"✗ Erro ao armazenar compras: {e}")
            return False
    
    def store_amigos(self, cliente_id, amigos):
        """Armazena lista de amigos de um cliente"""
        try:
            key = f"amigos:{cliente_id}"
            self.client.delete(key)
            for amigo in amigos:
                self.client.lpush(key, json.dumps(amigo))
            print(f"✓ Amigos do cliente {cliente_id} armazenados no Redis")
            return True
        except Exception as e:
            print(f"✗ Erro ao armazenar amigos: {e}")
            return False
    
    def store_recomendacoes(self, amigo_id, recomendacoes):
        """Armazena recomendações para um amigo"""
        try:
            key = f"recomendacoes:{amigo_id}"
            self.client.delete(key)
            for rec in recomendacoes:
                self.client.lpush(key, json.dumps(rec))
            print(f"✓ Recomendações para amigo {amigo_id} armazenadas")
            return True
        except Exception as e:
            print(f"✗ Erro ao armazenar recomendações: {e}")
            return False
    
    def get_clientes(self):
        """Retorna todos os clientes do cache"""
        try:
            keys = self.client.lrange('clientes', 0, -1)
            clientes = []
            for key in keys:
                cliente = self.client.hgetall(key)
                clientes.append(cliente)
            return clientes
        except Exception as e:
            print(f"✗ Erro ao buscar clientes: {e}")
            return []
    
    def get_compras(self):
        """Retorna todas as compras do cache"""
        try:
            keys = self.client.lrange('compras', 0, -1)
            compras = []
            for key in keys:
                compra = self.client.hgetall(key)
                compras.append(compra)
            return compras
        except Exception as e:
            print(f"✗ Erro ao buscar compras: {e}")
            return []
    
    def get_amigos(self, cliente_id):
        """Retorna amigos de um cliente do cache"""
        try:
            key = f"amigos:{cliente_id}"
            amigos_json = self.client.lrange(key, 0, -1)
            return [json.loads(amigo) for amigo in amigos_json]
        except Exception as e:
            print(f"✗ Erro ao buscar amigos: {e}")
            return []
    
    def get_recomendacoes(self, amigo_id):
        """Retorna recomendações de um amigo do cache"""
        try:
            key = f"recomendacoes:{amigo_id}"
            recomendacoes_json = self.client.lrange(key, 0, -1)
            return [json.loads(rec) for rec in recomendacoes_json]
        except Exception as e:
            print(f"✗ Erro ao buscar recomendações: {e}")
            return []
