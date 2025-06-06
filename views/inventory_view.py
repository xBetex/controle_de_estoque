"""
View de inventário/estoque
"""

import customtkinter as ctk
from tkinter import ttk
from views.base_view import BaseView
from config import FONT_SIZES, COLORS

class InventoryView(BaseView):
    """View de inventário/estoque"""
    
    def __init__(self, parent, manager):
        super().__init__(parent, manager)
        self.filter_var = None
        self.inventory_tree = None
    
    def create_widgets(self):
        """Criar widgets da view de inventário"""
        # Frame já criado na BaseView, não precisa recriar
        
        # Cabeçalho
        self.create_header("📦 Controle de Estoque", "Visualização completa do inventário")
        
        # Filtros
        self.create_filters_section()
        
        # Tabela de inventário
        self.create_inventory_table()
        
        # Carregar dados
        self.load_inventory_data()
    
    def create_filters_section(self):
        """Criar seção de filtros"""
        filters_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        filters_frame.pack(fill="x", padx=20, pady=10)
        
        # Linha superior - filtros
        top_filters = ctk.CTkFrame(filters_frame, fg_color="transparent")
        top_filters.pack(fill="x", pady=(0, 10))
        
        # Filtro por status
        ctk.CTkLabel(
            top_filters, 
            text="Status:", 
            font=ctk.CTkFont(size=FONT_SIZES["label"])
        ).pack(side="left", padx=(0, 5))
        
        self.filter_var = ctk.StringVar(value="Todos")
        filter_menu = ctk.CTkOptionMenu(
            top_filters,
            variable=self.filter_var,
            values=["Todos", "Normal", "Estoque Baixo", "Sem Estoque"],
            width=150
        )
        filter_menu.pack(side="left", padx=(0, 20))
        
        # Linha inferior - pesquisa
        bottom_filters = ctk.CTkFrame(filters_frame, fg_color="transparent")
        bottom_filters.pack(fill="x")
        
        # Campo de pesquisa
        ctk.CTkLabel(
            bottom_filters, 
            text="Pesquisar:", 
            font=ctk.CTkFont(size=FONT_SIZES["label"])
        ).pack(side="left", padx=(0, 5))
        
        self.search_entry = ctk.CTkEntry(
            bottom_filters,
            placeholder_text="Código, nome, categoria...",
            height=40,
            width=200,
            font=ctk.CTkFont(size=FONT_SIZES["text"])
        )
        self.search_entry.pack(side="left", padx=(0, 5))
        # Bind Enter para aplicar filtro
        self.search_entry.bind("<Return>", lambda e: self.apply_filters())
        
        # Botão filtrar
        filter_btn = self.create_action_button(
            bottom_filters, "Filtrar", self.apply_filters,
            color="primary", icon="🔍"
        )
        filter_btn.pack(side="left", padx=(0, 5))
        
        # Botão limpar
        clear_btn = self.create_action_button(
            bottom_filters, "Limpar", self.clear_filters,
            color="secondary", icon="🗑️"
        )
        clear_btn.pack(side="left", padx=(0, 20))
        
        # Resumo do estoque
        self.create_inventory_summary(bottom_filters)
    
    def create_inventory_summary(self, parent):
        """Criar resumo do estoque"""
        summary_frame = ctk.CTkFrame(parent)
        summary_frame.pack(side="right", padx=(20, 0))
        
        stats = self.calculate_inventory_stats()
        
        summary_text = f"Total: {stats['total']} | Normal: {stats['normal']} | Baixo: {stats['low']} | Sem: {stats['empty']}"
        
        ctk.CTkLabel(
            summary_frame,
            text=summary_text,
            font=ctk.CTkFont(size=FONT_SIZES["text"]),
            fg_color="transparent"
        ).pack(padx=10, pady=5)
    
    def create_inventory_table(self):
        """Criar tabela de inventário"""
        table_frame = ctk.CTkFrame(self.frame)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Colunas
        columns = ('code', 'name', 'quantity', 'min_stock', 'price', 'value', 'category', 'status')
        
        # Treeview
        self.inventory_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Cabeçalhos
        headers = {
            'code': 'Código',
            'name': 'Nome',
            'quantity': 'Quantidade',
            'min_stock': 'Mín. Estoque',
            'price': 'Preço Unit.',
            'value': 'Valor Total',
            'category': 'Categoria',
            'status': 'Status'
        }
        
        for col, header in headers.items():
            self.inventory_tree.heading(col, text=header, anchor='w')
            if col in ['quantity', 'min_stock', 'price', 'value']:
                self.inventory_tree.column(col, anchor='center', width=100)
            else:
                self.inventory_tree.column(col, anchor='w', width=120)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.inventory_tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=self.inventory_tree.xview)
        self.inventory_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack em vez de grid
        self.inventory_tree.pack(side="left", fill="both", expand=True)
        v_scrollbar.pack(side="right", fill="y")
        
        # Frame para scrollbar horizontal
        h_frame = ctk.CTkFrame(table_frame, fg_color="transparent")
        h_frame.pack(side="bottom", fill="x")
        h_scrollbar = ttk.Scrollbar(h_frame, orient="horizontal", command=self.inventory_tree.xview)
        h_scrollbar.pack(fill="x")
        self.inventory_tree.configure(xscrollcommand=h_scrollbar.set)
    
    def load_inventory_data(self, filter_status=None, search_term=None):
        """Carregar dados do inventário"""
        # Limpar tabela
        for item in self.inventory_tree.get_children():
            self.inventory_tree.delete(item)
        
        # Filtrar produtos se necessário
        products = self.manager.products
        
        # Aplicar filtro de pesquisa primeiro
        if search_term:
            products = self.filter_products_by_search(products, search_term)
        
        # Aplicar filtro por status
        if filter_status and filter_status != "Todos":
            products = self.filter_products_by_status(products, filter_status)
        
        # Adicionar produtos à tabela
        for product in products:
            quantity = product.get('quantity', 0)
            min_stock = product.get('min_stock', 0)
            price = product.get('price', 0)
            total_value = quantity * price
            
            # Determinar status
            if quantity == 0:
                status = "❌ Sem Estoque"
                tag = "empty"
            elif quantity <= min_stock:
                status = "⚠️ Estoque Baixo"
                tag = "low"
            else:
                status = "✅ Normal"
                tag = "normal"
            
            # Inserir na tabela
            item = self.inventory_tree.insert('', 'end', values=(
                product.get('code', ''),
                product.get('name', ''),
                quantity,
                min_stock,
                f"R$ {price:.2f}",
                f"R$ {total_value:.2f}",
                product.get('category', ''),
                status
            ), tags=(tag,))
        
        # Configurar cores por tag
        self.inventory_tree.tag_configure('empty', background='#ffebee')
        self.inventory_tree.tag_configure('low', background='#fff3e0')
        self.inventory_tree.tag_configure('normal', background='#e8f5e8')
    
    def filter_products_by_status(self, products, status):
        """Filtrar produtos por status"""
        filtered = []
        for product in products:
            quantity = product.get('quantity', 0)
            min_stock = product.get('min_stock', 0)
            
            if status == "Sem Estoque" and quantity == 0:
                filtered.append(product)
            elif status == "Estoque Baixo" and 0 < quantity <= min_stock:
                filtered.append(product)
            elif status == "Normal" and quantity > min_stock:
                filtered.append(product)
        
        return filtered
    
    def apply_filters(self):
        """Aplicar todos os filtros"""
        filter_status = self.filter_var.get() if self.filter_var else "Todos"
        search_term = self.search_entry.get().lower().strip() if hasattr(self, 'search_entry') else ""
        self.load_inventory_data(filter_status, search_term)
    
    def clear_filters(self):
        """Limpar todos os filtros"""
        self.filter_var.set("Todos")
        if hasattr(self, 'search_entry'):
            self.search_entry.delete(0, 'end')
        self.load_inventory_data()
    
    def filter_products_by_search(self, products, search_term):
        """Filtrar produtos por termo de pesquisa"""
        if not search_term:
            return products
        
        filtered = []
        for product in products:
            # Pesquisar em código, nome, categoria
            search_fields = [
                product.get('code', '').lower(),
                product.get('name', '').lower(),
                product.get('category', '').lower()
            ]
            
            # Se o termo de pesquisa está em qualquer campo, incluir o produto
            if any(search_term in field for field in search_fields):
                filtered.append(product)
        
        return filtered
    
    def filter_inventory(self, value=None):
        """Filtrar inventário por status (compatibilidade)"""
        self.apply_filters()
    
    def calculate_inventory_stats(self):
        """Calcular estatísticas do inventário"""
        total = len(self.manager.products)
        normal = 0
        low = 0
        empty = 0
        
        for product in self.manager.products:
            quantity = product.get('quantity', 0)
            min_stock = product.get('min_stock', 0)
            
            if quantity == 0:
                empty += 1
            elif quantity <= min_stock:
                low += 1
            else:
                normal += 1
        
        return {
            'total': total,
            'normal': normal,
            'low': low,
            'empty': empty
        }
    
    def refresh(self):
        """Atualizar dados da view"""
        self.load_inventory_data() 