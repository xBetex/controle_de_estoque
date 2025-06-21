# -*- coding: utf-8 -*-
"""
Janela de gerenciamento de categorias
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QLineEdit, QLabel,
                             QTextEdit, QFormLayout, QDialog, QDialogButtonBox, 
                             QMessageBox, QHeaderView)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from models.categoria import Categoria
import logging

logger = logging.getLogger(__name__)

class CategoriasWindow(QWidget):
    """Janela de gerenciamento de categorias"""
    
    def __init__(self):
        super().__init__()
        self.categoria_model = Categoria()
        self.setup_ui()
        self.carregar_dados()
    
    def setup_ui(self):
        """Configurar interface"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Título
        titulo = QLabel('Gerenciamento de Categorias')
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        titulo.setFont(font)
        layout.addWidget(titulo)
        
        # Botões de ação
        botoes_layout = QHBoxLayout()
        
        self.btn_nova = QPushButton('Nova Categoria')
        self.btn_nova.clicked.connect(self.nova_categoria)
        botoes_layout.addWidget(self.btn_nova)
        
        self.btn_editar = QPushButton('Editar')
        self.btn_editar.clicked.connect(self.editar_categoria)
        self.btn_editar.setEnabled(False)
        botoes_layout.addWidget(self.btn_editar)
        
        self.btn_excluir = QPushButton('Excluir')
        self.btn_excluir.clicked.connect(self.excluir_categoria)
        self.btn_excluir.setEnabled(False)
        botoes_layout.addWidget(self.btn_excluir)
        
        botoes_layout.addStretch()
        
        self.btn_atualizar = QPushButton('Atualizar')
        self.btn_atualizar.clicked.connect(self.carregar_dados)
        botoes_layout.addWidget(self.btn_atualizar)
        
        layout.addLayout(botoes_layout)
        
        # Tabela de categorias
        self.tabela = QTableWidget()
        self.tabela.setColumnCount(4)
        self.tabela.setHorizontalHeaderLabels(['ID', 'Nome', 'Descrição', 'Total Produtos'])
        
        # Configurar tabela
        header = self.tabela.horizontalHeader()
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)  # Descrição
        self.tabela.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabela.itemSelectionChanged.connect(self.on_selection_changed)
        self.tabela.itemDoubleClicked.connect(self.editar_categoria)
        
        layout.addWidget(self.tabela)
    
    def carregar_dados(self):
        """Carregar dados das categorias"""
        try:
            categorias = self.categoria_model.get_with_product_count()
            self.tabela.setRowCount(len(categorias))
            
            for row, categoria in enumerate(categorias):
                self.tabela.setItem(row, 0, QTableWidgetItem(str(categoria['id'])))
                self.tabela.setItem(row, 1, QTableWidgetItem(categoria['nome']))
                self.tabela.setItem(row, 2, QTableWidgetItem(categoria.get('descricao', '')))
                self.tabela.setItem(row, 3, QTableWidgetItem(str(categoria['total_produtos'])))
            
            self.tabela.resizeColumnsToContents()
            
        except Exception as e:
            logger.error(f"Erro ao carregar categorias: {e}")
            QMessageBox.critical(self, 'Erro', f'Erro ao carregar categorias: {e}')
    
    def on_selection_changed(self):
        """Evento de mudança de seleção na tabela"""
        tem_selecao = len(self.tabela.selectedItems()) > 0
        self.btn_editar.setEnabled(tem_selecao)
        self.btn_excluir.setEnabled(tem_selecao)
    
    def nova_categoria(self):
        """Abrir dialog para nova categoria"""
        dialog = CategoriaDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.carregar_dados()
    
    def editar_categoria(self):
        """Editar categoria selecionada"""
        row = self.tabela.currentRow()
        if row < 0:
            return
        
        categoria_id = int(self.tabela.item(row, 0).text())
        categoria = self.categoria_model.get_by_id(categoria_id)
        
        if categoria:
            dialog = CategoriaDialog(self, categoria)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self.carregar_dados()
    
    def excluir_categoria(self):
        """Excluir categoria selecionada"""
        row = self.tabela.currentRow()
        if row < 0:
            return
        
        categoria_id = int(self.tabela.item(row, 0).text())
        nome = self.tabela.item(row, 1).text()
        total_produtos = int(self.tabela.item(row, 3).text())
        
        if total_produtos > 0:
            QMessageBox.warning(
                self, 'Erro', 
                f'Não é possível excluir a categoria "{nome}" pois possui {total_produtos} produto(s) associado(s).'
            )
            return
        
        reply = QMessageBox.question(
            self, 'Confirmar Exclusão',
            f'Deseja realmente excluir a categoria "{nome}"?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.categoria_model.delete(categoria_id)
                self.carregar_dados()
                QMessageBox.information(self, 'Sucesso', 'Categoria excluída com sucesso!')
            except Exception as e:
                logger.error(f"Erro ao excluir categoria: {e}")
                QMessageBox.critical(self, 'Erro', f'Erro ao excluir categoria: {e}')

class CategoriaDialog(QDialog):
    """Dialog para cadastro/edição de categoria"""
    
    def __init__(self, parent, categoria=None):
        super().__init__(parent)
        self.categoria = categoria
        self.categoria_model = Categoria()
        self.setup_ui()
        
        if categoria:
            self.carregar_categoria()
    
    def setup_ui(self):
        """Configurar interface"""
        self.setWindowTitle('Nova Categoria' if not self.categoria else 'Editar Categoria')
        self.setFixedSize(400, 200)
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Formulário
        form_layout = QFormLayout()
        
        # Nome
        self.campo_nome = QLineEdit()
        self.campo_nome.setMaxLength(100)
        form_layout.addRow('Nome*:', self.campo_nome)
        
        # Descrição
        self.campo_descricao = QTextEdit()
        self.campo_descricao.setMaximumHeight(80)
        form_layout.addRow('Descrição:', self.campo_descricao)
        
        layout.addLayout(form_layout)
        
        # Botões
        botoes = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        botoes.accepted.connect(self.salvar)
        botoes.rejected.connect(self.reject)
        layout.addWidget(botoes)
    
    def carregar_categoria(self):
        """Carregar dados da categoria para edição"""
        self.campo_nome.setText(self.categoria['nome'])
        self.campo_descricao.setPlainText(self.categoria.get('descricao', ''))
    
    def salvar(self):
        """Salvar categoria"""
        if not self.campo_nome.text().strip():
            QMessageBox.warning(self, 'Erro', 'Nome é obrigatório!')
            return
        
        # Verificar se nome já existe
        nome_existe = self.categoria_model.existe_nome(
            self.campo_nome.text().strip(),
            self.categoria['id'] if self.categoria else None
        )
        
        if nome_existe:
            QMessageBox.warning(self, 'Erro', 'Nome já existe!')
            return
        
        try:
            # Preparar dados
            dados = {
                'nome': self.campo_nome.text().strip(),
                'descricao': self.campo_descricao.toPlainText().strip()
            }
            
            if self.categoria:
                dados['id'] = self.categoria['id']
            
            # Salvar
            self.categoria_model.save(dados)
            
            QMessageBox.information(
                self, 'Sucesso', 
                'Categoria salva com sucesso!'
            )
            self.accept()
            
        except Exception as e:
            logger.error(f"Erro ao salvar categoria: {e}")
            QMessageBox.critical(self, 'Erro', f'Erro ao salvar categoria: {e}') 