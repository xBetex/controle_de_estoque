"""
Módulo de configuração para o Sistema de Controle de Estoque
"""

import os

# Diretórios
DATA_DIR = "data"
LOGS_DIR = "logs"
BACKUPS_DIR = "backups"
ASSETS_DIR = "assets"

# Arquivos de dados
PRODUCTS_FILE = os.path.join(DATA_DIR, "products.json")
MOVEMENTS_FILE = os.path.join(DATA_DIR, "movements.json")
SUPPLIERS_FILE = os.path.join(DATA_DIR, "suppliers.json")
CATEGORIES_FILE = os.path.join(DATA_DIR, "categories.json")
SETTINGS_FILE = os.path.join(DATA_DIR, "settings.json")

# Configurações da aplicação
APP_TITLE = "Sistema de Controle de Estoque Avançado v2.0"
APP_VERSION = "2.0.0"
DEFAULT_WINDOW_SIZE = "1400x900"
MIN_WINDOW_SIZE = (1200, 700)

# Tema e cores
THEME_MODE = "dark"
COLOR_THEME = "blue"
SIDEBAR_WIDTH = 250

# Fontes
FONT_SIZES = {
    "title": 32,
    "heading": 24,
    "subheading": 18,
    "button": 16,
    "label": 14,
    "text": 14,
    "small": 12
}

# Cores do sistema
COLORS = {
    "success": "#4CAF50",
    "warning": "#FF9800", 
    "error": "#F44336",
    "info": "#2196F3",
    "primary": "#1976D2",
    "secondary": "#757575",
    "border": "#666666",
    "neutral": "#9E9E9E"
}

# Configurações padrão
DEFAULT_SETTINGS = {
    "theme": "dark",
    "language": "pt-BR",
    "low_stock_threshold": 5,
    "currency": "BRL",
    "backup_enabled": True,
    "auto_backup": True,
    "auto_backup_days": 7,
    "default_category": "",
    "theme_mode": "dark",
    "color_theme": "blue"
} 