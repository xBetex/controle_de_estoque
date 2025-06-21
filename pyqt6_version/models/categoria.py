# -*- coding: utf-8 -*-
"""
Modelo de dados para categorias
"""

from .base import BaseModel

class Categoria(BaseModel):
    """Modelo para categorias"""
    
    @property
    def table_name(self):
        return 'categorias'
    
    @property
    def fields(self):
        return ['nome', 'descricao', 'ativo', 'data_criacao']
    
    def existe_nome(self, nome, categoria_id=None):
        """Verificar se nome já existe"""
        if categoria_id:
            query = "SELECT COUNT(*) FROM categorias WHERE nome = ? AND id != ?"
            result = self.db_manager.execute_query(query, [nome, categoria_id])
        else:
            query = "SELECT COUNT(*) FROM categorias WHERE nome = ?"
            result = self.db_manager.execute_query(query, [nome])
        
        return result[0][0] > 0
    
    def get_with_product_count(self):
        """Buscar categorias com contagem de produtos"""
        query = '''
            SELECT 
                c.*,
                COUNT(p.id) as total_produtos
            FROM categorias c
            LEFT JOIN produtos p ON c.id = p.categoria_id AND p.ativo = 1
            WHERE c.ativo = 1
            GROUP BY c.id
            ORDER BY c.nome
        '''
        
        results = self.db_manager.execute_query(query)
        return [dict(row) for row in results] 