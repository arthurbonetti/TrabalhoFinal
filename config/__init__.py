"""
__init__.py para módulo de configuração
"""

from .databases import POSTGRES_CONFIG, MONGO_CONFIG, NEO4J_CONFIG, REDIS_CONFIG

__all__ = ['POSTGRES_CONFIG', 'MONGO_CONFIG', 'NEO4J_CONFIG', 'REDIS_CONFIG']
