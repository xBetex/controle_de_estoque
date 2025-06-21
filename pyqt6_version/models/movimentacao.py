# -*- coding: utf-8 -*-
"""
Modelo de dados para movimentações de estoque
"""

from .base import BaseModel
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class Movimentacao(BaseModel):
    """Modelo para movimentações de estoque"""
    
    @property
    def table_name(self):
        return 'movimentacoes'
    
    @property
    def fields(self):
        return [
            'produto_id', 'tipo', 'quantidade', 'motivo',
            'observacoes', 'usuario', 'data_movimentacao',
            'preco_unitario', 'valor_total'
        ]
    
    def registrar_entrada(self, produto_id, quantidade, motivo="Entrada", observacoes="", usuario="Sistema", preco_unitario=0):
        """Registrar entrada de estoque"""
        data = {
            'produto_id': produto_id,
            'tipo': 'ENTRADA',
            'quantidade': quantidade,
            'motivo': motivo,
            'observacoes': observacoes,
            'usuario': usuario,
            'data_movimentacao': datetime.now().isoformat(),
            'preco_unitario': preco_unitario,
            'valor_total': quantidade * preco_unitario
        }
        return self.create(data)
    
    def registrar_saida(self, produto_id, quantidade, motivo="Saída", observacoes="", usuario="Sistema"):
        """Registrar saída de estoque"""
        data = {
            'produto_id': produto_id,
            'tipo': 'SAIDA',
            'quantidade': quantidade,
            'motivo': motivo,
            'observacoes': observacoes,
            'usuario': usuario,
            'data_movimentacao': datetime.now().isoformat(),
            'preco_unitario': 0,
            'valor_total': 0
        }
        return self.create(data)
    
    def get_movimentacoes_produto(self, produto_id, limit=None):
        """Buscar movimentações de um produto específico"""
        query = '''
            SELECT 
                m.*,
                p.nome as produto_nome,
                p.codigo as produto_codigo
            FROM movimentacoes m
            JOIN produtos p ON m.produto_id = p.id
            WHERE m.produto_id = ?
            ORDER BY m.data_movimentacao DESC
        '''
        
        if limit:
            query += f" LIMIT {limit}"
        
        results = self.db_manager.execute_query(query, [produto_id])
        return [dict(row) for row in results]
    
    def get_movimentacoes_periodo(self, data_inicio, data_fim):
        """Buscar movimentações por período"""
        query = '''
            SELECT 
                m.*,
                p.nome as produto_nome,
                p.codigo as produto_codigo
            FROM movimentacoes m
            JOIN produtos p ON m.produto_id = p.id
            WHERE DATE(m.data_movimentacao) BETWEEN ? AND ?
            ORDER BY m.data_movimentacao DESC
        '''
        
        results = self.db_manager.execute_query(query, [data_inicio, data_fim])
        return [dict(row) for row in results]
    
    def get_resumo_movimentacoes(self, periodo_dias=30):
        """Obter resumo das movimentações dos últimos dias"""
        query = '''
            SELECT 
                m.tipo,
                COUNT(*) as total_movimentacoes,
                SUM(m.quantidade) as total_quantidade,
                SUM(m.valor_total) as valor_total
            FROM movimentacoes m
            WHERE DATE(m.data_movimentacao) >= DATE('now', '-' || ? || ' days')
            GROUP BY m.tipo
        '''
        
        results = self.db_manager.execute_query(query, [periodo_dias])
        return [dict(row) for row in results]
    
    def get_movimentacoes_completas(self, limit=None):
        """Buscar movimentações completas com informações do produto"""
        query = '''
            SELECT 
                m.*,
                p.nome as produto_nome,
                p.codigo as produto_codigo,
                c.nome as categoria_nome,
                f.nome as fornecedor_nome
            FROM movimentacoes m
            JOIN produtos p ON m.produto_id = p.id
            LEFT JOIN categorias c ON p.categoria_id = c.id
            LEFT JOIN fornecedores f ON p.fornecedor_id = f.id
            ORDER BY m.data_movimentacao DESC
        '''
        
        if limit:
            query += f" LIMIT {limit}"
        
        results = self.db_manager.execute_query(query)
        return [dict(row) for row in results]
    
    def registrar_movimentacao(self, produto_id, tipo, quantidade, motivo="", observacoes="", usuario="Sistema", preco_unitario=0, valor_total=0, documento=""):
        """Registrar uma movimentação geral"""
        # Ajustar tipo para maiúsculo
        tipo_upper = tipo.upper()
        if tipo_upper not in ['ENTRADA', 'SAIDA']:
            tipo_upper = 'ENTRADA' if tipo.lower() == 'entrada' else 'SAIDA'
        
        data = {
            'produto_id': produto_id,
            'tipo': tipo_upper,
            'quantidade': quantidade,
            'motivo': motivo,
            'observacoes': observacoes,
            'usuario': usuario,
            'data_movimentacao': datetime.now().isoformat(),
            'preco_unitario': preco_unitario,
            'valor_total': valor_total if valor_total > 0 else quantidade * preco_unitario
        }
        return self.create(data) 