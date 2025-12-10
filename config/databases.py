"""
Configuração de conexão com os bancos de dados
"""
import os
from dotenv import load_dotenv

load_dotenv()

# PostgreSQL
POSTGRES_CONFIG = {
    'host': 'localhost',
    'user': 'postgres',
    'password': '190309',
    'database': 'PostgreInt',
    'port': 5432
}

# MongoDB
MONGO_CONFIG = {
    'host': 'localhost',
    'port': 27017,
    'database': 'MongoInt',
}

# Neo4j
NEO4J_CONFIG = {
    'uri': 'bolt://98.92.119.153',
    'username': 'neo4j',
    'password': 'civilian-test-ornament',
    'database': 'neo4j'
}

# Redis
REDIS_CONFIG = {
    'host': 'localhost',
    'port': 6379,
    'db': 0
}
