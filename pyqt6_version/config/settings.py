# -*- coding: utf-8 -*-
"""
Configurações da aplicação
"""

import os
from pathlib import Path

# Diretórios da aplicação
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"
EXPORTS_DIR = BASE_DIR / "exports"
BACKUPS_DIR = BASE_DIR / "backups"
ASSETS_DIR = BASE_DIR / "assets"

# Criar diretórios se não existirem
for directory in [DATA_DIR, LOGS_DIR, EXPORTS_DIR, BACKUPS_DIR, ASSETS_DIR]:
    directory.mkdir(exist_ok=True)

# Configurações do banco de dados
DATABASE_CONFIG = {
    'name': 'estoque.db',
    'path': DATA_DIR / 'estoque.db'
}

# Configurações da aplicação
APP_CONFIG = {
    'name': 'Sistema de Controle de Estoque',
    'version': '1.0.0',
    'company': 'Sua Empresa',
    'window_size': (1200, 800),
    'min_window_size': (1000, 600)
}

# Configurações de logging
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': LOGS_DIR / 'sistema.log',
    'max_size': 10 * 1024 * 1024,  # 10MB
    'backup_count': 5
}

# Configurações de exportação
EXPORT_CONFIG = {
    'formats': ['xlsx', 'csv', 'pdf'],
    'default_format': 'xlsx'
}

# Configurações de backup
BACKUP_CONFIG = {
    'auto_backup': True,
    'backup_interval': 24,  # horas
    'max_backups': 30
} 