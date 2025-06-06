#!/usr/bin/env python3
"""
Script automático para resetar a database e gerar dados de teste
"""

import os
import json
from datetime import datetime, timedelta
from models import InventoryManager

def reset_database():
    """Limpar e resetar a database"""
    print("🗑️ Limpando database...")
    
    # Caminhos dos arquivos de dados
    data_files = [
        'data/products.json',
        'data/categories.json', 
        'data/suppliers.json',
        'data/movements.json'
    ]
    
    # Remover arquivos existentes
    for file_path in data_files:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"   ✅ {file_path} removido")
    
    print("✅ Database limpa!")

def generate_sample_data():
    """Gerar dados de teste"""
    print("\n📝 Gerando dados de teste...")
    
    # Criar manager
    manager = InventoryManager()
    
    # Gerar categorias
    categories = [
        {"name": "Eletrônicos", "description": "Produtos eletrônicos e tecnologia"},
        {"name": "Roupas", "description": "Vestuário em geral"},
        {"name": "Casa e Jardim", "description": "Produtos para casa e jardim"},
        {"name": "Livros", "description": "Livros e materiais educativos"},
        {"name": "Esportes", "description": "Artigos esportivos"}
    ]
    
    for cat in categories:
        manager.add_category(cat)
    print(f"   ✅ {len(categories)} categorias criadas")
    
    # Gerar fornecedores
    suppliers = [
        {
            "name": "TechCorp", 
            "contact": "João Silva", 
            "phone": "(11) 9999-1111", 
            "email": "joao@techcorp.com"
        },
        {
            "name": "Fashion Store", 
            "contact": "Maria Santos", 
            "phone": "(11) 9999-2222", 
            "email": "maria@fashionstore.com"
        },
        {
            "name": "Casa & Cia", 
            "contact": "Pedro Oliveira", 
            "phone": "(11) 9999-3333", 
            "email": "pedro@casaecia.com"
        },
        {
            "name": "Livraria Central", 
            "contact": "Ana Costa", 
            "phone": "(11) 9999-4444", 
            "email": "ana@livrariacentral.com"
        },
        {
            "name": "SportMax", 
            "contact": "Carlos Lima", 
            "phone": "(11) 9999-5555", 
            "email": "carlos@sportmax.com"
        }
    ]
    
    for sup in suppliers:
        manager.add_supplier(sup)
    print(f"   ✅ {len(suppliers)} fornecedores criados")
    
    # Gerar produtos
    products_data = [
        {"code": "PROD001", "name": "Smartphone Samsung", "category": "Eletrônicos", "price": 899.90, "min_stock": 5, "supplier": "TechCorp", "quantity": 0, "description": "Smartphone Samsung Galaxy"},
        {"code": "PROD002", "name": "Notebook Dell", "category": "Eletrônicos", "price": 2499.90, "min_stock": 3, "supplier": "TechCorp", "quantity": 0, "description": "Notebook Dell Inspiron"},
        {"code": "PROD003", "name": "Camiseta Básica", "category": "Roupas", "price": 29.90, "min_stock": 20, "supplier": "Fashion Store", "quantity": 0, "description": "Camiseta básica 100% algodão"},
        {"code": "PROD004", "name": "Jeans Masculino", "category": "Roupas", "price": 89.90, "min_stock": 10, "supplier": "Fashion Store", "quantity": 0, "description": "Jeans masculino azul"},
        {"code": "PROD005", "name": "Mesa de Jantar", "category": "Casa e Jardim", "price": 599.90, "min_stock": 2, "supplier": "Casa & Cia", "quantity": 0, "description": "Mesa de jantar 6 lugares"},
        {"code": "PROD006", "name": "Cadeira de Escritório", "category": "Casa e Jardim", "price": 299.90, "min_stock": 5, "supplier": "Casa & Cia", "quantity": 0, "description": "Cadeira ergonômica"},
        {"code": "PROD007", "name": "Python para Iniciantes", "category": "Livros", "price": 45.90, "min_stock": 15, "supplier": "Livraria Central", "quantity": 0, "description": "Livro de programação Python"},
        {"code": "PROD008", "name": "JavaScript Avançado", "category": "Livros", "price": 65.90, "min_stock": 10, "supplier": "Livraria Central", "quantity": 0, "description": "Livro JavaScript ES6+"},
        {"code": "PROD009", "name": "Tênis Running", "category": "Esportes", "price": 199.90, "min_stock": 8, "supplier": "SportMax", "quantity": 0, "description": "Tênis para corrida"},
        {"code": "PROD010", "name": "Bola de Futebol", "category": "Esportes", "price": 49.90, "min_stock": 12, "supplier": "SportMax", "quantity": 0, "description": "Bola oficial FIFA"}
    ]
    
    for prod in products_data:
        success = manager.add_product(prod)
        if success:
            # Adicionar quantidade inicial aleatória
            import random
            initial_qty = random.randint(prod["min_stock"], prod["min_stock"] * 3)
            manager.update_stock(prod["code"], initial_qty, "Estoque inicial")
    
    print(f"   ✅ {len(products_data)} produtos criados")
    
    # Gerar algumas movimentações adicionais
    print("\n📊 Gerando movimentações de teste...")
    
    import random
    movement_count = 0
    
    for _ in range(30):  # 30 movimentações aleatórias
        # Escolher produto aleatório
        if manager.products:
            product = random.choice(manager.products)
            code = product["code"]
            current_qty = product.get("quantity", 0)
            
            # Tipo de movimentação
            if current_qty > 5:
                # Saída se tiver estoque
                movement_type = random.choice(["entrada", "saída"])
            else:
                # Só entrada se estoque baixo
                movement_type = "entrada"
            
            if movement_type == "entrada":
                qty = random.randint(5, 20)
                reason = random.choice([
                    "Compra de fornecedor",
                    "Reposição de estoque",
                    "Transferência interna",
                    "Correção de inventário"
                ])
                # Para entrada, usar quantidade positiva
                manager.update_stock(code, qty, reason)
            else:
                qty = random.randint(1, min(5, current_qty))
                reason = random.choice([
                    "Venda ao cliente",
                    "Transferência para filial",
                    "Produto danificado",
                    "Amostra grátis"
                ])
                # Para saída, usar quantidade negativa
                manager.update_stock(code, -qty, reason)
            
            movement_count += 1
    
    print(f"   ✅ {movement_count} movimentações criadas")
    
    print("\n🎉 Dados de teste gerados com sucesso!")
    print("\n📊 Resumo:")
    print(f"   • Categorias: {len(manager.categories)}")
    print(f"   • Fornecedores: {len(manager.suppliers)}")
    print(f"   • Produtos: {len(manager.products)}")
    print(f"   • Movimentações: {len(manager.movements)}")

def main():
    """Função principal - execução automática"""
    print("🔄 Reset Automático do Sistema de Controle de Estoque")
    print("=" * 60)
    
    # Resetar database automaticamente
    reset_database()
    
    # Gerar dados de teste
    generate_sample_data()
    
    print("\n✅ Reset automático completo!")
    print("💡 Execute 'python main_modular.py' para testar.")

if __name__ == "__main__":
    main() 