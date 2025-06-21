# -*- coding: utf-8 -*-
"""
Janela de gerenciamento de produtos
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QLineEdit, QLabel,
                             QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit,
                             QFormLayout, QDialog, QDialogButtonBox, QMessageBox,
                             QHeaderView, QGroupBox, QCheckBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from models.produto import Produto
from models.categoria import Categoria
from models.fornecedor import Fornecedor
from utils.validators import Validators
import logging

logger = logging.getLogger(__name__)

class ProdutosWindow(QWidget):
    """Janela de gerenciamento de produtos"""
    
    def __init__(self):
        super().__init__()
        self.produto_model = Produto()
        self.categoria_model = Categoria()
        self.fornecedor_model = Fornecedor()
        self.produtos_data = []
        self.setup_ui()
        self.carregar_dados()
    
    def setup_ui(self):
        """Configurar interface"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Título
        titulo = QLabel('Gerenciamento de Produtos')
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        titulo.setFont(font)
        layout.addWidget(titulo)
        
        # Área de filtros
        filtros_group = QGroupBox('Filtros')
        filtros_layout = QHBoxLayout(filtros_group)
        
        # Busca por nome/código
        filtros_layout.addWidget(QLabel('Buscar:'))
        self.campo_busca = QLineEdit()
        self.campo_busca.setPlaceholderText('Nome ou código do produto...')
        self.campo_busca.textChanged.connect(self.filtrar_produtos)
        filtros_layout.addWidget(self.campo_busca)
        
        # Filtro por categoria
        filtros_layout.addWidget(QLabel('Categoria:'))
        self.combo_categoria_filtro = QComboBox()
        self.combo_categoria_filtro.addItem('Todas', None)
        self.combo_categoria_filtro.currentTextChanged.connect(self.filtrar_produtos)
        filtros_layout.addWidget(self.combo_categoria_filtro)
        
        # Checkbox estoque baixo
        self.check_estoque_baixo = QCheckBox('Apenas estoque baixo')
        self.check_estoque_baixo.stateChanged.connect(self.filtrar_produtos)
        filtros_layout.addWidget(self.check_estoque_baixo)
        
        layout.addWidget(filtros_group)
        
        # Botões de ação
        botoes_layout = QHBoxLayout()
        
        self.btn_novo = QPushButton('Novo Produto')
        self.btn_novo.clicked.connect(self.novo_produto)
        botoes_layout.addWidget(self.btn_novo)
        
        self.btn_editar = QPushButton('Editar')
        self.btn_editar.clicked.connect(self.editar_produto)
        self.btn_editar.setEnabled(False)
        botoes_layout.addWidget(self.btn_editar)
        
        self.btn_excluir = QPushButton('Excluir')
        self.btn_excluir.clicked.connect(self.excluir_produto)
        self.btn_excluir.setEnabled(False)
        botoes_layout.addWidget(self.btn_excluir)
        
        botoes_layout.addStretch()
        
        self.btn_atualizar = QPushButton('Atualizar')
        self.btn_atualizar.clicked.connect(self.carregar_dados)
        botoes_layout.addWidget(self.btn_atualizar)
        
        layout.addLayout(botoes_layout)
        
        # Tabela de produtos
        self.tabela = QTableWidget()
        self.tabela.setColumnCount(10)
        self.tabela.setHorizontalHeaderLabels([
            'Código', 'Nome', 'Categoria', 'Fornecedor', 'Preço Compra',
            'Preço Venda', 'Estoque Atual', 'Estoque Mínimo', 'Unidade', 'Localização'
        ])
        
        # Configurar tabela
        header = self.tabela.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # Nome do produto
        self.tabela.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabela.itemSelectionChanged.connect(self.on_selection_changed)
        self.tabela.itemDoubleClicked.connect(self.editar_produto)
        
        layout.addWidget(self.tabela)
        
        # Estilo aplicado globalmente
    
    def carregar_dados(self):
        """Carregar dados dos produtos"""
        try:
            self.produtos_data = self.produto_model.get_produtos_completos()
            self.carregar_categorias()
            self.atualizar_tabela(self.produtos_data)
        except Exception as e:
            logger.error(f"Erro ao carregar produtos: {e}")
            QMessageBox.critical(self, 'Erro', f'Erro ao carregar produtos: {e}')
    
    def carregar_categorias(self):
        """Carregar categorias no combo"""
        self.combo_categoria_filtro.clear()
        self.combo_categoria_filtro.addItem('Todas', None)
        
        categorias = self.categoria_model.get_all()
        for categoria in categorias:
            self.combo_categoria_filtro.addItem(categoria['nome'], categoria['id'])
    
    def atualizar_tabela(self, produtos):
        """Atualizar tabela com os produtos"""
        self.tabela.setRowCount(len(produtos))
        
        for row, produto in enumerate(produtos):
            self.tabela.setItem(row, 0, QTableWidgetItem(produto['codigo']))
            self.tabela.setItem(row, 1, QTableWidgetItem(produto['nome']))
            self.tabela.setItem(row, 2, QTableWidgetItem(produto.get('categoria_nome', '')))
            self.tabela.setItem(row, 3, QTableWidgetItem(produto.get('fornecedor_nome', '')))
            self.tabela.setItem(row, 4, QTableWidgetItem(f"R$ {produto['preco_compra']:.2f}"))
            self.tabela.setItem(row, 5, QTableWidgetItem(f"R$ {produto['preco_venda']:.2f}"))
            self.tabela.setItem(row, 6, QTableWidgetItem(str(produto['estoque_atual'])))
            self.tabela.setItem(row, 7, QTableWidgetItem(str(produto['estoque_minimo'])))
            self.tabela.setItem(row, 8, QTableWidgetItem(produto['unidade']))
            self.tabela.setItem(row, 9, QTableWidgetItem(produto.get('localizacao', '')))
            
            # Destacar produtos com estoque baixo
            if produto['estoque_atual'] <= produto['estoque_minimo']:
                for col in range(10):
                    item = self.tabela.item(row, col)
                    if item:
                        item.setBackground(Qt.GlobalColor.yellow)
        
        self.tabela.resizeColumnsToContents()
    
    def filtrar_produtos(self):
        """Filtrar produtos conforme critérios"""
        termo_busca = self.campo_busca.text().lower()
        categoria_id = self.combo_categoria_filtro.currentData()
        apenas_estoque_baixo = self.check_estoque_baixo.isChecked()
        
        produtos_filtrados = []
        
        for produto in self.produtos_data:
            # Filtro por termo de busca
            if termo_busca:
                if (termo_busca not in produto['nome'].lower() and 
                    termo_busca not in produto['codigo'].lower()):
                    continue
            
            # Filtro por categoria
            if categoria_id and produto['categoria_id'] != categoria_id:
                continue
            
            # Filtro por estoque baixo
            if apenas_estoque_baixo and produto['estoque_atual'] > produto['estoque_minimo']:
                continue
            
            produtos_filtrados.append(produto)
        
        self.atualizar_tabela(produtos_filtrados)
    
    def on_selection_changed(self):
        """Evento de mudança de seleção na tabela"""
        tem_selecao = len(self.tabela.selectedItems()) > 0
        self.btn_editar.setEnabled(tem_selecao)
        self.btn_excluir.setEnabled(tem_selecao)
    
    def novo_produto(self):
        """Abrir dialog para novo produto"""
        dialog = ProdutoDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.carregar_dados()
    
    def editar_produto(self):
        """Editar produto selecionado"""
        row = self.tabela.currentRow()
        if row < 0:
            return
        
        codigo = self.tabela.item(row, 0).text()
        produto = self.produto_model.get_by_codigo(codigo)
        
        if produto:
            dialog = ProdutoDialog(self, produto)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self.carregar_dados()
    
    def excluir_produto(self):
        """Excluir produto selecionado"""
        row = self.tabela.currentRow()
        if row < 0:
            return
        
        codigo = self.tabela.item(row, 0).text()
        nome = self.tabela.item(row, 1).text()
        
        reply = QMessageBox.question(
            self, 'Confirmar Exclusão',
            f'Deseja realmente excluir o produto "{nome}"?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                produto = self.produto_model.get_by_codigo(codigo)
                if produto:
                    self.produto_model.delete(produto['id'])
                    self.carregar_dados()
                    QMessageBox.information(self, 'Sucesso', 'Produto excluído com sucesso!')
            except Exception as e:
                logger.error(f"Erro ao excluir produto: {e}")
                QMessageBox.critical(self, 'Erro', f'Erro ao excluir produto: {e}')

class ProdutoDialog(QDialog):
    """Dialog para cadastro/edição de produto"""
    
    def __init__(self, parent, produto=None):
        super().__init__(parent)
        self.produto = produto
        self.produto_model = Produto()
        self.categoria_model = Categoria()
        self.fornecedor_model = Fornecedor()
        self.setup_ui()
        
        if produto:
            self.carregar_produto()
    
    def setup_ui(self):
        """Configurar interface"""
        self.setWindowTitle('Novo Produto' if not self.produto else 'Editar Produto')
        self.setFixedSize(500, 600)
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Formulário
        form_layout = QFormLayout()
        
        # Código
        self.campo_codigo = QLineEdit()
        self.campo_codigo.setMaxLength(20)
        form_layout.addRow('Código*:', self.campo_codigo)
        
        # Nome
        self.campo_nome = QLineEdit()
        self.campo_nome.setMaxLength(100)
        form_layout.addRow('Nome*:', self.campo_nome)
        
        # Descrição
        self.campo_descricao = QTextEdit()
        self.campo_descricao.setMaximumHeight(80)
        form_layout.addRow('Descrição:', self.campo_descricao)
        
        # Categoria
        self.combo_categoria = QComboBox()
        self.carregar_categorias()
        form_layout.addRow('Categoria:', self.combo_categoria)
        
        # Fornecedor
        self.combo_fornecedor = QComboBox()
        self.carregar_fornecedores()
        form_layout.addRow('Fornecedor:', self.combo_fornecedor)
        
        # Preço de compra
        self.campo_preco_compra = QDoubleSpinBox()
        self.campo_preco_compra.setMaximum(999999.99)
        self.campo_preco_compra.setDecimals(2)
        form_layout.addRow('Preço Compra:', self.campo_preco_compra)
        
        # Preço de venda
        self.campo_preco_venda = QDoubleSpinBox()
        self.campo_preco_venda.setMaximum(999999.99)
        self.campo_preco_venda.setDecimals(2)
        form_layout.addRow('Preço Venda:', self.campo_preco_venda)
        
        # Estoque mínimo
        self.campo_estoque_minimo = QSpinBox()
        self.campo_estoque_minimo.setMaximum(999999)
        form_layout.addRow('Estoque Mínimo:', self.campo_estoque_minimo)
        
        # Estoque atual
        self.campo_estoque_atual = QSpinBox()
        self.campo_estoque_atual.setMaximum(999999)
        form_layout.addRow('Estoque Atual:', self.campo_estoque_atual)
        
        # Unidade
        self.campo_unidade = QLineEdit()
        self.campo_unidade.setMaxLength(10)
        self.campo_unidade.setText('UN')
        form_layout.addRow('Unidade:', self.campo_unidade)
        
        # Localização
        self.campo_localizacao = QLineEdit()
        self.campo_localizacao.setMaxLength(50)
        form_layout.addRow('Localização:', self.campo_localizacao)
        
        layout.addLayout(form_layout)
        
        # Botões
        botoes = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        botoes.accepted.connect(self.salvar)
        botoes.rejected.connect(self.reject)
        layout.addWidget(botoes)
    
    def carregar_categorias(self):
        """Carregar categorias"""
        self.combo_categoria.addItem('Selecione...', None)
        categorias = self.categoria_model.get_all()
        for categoria in categorias:
            self.combo_categoria.addItem(categoria['nome'], categoria['id'])
    
    def carregar_fornecedores(self):
        """Carregar fornecedores"""
        self.combo_fornecedor.addItem('Selecione...', None)
        fornecedores = self.fornecedor_model.get_all()
        for fornecedor in fornecedores:
            self.combo_fornecedor.addItem(fornecedor['nome'], fornecedor['id'])
    
    def carregar_produto(self):
        """Carregar dados do produto para edição"""
        self.campo_codigo.setText(self.produto['codigo'])
        self.campo_nome.setText(self.produto['nome'])
        self.campo_descricao.setPlainText(self.produto.get('descricao', ''))
        
        # Selecionar categoria
        for i in range(self.combo_categoria.count()):
            if self.combo_categoria.itemData(i) == self.produto['categoria_id']:
                self.combo_categoria.setCurrentIndex(i)
                break
        
        # Selecionar fornecedor
        for i in range(self.combo_fornecedor.count()):
            if self.combo_fornecedor.itemData(i) == self.produto['fornecedor_id']:
                self.combo_fornecedor.setCurrentIndex(i)
                break
        
        self.campo_preco_compra.setValue(self.produto['preco_compra'])
        self.campo_preco_venda.setValue(self.produto['preco_venda'])
        self.campo_estoque_minimo.setValue(self.produto['estoque_minimo'])
        self.campo_estoque_atual.setValue(self.produto['estoque_atual'])
        self.campo_unidade.setText(self.produto['unidade'])
        self.campo_localizacao.setText(self.produto.get('localizacao', ''))
    
    def salvar(self):
        """Salvar produto"""
        # Validações
        if not Validators.validar_codigo_produto(self.campo_codigo.text()):
            QMessageBox.warning(self, 'Erro', 'Código inválido!')
            return
        
        if not self.campo_nome.text().strip():
            QMessageBox.warning(self, 'Erro', 'Nome é obrigatório!')
            return
        
        # Verificar se código já existe
        codigo_existe = self.produto_model.existe_codigo(
            self.campo_codigo.text(),
            self.produto['id'] if self.produto else None
        )
        
        if codigo_existe:
            QMessageBox.warning(self, 'Erro', 'Código já existe!')
            return
        
        try:
            # Preparar dados
            dados = {
                'codigo': self.campo_codigo.text().strip(),
                'nome': self.campo_nome.text().strip(),
                'descricao': self.campo_descricao.toPlainText().strip(),
                'categoria_id': self.combo_categoria.currentData(),
                'fornecedor_id': self.combo_fornecedor.currentData(),
                'preco_compra': self.campo_preco_compra.value(),
                'preco_venda': self.campo_preco_venda.value(),
                'estoque_minimo': self.campo_estoque_minimo.value(),
                'estoque_atual': self.campo_estoque_atual.value(),
                'unidade': self.campo_unidade.text().strip(),
                'localizacao': self.campo_localizacao.text().strip()
            }
            
            if self.produto:
                dados['id'] = self.produto['id']
            
            # Salvar
            self.produto_model.save(dados)
            
            QMessageBox.information(
                self, 'Sucesso', 
                'Produto salvo com sucesso!'
            )
            self.accept()
            
        except Exception as e:
            logger.error(f"Erro ao salvar produto: {e}")
            QMessageBox.critical(self, 'Erro', f'Erro ao salvar produto: {e}') 