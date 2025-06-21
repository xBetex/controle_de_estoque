#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Controle de Estoque
Aplicação principal para gerenciamento de inventário
"""

import sys
import os
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTranslator, QLocale
from PyQt6.QtGui import QIcon

# Adicionar o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent))

from views.main_window import MainWindow
from views.styles import get_app_style
from utils.database import DatabaseManager
from utils.logger import setup_logger
from config.settings import APP_CONFIG

def main():
    """Função principal da aplicação"""
    # Configurar logging
    logger = setup_logger()
    logger.info("Iniciando Sistema de Controle de Estoque")
    
    # Criar aplicação
    app = QApplication(sys.argv)
    app.setApplicationName("Controle de Estoque")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Empresa")
    
    # Aplicar tema moderno
    app.setStyleSheet(get_app_style())
    
    # Configurar ícone da aplicação
    icon_path = Path("assets/icons/app_icon.png")
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))
    
    # Inicializar banco de dados
    try:
        db_manager = DatabaseManager()
        db_manager.initialize_database()
        logger.info("Banco de dados inicializado com sucesso")
    except Exception as e:
        logger.error(f"Erro ao inicializar banco de dados: {e}")
        sys.exit(1)
    
    # Criar e mostrar janela principal
    main_window = MainWindow()
    main_window.show()
    
    logger.info("Sistema iniciado com sucesso")
    
    # Executar aplicação
    return app.exec()

if __name__ == "__main__":
    sys.exit(main()) 