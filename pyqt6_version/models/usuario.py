# -*- coding: utf-8 -*-
"""
Modelo de dados para usuários
"""

from .base import BaseModel
import hashlib
from datetime import datetime

class Usuario(BaseModel):
    """Modelo para usuários"""
    
    @property
    def table_name(self):
        return 'usuarios'
    
    @property
    def fields(self):
        return [
            'nome', 'usuario', 'senha', 'nivel', 'ativo',
            'ultimo_acesso', 'data_criacao'
        ]
    
    def hash_senha(self, senha):
        """Gerar hash da senha"""
        return hashlib.sha256(senha.encode()).hexdigest()
    
    def autenticar(self, usuario, senha):
        """Autenticar usuário"""
        senha_hash = self.hash_senha(senha)
        query = '''
            SELECT * FROM usuarios 
            WHERE usuario = ? AND senha = ? AND ativo = 1
        '''
        
        result = self.db_manager.execute_query(query, [usuario, senha_hash])
        
        if result:
            user_data = dict(result[0])
            # Atualizar último acesso
            self.atualizar_ultimo_acesso(user_data['id'])
            return user_data
        
        return None
    
    def atualizar_ultimo_acesso(self, user_id):
        """Atualizar último acesso do usuário"""
        query = "UPDATE usuarios SET ultimo_acesso = ? WHERE id = ?"
        self.db_manager.execute_query(query, [datetime.now(), user_id])
    
    def existe_usuario(self, usuario, user_id=None):
        """Verificar se nome de usuário já existe"""
        if user_id:
            query = "SELECT COUNT(*) FROM usuarios WHERE usuario = ? AND id != ?"
            result = self.db_manager.execute_query(query, [usuario, user_id])
        else:
            query = "SELECT COUNT(*) FROM usuarios WHERE usuario = ?"
            result = self.db_manager.execute_query(query, [usuario])
        
        return result[0][0] > 0
    
    def criar_usuario(self, data):
        """Criar novo usuário com senha hash"""
        if 'senha' in data:
            data['senha'] = self.hash_senha(data['senha'])
        
        return self.create(data)
    
    def alterar_senha(self, user_id, senha_nova):
        """Alterar senha do usuário"""
        senha_hash = self.hash_senha(senha_nova)
        query = "UPDATE usuarios SET senha = ? WHERE id = ?"
        return self.db_manager.execute_query(query, [senha_hash, user_id]) 