# -*- coding: utf-8 -*-
"""
Gerenciador do banco de dados SQLite
"""

import sqlite3
import logging
from pathlib import Path
from datetime import datetime
from config.settings import DATABASE_CONFIG

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Gerenciador do banco de dados"""
    
    def __init__(self):
        self.db_path = DATABASE_CONFIG['path']
        self.connection = None
    
    def get_connection(self):
        """Obter conexão com o banco de dados"""
        if self.connection is None:
            self.connection = sqlite3.connect(str(self.db_path))
            self.connection.row_factory = sqlite3.Row
        return self.connection
    
    def close_connection(self):
        """Fechar conexão com o banco de dados"""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def initialize_database(self):
        """Inicializar banco de dados e criar tabelas"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Tabela de categorias
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS categorias (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL UNIQUE,
                    descricao TEXT,
                    ativo BOOLEAN DEFAULT 1,
                    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabela de fornecedores
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS fornecedores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    cnpj TEXT UNIQUE,
                    telefone TEXT,
                    email TEXT,
                    endereco TEXT,
                    cidade TEXT,
                    estado TEXT,
                    cep TEXT,
                    contato TEXT,
                    ativo BOOLEAN DEFAULT 1,
                    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabela de produtos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS produtos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    codigo TEXT NOT NULL UNIQUE,
                    nome TEXT NOT NULL,
                    descricao TEXT,
                    categoria_id INTEGER,
                    fornecedor_id INTEGER,
                    preco_compra REAL DEFAULT 0,
                    preco_venda REAL DEFAULT 0,
                    estoque_minimo INTEGER DEFAULT 0,
                    estoque_atual INTEGER DEFAULT 0,
                    unidade TEXT DEFAULT 'UN',
                    localizacao TEXT,
                    ativo BOOLEAN DEFAULT 1,
                    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (categoria_id) REFERENCES categorias (id),
                    FOREIGN KEY (fornecedor_id) REFERENCES fornecedores (id)
                )
            ''')
            
            # Tabela de movimentações de estoque
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS movimentacoes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    produto_id INTEGER NOT NULL,
                    tipo TEXT NOT NULL CHECK (tipo IN ('entrada', 'saida')),
                    quantidade INTEGER NOT NULL,
                    preco_unitario REAL,
                    valor_total REAL,
                    motivo TEXT,
                    documento TEXT,
                    observacoes TEXT,
                    data_movimentacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    usuario TEXT,
                    FOREIGN KEY (produto_id) REFERENCES produtos (id)
                )
            ''')
            
            # Tabela de usuários (básica)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    usuario TEXT NOT NULL UNIQUE,
                    senha TEXT NOT NULL,
                    nivel TEXT DEFAULT 'operador' CHECK (nivel IN ('admin', 'operador')),
                    ativo BOOLEAN DEFAULT 1,
                    ultimo_acesso TIMESTAMP,
                    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Inserir dados iniciais
            self._insert_initial_data(cursor)
            
            conn.commit()
            logger.info("Banco de dados inicializado com sucesso")
            
        except Exception as e:
            conn.rollback()
            logger.error(f"Erro ao inicializar banco de dados: {e}")
            raise
    
    def _insert_initial_data(self, cursor):
        """Inserir dados iniciais no banco"""
        # Categoria padrão
        cursor.execute('''
            INSERT OR IGNORE INTO categorias (nome, descricao) 
            VALUES ('Geral', 'Categoria padrão')
        ''')
        
        # Fornecedor padrão
        cursor.execute('''
            INSERT OR IGNORE INTO fornecedores (nome) 
            VALUES ('Fornecedor Padrão')
        ''')
        
        # Usuário admin padrão
        cursor.execute('''
            INSERT OR IGNORE INTO usuarios (nome, usuario, senha, nivel) 
            VALUES ('Administrador', 'admin', 'admin123', 'admin')
        ''')
    
    def execute_query(self, query, params=None):
        """Executar query e retornar resultados"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if query.strip().upper().startswith('SELECT'):
                return cursor.fetchall()
            else:
                conn.commit()
                return cursor.rowcount
                
        except Exception as e:
            conn.rollback()
            logger.error(f"Erro ao executar query: {e}")
            raise
    
    def backup_database(self):
        """Criar backup do banco de dados"""
        try:
            backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            backup_path = Path("backups") / backup_name
            
            # Criar diretório de backup se não existir
            backup_path.parent.mkdir(exist_ok=True)
            
            # Copiar banco de dados
            import shutil
            shutil.copy2(self.db_path, backup_path)
            
            logger.info(f"Backup criado: {backup_path}")
            return backup_path
            
        except Exception as e:
            logger.error(f"Erro ao criar backup: {e}")
            raise 