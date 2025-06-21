# -*- coding: utf-8 -*-
"""
Janela principal do sistema
"""

from PyQt6.QtWidgets import (QMainWindow, QMdiArea, QMenuBar, QStatusBar, 
                             QToolBar, QVBoxLayout, QWidget, QLabel, 
                             QMessageBox, QApplication)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QAction, QIcon
from datetime import datetime
import logging

from config.settings import APP_CONFIG
from .produtos_window import ProdutosWindow
from .categorias_window import CategoriasWindow
from .fornecedores_window import FornecedoresWindow
from .movimentacoes_window import MovimentacoesWindow
from .relatorios_window import RelatoriosWindow
from .dashboard_window import DashboardWindow

logger = logging.getLogger(__name__)

class MainWindow(QMainWindow):
    """Janela principal da aplicação"""
    
    def __init__(self):
        super().__init__()
        self.mdi_area = None
        self.status_bar = None
        self.setup_ui()
        self.setup_menu()
        self.setup_toolbar()
        self.setup_statusbar()
        self.show_dashboard()
        
        logger.info("Janela principal inicializada")
    
    def setup_ui(self):
        """Configurar interface"""
        self.setWindowTitle(APP_CONFIG['name'])
        self.setGeometry(100, 100, *APP_CONFIG['window_size'])
        self.setMinimumSize(*APP_CONFIG['min_window_size'])
        
        # Área MDI
        self.mdi_area = QMdiArea()
        self.setCentralWidget(self.mdi_area)
        
        # Estilo aplicado globalmente
    
    def setup_menu(self):
        """Configurar menu"""
        menubar = self.menuBar()
        
        # Menu Arquivo
        arquivo_menu = menubar.addMenu('&Arquivo')
        
        backup_action = QAction('&Backup do Banco', self)
        backup_action.triggered.connect(self.fazer_backup)
        arquivo_menu.addAction(backup_action)
        
        arquivo_menu.addSeparator()
        
        sair_action = QAction('&Sair', self)
        sair_action.triggered.connect(self.close)
        arquivo_menu.addAction(sair_action)
        
        # Menu Cadastros
        cadastros_menu = menubar.addMenu('&Cadastros')
        
        produtos_action = QAction('&Produtos', self)
        produtos_action.triggered.connect(self.abrir_produtos)
        cadastros_menu.addAction(produtos_action)
        
        categorias_action = QAction('&Categorias', self)
        categorias_action.triggered.connect(self.abrir_categorias)
        cadastros_menu.addAction(categorias_action)
        
        fornecedores_action = QAction('&Fornecedores', self)
        fornecedores_action.triggered.connect(self.abrir_fornecedores)
        cadastros_menu.addAction(fornecedores_action)
        
        # Menu Estoque
        estoque_menu = menubar.addMenu('&Estoque')
        
        movimentacoes_action = QAction('&Movimentações', self)
        movimentacoes_action.triggered.connect(self.abrir_movimentacoes)
        estoque_menu.addAction(movimentacoes_action)
        
        # Menu Relatórios
        relatorios_menu = menubar.addMenu('&Relatórios')
        
        relatorios_action = QAction('&Relatórios', self)
        relatorios_action.triggered.connect(self.abrir_relatorios)
        relatorios_menu.addAction(relatorios_action)
        
        # Menu Ajuda
        ajuda_menu = menubar.addMenu('&Ajuda')
        
        sobre_action = QAction('&Sobre', self)
        sobre_action.triggered.connect(self.mostrar_sobre)
        ajuda_menu.addAction(sobre_action)
    
    def setup_toolbar(self):
        """Configurar barra de ferramentas"""
        toolbar = self.addToolBar('Principal')
        toolbar.setMovable(False)
        
        # Dashboard
        dashboard_action = QAction('Dashboard', self)
        dashboard_action.triggered.connect(self.show_dashboard)
        toolbar.addAction(dashboard_action)
        
        toolbar.addSeparator()
        
        # Produtos
        produtos_action = QAction('Produtos', self)
        produtos_action.triggered.connect(self.abrir_produtos)
        toolbar.addAction(produtos_action)
        
        # Movimentações
        movimentacoes_action = QAction('Movimentações', self)
        movimentacoes_action.triggered.connect(self.abrir_movimentacoes)
        toolbar.addAction(movimentacoes_action)
        
        toolbar.addSeparator()
        
        # Relatórios
        relatorios_action = QAction('Relatórios', self)
        relatorios_action.triggered.connect(self.abrir_relatorios)
        toolbar.addAction(relatorios_action)
    
    def setup_statusbar(self):
        """Configurar barra de status"""
        self.status_bar = self.statusBar()
        
        # Label para informações
        self.status_label = QLabel('Sistema iniciado')
        self.status_bar.addWidget(self.status_label)
        
        # Label para data/hora
        self.datetime_label = QLabel()
        self.status_bar.addPermanentWidget(self.datetime_label)
        
        # Timer para atualizar data/hora
        self.timer = QTimer()
        self.timer.timeout.connect(self.atualizar_datetime)
        self.timer.start(1000)  # Atualizar a cada segundo
        
        self.atualizar_datetime()
    
    def atualizar_datetime(self):
        """Atualizar data/hora na barra de status"""
        now = datetime.now()
        self.datetime_label.setText(now.strftime('%d/%m/%Y %H:%M:%S'))
    
    def atualizar_status(self, mensagem):
        """Atualizar mensagem na barra de status"""
        self.status_label.setText(mensagem)
    
    def show_dashboard(self):
        """Mostrar dashboard"""
        try:
            dashboard = DashboardWindow()
            sub_window = self.mdi_area.addSubWindow(dashboard)
            sub_window.setWindowTitle('Dashboard')
            sub_window.show()
            self.atualizar_status('Dashboard aberto')
        except Exception as e:
            logger.error(f"Erro ao abrir dashboard: {e}")
            self.mostrar_erro(f"Erro ao abrir dashboard: {e}")
    
    def abrir_produtos(self):
        """Abrir janela de produtos"""
        try:
            produtos_window = ProdutosWindow()
            sub_window = self.mdi_area.addSubWindow(produtos_window)
            sub_window.setWindowTitle('Gerenciar Produtos')
            sub_window.show()
            self.atualizar_status('Gerenciamento de produtos aberto')
        except Exception as e:
            logger.error(f"Erro ao abrir produtos: {e}")
            self.mostrar_erro(f"Erro ao abrir gerenciamento de produtos: {e}")
    
    def abrir_categorias(self):
        """Abrir janela de categorias"""
        try:
            categorias_window = CategoriasWindow()
            sub_window = self.mdi_area.addSubWindow(categorias_window)
            sub_window.setWindowTitle('Gerenciar Categorias')
            sub_window.show()
            self.atualizar_status('Gerenciamento de categorias aberto')
        except Exception as e:
            logger.error(f"Erro ao abrir categorias: {e}")
            self.mostrar_erro(f"Erro ao abrir gerenciamento de categorias: {e}")
    
    def abrir_fornecedores(self):
        """Abrir janela de fornecedores"""
        try:
            fornecedores_window = FornecedoresWindow()
            sub_window = self.mdi_area.addSubWindow(fornecedores_window)
            sub_window.setWindowTitle('Gerenciar Fornecedores')
            sub_window.show()
            self.atualizar_status('Gerenciamento de fornecedores aberto')
        except Exception as e:
            logger.error(f"Erro ao abrir fornecedores: {e}")
            self.mostrar_erro(f"Erro ao abrir gerenciamento de fornecedores: {e}")
    
    def abrir_movimentacoes(self):
        """Abrir janela de movimentações"""
        try:
            movimentacoes_window = MovimentacoesWindow()
            sub_window = self.mdi_area.addSubWindow(movimentacoes_window)
            sub_window.setWindowTitle('Movimentações de Estoque')
            sub_window.show()
            self.atualizar_status('Movimentações de estoque abertas')
        except Exception as e:
            logger.error(f"Erro ao abrir movimentações: {e}")
            self.mostrar_erro(f"Erro ao abrir movimentações: {e}")
    
    def abrir_relatorios(self):
        """Abrir janela de relatórios"""
        try:
            relatorios_window = RelatoriosWindow()
            sub_window = self.mdi_area.addSubWindow(relatorios_window)
            sub_window.setWindowTitle('Relatórios')
            sub_window.show()
            self.atualizar_status('Relatórios abertos')
        except Exception as e:
            logger.error(f"Erro ao abrir relatórios: {e}")
            self.mostrar_erro(f"Erro ao abrir relatórios: {e}")
    
    def fazer_backup(self):
        """Fazer backup do banco de dados"""
        try:
            from utils.database import DatabaseManager
            db_manager = DatabaseManager()
            backup_path = db_manager.backup_database()
            
            QMessageBox.information(
                self, 
                'Backup', 
                f'Backup criado com sucesso!\nLocal: {backup_path}'
            )
            self.atualizar_status('Backup realizado com sucesso')
            
        except Exception as e:
            logger.error(f"Erro ao fazer backup: {e}")
            self.mostrar_erro(f"Erro ao fazer backup: {e}")
    
    def mostrar_sobre(self):
        """Mostrar informações sobre o sistema"""
        sobre_texto = f"""
        <h2>{APP_CONFIG['name']}</h2>
        <p><b>Versão:</b> {APP_CONFIG['version']}</p>
        <p><b>Empresa:</b> {APP_CONFIG['company']}</p>
        <br>
        <p>Sistema completo para controle de estoque com funcionalidades de:</p>
        <ul>
        <li>Cadastro de produtos, categorias e fornecedores</li>
        <li>Controle de movimentações de estoque</li>
        <li>Relatórios e exportação de dados</li>
        <li>Dashboard com indicadores</li>
        </ul>
        """
        
        QMessageBox.about(self, 'Sobre', sobre_texto)
    
    def mostrar_erro(self, mensagem):
        """Mostrar mensagem de erro"""
        QMessageBox.critical(self, 'Erro', mensagem)
    
    def closeEvent(self, event):
        """Evento de fechamento da janela"""
        reply = QMessageBox.question(
            self, 
            'Sair', 
            'Deseja realmente sair do sistema?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            logger.info("Sistema sendo encerrado")
            event.accept()
        else:
            event.ignore() 