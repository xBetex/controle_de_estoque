# -*- coding: utf-8 -*-
"""
Modelo de dados para fornecedores
"""

from .base import BaseModel
import logging

logger = logging.getLogger(__name__)

class Fornecedor(BaseModel):
    """Modelo para fornecedores"""
    
    @property
    def table_name(self):
        return 'fornecedores'
    
    @property
    def fields(self):
        return [
            'nome', 'razao_social', 'cnpj', 'inscricao_estadual',
            'telefone', 'email', 'endereco', 'cidade', 'estado',
            'cep', 'contato', 'observacoes', 'ativo', 'data_criacao'
        ]
    
    def get_by_cnpj(self, cnpj):
        """Buscar fornecedor por CNPJ"""
        query = "SELECT * FROM fornecedores WHERE cnpj = ? AND ativo = 1"
        result = self.db_manager.execute_query(query, [cnpj])
        return dict(result[0]) if result else None
    
    def existe_cnpj(self, cnpj, fornecedor_id=None):
        """Verificar se CNPJ já existe"""
        if fornecedor_id:
            query = "SELECT COUNT(*) FROM fornecedores WHERE cnpj = ? AND id != ?"
            result = self.db_manager.execute_query(query, [cnpj, fornecedor_id])
        else:
            query = "SELECT COUNT(*) FROM fornecedores WHERE cnpj = ?"
            result = self.db_manager.execute_query(query, [cnpj])
        
        return result[0][0] > 0
    
    def get_fornecedores_ativos(self):
        """Buscar apenas fornecedores ativos"""
        query = "SELECT * FROM fornecedores WHERE ativo = 1 ORDER BY nome"
        results = self.db_manager.execute_query(query)
        return [dict(row) for row in results]
    
    def search_advanced(self, **kwargs):
        """Busca avançada de fornecedores"""
        conditions = []
        values = []
        
        if kwargs.get('nome'):
            conditions.append("nome LIKE ?")
            values.append(f"%{kwargs['nome']}%")
        
        if kwargs.get('cnpj'):
            conditions.append("cnpj LIKE ?")
            values.append(f"%{kwargs['cnpj']}%")
        
        if kwargs.get('cidade'):
            conditions.append("cidade LIKE ?")
            values.append(f"%{kwargs['cidade']}%")
        
        if kwargs.get('estado'):
            conditions.append("estado = ?")
            values.append(kwargs['estado'])
        
        where_clause = " AND ".join(conditions) if conditions else "1=1"
        
        query = f'''
            SELECT * FROM fornecedores 
            WHERE {where_clause} AND ativo = 1
            ORDER BY nome
        '''
        
        results = self.db_manager.execute_query(query, values)
        return [dict(row) for row in results] 