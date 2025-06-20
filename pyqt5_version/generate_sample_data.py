#!/usr/bin/env python3
"""
Sample data generator for PyQt5 Inventory Management System
"""

import sys
import os
from datetime import datetime, timedelta
import random

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models import InventoryManager

def generate_sample_data():
    """Generate sample data for testing"""
    print("Gerando dados de exemplo...")
    
    # Create inventory manager
    manager = InventoryManager()
    
    # Sample categories
    categories = [
        {"name": "Eletrônicos", "description": "Produtos eletrônicos e tecnologia"},
        {"name": "Roupas", "description": "Vestuário e acessórios"},
        {"name": "Casa e Jardim", "description": "Produtos para casa e jardim"},
        {"name": "Esportes", "description": "Artigos esportivos"},
        {"name": "Livros", "description": "Livros e material educativo"},
    ]
    
    print("Criando categorias...")
    for category in categories:
        success = manager.add_category(category)
        if success:
            print(f"  ✓ Categoria '{category['name']}' criada")
        else:
            print(f"  ✗ Erro ao criar categoria '{category['name']}'")
    
    # Sample suppliers
    suppliers = [
        {
            "name": "TechCorp Ltda",
            "email": "vendas@techcorp.com.br",
            "phone": "(11) 1234-5678",
            "address": "Rua da Tecnologia, 123 - São Paulo, SP"
        },
        {
            "name": "Moda Brasil S/A",
            "email": "comercial@modabrasil.com.br",
            "phone": "(21) 2345-6789",
            "address": "Av. Fashion, 456 - Rio de Janeiro, RJ"
        },
        {
            "name": "Casa & Cia",
            "email": "contato@casaecia.com.br",
            "phone": "(31) 3456-7890",
            "address": "Rua do Lar, 789 - Belo Horizonte, MG"
        },
        {
            "name": "Esportes Total",
            "email": "info@esportestotal.com.br",
            "phone": "(41) 4567-8901",
            "address": "Av. Olímpica, 321 - Curitiba, PR"
        },
        {
            "name": "Editora Saber",
            "email": "vendas@editorasaber.com.br",
            "phone": "(51) 5678-9012",
            "address": "Rua dos Livros, 654 - Porto Alegre, RS"
        }
    ]
    
    print("Criando fornecedores...")
    for supplier in suppliers:
        success = manager.add_supplier(supplier)
        if success:
            print(f"  ✓ Fornecedor '{supplier['name']}' criado")
        else:
            print(f"  ✗ Erro ao criar fornecedor '{supplier['name']}'")
    
    # Sample products
    products = [
        # Electronics
        {"code": "SMART001", "name": "Smartphone Galaxy", "category": "Eletrônicos", "supplier": "TechCorp Ltda", "price": 899.99, "quantity": 25},
        {"code": "LAP001", "name": "Laptop Professional", "category": "Eletrônicos", "supplier": "TechCorp Ltda", "price": 2499.99, "quantity": 10},
        {"code": "TAB001", "name": "Tablet 10 polegadas", "category": "Eletrônicos", "supplier": "TechCorp Ltda", "price": 699.99, "quantity": 15},
        {"code": "HDPHN001", "name": "Fone de Ouvido Bluetooth", "category": "Eletrônicos", "supplier": "TechCorp Ltda", "price": 149.99, "quantity": 50},
        
        # Clothes
        {"code": "CAMS001", "name": "Camisa Social Branca", "category": "Roupas", "supplier": "Moda Brasil S/A", "price": 79.99, "quantity": 30},
        {"code": "CALC001", "name": "Calça Jeans", "category": "Roupas", "supplier": "Moda Brasil S/A", "price": 129.99, "quantity": 20},
        {"code": "VEST001", "name": "Vestido Casual", "category": "Roupas", "supplier": "Moda Brasil S/A", "price": 89.99, "quantity": 25},
        {"code": "TEN001", "name": "Tênis Esportivo", "category": "Roupas", "supplier": "Moda Brasil S/A", "price": 199.99, "quantity": 18},
        
        # Home & Garden
        {"code": "MESA001", "name": "Mesa de Jantar 6 lugares", "category": "Casa e Jardim", "supplier": "Casa & Cia", "price": 599.99, "quantity": 5},
        {"code": "CADE001", "name": "Cadeira Escritório", "category": "Casa e Jardim", "supplier": "Casa & Cia", "price": 299.99, "quantity": 12},
        {"code": "LAMP001", "name": "Luminária de Mesa", "category": "Casa e Jardim", "supplier": "Casa & Cia", "price": 89.99, "quantity": 20},
        {"code": "VASOS001", "name": "Vaso Decorativo", "category": "Casa e Jardim", "supplier": "Casa & Cia", "price": 45.99, "quantity": 35},
        
        # Sports
        {"code": "BOLA001", "name": "Bola de Futebol", "category": "Esportes", "supplier": "Esportes Total", "price": 49.99, "quantity": 40},
        {"code": "RAQ001", "name": "Raquete de Tênis", "category": "Esportes", "supplier": "Esportes Total", "price": 179.99, "quantity": 15},
        {"code": "BIKE001", "name": "Bicicleta Mountain Bike", "category": "Esportes", "supplier": "Esportes Total", "price": 899.99, "quantity": 8},
        {"code": "HALTER001", "name": "Kit Halteres", "category": "Esportes", "supplier": "Esportes Total", "price": 299.99, "quantity": 10},
        
        # Books
        {"code": "LIV001", "name": "Python Programming", "category": "Livros", "supplier": "Editora Saber", "price": 89.99, "quantity": 25},
        {"code": "LIV002", "name": "Gestão de Projetos", "category": "Livros", "supplier": "Editora Saber", "price": 79.99, "quantity": 30},
        {"code": "LIV003", "name": "Marketing Digital", "category": "Livros", "supplier": "Editora Saber", "price": 69.99, "quantity": 22},
        {"code": "LIV004", "name": "Contabilidade Básica", "category": "Livros", "supplier": "Editora Saber", "price": 59.99, "quantity": 18},
    ]
    
    print("Criando produtos...")
    for product in products:
        success = manager.add_product(product)
        if success:
            print(f"  ✓ Produto '{product['name']}' criado")
        else:
            print(f"  ✗ Erro ao criar produto '{product['name']}'")
    
    # Generate some sample movements
    print("Gerando movimentações de exemplo...")
    movement_types = ["entrada", "saída"]
    reasons = [
        "Compra de fornecedor",
        "Venda para cliente",
        "Ajuste de inventário",
        "Devolução de cliente",
        "Transferência entre filiais",
        "Produto danificado",
        "Amostra grátis"
    ]
    
    # Get all products
    all_products = manager.get_all_products()
    
    # Generate 50 random movements over the last 30 days
    for _ in range(50):
        if not all_products:
            break
            
        product = random.choice(all_products)
        movement_type = random.choice(movement_types)
        reason = random.choice(reasons)
        quantity = random.randint(1, 5)
        
        # Adjust quantity for exits to not go negative
        if movement_type == "saída":
            current_qty = product.get('quantity', 0)
            if current_qty > 0:
                quantity = min(quantity, current_qty)
                manager.update_stock(product['code'], -quantity, reason)
        else:
            manager.update_stock(product['code'], quantity, reason)
    
    print("✓ Dados de exemplo gerados com sucesso!")
    print("\nEstatísticas:")
    
    # Print statistics
    stats = manager.get_dashboard_stats()
    print(f"  • Total de produtos: {stats['total_products']}")
    print(f"  • Total de itens em estoque: {stats['total_items']}")
    print(f"  • Valor total do estoque: R$ {stats['total_value']:,.2f}")
    print(f"  • Produtos com estoque baixo: {stats['low_stock_count']}")
    print(f"  • Total de fornecedores: {stats['total_suppliers']}")
    print(f"  • Total de categorias: {stats['total_categories']}")

def main():
    """Main function"""
    print("=" * 60)
    print("GERADOR DE DADOS DE EXEMPLO")
    print("Sistema de Controle de Estoque - PyQt5")
    print("=" * 60)
    
    try:
        response = input("Deseja gerar dados de exemplo? (s/N): ").lower().strip()
        
        if response in ['s', 'sim', 'y', 'yes']:
            generate_sample_data()
        else:
            print("Operação cancelada.")
            
    except KeyboardInterrupt:
        print("\nOperação cancelada pelo usuário.")
    except Exception as e:
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()
    
    input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    main() 