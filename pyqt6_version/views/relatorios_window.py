# -*- coding: utf-8 -*-
"""
Janela de relatórios
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QComboBox, QDateEdit, QGroupBox,
                             QMessageBox, QProgressBar, QTextEdit, QCheckBox)
from PyQt6.QtCore import Qt, QDate, QThread, pyqtSignal
from PyQt6.QtGui import QFont
from models.produto import Produto
from models.movimentacao import Movimentacao
from models.categoria import Categoria
from models.fornecedor import Fornecedor
from utils.export import ExportManager
import os
import logging

logger = logging.getLogger(__name__)

class RelatoriosWindow(QWidget):
    """Janela de relatórios"""
    
    def __init__(self):
        super().__init__()
        self.produto_model = Produto()
        self.movimentacao_model = Movimentacao()
        self.categoria_model = Categoria()
        self.fornecedor_model = Fornecedor()
        self.export_manager = ExportManager()
        self.setup_ui()
    
    def setup_ui(self):
        """Configurar interface"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Título
        titulo = QLabel('Relatórios e Exportações')
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        titulo.setFont(font)
        layout.addWidget(titulo)
        
        # Grupo Relatório de Produtos
        produtos_group = QGroupBox('Relatório de Produtos')
        produtos_layout = QVBoxLayout(produtos_group)
        
        # Filtros de produtos
        filtros_produtos = QHBoxLayout()
        
        filtros_produtos.addWidget(QLabel('Categoria:'))
        self.combo_categoria = QComboBox()
        self.combo_categoria.addItem('Todas', None)
        self.carregar_categorias()
        filtros_produtos.addWidget(self.combo_categoria)
        
        filtros_produtos.addWidget(QLabel('Fornecedor:'))
        self.combo_fornecedor = QComboBox()
        self.combo_fornecedor.addItem('Todos', None)
        self.carregar_fornecedores()
        filtros_produtos.addWidget(self.combo_fornecedor)
        
        self.check_estoque_baixo = QCheckBox('Apenas estoque baixo')
        filtros_produtos.addWidget(self.check_estoque_baixo)
        
        filtros_produtos.addStretch()
        produtos_layout.addLayout(filtros_produtos)
        
        # Botões de exportação de produtos
        botoes_produtos = QHBoxLayout()
        
        self.btn_produtos_excel = QPushButton('Exportar Excel')
        self.btn_produtos_excel.clicked.connect(lambda: self.exportar_produtos('xlsx'))
        botoes_produtos.addWidget(self.btn_produtos_excel)
        
        self.btn_produtos_csv = QPushButton('Exportar CSV')
        self.btn_produtos_csv.clicked.connect(lambda: self.exportar_produtos('csv'))
        botoes_produtos.addWidget(self.btn_produtos_csv)
        
        self.btn_produtos_pdf = QPushButton('Exportar PDF')
        self.btn_produtos_pdf.clicked.connect(lambda: self.exportar_produtos('pdf'))
        botoes_produtos.addWidget(self.btn_produtos_pdf)
        
        botoes_produtos.addStretch()
        produtos_layout.addLayout(botoes_produtos)
        
        layout.addWidget(produtos_group)
        
        # Grupo Relatório de Movimentações
        movimentacoes_group = QGroupBox('Relatório de Movimentações')
        movimentacoes_layout = QVBoxLayout(movimentacoes_group)
        
        # Filtros de movimentações
        filtros_mov = QHBoxLayout()
        
        filtros_mov.addWidget(QLabel('De:'))
        self.data_inicio = QDateEdit()
        self.data_inicio.setDate(QDate.currentDate().addMonths(-1))
        filtros_mov.addWidget(self.data_inicio)
        
        filtros_mov.addWidget(QLabel('Até:'))
        self.data_fim = QDateEdit()
        self.data_fim.setDate(QDate.currentDate())
        filtros_mov.addWidget(self.data_fim)
        
        filtros_mov.addWidget(QLabel('Tipo:'))
        self.combo_tipo = QComboBox()
        self.combo_tipo.addItems(['Todos', 'Entrada', 'Saída'])
        filtros_mov.addWidget(self.combo_tipo)
        
        filtros_mov.addStretch()
        movimentacoes_layout.addLayout(filtros_mov)
        
        # Botões de exportação de movimentações
        botoes_mov = QHBoxLayout()
        
        self.btn_mov_excel = QPushButton('Exportar Excel')
        self.btn_mov_excel.clicked.connect(lambda: self.exportar_movimentacoes('xlsx'))
        botoes_mov.addWidget(self.btn_mov_excel)
        
        self.btn_mov_csv = QPushButton('Exportar CSV')
        self.btn_mov_csv.clicked.connect(lambda: self.exportar_movimentacoes('csv'))
        botoes_mov.addWidget(self.btn_mov_csv)
        
        self.btn_mov_pdf = QPushButton('Exportar PDF')
        self.btn_mov_pdf.clicked.connect(lambda: self.exportar_movimentacoes('pdf'))
        botoes_mov.addWidget(self.btn_mov_pdf)
        
        botoes_mov.addStretch()
        movimentacoes_layout.addLayout(botoes_mov)
        
        layout.addWidget(movimentacoes_group)
        
        # Grupo Relatórios Especiais
        especiais_group = QGroupBox('Relatórios Especiais')
        especiais_layout = QVBoxLayout(especiais_group)
        
        botoes_especiais = QHBoxLayout()
        
        self.btn_estoque_baixo = QPushButton('Produtos em Falta')
        self.btn_estoque_baixo.clicked.connect(self.relatorio_estoque_baixo)
        botoes_especiais.addWidget(self.btn_estoque_baixo)
        
        self.btn_valor_estoque = QPushButton('Valor do Estoque')
        self.btn_valor_estoque.clicked.connect(self.relatorio_valor_estoque)
        botoes_especiais.addWidget(self.btn_valor_estoque)
        
        self.btn_resumo_mensal = QPushButton('Resumo Mensal')
        self.btn_resumo_mensal.clicked.connect(self.relatorio_resumo_mensal)
        botoes_especiais.addWidget(self.btn_resumo_mensal)
        
        botoes_especiais.addStretch()
        especiais_layout.addLayout(botoes_especiais)
        
        layout.addWidget(especiais_group)
        
        # Barra de progresso
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Log de operações
        log_group = QGroupBox('Log de Operações')
        log_layout = QVBoxLayout(log_group)
        
        self.log_text = QTextEdit()
        self.log_text.setMaximumHeight(100)
        self.log_text.setReadOnly(True)
        log_layout.addWidget(self.log_text)
        
        layout.addWidget(log_group)
        
        # Estilo aplicado globalmente
    
    def carregar_categorias(self):
        """Carregar categorias no combo"""
        try:
            categorias = self.categoria_model.get_all()
            for categoria in categorias:
                self.combo_categoria.addItem(categoria['nome'], categoria['id'])
        except Exception as e:
            logger.error(f"Erro ao carregar categorias: {e}")
    
    def carregar_fornecedores(self):
        """Carregar fornecedores no combo"""
        try:
            fornecedores = self.fornecedor_model.get_all()
            for fornecedor in fornecedores:
                self.combo_fornecedor.addItem(fornecedor['nome'], fornecedor['id'])
        except Exception as e:
            logger.error(f"Erro ao carregar fornecedores: {e}")
    
    def log_operacao(self, mensagem):
        """Adicionar mensagem ao log"""
        self.log_text.append(f"[{QDate.currentDate().toString()}] {mensagem}")
    
    def exportar_produtos(self, formato):
        """Exportar relatório de produtos"""
        try:
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(0)
            
            # Obter filtros
            categoria_id = self.combo_categoria.currentData()
            fornecedor_id = self.combo_fornecedor.currentData()
            apenas_estoque_baixo = self.check_estoque_baixo.isChecked()
            
            # Buscar produtos
            if apenas_estoque_baixo:
                produtos = self.produto_model.get_produtos_estoque_baixo()
            else:
                filtros = {}
                if categoria_id:
                    filtros['categoria_id'] = categoria_id
                if fornecedor_id:
                    filtros['fornecedor_id'] = fornecedor_id
                
                if filtros:
                    produtos = self.produto_model.search_advanced(**filtros)
                else:
                    produtos = self.produto_model.get_produtos_completos()
            
            self.progress_bar.setValue(50)
            
            # Exportar
            arquivo = self.export_manager.export_produtos(produtos, formato)
            
            self.progress_bar.setValue(100)
            self.progress_bar.setVisible(False)
            
            self.log_operacao(f"Relatório de produtos exportado: {os.path.basename(arquivo)}")
            
            QMessageBox.information(
                self, 'Sucesso', 
                f'Relatório exportado com sucesso!\nArquivo: {arquivo}'
            )
            
        except Exception as e:
            self.progress_bar.setVisible(False)
            logger.error(f"Erro ao exportar produtos: {e}")
            QMessageBox.critical(self, 'Erro', f'Erro ao exportar produtos: {e}')
    
    def exportar_movimentacoes(self, formato):
        """Exportar relatório de movimentações"""
        try:
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(0)
            
            # Obter filtros
            data_inicio = self.data_inicio.date().toPyDate().strftime('%Y-%m-%d')
            data_fim = self.data_fim.date().toPyDate().strftime('%Y-%m-%d')
            tipo = self.combo_tipo.currentText()
            
            # Buscar movimentações
            movimentacoes = self.movimentacao_model.get_movimentacoes_periodo(data_inicio, data_fim)
            
            # Filtrar por tipo se necessário
            if tipo != 'Todos':
                movimentacoes = [m for m in movimentacoes if m['tipo'] == tipo.lower()]
            
            self.progress_bar.setValue(50)
            
            # Exportar
            arquivo = self.export_manager.export_movimentacoes(movimentacoes, formato)
            
            self.progress_bar.setValue(100)
            self.progress_bar.setVisible(False)
            
            self.log_operacao(f"Relatório de movimentações exportado: {os.path.basename(arquivo)}")
            
            QMessageBox.information(
                self, 'Sucesso', 
                f'Relatório exportado com sucesso!\nArquivo: {arquivo}'
            )
            
        except Exception as e:
            self.progress_bar.setVisible(False)
            logger.error(f"Erro ao exportar movimentações: {e}")
            QMessageBox.critical(self, 'Erro', f'Erro ao exportar movimentações: {e}')
    
    def relatorio_estoque_baixo(self):
        """Gerar relatório de produtos em falta"""
        try:
            produtos = self.produto_model.get_produtos_estoque_baixo()
            
            if not produtos:
                QMessageBox.information(
                    self, 'Informação', 
                    'Não há produtos com estoque baixo!'
                )
                return
            
            arquivo = self.export_manager.export_produtos(produtos, 'xlsx')
            
            self.log_operacao(f"Relatório de estoque baixo gerado: {os.path.basename(arquivo)}")
            
            QMessageBox.information(
                self, 'Sucesso', 
                f'Relatório de produtos em falta gerado!\nTotal: {len(produtos)} produtos\nArquivo: {arquivo}'
            )
            
        except Exception as e:
            logger.error(f"Erro ao gerar relatório de estoque baixo: {e}")
            QMessageBox.critical(self, 'Erro', f'Erro ao gerar relatório: {e}')
    
    def relatorio_valor_estoque(self):
        """Gerar relatório de valor do estoque"""
        try:
            produtos = self.produto_model.get_produtos_completos()
            
            # Calcular valores
            valor_total = 0
            dados_relatorio = []
            
            for produto in produtos:
                valor_produto = produto['preco_venda'] * produto['estoque_atual']
                valor_total += valor_produto
                
                dados_relatorio.append({
                    'Código': produto['codigo'],
                    'Produto': produto['nome'],
                    'Categoria': produto.get('categoria_nome', ''),
                    'Estoque': produto['estoque_atual'],
                    'Preço Unitário': f"R$ {produto['preco_venda']:.2f}",
                    'Valor Total': f"R$ {valor_produto:.2f}"
                })
            
            # Adicionar total
            dados_relatorio.append({
                'Código': '',
                'Produto': 'TOTAL GERAL',
                'Categoria': '',
                'Estoque': '',
                'Preço Unitário': '',
                'Valor Total': f"R$ {valor_total:.2f}"
            })
            
            arquivo = self.export_manager.export_to_excel(
                dados_relatorio, 'relatorio_valor_estoque', 'Valor do Estoque'
            )
            
            self.log_operacao(f"Relatório de valor do estoque gerado: {os.path.basename(arquivo)}")
            
            QMessageBox.information(
                self, 'Sucesso', 
                f'Relatório de valor do estoque gerado!\nValor Total: R$ {valor_total:,.2f}\nArquivo: {arquivo}'
            )
            
        except Exception as e:
            logger.error(f"Erro ao gerar relatório de valor: {e}")
            QMessageBox.critical(self, 'Erro', f'Erro ao gerar relatório: {e}')
    
    def relatorio_resumo_mensal(self):
        """Gerar relatório resumo mensal"""
        try:
            # Usar data atual para o mês
            data_atual = QDate.currentDate()
            primeiro_dia = QDate(data_atual.year(), data_atual.month(), 1)
            ultimo_dia = data_atual
            
            # Buscar movimentações do mês
            movimentacoes = self.movimentacao_model.get_movimentacoes_periodo(
                primeiro_dia.toString('yyyy-MM-dd'),
                ultimo_dia.toString('yyyy-MM-dd')
            )
            
            # Calcular estatísticas
            entradas = [m for m in movimentacoes if m['tipo'] == 'entrada']
            saidas = [m for m in movimentacoes if m['tipo'] == 'saida']
            
            total_entradas = sum(m['quantidade'] for m in entradas)
            total_saidas = sum(m['quantidade'] for m in saidas)
            valor_entradas = sum(m['valor_total'] for m in entradas)
            valor_saidas = sum(m['valor_total'] for m in saidas)
            
            # Preparar dados do relatório
            dados_resumo = [
                {'Indicador': 'Total de Movimentações', 'Valor': len(movimentacoes)},
                {'Indicador': 'Total de Entradas', 'Valor': len(entradas)},
                {'Indicador': 'Total de Saídas', 'Valor': len(saidas)},
                {'Indicador': 'Quantidade Entrada', 'Valor': total_entradas},
                {'Indicador': 'Quantidade Saída', 'Valor': total_saidas},
                {'Indicador': 'Valor Total Entradas', 'Valor': f"R$ {valor_entradas:.2f}"},
                {'Indicador': 'Valor Total Saídas', 'Valor': f"R$ {valor_saidas:.2f}"},
                {'Indicador': 'Saldo (Entrada - Saída)', 'Valor': f"R$ {valor_entradas - valor_saidas:.2f}"}
            ]
            
            arquivo = self.export_manager.export_to_excel(
                dados_resumo, 'resumo_mensal', 'Resumo Mensal'
            )
            
            self.log_operacao(f"Resumo mensal gerado: {os.path.basename(arquivo)}")
            
            QMessageBox.information(
                self, 'Sucesso', 
                f'Resumo mensal gerado!\n'
                f'Período: {primeiro_dia.toString("dd/MM/yyyy")} a {ultimo_dia.toString("dd/MM/yyyy")}\n'
                f'Total de movimentações: {len(movimentacoes)}\n'
                f'Arquivo: {arquivo}'
            )
            
        except Exception as e:
            logger.error(f"Erro ao gerar resumo mensal: {e}")
            QMessageBox.critical(self, 'Erro', f'Erro ao gerar resumo: {e}') 