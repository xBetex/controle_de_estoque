"""
View de gerenciamento de categorias
"""

import customtkinter as ctk
from tkinter import ttk
from views.base_view import BaseView
from dialogs import CategoryDialog
from config import FONT_SIZES, COLORS

class CategoriesView(BaseView):
    """View de gerenciamento de categorias"""
    
    def __init__(self, parent, manager, root_window):
        super().__init__(parent, manager)
        self.root_window = root_window
        self.selected_category = None
        self.categories_tree = None
    
    def create_widgets(self):
        """Criar widgets da view de categorias"""
        # Frame já criado na BaseView, não precisa recriar
        
        # Cabeçalho 
        self.create_header("🏷️ Gestão de Categorias", "Cadastro e controle de categorias")
        
        # Barra de ferramentas
        self.create_toolbar_section()
        
        # Tabela de categorias
        self.create_categories_table()
        
        # Carregar dados
        self.load_categories_data()
    
    def create_toolbar_section(self):
        """Criar barra de ferramentas"""
        toolbar = self.create_toolbar()
        
        # Botão Nova Categoria
        self.add_btn = self.create_action_button(
            toolbar, "Nova Categoria", self.show_add_category_dialog,
            color="success", icon="➕"
        )
        self.add_btn.pack(side="left", padx=(0, 10))
        
        # Botão Editar
        self.edit_btn = self.create_action_button(
            toolbar, "Editar", self.edit_selected_category,
            color="warning", icon="✏️"
        )
        self.edit_btn.pack(side="left", padx=(0, 10))
    
    def create_categories_table(self):
        """Criar tabela de categorias"""
        table_frame = ctk.CTkFrame(self.frame)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Colunas
        columns = ('name', 'description', 'products_count')
        
        # Treeview
        self.categories_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Cabeçalhos
        headers = {
            'name': 'Nome',
            'description': 'Descrição',
            'products_count': 'Produtos'
        }
        
        for col, header in headers.items():
            self.categories_tree.heading(col, text=header, anchor='w')
            if col == 'products_count':
                self.categories_tree.column(col, anchor='center', width=100)
            else:
                self.categories_tree.column(col, anchor='w', width=200)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.categories_tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=self.categories_tree.xview)
        self.categories_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack em vez de grid
        self.categories_tree.pack(side="left", fill="both", expand=True)
        v_scrollbar.pack(side="right", fill="y")
        
        # Frame para scrollbar horizontal
        h_frame = ctk.CTkFrame(table_frame, fg_color="transparent")  
        h_frame.pack(side="bottom", fill="x")
        h_scrollbar = ttk.Scrollbar(h_frame, orient="horizontal", command=self.categories_tree.xview)
        h_scrollbar.pack(fill="x")
        self.categories_tree.configure(xscrollcommand=h_scrollbar.set)
        
        # Bind duplo clique para editar
        self.categories_tree.bind("<Double-1>", self.edit_category)
        
        # Bind seleção para atualizar status
        self.categories_tree.bind("<<TreeviewSelect>>", self.on_category_select)
    
    def load_categories_data(self):
        """Carregar dados das categorias"""
        # Limpar tabela
        for item in self.categories_tree.get_children():
            self.categories_tree.delete(item)
        
        # Adicionar categorias
        for category in self.manager.categories:
            # Contar produtos na categoria
            products_count = len(self.manager.get_products_by_category(category['name']))
            
            self.categories_tree.insert('', 'end', values=(
                category.get('name', ''),
                category.get('description', ''),
                products_count
            ))
    
    def on_category_select(self, event):
        """Evento de seleção de categoria"""
        selection = self.categories_tree.selection()
        if selection:
            item = self.categories_tree.item(selection[0])
            name = item['values'][0]
            self.selected_category = self.manager.get_category_by_name(name)
    
    def show_add_category_dialog(self):
        """Mostrar diálogo de adicionar categoria"""
        dialog = CategoryDialog(self.root_window, self.manager, title="Nova Categoria")
        self.root_window.wait_window(dialog.dialog)
        
        if dialog.result:
            self.load_categories_data()
            self.show_message("Categoria adicionada com sucesso!", "success")
    
    def edit_selected_category(self, event=None):
        """Editar categoria selecionada"""
        if not self.selected_category:
            self.show_message("Selecione uma categoria para editar.", "warning")
            return
        
        dialog = CategoryDialog(
            self.root_window, 
            self.manager, 
            self.selected_category, 
            title="Editar Categoria"
        )
        self.root_window.wait_window(dialog.dialog)
        
        if dialog.result:
            self.load_categories_data()
            self.show_message("Categoria atualizada com sucesso!", "success")
    
    def refresh(self):
        """Atualizar dados da view"""
        self.load_categories_data()

    def edit_category(self, event=None):
        """Editar categoria selecionada"""
        selection = self.categories_tree.selection()
        if not selection:
            self.show_message("Selecione uma categoria para editar.", "warning")
            return
            
        item = self.categories_tree.item(selection[0])
        category_name = item['values'][0]  # Nome está na primeira coluna
        
        # Buscar categoria pelo nome
        category = None
        for c in self.manager.categories:
            if c.get('name') == category_name:
                category = c
                break
        
        if category:
            # Usar o diálogo de categoria existente
            dialog = CategoryDialog(
                self.root_window, 
                self.manager, 
                category, 
                title="Editar Categoria"
            )
            self.root_window.wait_window(dialog.dialog)
            
            if dialog.result:
                self.load_categories_data()
                self.show_message("Categoria atualizada com sucesso!", "success")
        else:
            self.show_message("Categoria não encontrada", "error")

    def add_category(self):
        """Adicionar nova categoria"""
        self.show_message("Adição de categoria em desenvolvimento", "info")

    def delete_category(self):
        """Excluir categoria selecionada"""
        selection = self.categories_tree.selection()
        if not selection:
            self.show_message("Selecione uma categoria para excluir.", "warning")
            return
            
        item = self.categories_tree.item(selection[0])
        category_name = item['values'][0]
        
        if self.confirm_action(f"Tem certeza que deseja excluir a categoria '{category_name}'?"):
            self.show_message("Exclusão de categoria em desenvolvimento", "info") 