# -*- coding: utf-8 -*-
"""
Validadores de dados
"""

import re
from datetime import datetime

class Validators:
    """Classe com métodos de validação"""
    
    @staticmethod
    def validar_cnpj(cnpj):
        """Validar CNPJ"""
        if not cnpj:
            return False
            
        # Remover caracteres não numéricos
        cnpj = re.sub(r'[^0-9]', '', cnpj)
        
        # Verificar se tem 14 dígitos
        if len(cnpj) != 14:
            return False
        
        # Verificar se não são todos iguais
        if cnpj == cnpj[0] * 14:
            return False
        
        # Calcular primeiro dígito verificador
        soma = 0
        peso = 5
        for i in range(12):
            soma += int(cnpj[i]) * peso
            peso -= 1
            if peso < 2:
                peso = 9
        
        resto = soma % 11
        digito1 = 0 if resto < 2 else 11 - resto
        
        # Calcular segundo dígito verificador
        soma = 0
        peso = 6
        for i in range(13):
            soma += int(cnpj[i]) * peso
            peso -= 1
            if peso < 2:
                peso = 9
        
        resto = soma % 11
        digito2 = 0 if resto < 2 else 11 - resto
        
        # Verificar se os dígitos estão corretos
        return int(cnpj[12]) == digito1 and int(cnpj[13]) == digito2
    
    @staticmethod
    def validar_email(email):
        """Validar e-mail"""
        if not email:
            return True  # E-mail é opcional
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validar_cep(cep):
        """Validar CEP"""
        if not cep:
            return True  # CEP é opcional
        
        # Remover caracteres não numéricos
        cep = re.sub(r'[^0-9]', '', cep)
        
        # Verificar se tem 8 dígitos
        return len(cep) == 8
    
    @staticmethod
    def validar_telefone(telefone):
        """Validar telefone"""
        if not telefone:
            return True  # Telefone é opcional
        
        # Remover caracteres não numéricos
        telefone = re.sub(r'[^0-9]', '', telefone)
        
        # Verificar se tem entre 10 e 11 dígitos
        return 10 <= len(telefone) <= 11
    
    @staticmethod
    def validar_codigo_produto(codigo):
        """Validar código de produto"""
        if not codigo:
            return False
        
        # Código deve ter pelo menos 2 caracteres e máximo 20
        return 2 <= len(codigo.strip()) <= 20
    
    @staticmethod
    def validar_preco(preco):
        """Validar preço"""
        try:
            valor = float(preco)
            return valor >= 0
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validar_quantidade(quantidade):
        """Validar quantidade"""
        try:
            valor = int(quantidade)
            return valor >= 0
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def formatar_cnpj(cnpj):
        """Formatar CNPJ com máscara"""
        if not cnpj:
            return ""
        
        # Remover caracteres não numéricos
        cnpj = re.sub(r'[^0-9]', '', cnpj)
        
        # Aplicar máscara
        if len(cnpj) == 14:
            return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:14]}"
        
        return cnpj
    
    @staticmethod
    def formatar_cep(cep):
        """Formatar CEP com máscara"""
        if not cep:
            return ""
        
        # Remover caracteres não numéricos
        cep = re.sub(r'[^0-9]', '', cep)
        
        # Aplicar máscara
        if len(cep) == 8:
            return f"{cep[:5]}-{cep[5:8]}"
        
        return cep
    
    @staticmethod
    def formatar_telefone(telefone):
        """Formatar telefone com máscara"""
        if not telefone:
            return ""
        
        # Remover caracteres não numéricos
        telefone = re.sub(r'[^0-9]', '', telefone)
        
        # Aplicar máscara
        if len(telefone) == 10:
            return f"({telefone[:2]}) {telefone[2:6]}-{telefone[6:10]}"
        elif len(telefone) == 11:
            return f"({telefone[:2]}) {telefone[2:7]}-{telefone[7:11]}"
        
        return telefone
    
    @staticmethod
    def formatar_moeda(valor):
        """Formatar valor monetário"""
        try:
            valor = float(valor)
            return f"R$ {valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        except (ValueError, TypeError):
            return "R$ 0,00" 