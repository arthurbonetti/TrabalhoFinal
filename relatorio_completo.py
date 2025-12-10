"""
Relatório completo e consolidado do sistema de recomendação
Integra dados de todos os 4 bancos
"""
from database.postgres_db import PostgresDB
from database.mongo_db import MongoDB
from database.neo4j_db import Neo4jDB
from datetime import datetime


def gerar_relatorio_completo():
    """Gera um relatório completo e consolidado"""
    
    print("\n" + "=" * 80)
    print(" RELATÓRIO COMPLETO - SISTEMA DE RECOMENDAÇÃO DE COMPRAS")
    print(f" Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("=" * 80)
    
    # 1. PostgreSQL
    print("\n" + "=" * 80)
    print("1. BANCO RELACIONAL - POSTGRESQL (PostegreInt)")
    print("=" * 80)
    
    pg = PostgresDB()
    if not pg.connect():
        print("Erro ao conectar PostgreSQL")
        return
    
    clientes_pg = pg.get_all_clientes()
    compras_pg = pg.get_all_compras()
    
    print(f"\n📋 CLIENTES ({len(clientes_pg)}):")
    print("-" * 80)
    print(f"{'ID':<5} {'CPF':<15} {'Nome':<30} {'Cidade':<20} {'UF':<3} {'E-mail':<30}")
    print("-" * 80)
    for cliente in clientes_pg:
        email = cliente.get('email', 'N/A')[:30]
        print(f"{cliente['id']:<5} {cliente['cpf']:<15} {cliente['nome']:<30} {cliente['cidade']:<20} {cliente['uf']:<3} {email:<30}")
    
    print(f"\n📦 PRODUTOS:")
    print("-" * 80)
    try:
        with pg.conn.cursor() as cur:
            cur.execute("SELECT id, produto, valor, quantidade, tipo FROM produtos")
            produtos = cur.fetchall()
            print(f"{'ID':<5} {'Produto':<35} {'Valor':<12} {'Qtd':<5} {'Tipo':<20}")
            print("-" * 80)
            for p in produtos:
                print(f"{p[0]:<5} {p[1]:<35} R$ {p[2]:<10.2f} {p[3]:<5} {p[4]:<20}")
    except Exception as e:
        print(f"Erro: {e}")
    
    print(f"\n🛍️  COMPRAS ({len(compras_pg)}):")
    print("-" * 80)
    print(f"{'ID':<5} {'Cliente':<30} {'Produto':<35} {'Valor':<12} {'Data':<20}")
    print("-" * 80)
    for compra in compras_pg:
        data_str = str(compra['data'])[:19]
        print(f"{compra['id']:<5} {compra['cliente_nome']:<30} {compra['produto']:<35} R$ {compra['valor']:<10.2f} {data_str:<20}")
    
    # Estatísticas PostgreSQL
    print(f"\n📊 ESTATÍSTICAS:")
    print("-" * 80)
    try:
        with pg.conn.cursor() as cur:
            cur.execute("SELECT SUM(p.valor) FROM compras c JOIN produtos p ON c.id_produto = p.id")
            total_vendas = cur.fetchone()[0] or 0
            
            cur.execute("""
                SELECT c.nome, COUNT(comp.id) as total, SUM(p.valor) as total_gasto
                FROM clientes c
                LEFT JOIN compras comp ON c.id = comp.id_cliente
                LEFT JOIN produtos p ON comp.id_produto = p.id
                GROUP BY c.id, c.nome
                ORDER BY total_gasto DESC
            """)
            stats = cur.fetchall()
            print(f"  • Total de vendas: R$ {total_vendas:.2f}")
            print(f"  • Clientes com compras:")
            for nome, total, gasto in stats:
                if total and total > 0:
                    print(f"    - {nome}: {total} compra(s), Total gasto: R$ {gasto:.2f}")
    except Exception as e:
        print(f"Erro: {e}")
    
    pg.disconnect()
    
    # 2. MongoDB
    print("\n" + "=" * 80)
    print("2. BANCO DE DOCUMENTOS - MONGODB (MongoInt)")
    print("=" * 80)
    
    mongo = MongoDB()
    if not mongo.connect():
        print("Erro ao conectar MongoDB")
        return
    
    col = mongo.db['Int']
    documentos = list(col.find())
    
    print(f"\n📄 PERFIS DE CLIENTES ({len(documentos)}):")
    print("-" * 80)
    
    for i, doc in enumerate(documentos, 1):
        cliente_id = doc.get('id_cliente', 'N/A')
        nome = doc.get('nome', 'N/A')
        print(f"\n{i}. Cliente ID {cliente_id} - {nome}")
        
        interesses = doc.get('interesses', {})
        if interesses:
            print("   Interesses:")
            for categoria, items in interesses.items():
                if isinstance(items, list) and items:
                    items_str = ', '.join(str(item) for item in items)
                    print(f"     • {categoria}: {items_str}")
                elif isinstance(items, dict):
                    for sub_cat, sub_items in items.items():
                        if isinstance(sub_items, list) and sub_items:
                            items_str = ', '.join(str(item) for item in sub_items)
                            print(f"     • {categoria} - {sub_cat}: {items_str}")
        else:
            print("   Interesses: Nenhum registrado")
    
    mongo.disconnect()
    
    # 3. Neo4j
    print("\n" + "=" * 80)
    print("3. BANCO DE GRAFOS - NEO4J (Sandbox)")
    print("=" * 80)
    
    neo = Neo4jDB()
    if not neo.connect():
        print("Erro ao conectar Neo4j")
        return
    
    with neo.driver.session() as session:
        # Pessoas
        result = session.run("MATCH (p:Pessoa) RETURN p.id as id, p.nome as nome, p.cpf as cpf ORDER BY p.id")
        pessoas = [dict(record) for record in result]
        
        print(f"\n👥 PESSOAS ({len(pessoas)}):")
        print("-" * 80)
        print(f"{'ID':<5} {'CPF':<15} {'Nome':<40}")
        print("-" * 80)
        for pessoa in pessoas:
            print(f"{pessoa['id']:<5} {pessoa['cpf']:<15} {pessoa['nome']:<40}")
        
        # Amizades
        result = session.run("""
            MATCH (p1:Pessoa)-[r:AMIGO_DE]->(p2:Pessoa)
            RETURN p1.id as id1, p1.nome as nome1, p2.id as id2, p2.nome as nome2
            ORDER BY p1.id, p2.id
        """)
        amizades = [dict(record) for record in result]
        
        print(f"\n🤝 RELAÇÕES DE AMIZADE ({len(amizades)}):")
        print("-" * 80)
        print(f"{'De':<30} {'→':<3} {'Para':<30}")
        print("-" * 80)
        for amizade in amizades:
            print(f"{amizade['nome1']:<30} → {amizade['nome2']:<30}")
        
        # Análise de conectividade
        print(f"\n📊 ANÁLISE DE REDE:")
        print("-" * 80)
        
        result = session.run("""
            MATCH (p:Pessoa)
            OPTIONAL MATCH (p)-[r:AMIGO_DE]->()
            RETURN p.nome as nome, COUNT(r) as grau
            ORDER BY grau DESC
        """)
        
        pessoas_grau = [dict(record) for record in result]
        print("Pessoas mais conectadas:")
        for pessoa in pessoas_grau[:5]:
            if pessoa['grau'] > 0:
                print(f"  • {pessoa['nome']}: {pessoa['grau']} amigo(s)")
    
    neo.disconnect()
    
    # Resumo Final
    print("\n" + "=" * 80)
    print("RESUMO CONSOLIDADO")
    print("=" * 80)
    print(f"\n✓ Total de Clientes: {len(clientes_pg)}")
    print(f"✓ Total de Produtos: {len(produtos) if 'produtos' in locals() else 'N/A'}")
    print(f"✓ Total de Compras: {len(compras_pg)}")
    print(f"✓ Perfis de Interesses: {len(documentos)}")
    print(f"✓ Pessoas no Grafo: {len(pessoas)}")
    print(f"✓ Relações de Amizade: {len(amizades)}")
    
    print("\n" + "=" * 80)
    print("📋 RECOMENDAÇÕES BASEADAS EM AMIGOS")
    print("=" * 80)
    
    # Buscar compras e recomendar aos amigos
    print("\nPara cada compra realizada, recomendações podem ser feitas aos amigos:\n")
    
    neo = Neo4jDB()
    if neo.connect():
        with neo.driver.session() as session:
            # Exemplo de recomendação
            result = session.run("""
                MATCH (cliente:Pessoa)-[:AMIGO_DE]->(amigo:Pessoa)
                RETURN DISTINCT cliente.nome as cliente, amigo.nome as amigo
                LIMIT 5
            """)
            
            for i, record in enumerate(result, 1):
                print(f"{i}. {record['cliente']} pode recomendar a {record['amigo']}")
        
        neo.disconnect()
    
    print("\n" + "=" * 80)
    print("✅ RELATÓRIO CONCLUÍDO")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    gerar_relatorio_completo()
