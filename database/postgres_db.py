"""
Conexão e operações com PostgreSQL
"""
import psycopg2
import psycopg2.extras
from config.databases import POSTGRES_CONFIG


class PostgresDB:
    def __init__(self):
        self.config = POSTGRES_CONFIG
        self.conn = None
    
    def connect(self):
        """Conecta ao banco PostgreSQL"""
        try:
            self.conn = psycopg2.connect(
                host=self.config['host'],
                user=self.config['user'],
                password=self.config['password'],
                dbname=self.config['database'],
                port=self.config['port']
            )
            print("✓ Conectado ao PostgreSQL")
            return True
        except Exception as e:
            print(f"✗ Erro ao conectar PostgreSQL: {e}")
            return False
    
    def disconnect(self):
        """Desconecta do banco PostgreSQL"""
        if self.conn:
            self.conn.close()
            print("✓ Desconectado do PostgreSQL")
    
    def create_tables(self):
        """Cria as tabelas necessárias"""
        try:
            cursor = self.conn.cursor()
            
            # Tabela Clientes
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS clientes (
                    id SERIAL PRIMARY KEY,
                    cpf VARCHAR(11) UNIQUE NOT NULL,
                    nome VARCHAR(255) NOT NULL,
                    endereco VARCHAR(255),
                    cidade VARCHAR(100),
                    uf VARCHAR(2),
                    email VARCHAR(255)
                );
            """)
            
            # Tabela Produtos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS produtos (
                    id SERIAL PRIMARY KEY,
                    produto VARCHAR(255) NOT NULL,
                    valor DECIMAL(10, 2),
                    quantidade INT,
                    tipo VARCHAR(100)
                );
            """)
            
            # Tabela Compras
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS compras (
                    id SERIAL PRIMARY KEY,
                    id_cliente INT NOT NULL,
                    id_produto INT NOT NULL,
                    data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (id_cliente) REFERENCES clientes(id),
                    FOREIGN KEY (id_produto) REFERENCES produtos(id)
                );
            """)
            
            self.conn.commit()
            print("✓ Tabelas criadas no PostgreSQL")
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"✗ Erro ao criar tabelas: {e}")
            return False
    
    def insert_cliente(self, cpf, nome, endereco, cidade, uf, email):
        """Insere um cliente"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO clientes (cpf, nome, endereco, cidade, uf, email)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id;
            """, (cpf, nome, endereco, cidade, uf, email))
            cliente_id = cursor.fetchone()[0]
            self.conn.commit()
            print(f"✓ Cliente {nome} inserido com ID {cliente_id}")
            return cliente_id
        except Exception as e:
            self.conn.rollback()
            print(f"✗ Erro ao inserir cliente: {e}")
            return None
    
    def insert_produto(self, produto, valor, quantidade, tipo):
        """Insere um produto"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO produtos (produto, valor, quantidade, tipo)
                VALUES (%s, %s, %s, %s)
                RETURNING id;
            """, (produto, valor, quantidade, tipo))
            produto_id = cursor.fetchone()[0]
            self.conn.commit()
            print(f"✓ Produto {produto} inserido com ID {produto_id}")
            return produto_id
        except Exception as e:
            self.conn.rollback()
            print(f"✗ Erro ao inserir produto: {e}")
            return None
    
    def insert_compra(self, id_cliente, id_produto):
        """Insere uma compra"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO compras (id_cliente, id_produto)
                VALUES (%s, %s)
                RETURNING id;
            """, (id_cliente, id_produto))
            compra_id = cursor.fetchone()[0]
            self.conn.commit()
            print(f"✓ Compra inserida com ID {compra_id}")
            return compra_id
        except Exception as e:
            self.conn.rollback()
            print(f"✗ Erro ao inserir compra: {e}")
            return None
    
    def get_all_clientes(self):
        """Retorna todos os clientes"""
        try:
            cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cursor.execute("SELECT * FROM clientes;")
            resultado = cursor.fetchall() or []
            cursor.close()
            return resultado
        except Exception as e:
            print(f"✗ Erro ao buscar clientes: {e}")
            return []
    
    def get_all_compras(self):
        """Retorna todas as compras com dados do cliente e produto"""
        try:
            cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cursor.execute("""
                SELECT c.id, cl.id as cliente_id, cl.nome as cliente_nome,
                       p.id as produto_id, p.produto, p.valor, c.data
                FROM compras c
                JOIN clientes cl ON c.id_cliente = cl.id
                JOIN produtos p ON c.id_produto = p.id
                ORDER BY c.data DESC;
            """)
            resultado = cursor.fetchall() or []
            cursor.close()
            return resultado
        except Exception as e:
            print(f"✗ Erro ao buscar compras: {e}")
            return []
    
    def get_cliente_by_cpf(self, cpf):
        """Busca um cliente pelo CPF"""
        try:
            cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cursor.execute("SELECT * FROM clientes WHERE cpf = %s;", (cpf,))
            resultado = cursor.fetchone()
            cursor.close()
            return resultado
        except Exception as e:
            print(f"✗ Erro ao buscar cliente: {e}")
            return None
