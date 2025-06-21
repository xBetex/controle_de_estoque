#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para gerar dados de exemplo para o sistema de controle de estoque
"""

import sys
import random
from datetime import datetime, timedelta
from pathlib import Path

# Adicionar o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent))

from utils.database import DatabaseManager
from models.categoria import Categoria
from models.fornecedor import Fornecedor
from models.produto import Produto
from models.movimentacao import Movimentacao

def gerar_dados_exemplo():
    """Gerar dados de exemplo para o sistema"""
    print("🎯 Gerando dados de exemplo para o Sistema de Controle de Estoque...")
    
    # Inicializar modelos
    categoria_model = Categoria()
    fornecedor_model = Fornecedor()
    produto_model = Produto()
    movimentacao_model = Movimentacao()
    
    print("\n📂 Criando categorias...")
    
    # Categorias de exemplo
    categorias = [
        {'nome': 'Eletrônicos', 'descricao': 'Produtos eletrônicos e gadgets'},
        {'nome': 'Informática', 'descricao': 'Computadores, periféricos e acessórios'},
        {'nome': 'Móveis', 'descricao': 'Móveis para escritório e casa'},
        {'nome': 'Papelaria', 'descricao': 'Materiais de escritório e papelaria'},
        {'nome': 'Limpeza', 'descricao': 'Produtos de limpeza e higiene'},
        {'nome': 'Alimentação', 'descricao': 'Alimentos e bebidas'},
        {'nome': 'Ferramentas', 'descricao': 'Ferramentas e equipamentos'},
        {'nome': 'Vestuário', 'descricao': 'Roupas e acessórios'},
    ]
    
    categorias_ids = {}
    for cat in categorias:
        try:
            cat_id = categoria_model.save(cat)
            categorias_ids[cat['nome']] = cat_id
            print(f"  ✓ {cat['nome']}")
        except Exception as e:
            print(f"  ❌ Erro ao criar categoria {cat['nome']}: {e}")
    
    print(f"\n🏢 Criando fornecedores...")
    
    # Fornecedores de exemplo
    fornecedores = [
        {
            'nome': 'TechSupply Ltda',
            'cnpj': '12.345.678/0001-90',
            'telefone': '(11) 3333-4444',
            'email': 'vendas@techsupply.com.br',
            'endereco': 'Rua das Tecnologias, 123',
            'cidade': 'São Paulo',
            'estado': 'SP',
            'cep': '01234-567',
            'contato': 'João Silva'
        },
        {
            'nome': 'Móveis & Cia',
            'cnpj': '98.765.432/0001-10',
            'telefone': '(11) 5555-6666',
            'email': 'contato@moveisecia.com.br',
            'endereco': 'Av. dos Móveis, 456',
            'cidade': 'São Paulo',
            'estado': 'SP',
            'cep': '02345-678',
            'contato': 'Maria Santos'
        },
        {
            'nome': 'Papelaria Central',
            'cnpj': '11.222.333/0001-44',
            'telefone': '(11) 7777-8888',
            'email': 'vendas@papelariacentral.com.br',
            'endereco': 'Rua do Papel, 789',
            'cidade': 'Rio de Janeiro',
            'estado': 'RJ',
            'cep': '20123-456',
            'contato': 'Pedro Oliveira'
        },
        {
            'nome': 'CleanMax Produtos',
            'cnpj': '55.666.777/0001-88',
            'telefone': '(11) 9999-0000',
            'email': 'info@cleanmax.com.br',
            'endereco': 'Av. da Limpeza, 321',
            'cidade': 'Belo Horizonte',
            'estado': 'MG',
            'cep': '30123-789',
            'contato': 'Ana Costa'
        },
        {
            'nome': 'AlimentaBem Distribuidora',
            'cnpj': '33.444.555/0001-22',
            'telefone': '(11) 1111-2222',
            'email': 'pedidos@alimentabem.com.br',
            'endereco': 'Rua dos Alimentos, 654',
            'cidade': 'Curitiba',
            'estado': 'PR',
            'cep': '80123-456',
            'contato': 'Carlos Ferreira'
        }
    ]
    
    fornecedores_ids = {}
    for forn in fornecedores:
        try:
            forn_id = fornecedor_model.save(forn)
            fornecedores_ids[forn['nome']] = forn_id
            print(f"  ✓ {forn['nome']}")
        except Exception as e:
            print(f"  ❌ Erro ao criar fornecedor {forn['nome']}: {e}")
    
    print(f"\n📦 Criando produtos...")
    
    # Produtos de exemplo
    produtos = [
        # Eletrônicos
        {
            'codigo': 'ELE001',
            'nome': 'Smartphone Samsung Galaxy',
            'descricao': 'Smartphone com 128GB de armazenamento',
            'categoria': 'Eletrônicos',
            'fornecedor': 'TechSupply Ltda',
            'preco_compra': 800.00,
            'preco_venda': 1200.00,
            'estoque_minimo': 5,
            'estoque_atual': 15,
            'unidade': 'UN',
            'localizacao': 'A1-01'
        },
        {
            'codigo': 'ELE002',
            'nome': 'Fone de Ouvido Bluetooth',
            'descricao': 'Fone sem fio com cancelamento de ruído',
            'categoria': 'Eletrônicos',
            'fornecedor': 'TechSupply Ltda',
            'preco_compra': 150.00,
            'preco_venda': 250.00,
            'estoque_minimo': 10,
            'estoque_atual': 8,
            'unidade': 'UN',
            'localizacao': 'A1-02'
        },
        # Informática
        {
            'codigo': 'INF001',
            'nome': 'Notebook Lenovo ThinkPad',
            'descricao': 'Notebook profissional i7 16GB RAM',
            'categoria': 'Informática',
            'fornecedor': 'TechSupply Ltda',
            'preco_compra': 2500.00,
            'preco_venda': 3500.00,
            'estoque_minimo': 3,
            'estoque_atual': 7,
            'unidade': 'UN',
            'localizacao': 'B1-01'
        },
        {
            'codigo': 'INF002',
            'nome': 'Mouse Gamer RGB',
            'descricao': 'Mouse óptico com iluminação RGB',
            'categoria': 'Informática',
            'fornecedor': 'TechSupply Ltda',
            'preco_compra': 80.00,
            'preco_venda': 120.00,
            'estoque_minimo': 15,
            'estoque_atual': 25,
            'unidade': 'UN',
            'localizacao': 'B1-02'
        },
        {
            'codigo': 'INF003',
            'nome': 'Teclado Mecânico',
            'descricao': 'Teclado mecânico com switches blue',
            'categoria': 'Informática',
            'fornecedor': 'TechSupply Ltda',
            'preco_compra': 200.00,
            'preco_venda': 300.00,
            'estoque_minimo': 8,
            'estoque_atual': 12,
            'unidade': 'UN',
            'localizacao': 'B1-03'
        },
        # Móveis
        {
            'codigo': 'MOV001',
            'nome': 'Cadeira Ergonômica',
            'descricao': 'Cadeira de escritório com apoio lombar',
            'categoria': 'Móveis',
            'fornecedor': 'Móveis & Cia',
            'preco_compra': 300.00,
            'preco_venda': 450.00,
            'estoque_minimo': 5,
            'estoque_atual': 12,
            'unidade': 'UN',
            'localizacao': 'C1-01'
        },
        {
            'codigo': 'MOV002',
            'nome': 'Mesa de Escritório',
            'descricao': 'Mesa em MDF com gavetas',
            'categoria': 'Móveis',
            'fornecedor': 'Móveis & Cia',
            'preco_compra': 250.00,
            'preco_venda': 400.00,
            'estoque_minimo': 3,
            'estoque_atual': 8,
            'unidade': 'UN',
            'localizacao': 'C1-02'
        },
        # Papelaria
        {
            'codigo': 'PAP001',
            'nome': 'Papel A4 500 folhas',
            'descricao': 'Resma de papel A4 branco',
            'categoria': 'Papelaria',
            'fornecedor': 'Papelaria Central',
            'preco_compra': 18.00,
            'preco_venda': 25.00,
            'estoque_minimo': 50,
            'estoque_atual': 120,
            'unidade': 'PCT',
            'localizacao': 'D1-01'
        },
        {
            'codigo': 'PAP002',
            'nome': 'Caneta Esferográfica Azul',
            'descricao': 'Caneta esferográfica ponta média',
            'categoria': 'Papelaria',
            'fornecedor': 'Papelaria Central',
            'preco_compra': 1.50,
            'preco_venda': 2.50,
            'estoque_minimo': 100,
            'estoque_atual': 250,
            'unidade': 'UN',
            'localizacao': 'D1-02'
        },
        {
            'codigo': 'PAP003',
            'nome': 'Grampeador Médio',
            'descricao': 'Grampeador para até 25 folhas',
            'categoria': 'Papelaria',
            'fornecedor': 'Papelaria Central',
            'preco_compra': 25.00,
            'preco_venda': 40.00,
            'estoque_minimo': 10,
            'estoque_atual': 18,
            'unidade': 'UN',
            'localizacao': 'D1-03'
        },
        # Limpeza
        {
            'codigo': 'LMP001',
            'nome': 'Detergente Neutro 5L',
            'descricao': 'Detergente neutro concentrado',
            'categoria': 'Limpeza',
            'fornecedor': 'CleanMax Produtos',
            'preco_compra': 15.00,
            'preco_venda': 22.00,
            'estoque_minimo': 20,
            'estoque_atual': 45,
            'unidade': 'UN',
            'localizacao': 'E1-01'
        },
        {
            'codigo': 'LMP002',
            'nome': 'Papel Higiênico 12 rolos',
            'descricao': 'Papel higiênico folha dupla',
            'categoria': 'Limpeza',
            'fornecedor': 'CleanMax Produtos',
            'preco_compra': 12.00,
            'preco_venda': 18.00,
            'estoque_minimo': 30,
            'estoque_atual': 2,  # Estoque baixo para demonstrar alerta
            'unidade': 'PCT',
            'localizacao': 'E1-02'
        },
        # Alimentação
        {
            'codigo': 'ALI001',
            'nome': 'Café Premium 500g',
            'descricao': 'Café torrado e moído premium',
            'categoria': 'Alimentação',
            'fornecedor': 'AlimentaBem Distribuidora',
            'preco_compra': 18.00,
            'preco_venda': 28.00,
            'estoque_minimo': 25,
            'estoque_atual': 60,
            'unidade': 'PCT',
            'localizacao': 'F1-01'
        },
        {
            'codigo': 'ALI002',
            'nome': 'Água Mineral 20L',
            'descricao': 'Galão de água mineral',
            'categoria': 'Alimentação',
            'fornecedor': 'AlimentaBem Distribuidora',
            'preco_compra': 8.00,
            'preco_venda': 12.00,
            'estoque_minimo': 15,
            'estoque_atual': 1,  # Estoque baixo
            'unidade': 'UN',
            'localizacao': 'F1-02'
        }
    ]
    
    produtos_ids = {}
    for prod in produtos:
        try:
            # Buscar IDs das categorias e fornecedores
            categoria_id = categorias_ids.get(prod['categoria'])
            fornecedor_id = fornecedores_ids.get(prod['fornecedor'])
            
            produto_data = {
                'codigo': prod['codigo'],
                'nome': prod['nome'],
                'descricao': prod['descricao'],
                'categoria_id': categoria_id,
                'fornecedor_id': fornecedor_id,
                'preco_compra': prod['preco_compra'],
                'preco_venda': prod['preco_venda'],
                'estoque_minimo': prod['estoque_minimo'],
                'estoque_atual': prod['estoque_atual'],
                'unidade': prod['unidade'],
                'localizacao': prod['localizacao']
            }
            
            prod_id = produto_model.save(produto_data)
            produtos_ids[prod['codigo']] = prod_id
            print(f"  ✓ {prod['codigo']} - {prod['nome']}")
        except Exception as e:
            print(f"  ❌ Erro ao criar produto {prod['codigo']}: {e}")
    
    print(f"\n📊 Criando movimentações de estoque...")
    
    # Gerar movimentações dos últimos 30 dias
    data_base = datetime.now() - timedelta(days=30)
    
    movimentacoes = [
        # Entradas iniciais (simulando compras)
        {'produto': 'ELE001', 'tipo': 'entrada', 'quantidade': 20, 'dias_atras': 25, 'motivo': 'Compra inicial'},
        {'produto': 'ELE002', 'tipo': 'entrada', 'quantidade': 15, 'dias_atras': 25, 'motivo': 'Compra inicial'},
        {'produto': 'INF001', 'tipo': 'entrada', 'quantidade': 10, 'dias_atras': 25, 'motivo': 'Compra inicial'},
        {'produto': 'INF002', 'tipo': 'entrada', 'quantidade': 30, 'dias_atras': 25, 'motivo': 'Compra inicial'},
        {'produto': 'MOV001', 'tipo': 'entrada', 'quantidade': 15, 'dias_atras': 20, 'motivo': 'Reposição estoque'},
        {'produto': 'PAP001', 'tipo': 'entrada', 'quantidade': 100, 'dias_atras': 20, 'motivo': 'Compra mensal'},
        
        # Saídas (vendas)
        {'produto': 'ELE001', 'tipo': 'saida', 'quantidade': 5, 'dias_atras': 15, 'motivo': 'Venda cliente'},
        {'produto': 'ELE002', 'tipo': 'saida', 'quantidade': 7, 'dias_atras': 12, 'motivo': 'Venda cliente'},
        {'produto': 'INF001', 'tipo': 'saida', 'quantidade': 3, 'dias_atras': 10, 'motivo': 'Venda corporativa'},
        {'produto': 'INF002', 'tipo': 'saida', 'quantidade': 5, 'dias_atras': 8, 'motivo': 'Venda cliente'},
        {'produto': 'MOV001', 'tipo': 'saida', 'quantidade': 3, 'dias_atras': 7, 'motivo': 'Venda cliente'},
        {'produto': 'PAP001', 'tipo': 'saida', 'quantidade': 30, 'dias_atras': 5, 'motivo': 'Uso interno'},
        {'produto': 'LMP002', 'tipo': 'saida', 'quantidade': 28, 'dias_atras': 3, 'motivo': 'Consumo alto'},
        {'produto': 'ALI002', 'tipo': 'saida', 'quantidade': 14, 'dias_atras': 2, 'motivo': 'Consumo escritório'},
        
        # Movimentações recentes
        {'produto': 'INF003', 'tipo': 'entrada', 'quantidade': 15, 'dias_atras': 1, 'motivo': 'Nova remessa'},
        {'produto': 'PAP002', 'tipo': 'saida', 'quantidade': 50, 'dias_atras': 1, 'motivo': 'Pedido grande'},
    ]
    
    for mov in movimentacoes:
        try:
            produto_id = produtos_ids.get(mov['produto'])
            if not produto_id:
                continue
            
            # Buscar dados do produto para calcular preço
            produto = produto_model.get_by_id(produto_id)
            if not produto:
                continue
            
            # Definir preço baseado no tipo
            if mov['tipo'] == 'entrada':
                preco_unitario = produto['preco_compra']
            else:
                preco_unitario = produto['preco_venda']
            
            valor_total = mov['quantidade'] * preco_unitario
            
            # Data da movimentação
            data_mov = data_base + timedelta(days=mov['dias_atras'])
            
            movimentacao_model.registrar_movimentacao(
                produto_id=produto_id,
                tipo=mov['tipo'],
                quantidade=mov['quantidade'],
                preco_unitario=preco_unitario,
                valor_total=valor_total,
                motivo=mov['motivo'],
                documento=f"DOC{random.randint(1000, 9999)}",
                observacoes=f"Movimentação de exemplo - {mov['motivo']}",
                data_movimentacao=data_mov,
                usuario="Sistema"
            )
            
            print(f"  ✓ {mov['produto']} - {mov['tipo'].title()}: {mov['quantidade']} unidades")
            
        except Exception as e:
            print(f"  ❌ Erro ao criar movimentação {mov['produto']}: {e}")
    
    print(f"\n🎉 Dados de exemplo criados com sucesso!")
    print(f"\n📊 Resumo:")
    print(f"  • {len(categorias)} categorias")
    print(f"  • {len(fornecedores)} fornecedores")
    print(f"  • {len(produtos)} produtos")
    print(f"  • {len(movimentacoes)} movimentações")
    
    print(f"\n💡 Recursos para testar:")
    print(f"  • Dashboard mostra indicadores")
    print(f"  • Produtos com estoque baixo: Papel Higiênico, Água Mineral")
    print(f"  • Histórico de movimentações dos últimos 30 dias")
    print(f"  • Relatórios com dados reais")
    
    print(f"\n🚀 Execute: python main.py")

if __name__ == "__main__":
    try:
        # Inicializar banco de dados primeiro
        db_manager = DatabaseManager()
        db_manager.initialize_database()
        
        # Gerar dados de exemplo
        gerar_dados_exemplo()
        
    except Exception as e:
        print(f"❌ Erro ao gerar dados de exemplo: {e}")
        sys.exit(1)