# -*- coding: utf-8 -*-
"""
Classe base para modelos de dados
"""

from abc import ABC, abstractmethod
from utils.database import DatabaseManager
import logging

logger = logging.getLogger(__name__)

class BaseModel(ABC):
    """Classe base para todos os modelos"""
    
    def __init__(self):
        self.db_manager = DatabaseManager()
    
    @property
    @abstractmethod
    def table_name(self):
        """Nome da tabela no banco de dados"""
        pass
    
    @property
    @abstractmethod
    def fields(self):
        """Campos da tabela"""
        pass
    
    def save(self, data):
        """Salvar registro no banco"""
        try:
            if 'id' in data and data['id']:
                return self.update(data['id'], data)
            else:
                return self.create(data)
        except Exception as e:
            logger.error(f"Erro ao salvar {self.table_name}: {e}")
            raise
    
    def create(self, data):
        """Criar novo registro"""
        fields = [field for field in data.keys() if field != 'id' and field in self.fields]
        placeholders = ', '.join(['?' for _ in fields])
        field_names = ', '.join(fields)
        
        query = f"INSERT INTO {self.table_name} ({field_names}) VALUES ({placeholders})"
        values = [data[field] for field in fields]
        
        self.db_manager.execute_query(query, values)
        
        # Retornar o ID do registro criado
        return self.db_manager.execute_query("SELECT last_insert_rowid()")[0][0]
    
    def update(self, record_id, data):
        """Atualizar registro existente"""
        fields = [field for field in data.keys() if field != 'id' and field in self.fields]
        set_clause = ', '.join([f"{field} = ?" for field in fields])
        values = [data[field] for field in fields] + [record_id]
        
        query = f"UPDATE {self.table_name} SET {set_clause} WHERE id = ?"
        
        return self.db_manager.execute_query(query, values)
    
    def delete(self, record_id):
        """Excluir registro"""
        query = f"DELETE FROM {self.table_name} WHERE id = ?"
        return self.db_manager.execute_query(query, [record_id])
    
    def get_by_id(self, record_id):
        """Buscar registro por ID"""
        query = f"SELECT * FROM {self.table_name} WHERE id = ?"
        result = self.db_manager.execute_query(query, [record_id])
        return dict(result[0]) if result else None
    
    def get_all(self, active_only=True):
        """Buscar todos os registros"""
        query = f"SELECT * FROM {self.table_name}"
        if active_only and 'ativo' in self.fields:
            query += " WHERE ativo = 1"
        query += " ORDER BY id DESC"
        
        results = self.db_manager.execute_query(query)
        return [dict(row) for row in results]
    
    def search(self, search_term, fields=None):
        """Buscar registros por termo"""
        if not fields:
            fields = ['nome'] if 'nome' in self.fields else []
        
        if not fields:
            return []
        
        conditions = [f"{field} LIKE ?" for field in fields]
        where_clause = " OR ".join(conditions)
        
        query = f"SELECT * FROM {self.table_name} WHERE {where_clause}"
        if 'ativo' in self.fields:
            query += " AND ativo = 1"
        query += " ORDER BY id DESC"
        
        values = [f"%{search_term}%" for _ in fields]
        results = self.db_manager.execute_query(query, values)
        return [dict(row) for row in results] 