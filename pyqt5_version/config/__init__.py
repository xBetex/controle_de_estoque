"""
Configuration module for PyQt5 Inventory Management System
"""

import os
from PyQt5.QtCore import QStandardPaths
from PyQt5.QtGui import QFont

# Application Info
APP_NAME = "Inventory Manager"
APP_VERSION = "3.0.0"
APP_TITLE = "Sistema de Controle de Estoque - PyQt5 v3.0"
APP_ORGANIZATION = "Inventory Systems"

# Directories
DATA_DIR = "data"
LOGS_DIR = "logs"
BACKUPS_DIR = "backups"
ASSETS_DIR = "assets"
EXPORTS_DIR = "exports"

# Data Files
PRODUCTS_FILE = os.path.join(DATA_DIR, "products.json")
MOVEMENTS_FILE = os.path.join(DATA_DIR, "movements.json")
SUPPLIERS_FILE = os.path.join(DATA_DIR, "suppliers.json")
CATEGORIES_FILE = os.path.join(DATA_DIR, "categories.json")
SETTINGS_FILE = os.path.join(DATA_DIR, "settings.json")

# Window Settings
DEFAULT_WINDOW_SIZE = (1400, 900)
MIN_WINDOW_SIZE = (1000, 600)
SIDEBAR_WIDTH = 250

# Colors
COLORS = {
    # Primary colors
    'primary': '#1976D2',
    'primary_dark': '#1565C0',
    'primary_light': '#42A5F5',
    
    # Status colors
    'success': '#4CAF50',
    'warning': '#FF9800',
    'error': '#F44336',
    'info': '#2196F3',
    
    # UI colors
    'background': '#FAFAFA',
    'surface': '#FFFFFF',
    'border': '#E0E0E0',
    'text_primary': '#212121',
    'text_secondary': '#757575',
    
    # Dark theme colors
    'dark_background': '#121212',
    'dark_surface': '#1E1E1E',
    'dark_border': '#333333',
    'dark_text_primary': '#FFFFFF',
    'dark_text_secondary': '#B0B0B0',
}

# Fonts
FONTS = {
    'title': QFont('Arial', 16, QFont.Bold),
    'heading': QFont('Arial', 14, QFont.Bold),
    'subheading': QFont('Arial', 12, QFont.Bold),
    'body': QFont('Arial', 10),
    'caption': QFont('Arial', 9),
    'button': QFont('Arial', 10),
}

# Styles
STYLES = {
    'main_window': """
        QMainWindow {
            background-color: #FAFAFA;
        }
    """,
    
    'sidebar': """
        QFrame {
            background-color: #1976D2;
            border: none;
        }
        QLabel {
            color: white;
            font-size: 18px;
            font-weight: bold;
            padding: 10px;
        }
    """,
    
    'nav_button': """
        QPushButton {
            background-color: transparent;
            color: white;
            border: none;
            padding: 12px 20px;
            text-align: left;
            font-size: 14px;
            min-height: 40px;
        }
        QPushButton:hover {
            background-color: rgba(255, 255, 255, 0.1);
        }
        QPushButton:pressed {
            background-color: rgba(255, 255, 255, 0.2);
        }
        QPushButton:checked {
            background-color: rgba(255, 255, 255, 0.15);
            border-left: 4px solid white;
        }
    """,
    
    'content_area': """
        QFrame {
            background-color: white;
            border: 1px solid #E0E0E0;
            border-radius: 8px;
        }
    """,
    
    'table': """
        QTableWidget {
            background-color: white;
            border: 1px solid #E0E0E0;
            gridline-color: #E0E0E0;
            selection-background-color: #E3F2FD;
            font-size: 10px;
        }
        QTableWidget::item {
            padding: 8px;
            border: none;
        }
        QTableWidget::item:selected {
            background-color: #E3F2FD;
            color: #1976D2;
        }
        QHeaderView::section {
            background-color: #F5F5F5;
            border: 1px solid #E0E0E0;
            padding: 8px;
            font-weight: bold;
            color: #424242;
        }
    """,
    
    'button_primary': """
        QPushButton {
            background-color: #1976D2;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
            min-width: 80px;
        }
        QPushButton:hover {
            background-color: #1565C0;
        }
        QPushButton:pressed {
            background-color: #0D47A1;
        }
        QPushButton:disabled {
            background-color: #BDBDBD;
            color: #757575;
        }
    """,
    
    'button_secondary': """
        QPushButton {
            background-color: transparent;
            color: #1976D2;
            border: 2px solid #1976D2;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
            min-width: 80px;
        }
        QPushButton:hover {
            background-color: #E3F2FD;
        }
        QPushButton:pressed {
            background-color: #BBDEFB;
        }
    """,
    
    'input_field': """
        QLineEdit, QTextEdit, QComboBox, QSpinBox, QDoubleSpinBox {
            border: 2px solid #E0E0E0;
            border-radius: 4px;
            padding: 8px;
            font-size: 10px;
            background-color: white;
        }
        QLineEdit:focus, QTextEdit:focus, QComboBox:focus, 
        QSpinBox:focus, QDoubleSpinBox:focus {
            border-color: #1976D2;
        }
    """,
    
    'card': """
        QFrame {
            background-color: white;
            border: 1px solid #E0E0E0;
            border-radius: 8px;
            padding: 16px;
        }
    """,
}

# Default Settings
DEFAULT_SETTINGS = {
    'theme': 'light',
    'language': 'pt-BR',
    'low_stock_threshold': 5,
    'currency': 'BRL',
    'currency_symbol': 'R$',
    'date_format': 'dd/MM/yyyy',
    'backup_enabled': True,
    'auto_backup': True,
    'auto_backup_days': 7,
    'show_tooltips': True,
    'confirm_deletions': True,
    'window_state': 'normal',
    'window_size': DEFAULT_WINDOW_SIZE,
    'sidebar_expanded': True,
}

# Table Columns
PRODUCT_COLUMNS = [
    {'key': 'code', 'title': 'Código', 'width': 100},
    {'key': 'name', 'title': 'Nome', 'width': 200},
    {'key': 'category', 'title': 'Categoria', 'width': 120},
    {'key': 'supplier', 'title': 'Fornecedor', 'width': 150},
    {'key': 'quantity', 'title': 'Quantidade', 'width': 100},
    {'key': 'price', 'title': 'Preço', 'width': 100},
    {'key': 'total_value', 'title': 'Valor Total', 'width': 120},
]

MOVEMENT_COLUMNS = [
    {'key': 'date', 'title': 'Data', 'width': 120},
    {'key': 'type', 'title': 'Tipo', 'width': 80},
    {'key': 'product_code', 'title': 'Produto', 'width': 100},
    {'key': 'quantity', 'title': 'Quantidade', 'width': 100},
    {'key': 'reason', 'title': 'Motivo', 'width': 200},
    {'key': 'user', 'title': 'Usuário', 'width': 100},
]

SUPPLIER_COLUMNS = [
    {'key': 'name', 'title': 'Nome', 'width': 200},
    {'key': 'email', 'title': 'Email', 'width': 200},
    {'key': 'phone', 'title': 'Telefone', 'width': 120},
    {'key': 'address', 'title': 'Endereço', 'width': 250},
]

CATEGORY_COLUMNS = [
    {'key': 'name', 'title': 'Nome', 'width': 200},
    {'key': 'description', 'title': 'Descrição', 'width': 300},
    {'key': 'products_count', 'title': 'Produtos', 'width': 100},
]

# Icons (using Unicode emojis as simple icons)
ICONS = {
    'dashboard': '📊',
    'products': '📦',
    'inventory': '📋',
    'movements': '🔄',
    'suppliers': '🏢',
    'categories': '🏷️',
    'reports': '📈',
    'settings': '⚙️',
    'backup': '💾',
    'help': '❓',
    'add': '➕',
    'edit': '✏️',
    'delete': '🗑️',
    'save': '💾',
    'cancel': '❌',
    'search': '🔍',
    'filter': '🔽',
    'export': '📤',
    'import': '📥',
    'refresh': '🔄',
    'success': '✅',
    'warning': '⚠️',
    'error': '❌',
    'info': 'ℹ️',
}

# Validation Rules
VALIDATION_RULES = {
    'product_code': {
        'required': True,
        'min_length': 3,
        'max_length': 20,
        'pattern': r'^[A-Z0-9]+$'
    },
    'product_name': {
        'required': True,
        'min_length': 2,
        'max_length': 100
    },
    'price': {
        'required': True,
        'min_value': 0.01,
        'max_value': 999999.99
    },
    'quantity': {
        'required': True,
        'min_value': 0,
        'max_value': 999999
    },
    'email': {
        'pattern': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    },
    'phone': {
        'pattern': r'^\(\d{2}\)\s\d{4,5}-\d{4}$'
    }
} 