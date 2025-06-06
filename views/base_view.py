"""
Classe base para todas as views do sistema
"""

import customtkinter as ctk
from abc import ABC, abstractmethod
from config import FONT_SIZES, COLORS

class BaseView(ABC):
    """Classe base para todas as views"""
    
    def __init__(self, parent, manager):
        self.parent = parent
        self.manager = manager
        self.frame = None
        self.is_created = False
    
    def show(self):
        """Mostrar a view"""
        # Sempre recriar o frame para evitar problemas de path
        if self.frame:
            self.frame.destroy()
        
        self.frame = ctk.CTkScrollableFrame(self.parent)
        self.create_widgets()
        self.frame.pack(fill="both", expand=True)
        
        # Atualizar dados se necessário
        self.refresh()
    
    def hide(self):
        """Esconder a view"""
        if self.frame:
            self.frame.pack_forget()
    
    def destroy(self):
        """Destruir a view completamente"""
        if self.frame:
            self.frame.destroy()
            self.frame = None
        self.is_created = False
    
    @abstractmethod
    def create_widgets(self):
        """Criar widgets da view - deve ser implementado pelas subclasses"""
        pass
    
    def refresh(self):
        """Atualizar dados da view - pode ser sobrescrito pelas subclasses"""
        pass
    
    def create_header(self, title: str, subtitle: str = ""):
        """Criar cabeçalho padrão para a view"""
        header_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        # Título
        title_label = ctk.CTkLabel(
            header_frame,
            text=title,
            font=ctk.CTkFont(size=FONT_SIZES["heading"], weight="bold")
        )
        title_label.pack(anchor="w")
        
        # Subtítulo (opcional)
        if subtitle:
            subtitle_label = ctk.CTkLabel(
                header_frame,
                text=subtitle,
                font=ctk.CTkFont(size=FONT_SIZES["text"]),
                text_color="gray"
            )
            subtitle_label.pack(anchor="w", pady=(5, 0))
        
        return header_frame
    
    def create_toolbar(self):
        """Criar barra de ferramentas padrão"""
        toolbar_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        toolbar_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        return toolbar_frame
    
    def create_search_bar(self, parent, placeholder="Pesquisar...", command=None):
        """Criar barra de pesquisa padrão"""
        search_frame = ctk.CTkFrame(parent, fg_color="transparent")
        search_frame.pack(side="left", fill="x", expand=True)
        
        search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text=placeholder,
            height=40,
            font=ctk.CTkFont(size=FONT_SIZES["text"])
        )
        search_entry.pack(side="left", fill="x", expand=True)
        
        if command:
            search_entry.bind("<KeyRelease>", command)
        
        return search_entry
    
    def create_action_button(self, parent, text: str, command=None, color=None, icon=""):
        """Criar botão de ação padrão"""
        button_text = f"{icon} {text}" if icon else text
        
        button = ctk.CTkButton(
            parent,
            text=button_text,
            command=command,
            height=40,
            font=ctk.CTkFont(size=FONT_SIZES["button"])
        )
        
        if color:
            if color in COLORS:
                button.configure(fg_color=COLORS[color])
            else:
                button.configure(fg_color=color)
        
        return button
    
    def create_stat_card(self, parent, title: str, value: str, icon: str = "", color: str = "primary"):
        """Criar card de estatística padrão"""
        card = ctk.CTkFrame(parent)
        # Removido o pack() - deixar para quem chama gerenciar o posicionamento
        
        # Ícone e título
        header_frame = ctk.CTkFrame(card, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        if icon:
            icon_label = ctk.CTkLabel(
                header_frame,
                text=icon,
                font=ctk.CTkFont(size=24)
            )
            icon_label.pack(side="left")
        
        title_label = ctk.CTkLabel(
            header_frame,
            text=title,
            font=ctk.CTkFont(size=FONT_SIZES["label"]),
            text_color="gray"
        )
        title_label.pack(side="left", padx=(10, 0) if icon else (0, 0))
        
        # Valor
        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(size=FONT_SIZES["title"], weight="bold")
        )
        value_label.pack(padx=20, pady=(0, 20))
        
        # Aplicar cor se especificada
        if color and color in COLORS:
            card.configure(border_width=2, border_color=COLORS[color])
        
        return card
    
    def show_message(self, message: str, type: str = "info"):
        """Mostrar mensagem para o usuário"""
        from tkinter import messagebox
        
        if type == "success":
            messagebox.showinfo("Sucesso", message)
        elif type == "warning":
            messagebox.showwarning("Aviso", message)
        elif type == "error":
            messagebox.showerror("Erro", message)
        else:
            messagebox.showinfo("Informação", message)
    
    def confirm_action(self, message: str, title: str = "Confirmação") -> bool:
        """Solicitar confirmação do usuário"""
        from tkinter import messagebox
        return messagebox.askyesno(title, message) 