# -*- coding: utf-8 -*-
"""
Janela de gerenciamento de fornecedores
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QLineEdit, QLabel,
                             QTextEdit, QFormLayout, QDialog, QDialogButtonBox, 
                             QMessageBox, QHeaderView, QGroupBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from models.fornecedor import Fornecedor
from utils.validators import Validators
import logging

logger = logging.getLogger(__name__)

class FornecedoresWindow(QWidget):
    """Janela de gerenciamento de fornecedores"""
    
    def __init__(self):
        super().__init__()
        self.fornecedor_model = Fornecedor()
        self.setup_ui()
        self.carregar_dados()
    
    def setup_ui(self):
        """Configurar interface"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Título
        titulo = QLabel('Gerenciamento de Fornecedores')
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        titulo.setFont(font)
        layout.addWidget(titulo)
        
        # Área de busca
        busca_group = QGroupBox('Buscar')
        busca_layout = QHBoxLayout(busca_group)
        
        busca_layout.addWidget(QLabel('Buscar:'))
        self.campo_busca = QLineEdit()
        self.campo_busca.setPlaceholderText('Nome, CNPJ, email ou contato...')
        self.campo_busca.textChanged.connect(self.filtrar_fornecedores)
        busca_layout.addWidget(self.campo_busca)
        
        layout.addWidget(busca_group)
        
        # Botões de ação
        botoes_layout = QHBoxLayout()
        
        self.btn_novo = QPushButton('Novo Fornecedor')
        self.btn_novo.clicked.connect(self.novo_fornecedor)
        botoes_layout.addWidget(self.btn_novo)
        
        self.btn_editar = QPushButton('Editar')
        self.btn_editar.clicked.connect(self.editar_fornecedor)
        self.btn_editar.setEnabled(False)
        botoes_layout.addWidget(self.btn_editar)
        
        self.btn_excluir = QPushButton('Excluir')
        self.btn_excluir.clicked.connect(self.excluir_fornecedor)
        self.btn_excluir.setEnabled(False)
        botoes_layout.addWidget(self.btn_excluir)
        
        botoes_layout.addStretch()
        
        self.btn_atualizar = QPushButton('Atualizar')
        self.btn_atualizar.clicked.connect(self.carregar_dados)
        botoes_layout.addWidget(self.btn_atualizar)
        
        layout.addLayout(botoes_layout)
        
        # Tabela de fornecedores
        self.tabela = QTableWidget()
        self.tabela.setColumnCount(7)
        self.tabela.setHorizontalHeaderLabels([
            'ID', 'Nome', 'CNPJ', 'Telefone', 'Email', 'Cidade/Estado', 'Total Produtos'
        ])
        
        # Configurar tabela
        header = self.tabela.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # Nome
        self.tabela.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabela.itemSelectionChanged.connect(self.on_selection_changed)
        self.tabela.itemDoubleClicked.connect(self.editar_fornecedor)
        
        layout.addWidget(self.tabela)
        
        # Armazenar dados para filtragem
        self.fornecedores_data = []
    
    def carregar_dados(self):
        """Carregar dados dos fornecedores"""
        try:
            self.fornecedores_data = self.fornecedor_model.get_with_product_count()
            self.atualizar_tabela(self.fornecedores_data)
            
        except Exception as e:
            logger.error(f"Erro ao carregar fornecedores: {e}")
            QMessageBox.critical(self, 'Erro', f'Erro ao carregar fornecedores: {e}')
    
    def atualizar_tabela(self, fornecedores):
        """Atualizar tabela com os fornecedores"""
        self.tabela.setRowCount(len(fornecedores))
        
        for row, fornecedor in enumerate(fornecedores):
            self.tabela.setItem(row, 0, QTableWidgetItem(str(fornecedor['id'])))
            self.tabela.setItem(row, 1, QTableWidgetItem(fornecedor['nome']))
            self.tabela.setItem(row, 2, QTableWidgetItem(Validators.formatar_cnpj(fornecedor.get('cnpj', ''))))
            self.tabela.setItem(row, 3, QTableWidgetItem(Validators.formatar_telefone(fornecedor.get('telefone', ''))))
            self.tabela.setItem(row, 4, QTableWidgetItem(fornecedor.get('email', '')))
            
            cidade_estado = f"{fornecedor.get('cidade', '')}/{fornecedor.get('estado', '')}"
            self.tabela.setItem(row, 5, QTableWidgetItem(cidade_estado.strip('/')))
            
            self.tabela.setItem(row, 6, QTableWidgetItem(str(fornecedor['total_produtos'])))
        
        self.tabela.resizeColumnsToContents()
    
    def filtrar_fornecedores(self):
        """Filtrar fornecedores por termo de busca"""
        termo = self.campo_busca.text().lower()
        
        if not termo:
            self.atualizar_tabela(self.fornecedores_data)
            return
        
        fornecedores_filtrados = []
        for fornecedor in self.fornecedores_data:
            if (termo in fornecedor['nome'].lower() or
                termo in fornecedor.get('cnpj', '').lower() or
                termo in fornecedor.get('email', '').lower() or
                termo in fornecedor.get('contato', '').lower()):
                fornecedores_filtrados.append(fornecedor)
        
        self.atualizar_tabela(fornecedores_filtrados)
    
    def on_selection_changed(self):
        """Evento de mudança de seleção na tabela"""
        tem_selecao = len(self.tabela.selectedItems()) > 0
        self.btn_editar.setEnabled(tem_selecao)
        self.btn_excluir.setEnabled(tem_selecao)
    
    def novo_fornecedor(self):
        """Abrir dialog para novo fornecedor"""
        dialog = FornecedorDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.carregar_dados()
    
    def editar_fornecedor(self):
        """Editar fornecedor selecionado"""
        row = self.tabela.currentRow()
        if row < 0:
            return
        
        fornecedor_id = int(self.tabela.item(row, 0).text())
        fornecedor = self.fornecedor_model.get_by_id(fornecedor_id)
        
        if fornecedor:
            dialog = FornecedorDialog(self, fornecedor)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self.carregar_dados()
    
    def excluir_fornecedor(self):
        """Excluir fornecedor selecionado"""
        row = self.tabela.currentRow()
        if row < 0:
            return
        
        fornecedor_id = int(self.tabela.item(row, 0).text())
        nome = self.tabela.item(row, 1).text()
        total_produtos = int(self.tabela.item(row, 6).text())
        
        if total_produtos > 0:
            QMessageBox.warning(
                self, 'Erro', 
                f'Não é possível excluir o fornecedor "{nome}" pois possui {total_produtos} produto(s) associado(s).'
            )
            return
        
        reply = QMessageBox.question(
            self, 'Confirmar Exclusão',
            f'Deseja realmente excluir o fornecedor "{nome}"?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.fornecedor_model.delete(fornecedor_id)
                self.carregar_dados()
                QMessageBox.information(self, 'Sucesso', 'Fornecedor excluído com sucesso!')
            except Exception as e:
                logger.error(f"Erro ao excluir fornecedor: {e}")
                QMessageBox.critical(self, 'Erro', f'Erro ao excluir fornecedor: {e}')

class FornecedorDialog(QDialog):
    """Dialog para cadastro/edição de fornecedor"""
    
    def __init__(self, parent, fornecedor=None):
        super().__init__(parent)
        self.fornecedor = fornecedor
        self.fornecedor_model = Fornecedor()
        self.setup_ui()
        
        if fornecedor:
            self.carregar_fornecedor()
    
    def setup_ui(self):
        """Configurar interface"""
        self.setWindowTitle('Novo Fornecedor' if not self.fornecedor else 'Editar Fornecedor')
        self.setFixedSize(500, 400)
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Formulário
        form_layout = QFormLayout()
        
        # Nome
        self.campo_nome = QLineEdit()
        self.campo_nome.setMaxLength(100)
        form_layout.addRow('Nome*:', self.campo_nome)
        
        # CNPJ
        self.campo_cnpj = QLineEdit()
        self.campo_cnpj.setMaxLength(18)
        self.campo_cnpj.setPlaceholderText('00.000.000/0000-00')
        form_layout.addRow('CNPJ:', self.campo_cnpj)
        
        # Telefone
        self.campo_telefone = QLineEdit()
        self.campo_telefone.setMaxLength(15)
        self.campo_telefone.setPlaceholderText('(00) 00000-0000')
        form_layout.addRow('Telefone:', self.campo_telefone)
        
        # Email
        self.campo_email = QLineEdit()
        self.campo_email.setMaxLength(100)
        form_layout.addRow('Email:', self.campo_email)
        
        # Endereço
        self.campo_endereco = QLineEdit()
        self.campo_endereco.setMaxLength(200)
        form_layout.addRow('Endereço:', self.campo_endereco)
        
        # Cidade
        self.campo_cidade = QLineEdit()
        self.campo_cidade.setMaxLength(50)
        form_layout.addRow('Cidade:', self.campo_cidade)
        
        # Estado
        self.campo_estado = QLineEdit()
        self.campo_estado.setMaxLength(2)
        self.campo_estado.setPlaceholderText('UF')
        form_layout.addRow('Estado:', self.campo_estado)
        
        # CEP
        self.campo_cep = QLineEdit()
        self.campo_cep.setMaxLength(9)
        self.campo_cep.setPlaceholderText('00000-000')
        form_layout.addRow('CEP:', self.campo_cep)
        
        # Contato
        self.campo_contato = QLineEdit()
        self.campo_contato.setMaxLength(100)
        form_layout.addRow('Contato:', self.campo_contato)
        
        layout.addLayout(form_layout)
        
        # Botões
        botoes = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        botoes.accepted.connect(self.salvar)
        botoes.rejected.connect(self.reject)
        layout.addWidget(botoes)
    
    def carregar_fornecedor(self):
        """Carregar dados do fornecedor para edição"""
        self.campo_nome.setText(self.fornecedor['nome'])
        self.campo_cnpj.setText(self.fornecedor.get('cnpj', ''))
        self.campo_telefone.setText(self.fornecedor.get('telefone', ''))
        self.campo_email.setText(self.fornecedor.get('email', ''))
        self.campo_endereco.setText(self.fornecedor.get('endereco', ''))
        self.campo_cidade.setText(self.fornecedor.get('cidade', ''))
        self.campo_estado.setText(self.fornecedor.get('estado', ''))
        self.campo_cep.setText(self.fornecedor.get('cep', ''))
        self.campo_contato.setText(self.fornecedor.get('contato', ''))
    
    def salvar(self):
        """Salvar fornecedor"""
        # Validações
        if not self.campo_nome.text().strip():
            QMessageBox.warning(self, 'Erro', 'Nome é obrigatório!')
            return
        
        cnpj = self.campo_cnpj.text().strip()
        if cnpj and not Validators.validar_cnpj(cnpj):
            QMessageBox.warning(self, 'Erro', 'CNPJ inválido!')
            return
        
        email = self.campo_email.text().strip()
        if email and not Validators.validar_email(email):
            QMessageBox.warning(self, 'Erro', 'Email inválido!')
            return
        
        telefone = self.campo_telefone.text().strip()
        if telefone and not Validators.validar_telefone(telefone):
            QMessageBox.warning(self, 'Erro', 'Telefone inválido!')
            return
        
        cep = self.campo_cep.text().strip()
        if cep and not Validators.validar_cep(cep):
            QMessageBox.warning(self, 'Erro', 'CEP inválido!')
            return
        
        # Verificar se CNPJ já existe
        if cnpj:
            cnpj_existe = self.fornecedor_model.existe_cnpj(
                cnpj,
                self.fornecedor['id'] if self.fornecedor else None
            )
            
            if cnpj_existe:
                QMessageBox.warning(self, 'Erro', 'CNPJ já existe!')
                return
        
        try:
            # Preparar dados
            dados = {
                'nome': self.campo_nome.text().strip(),
                'cnpj': cnpj,
                'telefone': telefone,
                'email': email,
                'endereco': self.campo_endereco.text().strip(),
                'cidade': self.campo_cidade.text().strip(),
                'estado': self.campo_estado.text().strip().upper(),
                'cep': cep,
                'contato': self.campo_contato.text().strip()
            }
            
            if self.fornecedor:
                dados['id'] = self.fornecedor['id']
            
            # Salvar
            self.fornecedor_model.save(dados)
            
            QMessageBox.information(
                self, 'Sucesso', 
                'Fornecedor salvo com sucesso!'
            )
            self.accept()
            
        except Exception as e:
            logger.error(f"Erro ao salvar fornecedor: {e}")
            QMessageBox.critical(self, 'Erro', f'Erro ao salvar fornecedor: {e}') 