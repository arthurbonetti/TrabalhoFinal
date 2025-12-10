"""
Interface CLI para consultar dados integrados de múltiplos bancos
Funciona com dados já existentes nos bancos
"""
import os
from database.postgres_db import PostgresDB
from database.mongo_db import MongoDB
from database.neo4j_db import Neo4jDB
from database.redis_db import RedisDB


class InterfaceConsultaDados:
    def __init__(self):
        self.postgres = PostgresDB()
        self.mongo = MongoDB()
        self.neo4j = Neo4jDB()
        self.redis = RedisDB()
        self.conectado = False
    
    def limpar_tela(self):
        """Limpa a tela do terminal"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def conectar(self):
        """Conecta em todos os bancos"""
        print("\n=== CONECTANDO AOS BANCOS DE DADOS ===\n")
        
        self.postgres.connect()
        self.mongo.connect()
        self.neo4j.connect()
        self.redis.connect()
        
        self.conectado = True
        input("\nPressione Enter para continuar...")
    
    def desconectar(self):
        """Desconecta dos bancos"""
        self.postgres.disconnect()
        self.mongo.disconnect()
        self.neo4j.disconnect()
        self.redis.disconnect()
    
    def exibir_menu_principal(self):
        """Exibe menu principal"""
        self.limpar_tela()
        print("=" * 70)
        print(" SISTEMA DE RECOMENDAÇÃO - CONSULTA DE DADOS INTEGRADOS")
        print("=" * 70)
        print("\n1. Conectar aos Bancos")
        print("2. Visualizar Dados do PostgreSQL")
        print("3. Visualizar Dados do MongoDB")
        print("4. Visualizar Dados do Neo4j")
        print("5. Sincronizar Cache (Redis)")
        print("6. Consultar Dados Consolidados")
        print("7. Sair")
        print("\n" + "=" * 70)
    
    def visualizar_postgres(self):
        """Visualiza dados do PostgreSQL"""
        self.limpar_tela()
        print("=== POSTGRESQL - PostegreInt ===\n")
        
        print("📋 CLIENTES:")
        print("-" * 70)
        clientes = self.postgres.get_all_clientes()
        print(f"{'ID':<5} {'CPF':<15} {'Nome':<25} {'Cidade':<20} {'UF':<3}")
        print("-" * 70)
        for cliente in clientes:
            print(f"{cliente['id']:<5} {cliente['cpf']:<15} {cliente['nome']:<25} {cliente['cidade']:<20} {cliente['uf']:<3}")
        
        print(f"\n📦 PRODUTOS:")
        print("-" * 70)
        try:
            with self.postgres.conn.cursor() as cur:
                cur.execute("SELECT id, produto, valor, tipo FROM produtos")
                produtos = cur.fetchall()
                print(f"{'ID':<5} {'Produto':<30} {'Valor':<15} {'Tipo':<20}")
                print("-" * 70)
                for p in produtos:
                    print(f"{p[0]:<5} {p[1]:<30} R$ {p[2]:<13.2f} {p[3]:<20}")
        except Exception as e:
            print(f"Erro: {e}")
        
        print(f"\n🛍️  COMPRAS:")
        print("-" * 70)
        compras = self.postgres.get_all_compras()
        print(f"{'ID':<5} {'Cliente':<25} {'Produto':<30} {'Valor':<15} {'Data':<20}")
        print("-" * 70)
        for compra in compras:
            print(f"{compra['id']:<5} {compra['cliente_nome']:<25} {compra['produto']:<30} R$ {compra['valor']:<13.2f} {str(compra['data']):<20}")
        
        input(f"\n\nTotal: {len(clientes)} clientes | {len(compras)} compras\nPressione Enter para continuar...")
    
    def visualizar_mongodb(self):
        """Visualiza dados do MongoDB"""
        self.limpar_tela()
        print("=== MONGODB - MongoInt ===\n")
        
        col = self.mongo.db['Int']
        documentos = list(col.find())
        
        print(f"Documentos encontrados: {len(documentos)}\n")
        print("-" * 70)
        
        for doc in documentos:
            print(f"\n👤 Cliente ID: {doc.get('id_cliente', 'N/A')}")
            print(f"   Nome: {doc.get('nome', 'N/A')}")
            
            interesses = doc.get('interesses', {})
            if interesses:
                print(f"   Interesses:")
                for categoria, items in interesses.items():
                    if isinstance(items, list) and items:
                        items_str = ', '.join(str(item) for item in items)
                        print(f"     • {categoria}: {items_str}")
                    elif isinstance(items, dict):
                        sub_items = ', '.join(str(v) for v in items.values() if v)
                        if sub_items:
                            print(f"     • {categoria}: {sub_items}")
            else:
                print(f"   Interesses: Nenhum registrado")
        
        input(f"\n\nTotal: {len(documentos)} documentos\nPressione Enter para continuar...")
    
    def visualizar_neo4j(self):
        """Visualiza dados do Neo4j"""
        self.limpar_tela()
        print("=== NEO4J - Sandbox ===\n")
        
        print("👥 PESSOAS:")
        print("-" * 70)
        with self.neo4j.driver.session() as session:
            result = session.run("MATCH (p:Pessoa) RETURN p.id as id, p.nome as nome, p.cpf as cpf")
            pessoas = [dict(record) for record in result]
            
            print(f"{'ID':<5} {'CPF':<15} {'Nome':<30}")
            print("-" * 70)
            for pessoa in pessoas:
                print(f"{pessoa['id']:<5} {pessoa['cpf']:<15} {pessoa['nome']:<30}")
            
            print(f"\n\n🔗 RELAÇÕES DE AMIZADE:")
            print("-" * 70)
            result = session.run("""
                MATCH (p1:Pessoa)-[r:AMIGO_DE]->(p2:Pessoa)
                RETURN p1.nome as pessoa1, p2.nome as pessoa2
            """)
            amizades = [dict(record) for record in result]
            
            print(f"{'Pessoa 1':<30} {'→ Amigo':<30}")
            print("-" * 70)
            for amizade in amizades:
                print(f"{amizade['pessoa1']:<30} → {amizade['pessoa2']:<30}")
            
            print(f"\n\nTotal: {len(pessoas)} pessoas | {len(amizades)} relações de amizade")
        
        input("\nPressione Enter para continuar...")
    
    def sincronizar_redis(self):
        """Sincroniza dados para Redis"""
        print("\n=== SINCRONIZANDO CACHE REDIS ===\n")
        
        try:
            print("Limpando cache anterior...")
            self.redis.clear_cache()
            
            print("Copiando dados do PostgreSQL...")
            clientes = self.postgres.get_all_clientes()
            self.redis.store_clientes(clientes)
            
            compras = self.postgres.get_all_compras()
            self.redis.store_compras(compras)
            
            print("Copiando dados do Neo4j...")
            with self.neo4j.driver.session() as session:
                # Copiar amigos para Redis
                result = session.run("""
                    MATCH (p:Pessoa)-[:AMIGO_DE]->(amigo:Pessoa)
                    RETURN p.id as pessoa_id, amigo.id as amigo_id, amigo.nome as amigo_nome, amigo.cpf as amigo_cpf
                """)
                
                amigos_por_pessoa = {}
                for record in result:
                    pessoa_id = record['pessoa_id']
                    if pessoa_id not in amigos_por_pessoa:
                        amigos_por_pessoa[pessoa_id] = []
                    amigos_por_pessoa[pessoa_id].append({
                        'id': record['amigo_id'],
                        'nome': record['amigo_nome'],
                        'cpf': record['amigo_cpf']
                    })
                
                for pessoa_id, amigos in amigos_por_pessoa.items():
                    self.redis.store_amigos(pessoa_id, amigos)
            
            print("\n✓ Cache sincronizado com sucesso!")
            
        except Exception as e:
            print(f"✗ Erro: {e}")
        
        input("\nPressione Enter para continuar...")
    
    def consultar_dados_consolidados(self):
        """Consulta dados consolidados"""
        self.limpar_tela()
        print("=== DADOS CONSOLIDADOS ===\n")
        
        # Tentar obter do Redis
        clientes_redis = self.redis.get_clientes()
        compras_redis = self.redis.get_compras()
        
        if not clientes_redis:
            print("Cache vazio. Sincronizando...")
            self.sincronizar_redis()
            clientes_redis = self.redis.get_clientes()
            compras_redis = self.redis.get_compras()
        
        print("\n📋 CLIENTES EM CACHE:")
        print("-" * 70)
        print(f"{'ID':<5} {'CPF':<15} {'Nome':<30} {'E-mail':<30}")
        print("-" * 70)
        for cliente in clientes_redis:
            print(f"{cliente['id']:<5} {cliente['cpf']:<15} {cliente['nome']:<30} {cliente['email']:<30}")
        
        print(f"\n\n🛍️  COMPRAS EM CACHE:")
        print("-" * 70)
        print(f"{'Cliente':<25} {'Produto':<30} {'Valor':<15}")
        print("-" * 70)
        for compra in compras_redis:
            print(f"{compra['cliente_nome']:<25} {compra['produto']:<30} R$ {float(compra['valor']):<13.2f}")
        
        print(f"\n\n🤝 AMIGOS CADASTRADOS E RECOMENDAÇÕES:")
        print("-" * 70)
        
        # Obter dados de compras para recomendação
        compras_por_cliente = {}
        for compra in compras_redis:
            cliente = compra['cliente_nome']
            produto = compra['produto']
            if cliente not in compras_por_cliente:
                compras_por_cliente[cliente] = []
            if produto not in compras_por_cliente[cliente]:
                compras_por_cliente[cliente].append(produto)
        
        with self.neo4j.driver.session() as session:
            result = session.run("""
                MATCH (p:Pessoa)-[:AMIGO_DE]->(amigo:Pessoa)
                RETURN p.id as pessoa_id, p.nome as pessoa, amigo.nome as amigo
                ORDER BY p.nome
            """)
            
            pessoas_amigos = {}
            for record in result:
                pessoa = record['pessoa']
                amigo = record['amigo']
                if pessoa not in pessoas_amigos:
                    pessoas_amigos[pessoa] = []
                pessoas_amigos[pessoa].append(amigo)
            
            for pessoa, amigos in pessoas_amigos.items():
                print(f"\n👤 {pessoa}:")
                
                # Mostrar amigos
                print(f"  Amigos:")
                for amigo in amigos:
                    print(f"    • {amigo}")
                
                # Mostrar recomendações baseadas em compras
                if pessoa in compras_por_cliente:
                    produtos_comprados = compras_por_cliente[pessoa]
                    print(f"\n  📋 Recomendações para seus amigos:")
                    
                    for amigo in amigos:
                        # Filtrar produtos que o amigo ainda não comprou
                        produtos_amigo = compras_por_cliente.get(amigo, [])
                        recomendacoes = [p for p in produtos_comprados if p not in produtos_amigo]
                        
                        if recomendacoes:
                            print(f"    Para {amigo}: {', '.join(recomendacoes)}")
                        else:
                            print(f"    Para {amigo}: Nenhuma recomendação (já comprou tudo)")
                else:
                    print(f"\n  ℹ️  Sem compras registradas para recomendar")
        
        input("\n\nPressione Enter para continuar...")
    
    def executar(self):
        """Executa a interface"""
        if not self.conectado:
            self.conectar()
        
        while True:
            self.exibir_menu_principal()
            opcao = input("Escolha uma opção: ").strip()
            
            if opcao == "1":
                self.conectar()
            elif opcao == "2":
                self.visualizar_postgres()
            elif opcao == "3":
                self.visualizar_mongodb()
            elif opcao == "4":
                self.visualizar_neo4j()
            elif opcao == "5":
                self.sincronizar_redis()
            elif opcao == "6":
                self.consultar_dados_consolidados()
            elif opcao == "7":
                print("\n=== ENCERRANDO SISTEMA ===")
                print("\nLimpando cache Redis...")
                self.redis.clear_cache()
                print("Desconectando dos bancos...")
                self.desconectar()
                print("\n✓ Sistema encerrado com sucesso!")
                print("Até logo!")
                break
            else:
                input("Opção inválida. Pressione Enter para continuar...")


if __name__ == "__main__":
    interface = InterfaceConsultaDados()
    interface.executar()
