# -*- coding: utf-8 -*-
"""
Dashboard com indicadores do sistema
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QLabel, QFrame, QPushButton, QTableWidget, QTableWidgetItem)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from models.produto import Produto
from models.movimentacao import Movimentacao
import logging

logger = logging.getLogger(__name__)

class DashboardWindow(QWidget):
    """Dashboard principal do sistema"""
    
    def __init__(self):
        super().__init__()
        self.produto_model = Produto()
        self.movimentacao_model = Movimentacao()
        self.setup_ui()
        self.carregar_dados()
        
        # Timer para atualizar dados
        self.timer = QTimer()
        self.timer.timeout.connect(self.carregar_dados)
        self.timer.start(60000)  # Atualizar a cada minuto
    
    def setup_ui(self):
        """Configurar interface"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Título
        titulo = QLabel('Dashboard - Controle de Estoque')
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        titulo.setFont(font)
        layout.addWidget(titulo)
        
        # Cards com indicadores
        cards_layout = QHBoxLayout()
        layout.addLayout(cards_layout)
        
        # Card Total de Produtos
        self.card_total_produtos = self.criar_card('Total de Produtos', '0', '#3498db')
        cards_layout.addWidget(self.card_total_produtos)
        
        # Card Produtos em Falta
        self.card_produtos_falta = self.criar_card('Produtos em Falta', '0', '#e74c3c')
        cards_layout.addWidget(self.card_produtos_falta)
        
        # Card Movimentações Hoje
        self.card_movimentacoes = self.criar_card('Movimentações Hoje', '0', '#2ecc71')
        cards_layout.addWidget(self.card_movimentacoes)
        
        # Card Valor Total Estoque
        self.card_valor_estoque = self.criar_card('Valor Total Estoque', 'R$ 0,00', '#f39c12')
        cards_layout.addWidget(self.card_valor_estoque)
        
        # Tabelas
        tabelas_layout = QHBoxLayout()
        layout.addLayout(tabelas_layout)
        
        # Produtos com estoque baixo
        left_frame = QFrame()
        left_frame.setFrameStyle(QFrame.Shape.Box)
        left_layout = QVBoxLayout(left_frame)
        
        label_estoque_baixo = QLabel('Produtos com Estoque Baixo')
        label_estoque_baixo.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        left_layout.addWidget(label_estoque_baixo)
        
        self.tabela_estoque_baixo = QTableWidget()
        self.tabela_estoque_baixo.setColumnCount(4)
        self.tabela_estoque_baixo.setHorizontalHeaderLabels(['Código', 'Produto', 'Atual', 'Mínimo'])
        left_layout.addWidget(self.tabela_estoque_baixo)
        
        tabelas_layout.addWidget(left_frame)
        
        # Últimas movimentações
        right_frame = QFrame()
        right_frame.setFrameStyle(QFrame.Shape.Box)
        right_layout = QVBoxLayout(right_frame)
        
        label_movimentacoes = QLabel('Últimas Movimentações')
        label_movimentacoes.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        right_layout.addWidget(label_movimentacoes)
        
        self.tabela_movimentacoes = QTableWidget()
        self.tabela_movimentacoes.setColumnCount(4)
        self.tabela_movimentacoes.setHorizontalHeaderLabels(['Data', 'Produto', 'Tipo', 'Quantidade'])
        right_layout.addWidget(self.tabela_movimentacoes)
        
        tabelas_layout.addWidget(right_frame)
        
        # Estilo aplicado globalmente
    
    def criar_card(self, titulo, valor, cor):
        """Criar card com indicador"""
        frame = QFrame()
        frame.setFrameStyle(QFrame.Shape.Box)
        
        # Definir classe CSS baseada na cor
        if cor == '#e74c3c':
            frame.setProperty("class", "card-danger")
        elif cor == '#2ecc71':
            frame.setProperty("class", "card-success")
        elif cor == '#f39c12':
            frame.setProperty("class", "card-warning")
        else:
            frame.setProperty("class", "card")
        
        layout = QVBoxLayout(frame)
        
        # Título
        label_titulo = QLabel(titulo)
        label_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_titulo.setFont(QFont("Arial", 10))
        layout.addWidget(label_titulo)
        
        # Valor
        label_valor = QLabel(valor)
        label_valor.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font_valor = QFont("Arial", 18, QFont.Weight.Bold)
        label_valor.setFont(font_valor)
        label_valor.setStyleSheet(f"color: {cor};")
        layout.addWidget(label_valor)
        
        # Armazenar referência do label do valor
        frame.label_valor = label_valor
        
        return frame
    
    def carregar_dados(self):
        """Carregar dados do dashboard"""
        try:
            # Total de produtos
            produtos = self.produto_model.get_all()
            total_produtos = len(produtos)
            self.card_total_produtos.label_valor.setText(str(total_produtos))
            
            # Produtos com estoque baixo
            produtos_estoque_baixo = self.produto_model.get_produtos_estoque_baixo()
            self.card_produtos_falta.label_valor.setText(str(len(produtos_estoque_baixo)))
            
            # Carregar tabela de estoque baixo
            self.carregar_tabela_estoque_baixo(produtos_estoque_baixo)
            
            # Movimentações recentes
            movimentacoes = self.movimentacao_model.get_movimentacoes_completas(limit=10)
            self.carregar_tabela_movimentacoes(movimentacoes)
            
            # Contar movimentações de hoje
            from datetime import date
            hoje = date.today().strftime('%Y-%m-%d')
            movimentacoes_hoje = [m for m in movimentacoes if m['data_movimentacao'].startswith(hoje)]
            self.card_movimentacoes.label_valor.setText(str(len(movimentacoes_hoje)))
            
            # Calcular valor total do estoque
            valor_total = sum(p['preco_venda'] * p['estoque_atual'] for p in produtos)
            self.card_valor_estoque.label_valor.setText(f"R$ {valor_total:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
            
        except Exception as e:
            logger.error(f"Erro ao carregar dados do dashboard: {e}")
    
    def carregar_tabela_estoque_baixo(self, produtos):
        """Carregar tabela de produtos com estoque baixo"""
        self.tabela_estoque_baixo.setRowCount(len(produtos))
        
        for row, produto in enumerate(produtos):
            self.tabela_estoque_baixo.setItem(row, 0, QTableWidgetItem(produto['codigo']))
            self.tabela_estoque_baixo.setItem(row, 1, QTableWidgetItem(produto['nome']))
            self.tabela_estoque_baixo.setItem(row, 2, QTableWidgetItem(str(produto['estoque_atual'])))
            self.tabela_estoque_baixo.setItem(row, 3, QTableWidgetItem(str(produto['estoque_minimo'])))
        
        self.tabela_estoque_baixo.resizeColumnsToContents()
    
    def carregar_tabela_movimentacoes(self, movimentacoes):
        """Carregar tabela de movimentações recentes"""
        self.tabela_movimentacoes.setRowCount(len(movimentacoes))
        
        for row, mov in enumerate(movimentacoes):
            # Formatizar data
            data_str = mov['data_movimentacao'][:16]  # YYYY-MM-DD HH:MM
            
            self.tabela_movimentacoes.setItem(row, 0, QTableWidgetItem(data_str))
            self.tabela_movimentacoes.setItem(row, 1, QTableWidgetItem(mov['produto_nome']))
            self.tabela_movimentacoes.setItem(row, 2, QTableWidgetItem(mov['tipo'].title()))
            self.tabela_movimentacoes.setItem(row, 3, QTableWidgetItem(str(mov['quantidade'])))
        
        self.tabela_movimentacoes.resizeColumnsToContents() 