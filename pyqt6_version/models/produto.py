# -*- coding: utf-8 -*-
"""
Modelo de dados para produtos
"""

from .base import BaseModel
import logging

logger = logging.getLogger(__name__)

class Produto(BaseModel):
    """Modelo para produtos"""
    
    @property
    def table_name(self):
        return 'produtos'
    
    @property
    def fields(self):
        return [
            'codigo', 'nome', 'descricao', 'categoria_id', 'fornecedor_id',
            'preco_compra', 'preco_venda', 'estoque_minimo', 'estoque_atual',
            'unidade', 'localizacao', 'ativo', 'data_criacao'
        ]
    
    def get_produtos_completos(self):
        """Buscar produtos com informações de categoria e fornecedor"""
        query = '''
            SELECT 
                p.*,
                c.nome as categoria_nome,
                f.nome as fornecedor_nome
            FROM produtos p
            LEFT JOIN categorias c ON p.categoria_id = c.id
            LEFT JOIN fornecedores f ON p.fornecedor_id = f.id
            WHERE p.ativo = 1
            ORDER BY p.nome
        '''
        
        results = self.db_manager.execute_query(query)
        return [dict(row) for row in results]
    
    def get_by_codigo(self, codigo):
        """Buscar produto por código"""
        query = "SELECT * FROM produtos WHERE codigo = ? AND ativo = 1"
        result = self.db_manager.execute_query(query, [codigo])
        return dict(result[0]) if result else None
    
    def existe_codigo(self, codigo, produto_id=None):
        """Verificar se código já existe"""
        if produto_id:
            query = "SELECT COUNT(*) FROM produtos WHERE codigo = ? AND id != ?"
            result = self.db_manager.execute_query(query, [codigo, produto_id])
        else:
            query = "SELECT COUNT(*) FROM produtos WHERE codigo = ?"
            result = self.db_manager.execute_query(query, [codigo])
        
        return result[0][0] > 0
    
    def get_produtos_estoque_baixo(self):
        """Buscar produtos com estoque abaixo do mínimo"""
        query = '''
            SELECT 
                p.*,
                c.nome as categoria_nome,
                f.nome as fornecedor_nome
            FROM produtos p
            LEFT JOIN categorias c ON p.categoria_id = c.id
            LEFT JOIN fornecedores f ON p.fornecedor_id = f.id
            WHERE p.ativo = 1 AND p.estoque_atual <= p.estoque_minimo
            ORDER BY p.nome
        '''
        
        results = self.db_manager.execute_query(query)
        return [dict(row) for row in results]
    
    def atualizar_estoque(self, produto_id, nova_quantidade):
        """Atualizar estoque atual do produto"""
        query = "UPDATE produtos SET estoque_atual = ? WHERE id = ?"
        return self.db_manager.execute_query(query, [nova_quantidade, produto_id])
    
    def search_advanced(self, **kwargs):
        """Busca avançada de produtos"""
        conditions = []
        values = []
        
        if kwargs.get('nome'):
            conditions.append("p.nome LIKE ?")
            values.append(f"%{kwargs['nome']}%")
        
        if kwargs.get('codigo'):
            conditions.append("p.codigo LIKE ?")
            values.append(f"%{kwargs['codigo']}%")
        
        if kwargs.get('categoria_id'):
            conditions.append("p.categoria_id = ?")
            values.append(kwargs['categoria_id'])
        
        if kwargs.get('fornecedor_id'):
            conditions.append("p.fornecedor_id = ?")
            values.append(kwargs['fornecedor_id'])
        
        if kwargs.get('estoque_baixo'):
            conditions.append("p.estoque_atual <= p.estoque_minimo")
        
        where_clause = " AND ".join(conditions) if conditions else "1=1"
        
        query = f'''
            SELECT 
                p.*,
                c.nome as categoria_nome,
                f.nome as fornecedor_nome
            FROM produtos p
            LEFT JOIN categorias c ON p.categoria_id = c.id
            LEFT JOIN fornecedores f ON p.fornecedor_id = f.id
            WHERE {where_clause} AND p.ativo = 1
            ORDER BY p.nome
        '''
        
        results = self.db_manager.execute_query(query, values)
        return [dict(row) for row in results] 