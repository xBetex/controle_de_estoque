# -*- coding: utf-8 -*-
"""
Configuração do sistema de logging
"""

import logging
import logging.handlers
from pathlib import Path
from config.settings import LOGGING_CONFIG

def setup_logger():
    """Configurar sistema de logging"""
    # Criar diretório de logs se não existir
    log_file = Path(LOGGING_CONFIG['file'])
    log_file.parent.mkdir(exist_ok=True)
    
    # Configurar logger principal
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, LOGGING_CONFIG['level']))
    
    # Remover handlers existentes
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Handler para arquivo com rotação
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=LOGGING_CONFIG['max_size'],
        backupCount=LOGGING_CONFIG['backup_count'],
        encoding='utf-8'
    )
    file_handler.setLevel(logging.INFO)
    
    # Handler para console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    
    # Formato das mensagens
    formatter = logging.Formatter(LOGGING_CONFIG['format'])
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Adicionar handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger 