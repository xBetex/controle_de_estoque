"""
View de gerenciamento de produtos
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
from views.base_view import BaseView
from dialogs import ProductDialog, StockAdjustmentDialog
from config import FONT_SIZES, COLORS

class ProductsView(BaseView):
    """View de gerenciamento de produtos"""
    
    def __init__(self, parent, manager, root_window):
        super().__init__(parent, manager)
        self.root_window = root_window
        self.selected_product = None
        self.search_var = None
        self.products_tree = None
    
    def create_widgets(self):
        """Criar widgets da view de produtos"""
        # Frame já criado na BaseView, não precisa recriar
        
        # Cabeçalho
        self.create_header("📋 Gestão de Produtos", "Cadastro e controle de produtos")
        
        # Barra de ferramentas
        self.create_toolbar_section()
        
        # Tabela de produtos
        self.create_products_table()
        
        # Carregar dados
        self.load_products_data()
    
    def create_toolbar_section(self):
        """Criar barra de ferramentas"""
        toolbar = self.create_toolbar()
        
        # Botão Novo Produto
        add_btn = self.create_action_button(
            toolbar, "Novo Produto", self.show_add_product_dialog,
            color="success", icon="➕"
        )
        add_btn.pack(side="left", padx=(0, 10))
        
        # Botão Editar
        edit_btn = self.create_action_button(
            toolbar, "Editar", self.edit_selected_product,
            color="warning", icon="✏️"
        )
        edit_btn.pack(side="left", padx=(0, 10))
        
        # Status da seleção
        self.selected_product_label = ctk.CTkLabel(
            toolbar,
            text="❌ Nenhum produto selecionado",
            font=ctk.CTkFont(size=FONT_SIZES["text"], weight="bold"),
            text_color=COLORS["error"]
        )
        self.selected_product_label.pack(side="right", padx=(0, 10))
        
        # Campo de pesquisa
        search_frame = ctk.CTkFrame(toolbar, fg_color="transparent")
        search_frame.pack(side="right", padx=(10, 0))
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Pesquisar produtos...",
            height=40,
            width=200,
            font=ctk.CTkFont(size=FONT_SIZES["text"])
        )
        self.search_entry.pack(side="left", padx=(0, 5))
        # Bind Enter para aplicar filtro
        self.search_entry.bind("<Return>", self.on_search_products)
        
        # Botão de pesquisa
        search_btn = self.create_action_button(
            search_frame, "Filtrar", self.on_search_products,
            color="primary", icon="🔍"
        )
        search_btn.pack(side="left", padx=(0, 5))
        
        # Botão limpar filtro
        clear_btn = self.create_action_button(
            search_frame, "Limpar", self.clear_search,
            color="secondary", icon="🗑️"
        )
        clear_btn.pack(side="left")

    def edit_product(self, event=None):
        """Editar produto selecionado (melhorado)"""
        selection = self.products_tree.selection()
        if not selection:
            self.show_message("Selecione um produto para editar.", "warning")
            return
            
        item = self.products_tree.item(selection[0])
        product_code = item['values'][0]  # Código está na primeira coluna
        
        # Buscar produto pelo código
        product = self.manager.get_product(product_code)
        if product:
            # Usar o diálogo de produto existente
            dialog = ProductDialog(
                self.root_window, 
                self.manager, 
                product, 
                title="Editar Produto"
            )
            self.root_window.wait_window(dialog.dialog)
            
            if dialog.result:
                self.load_products_table()
                self.show_message("Produto atualizado com sucesso!", "success")
        else:
            self.show_message("Produto não encontrado", "error")

    def load_products_data(self):
        """Carregar dados dos produtos"""
        self.load_products_table()

    def create_products_table(self):
        """Criar tabela de produtos"""
        table_frame = ctk.CTkFrame(self.frame)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Colunas
        columns = ('code', 'name', 'category', 'quantity', 'min_stock', 'price', 'supplier')
        
        # Treeview
        self.products_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Cabeçalhos
        headers = {
            'code': 'Código',
            'name': 'Nome',
            'category': 'Categoria',
            'quantity': 'Quantidade',
            'min_stock': 'Estoque Mín.',
            'price': 'Preço',
            'supplier': 'Fornecedor'
        }
        
        for col, header in headers.items():
            self.products_tree.heading(col, text=header, anchor='w')
            if col in ['quantity', 'min_stock', 'price']:
                self.products_tree.column(col, anchor='center', width=100)
            else:
                self.products_tree.column(col, anchor='w', width=120)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.products_tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=self.products_tree.xview)
        self.products_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack em vez de grid
        self.products_tree.pack(side="left", fill="both", expand=True)
        v_scrollbar.pack(side="right", fill="y")
        
        # Frame para scrollbar horizontal
        h_frame = ctk.CTkFrame(table_frame, fg_color="transparent")
        h_frame.pack(side="bottom", fill="x")
        h_scrollbar = ttk.Scrollbar(h_frame, orient="horizontal", command=self.products_tree.xview)
        h_scrollbar.pack(fill="x")
        self.products_tree.configure(xscrollcommand=h_scrollbar.set)
        
        # Bind duplo clique para editar
        self.products_tree.bind("<Double-1>", self.edit_product)
        
        # Bind seleção para rastrear produto selecionado
        self.products_tree.bind('<ButtonRelease-1>', self.on_product_select)
    
    def create_products_context_menu(self):
        """Criar menu de contexto para produtos"""
        self.context_menu = tk.Menu(self.root_window, tearoff=0)
        self.context_menu.add_command(label="✏️ Editar", command=self.edit_selected_product)
        self.context_menu.add_command(label="🔄 Ajustar Estoque", command=self.adjust_stock_dialog)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="🗑️ Excluir", command=self.delete_selected_product)
        
        self.products_tree.bind("<Button-3>", self.show_products_context_menu)
    
    def show_products_context_menu(self, event):
        """Mostrar menu de contexto"""
        if self.selected_product:
            self.context_menu.post(event.x_root, event.y_root)
    
    def load_products_table(self, products=None):
        """Carregar produtos na tabela"""
        # Limpar tabela
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)
        
        # Produtos a exibir
        products_to_show = products if products is not None else self.manager.products
        
        # Adicionar produtos
        for product in products_to_show:
            # Determinar status
            quantity = product.get('quantity', 0)
            min_stock = product.get('min_stock', 0)
            
            if quantity == 0:
                status = "❌ Sem Estoque"
            elif quantity <= min_stock:
                status = "⚠️ Estoque Baixo"
            else:
                status = "✅ Normal"
            
            # Inserir na tabela
            self.products_tree.insert('', 'end', values=(
                product.get('code', ''),
                product.get('name', ''),
                product.get('category', ''),
                quantity,
                min_stock,
                f"{product.get('price', 0):.2f}",
                product.get('supplier', '')
            ))
    
    def on_product_select(self, event):
        """Evento de seleção de produto"""
        selection = self.products_tree.selection()
        if selection:
            item = self.products_tree.item(selection[0])
            code = item['values'][0]
            self.selected_product = self.manager.get_product(code)
            
            if self.selected_product:
                self.selected_product_label.configure(
                    text=f"✅ Selecionado: {self.selected_product['name']}",
                    text_color=COLORS["success"]
                )
        else:
            self.selected_product = None
            self.selected_product_label.configure(
                text="❌ Nenhum produto selecionado",
                text_color=COLORS["error"]
            )
    
    def on_search_products(self, event=None):
        """Evento de pesquisa de produtos"""
        search_term = self.search_entry.get().lower().strip()
        
        if not search_term:
            # Se não há termo de pesquisa, mostrar todos os produtos
            self.load_products_table()
            return
        
        # Filtrar produtos baseado no termo de pesquisa
        filtered_products = []
        for product in self.manager.products:
            # Pesquisar em código, nome, categoria e fornecedor
            search_fields = [
                product.get('code', '').lower(),
                product.get('name', '').lower(),
                product.get('category', '').lower(),
                product.get('supplier', '').lower()
            ]
            
            # Se o termo de pesquisa está em qualquer campo, incluir o produto
            if any(search_term in field for field in search_fields):
                filtered_products.append(product)
        
        # Atualizar tabela com produtos filtrados
        self.load_products_table(filtered_products)
        
        # Atualizar label de status sem popup
        total_products = len(self.manager.products)
        found_products = len(filtered_products)
        
        if found_products < total_products:
            if hasattr(self, 'selected_product_label'):
                self.selected_product_label.configure(
                    text=f"🔍 {found_products} de {total_products} produtos encontrados",
                    text_color=COLORS["primary"]
                )
        else:
            if hasattr(self, 'selected_product_label'):
                self.selected_product_label.configure(
                    text="✅ Mostrando todos os produtos",
                    text_color=COLORS["success"]
                )
    
    def clear_search(self):
        """Limpar pesquisa e mostrar todos os produtos"""
        self.search_entry.delete(0, 'end')
        self.load_products_table()
        if hasattr(self, 'selected_product_label'):
            self.selected_product_label.configure(
                text="❌ Nenhum produto selecionado",
                text_color=COLORS["error"]
            )
    
    def show_add_product_dialog(self):
        """Mostrar diálogo de adicionar produto"""
        dialog = ProductDialog(self.root_window, self.manager, title="Novo Produto")
        self.root_window.wait_window(dialog.dialog)
        
        if dialog.result:
            self.load_products_table()
            self.show_message("Produto adicionado com sucesso!", "success")
    
    def edit_selected_product(self, event=None):
        """Editar produto selecionado"""
        if not self.selected_product:
            self.show_message("Selecione um produto para editar.", "warning")
            return
        
        dialog = ProductDialog(
            self.root_window, 
            self.manager, 
            self.selected_product, 
            title="Editar Produto"
        )
        self.root_window.wait_window(dialog.dialog)
        
        if dialog.result:
            self.load_products_table()
            self.show_message("Produto atualizado com sucesso!", "success")
    
    def delete_selected_product(self):
        """Excluir produto selecionado"""
        if not self.selected_product:
            self.show_message("Selecione um produto para excluir.", "warning")
            return
        
        product_name = self.selected_product['name']
        if self.confirm_action(
            f"Tem certeza que deseja excluir o produto '{product_name}'?\n"
            "Esta ação não pode ser desfeita.",
            "Confirmar Exclusão"
        ):
            if self.manager.delete_product(self.selected_product['code']):
                self.selected_product = None
                self.selected_product_label.configure(
                    text="❌ Nenhum produto selecionado",
                    text_color=COLORS["error"]
                )
                self.load_products_table()
                self.show_message("Produto excluído com sucesso!", "success")
            else:
                self.show_message("Erro ao excluir produto.", "error")
    
    def adjust_stock_dialog(self):
        """Mostrar diálogo de ajuste de estoque"""
        if not self.selected_product:
            self.show_message("Selecione um produto para ajustar o estoque.", "warning")
            return
        
        dialog = StockAdjustmentDialog(self.root_window, self.manager, self.selected_product)
        self.root_window.wait_window(dialog.dialog)
        
        if dialog.result:
            self.load_products_table()
            self.show_message("Estoque ajustado com sucesso!", "success")
    
    def refresh(self):
        """Atualizar dados da view"""
        self.load_products_table() 