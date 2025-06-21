# -*- coding: utf-8 -*-
"""
Janela de movimentações de estoque
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QLineEdit, QLabel,
                             QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit,
                             QFormLayout, QDialog, QDialogButtonBox, QMessageBox,
                             QHeaderView, QGroupBox, QDateEdit, QTabWidget)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont, QColor
from models.movimentacao import Movimentacao
from models.produto import Produto
from datetime import datetime, date
import logging

logger = logging.getLogger(__name__)

class MovimentacoesWindow(QWidget):
    """Janela de movimentações de estoque"""
    
    def __init__(self):
        super().__init__()
        self.movimentacao_model = Movimentacao()
        self.produto_model = Produto()
        self.setup_ui()
        self.carregar_dados()
    
    def setup_ui(self):
        """Configurar interface"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Título
        titulo = QLabel('Movimentações de Estoque')
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        titulo.setFont(font)
        layout.addWidget(titulo)
        
        # Tabs
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # Tab Nova Movimentação
        self.tab_nova = QWidget()
        self.setup_tab_nova()
        self.tab_widget.addTab(self.tab_nova, 'Nova Movimentação')
        
        # Tab Histórico
        self.tab_historico = QWidget()
        self.setup_tab_historico()
        self.tab_widget.addTab(self.tab_historico, 'Histórico')
    
    def setup_tab_nova(self):
        """Configurar tab de nova movimentação"""
        layout = QVBoxLayout(self.tab_nova)
        
        # Formulário de movimentação
        form_group = QGroupBox('Nova Movimentação')
        form_layout = QFormLayout(form_group)
        
        # Produto
        self.combo_produto = QComboBox()
        self.combo_produto.setEditable(True)
        self.combo_produto.currentTextChanged.connect(self.on_produto_changed)
        form_layout.addRow('Produto*:', self.combo_produto)
        
        # Tipo
        self.combo_tipo = QComboBox()
        self.combo_tipo.addItems(['Entrada', 'Saída'])
        self.combo_tipo.currentTextChanged.connect(self.on_tipo_changed)
        form_layout.addRow('Tipo*:', self.combo_tipo)
        
        # Quantidade
        self.campo_quantidade = QSpinBox()
        self.campo_quantidade.setMinimum(1)
        self.campo_quantidade.setMaximum(999999)
        self.campo_quantidade.valueChanged.connect(self.calcular_valor_total)
        form_layout.addRow('Quantidade*:', self.campo_quantidade)
        
        # Preço unitário
        self.campo_preco_unitario = QDoubleSpinBox()
        self.campo_preco_unitario.setMaximum(999999.99)
        self.campo_preco_unitario.setDecimals(2)
        self.campo_preco_unitario.valueChanged.connect(self.calcular_valor_total)
        form_layout.addRow('Preço Unitário:', self.campo_preco_unitario)
        
        # Valor total
        self.campo_valor_total = QDoubleSpinBox()
        self.campo_valor_total.setMaximum(999999.99)
        self.campo_valor_total.setDecimals(2)
        self.campo_valor_total.setEnabled(False)
        form_layout.addRow('Valor Total:', self.campo_valor_total)
        
        # Motivo
        self.campo_motivo = QLineEdit()
        self.campo_motivo.setMaxLength(100)
        form_layout.addRow('Motivo:', self.campo_motivo)
        
        # Documento
        self.campo_documento = QLineEdit()
        self.campo_documento.setMaxLength(50)
        form_layout.addRow('Documento:', self.campo_documento)
        
        # Observações
        self.campo_observacoes = QTextEdit()
        self.campo_observacoes.setMaximumHeight(60)
        form_layout.addRow('Observações:', self.campo_observacoes)
        
        layout.addWidget(form_group)
        
        # Informações do produto
        self.info_produto = QLabel('Selecione um produto para ver suas informações')
        self.info_produto.setProperty("class", "info-box")
        layout.addWidget(self.info_produto)
        
        # Botões
        botoes_layout = QHBoxLayout()
        
        self.btn_salvar = QPushButton('Registrar Movimentação')
        self.btn_salvar.clicked.connect(self.registrar_movimentacao)
        self.btn_salvar.setProperty("class", "success")
        botoes_layout.addWidget(self.btn_salvar)
        
        self.btn_limpar = QPushButton('Limpar')
        self.btn_limpar.clicked.connect(self.limpar_formulario)
        botoes_layout.addWidget(self.btn_limpar)
        
        botoes_layout.addStretch()
        layout.addLayout(botoes_layout)
        
        # Carregar produtos
        self.carregar_produtos()
    
    def setup_tab_historico(self):
        """Configurar tab de histórico"""
        layout = QVBoxLayout(self.tab_historico)
        
        # Filtros
        filtros_group = QGroupBox('Filtros')
        filtros_layout = QHBoxLayout(filtros_group)
        
        # Data início
        filtros_layout.addWidget(QLabel('De:'))
        self.data_inicio = QDateEdit()
        self.data_inicio.setDate(QDate.currentDate().addDays(-30))
        self.data_inicio.dateChanged.connect(self.filtrar_historico)
        filtros_layout.addWidget(self.data_inicio)
        
        # Data fim
        filtros_layout.addWidget(QLabel('Até:'))
        self.data_fim = QDateEdit()
        self.data_fim.setDate(QDate.currentDate())
        self.data_fim.dateChanged.connect(self.filtrar_historico)
        filtros_layout.addWidget(self.data_fim)
        
        # Tipo
        filtros_layout.addWidget(QLabel('Tipo:'))
        self.combo_tipo_filtro = QComboBox()
        self.combo_tipo_filtro.addItems(['Todos', 'Entrada', 'Saída'])
        self.combo_tipo_filtro.currentTextChanged.connect(self.filtrar_historico)
        filtros_layout.addWidget(self.combo_tipo_filtro)
        
        # Produto
        filtros_layout.addWidget(QLabel('Produto:'))
        self.combo_produto_filtro = QComboBox()
        self.combo_produto_filtro.addItem('Todos', None)
        self.combo_produto_filtro.currentTextChanged.connect(self.filtrar_historico)
        filtros_layout.addWidget(self.combo_produto_filtro)
        
        filtros_layout.addStretch()
        
        layout.addWidget(filtros_group)
        
        # Botões do histórico
        botoes_historico = QHBoxLayout()
        
        self.btn_atualizar_historico = QPushButton('Atualizar')
        self.btn_atualizar_historico.clicked.connect(self.carregar_historico)
        botoes_historico.addWidget(self.btn_atualizar_historico)
        
        botoes_historico.addStretch()
        layout.addLayout(botoes_historico)
        
        # Tabela de histórico
        self.tabela_historico = QTableWidget()
        self.tabela_historico.setColumnCount(9)
        self.tabela_historico.setHorizontalHeaderLabels([
            'Data', 'Produto', 'Código', 'Tipo', 'Quantidade', 
            'Preço Unit.', 'Valor Total', 'Motivo', 'Usuário'
        ])
        
        # Configurar tabela
        header = self.tabela_historico.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # Produto
        self.tabela_historico.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        layout.addWidget(self.tabela_historico)
    
    def carregar_produtos(self):
        """Carregar produtos nos combos"""
        try:
            produtos = self.produto_model.get_produtos_completos()
            
            # Combo principal
            self.combo_produto.clear()
            self.combo_produto.addItem('Selecione um produto...', None)
            
            # Combo filtro (só existe na tab histórico)
            if hasattr(self, 'combo_produto_filtro'):
                self.combo_produto_filtro.clear()
                self.combo_produto_filtro.addItem('Todos', None)
            
            for produto in produtos:
                texto = f"{produto['codigo']} - {produto['nome']}"
                self.combo_produto.addItem(texto, produto['id'])
                if hasattr(self, 'combo_produto_filtro'):
                    self.combo_produto_filtro.addItem(texto, produto['id'])
                
        except Exception as e:
            logger.error(f"Erro ao carregar produtos: {e}")
    
    def on_produto_changed(self):
        """Evento de mudança de produto"""
        produto_id = self.combo_produto.currentData()
        
        if produto_id:
            try:
                produto = self.produto_model.get_by_id(produto_id)
                if produto:
                    info = f"""
                    <b>Produto:</b> {produto['nome']}<br>
                    <b>Código:</b> {produto['codigo']}<br>
                    <b>Estoque Atual:</b> {produto['estoque_atual']} {produto['unidade']}<br>
                    <b>Estoque Mínimo:</b> {produto['estoque_minimo']} {produto['unidade']}<br>
                    <b>Preço Compra:</b> R$ {produto['preco_compra']:.2f}<br>
                    <b>Preço Venda:</b> R$ {produto['preco_venda']:.2f}
                    """
                    self.info_produto.setText(info)
                    
                    # Sugerir preço baseado no tipo
                    self.on_tipo_changed()
                else:
                    self.info_produto.setText('Produto não encontrado')
            except Exception as e:
                logger.error(f"Erro ao carregar informações do produto: {e}")
        else:
            self.info_produto.setText('Selecione um produto para ver suas informações')
    
    def on_tipo_changed(self):
        """Evento de mudança de tipo"""
        produto_id = self.combo_produto.currentData()
        tipo = self.combo_tipo.currentText().lower()
        
        if produto_id:
            try:
                produto = self.produto_model.get_by_id(produto_id)
                if produto:
                    if tipo == 'entrada':
                        self.campo_preco_unitario.setValue(produto['preco_compra'])
                        self.campo_motivo.setText('Compra')
                    else:  # saída
                        self.campo_preco_unitario.setValue(produto['preco_venda'])
                        self.campo_motivo.setText('Venda')
            except Exception as e:
                logger.error(f"Erro ao sugerir preço: {e}")
    
    def calcular_valor_total(self):
        """Calcular valor total"""
        quantidade = self.campo_quantidade.value()
        preco_unitario = self.campo_preco_unitario.value()
        valor_total = quantidade * preco_unitario
        self.campo_valor_total.setValue(valor_total)
    
    def registrar_movimentacao(self):
        """Registrar nova movimentação"""
        # Validações
        produto_id = self.combo_produto.currentData()
        if not produto_id:
            QMessageBox.warning(self, 'Erro', 'Selecione um produto!')
            return
        
        quantidade = self.campo_quantidade.value()
        if quantidade <= 0:
            QMessageBox.warning(self, 'Erro', 'Quantidade deve ser maior que zero!')
            return
        
        try:
            # Registrar movimentação
            tipo = self.combo_tipo.currentText().lower()
            
            mov_id = self.movimentacao_model.registrar_movimentacao(
                produto_id=produto_id,
                tipo=tipo,
                quantidade=quantidade,
                preco_unitario=self.campo_preco_unitario.value(),
                valor_total=self.campo_valor_total.value(),
                motivo=self.campo_motivo.text().strip(),
                documento=self.campo_documento.text().strip(),
                observacoes=self.campo_observacoes.toPlainText().strip(),
                usuario='Sistema'
            )
            
            QMessageBox.information(
                self, 'Sucesso', 
                f'Movimentação registrada com sucesso!\nID: {mov_id}'
            )
            
            # Limpar formulário e atualizar dados
            self.limpar_formulario()
            self.carregar_historico()
            self.on_produto_changed()  # Atualizar info do produto
            
        except Exception as e:
            logger.error(f"Erro ao registrar movimentação: {e}")
            QMessageBox.critical(self, 'Erro', f'Erro ao registrar movimentação: {e}')
    
    def limpar_formulario(self):
        """Limpar formulário"""
        self.combo_produto.setCurrentIndex(0)
        self.combo_tipo.setCurrentIndex(0)
        self.campo_quantidade.setValue(1)
        self.campo_preco_unitario.setValue(0.0)
        self.campo_valor_total.setValue(0.0)
        self.campo_motivo.clear()
        self.campo_documento.clear()
        self.campo_observacoes.clear()
    
    def carregar_dados(self):
        """Carregar dados iniciais"""
        self.carregar_historico()
        self.carregar_produtos()
    
    def carregar_historico(self):
        """Carregar histórico de movimentações"""
        try:
            movimentacoes = self.movimentacao_model.get_movimentacoes_completas(limit=100)
            self.atualizar_tabela_historico(movimentacoes)
            
        except Exception as e:
            logger.error(f"Erro ao carregar histórico: {e}")
            QMessageBox.critical(self, 'Erro', f'Erro ao carregar histórico: {e}')
    
    def atualizar_tabela_historico(self, movimentacoes):
        """Atualizar tabela de histórico"""
        self.tabela_historico.setRowCount(len(movimentacoes))
        
        for row, mov in enumerate(movimentacoes):
            # Formatizar data
            data_str = mov['data_movimentacao'][:16]  # YYYY-MM-DD HH:MM
            
            self.tabela_historico.setItem(row, 0, QTableWidgetItem(data_str))
            self.tabela_historico.setItem(row, 1, QTableWidgetItem(mov['produto_nome']))
            self.tabela_historico.setItem(row, 2, QTableWidgetItem(mov['produto_codigo']))
            self.tabela_historico.setItem(row, 3, QTableWidgetItem(mov['tipo'].title()))
            self.tabela_historico.setItem(row, 4, QTableWidgetItem(str(mov['quantidade'])))
            self.tabela_historico.setItem(row, 5, QTableWidgetItem(f"R$ {mov['preco_unitario']:.2f}"))
            self.tabela_historico.setItem(row, 6, QTableWidgetItem(f"R$ {mov['valor_total']:.2f}"))
            self.tabela_historico.setItem(row, 7, QTableWidgetItem(mov.get('motivo', '')))
            self.tabela_historico.setItem(row, 8, QTableWidgetItem(mov.get('usuario', '')))
            
            # Colorir por tipo
            if mov['tipo'] == 'entrada':
                for col in range(9):
                    item = self.tabela_historico.item(row, col)
                    if item:
                        item.setBackground(QColor(200, 255, 200))  # Verde claro para entrada
            else:  # saída
                for col in range(9):
                    item = self.tabela_historico.item(row, col)
                    if item:
                        item.setBackground(QColor(255, 200, 200))  # Rosa claro para saída
        
        self.tabela_historico.resizeColumnsToContents()
    
    def filtrar_historico(self):
        """Filtrar histórico por critérios"""
        try:
            data_inicio = self.data_inicio.date().toPyDate()
            data_fim = self.data_fim.date().toPyDate()
            
            movimentacoes = self.movimentacao_model.get_movimentacoes_periodo(
                data_inicio.strftime('%Y-%m-%d'),
                data_fim.strftime('%Y-%m-%d')
            )
            
            # Filtrar por tipo
            tipo_filtro = self.combo_tipo_filtro.currentText()
            if tipo_filtro != 'Todos':
                movimentacoes = [m for m in movimentacoes if m['tipo'] == tipo_filtro.lower()]
            
            # Filtrar por produto
            produto_id_filtro = self.combo_produto_filtro.currentData()
            if produto_id_filtro:
                movimentacoes = [m for m in movimentacoes if m['produto_id'] == produto_id_filtro]
            
            self.atualizar_tabela_historico(movimentacoes)
            
        except Exception as e:
            logger.error(f"Erro ao filtrar histórico: {e}")
            QMessageBox.critical(self, 'Erro', f'Erro ao filtrar histórico: {e}') 