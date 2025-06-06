"""
Módulo de utilitários para o Sistema de Controle de Estoque
"""

import json
import os
import sys
from datetime import datetime
from typing import Any, List, Dict, Optional
import tkinter as tk
from tkinter import messagebox

def create_directory(path: str) -> bool:
    """
    Cria um diretório se ele não existir
    
    Args:
        path: Caminho do diretório a ser criado
        
    Returns:
        True se criado com sucesso ou já existe, False caso contrário
    """
    try:
        if not os.path.exists(path):
            os.makedirs(path)
        return True
    except Exception as e:
        print(f"Erro ao criar diretório {path}: {e}")
        return False

def load_json_data(filename: str, default: Any = None) -> Any:
    """
    Carrega dados de um arquivo JSON
    
    Args:
        filename: Nome do arquivo JSON
        default: Valor padrão caso o arquivo não exista
        
    Returns:
        Dados carregados ou valor padrão
    """
    try:
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        return default if default is not None else []
    except Exception as e:
        print(f"Erro ao carregar {filename}: {e}")
        return default if default is not None else []

def save_json_data(data: Any, filename: str) -> bool:
    """
    Salva dados em um arquivo JSON
    
    Args:
        data: Dados a serem salvos
        filename: Nome do arquivo JSON
        
    Returns:
        True se salvo com sucesso, False caso contrário
    """
    try:
        # Criar diretório pai se não existir
        parent_dir = os.path.dirname(filename)
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir)
            
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Erro ao salvar {filename}: {e}")
        return False

def validate_required_fields(data: Dict, required_fields: List[str]) -> Optional[str]:
    """
    Valida se todos os campos obrigatórios estão preenchidos
    
    Args:
        data: Dicionário com os dados
        required_fields: Lista de campos obrigatórios
        
    Returns:
        Nome do primeiro campo não preenchido ou None se todos estão preenchidos
    """
    for field in required_fields:
        if not data.get(field, "").strip():
            return field
    return None

def validate_numeric_fields(data: Dict, numeric_fields: Dict[str, type]) -> Optional[str]:
    """
    Valida se os campos numéricos têm valores válidos
    
    Args:
        data: Dicionário com os dados
        numeric_fields: Dicionário com campo->tipo mapeamento
        
    Returns:
        Nome do primeiro campo inválido ou None se todos são válidos
    """
    for field, field_type in numeric_fields.items():
        if field in data and data[field]:
            try:
                field_type(data[field])
            except (ValueError, TypeError):
                return field
    return None

def format_currency(value: float, currency: str = "BRL") -> str:
    """
    Formata um valor monetário
    
    Args:
        value: Valor a ser formatado
        currency: Moeda (padrão BRL)
        
    Returns:
        Valor formatado como string
    """
    if currency == "BRL":
        return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{value:,.2f}"

def format_date(date_str: str, format_from: str = "%Y-%m-%dT%H:%M:%S.%f", 
                format_to: str = "%d/%m/%Y %H:%M") -> str:
    """
    Formata uma data
    
    Args:
        date_str: String da data original
        format_from: Formato original
        format_to: Formato desejado
        
    Returns:
        Data formatada
    """
    try:
        # Tenta diferentes formatos ISO
        for fmt in ["%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"]:
            try:
                date_obj = datetime.strptime(date_str, fmt)
                return date_obj.strftime(format_to)
            except ValueError:
                continue
        return date_str
    except Exception:
        return date_str

def show_error_message(title: str, message: str):
    """Exibe mensagem de erro"""
    messagebox.showerror(title, message)

def show_success_message(title: str, message: str):
    """Exibe mensagem de sucesso"""
    messagebox.showinfo(title, message)

def show_warning_message(title: str, message: str):
    """Exibe mensagem de aviso"""
    messagebox.showwarning(title, message)

def confirm_action(title: str, message: str) -> bool:
    """
    Solicita confirmação do usuário
    
    Returns:
        True se confirmado, False caso contrário
    """
    return messagebox.askyesno(title, message)

def center_window(window, width: int, height: int):
    """
    Centraliza uma janela na tela
    
    Args:
        window: Janela tkinter
        width: Largura da janela
        height: Altura da janela
    """
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    
    window.geometry(f"{width}x{height}+{x}+{y}")

def generate_id(existing_ids: List[int]) -> int:
    """
    Gera um novo ID único
    
    Args:
        existing_ids: Lista de IDs existentes
        
    Returns:
        Novo ID único
    """
    return max(existing_ids, default=0) + 1

def search_in_text(query: str, text: str) -> bool:
    """
    Verifica se uma consulta está contida em um texto (case-insensitive)
    
    Args:
        query: Texto a procurar
        text: Texto onde procurar
        
    Returns:
        True se encontrado, False caso contrário
    """
    return query.lower() in text.lower()

def darken_color(hex_color: str, factor: float = 0.8) -> str:
    """
    Escurece uma cor hexadecimal
    
    Args:
        hex_color: Cor em formato hex (#RRGGBB)
        factor: Fator de escurecimento (0.0-1.0)
        
    Returns:
        Cor escurecida em formato hex
    """
    try:
        # Remove o # se presente
        hex_color = hex_color.lstrip('#')
        
        # Converte para RGB
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        
        # Aplica o fator
        r = int(r * factor)
        g = int(g * factor)
        b = int(b * factor)
        
        # Converte de volta para hex
        return f"#{r:02x}{g:02x}{b:02x}"
    except:
        return hex_color 