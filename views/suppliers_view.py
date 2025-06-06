"""
View de gerenciamento de fornecedores
"""

import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
from views.base_view import BaseView
from dialogs import SupplierDialog
from config import FONT_SIZES, COLORS

class SuppliersView(BaseView):
    """View de gerenciamento de fornecedores"""
    
    def __init__(self, parent, manager, root_window):
        super().__init__(parent, manager)
        self.root_window = root_window
        self.selected_supplier = None
        self.suppliers_tree = None
    
    def create_widgets(self):
        """Criar widgets da view de fornecedores"""
        # Frame já criado na BaseView, não precisa recriar
        
        # Cabeçalho
        self.create_header("🏢 Gestão de Fornecedores", "Cadastro e controle de fornecedores")
        
        # Barra de ferramentas
        self.create_toolbar_section()
        
        # Tabela de fornecedores
        self.create_suppliers_table()
        
        # Carregar dados
        self.load_suppliers_data()
    
    def create_toolbar_section(self):
        """Criar barra de ferramentas"""
        toolbar = self.create_toolbar()
        
        # Botão Novo Fornecedor
        self.add_btn = self.create_action_button(
            toolbar, "Novo Fornecedor", self.show_add_supplier_dialog,
            color="success", icon="➕"
        )
        self.add_btn.pack(side="left", padx=(0, 10))
        
        # Botão Editar
        self.edit_btn = self.create_action_button(
            toolbar, "Editar", self.edit_selected_supplier,
            color="warning", icon="✏️"
        )
        self.edit_btn.pack(side="left", padx=(0, 10))
        
        # Separador
        separator = ctk.CTkFrame(toolbar, width=2, height=30, fg_color="#666666")
        separator.pack(side="left", padx=10)
        
        # Filtros de status
        status_label = ctk.CTkLabel(
            toolbar,
            text="Status:",
            font=ctk.CTkFont(size=FONT_SIZES["text"], weight="bold")
        )
        status_label.pack(side="left", padx=(10, 5))
        
        self.status_filter = ctk.CTkComboBox(
            toolbar,
            values=["Todos", "Ativos", "Inativos"],
            width=120,
            height=30,
            font=ctk.CTkFont(size=FONT_SIZES["text"]),
            command=self.on_status_filter_change
        )
        self.status_filter.set("Todos")
        self.status_filter.pack(side="left", padx=(0, 10))
        
        # Separador
        separator2 = ctk.CTkFrame(toolbar, width=2, height=30, fg_color="#666666")
        separator2.pack(side="left", padx=10)
        
        # Campo de busca
        search_label = ctk.CTkLabel(
            toolbar,
            text="Buscar:",
            font=ctk.CTkFont(size=FONT_SIZES["text"], weight="bold")
        )
        search_label.pack(side="left", padx=(10, 5))
        
        self.search_var = tk.StringVar()
        self.search_entry = ctk.CTkEntry(
            toolbar,
            textvariable=self.search_var,
            placeholder_text="Nome, contato, telefone...",
            width=200,
            height=30,
            font=ctk.CTkFont(size=FONT_SIZES["text"])
        )
        self.search_entry.pack(side="left", padx=(0, 5))
        self.search_var.trace('w', self.on_search_change)
        # Bind Enter para aplicar filtro
        self.search_entry.bind("<Return>", lambda e: self.on_search_change())
        
        # Botão limpar busca
        clear_btn = self.create_action_button(
            toolbar, "Limpar", self.clear_search,
            color="secondary", icon="🗑️"
        )
        clear_btn.configure(width=80)
        clear_btn.pack(side="left", padx=(0, 10))
        
        # Status da seleção
        self.selected_supplier_label = ctk.CTkLabel(
            toolbar,
            text="❌ Nenhum fornecedor selecionado",
            font=ctk.CTkFont(size=FONT_SIZES["text"], weight="bold"),
            text_color=COLORS["error"]
        )
        self.selected_supplier_label.pack(side="right")
    
    def create_suppliers_table(self):
        """Criar tabela de fornecedores"""
        table_frame = ctk.CTkFrame(self.frame)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Colunas
        columns = ('code', 'name', 'contact', 'phone', 'email', 'products_count', 'status')
        
        # Treeview
        self.suppliers_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Cabeçalhos
        headers = {
            'code': 'Código',
            'name': 'Nome',
            'contact': 'Contato',
            'phone': 'Telefone',
            'email': 'Email',
            'products_count': 'Produtos',
            'status': 'Status'
        }
        
        for col, header in headers.items():
            self.suppliers_tree.heading(col, text=header, anchor='w')
            if col in ['products_count', 'code']:
                self.suppliers_tree.column(col, anchor='center', width=80)
            elif col in ['phone']:
                self.suppliers_tree.column(col, anchor='center', width=120)
            elif col in ['status']:
                self.suppliers_tree.column(col, anchor='center', width=100)
            else:
                self.suppliers_tree.column(col, anchor='w', width=150)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.suppliers_tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=self.suppliers_tree.xview)
        self.suppliers_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid layout para melhor controle
        self.suppliers_tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Configurar peso das linhas e colunas
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # Bind duplo clique para editar
        self.suppliers_tree.bind("<Double-1>", self.edit_supplier)
        
        # Bind seleção para atualizar status
        self.suppliers_tree.bind("<<TreeviewSelect>>", self.on_supplier_select)
    
    def load_suppliers_data(self):
        """Carregar dados dos fornecedores"""
        # Limpar tabela
        for item in self.suppliers_tree.get_children():
            self.suppliers_tree.delete(item)
        
        # Obter filtros atuais
        status_filter = getattr(self, 'status_filter', None)
        current_filter = status_filter.get() if status_filter else "Todos"
        
        search_var = getattr(self, 'search_var', None)
        search_text = search_var.get().lower().strip() if search_var else ""
        
        # Filtrar fornecedores
        filtered_suppliers = []
        for supplier in self.manager.suppliers:
            is_active = supplier.get('active', True)
            
            # Aplicar filtro de status
            if current_filter == "Ativos" and not is_active:
                continue
            elif current_filter == "Inativos" and is_active:
                continue
            
            # Aplicar filtro de busca
            if search_text:
                contact = supplier.get('contact_person', '') or supplier.get('contact', '')
                searchable_fields = [
                    supplier.get('name', '').lower(),
                    contact.lower(),
                    supplier.get('phone', '').lower(),
                    supplier.get('email', '').lower()
                ]
                
                if not any(search_text in field for field in searchable_fields):
                    continue
            
            filtered_suppliers.append(supplier)
        
        # Adicionar fornecedores filtrados
        for supplier in filtered_suppliers:
            # Contar produtos do fornecedor
            products_count = len([p for p in self.manager.products if p.get('supplier') == supplier.get('name')])
            
            # Verificar status ativo/inativo
            is_active = supplier.get('active', True)
            status = "✅ Ativo" if is_active else "❌ Inativo"
            
            # Buscar contato (pode estar em 'contact' ou 'contact_person')
            contact = supplier.get('contact_person', '') or supplier.get('contact', '')
            
            self.suppliers_tree.insert('', 'end', values=(
                supplier.get('id', ''),  # Usar ID como código
                supplier.get('name', ''),
                contact,
                supplier.get('phone', ''),
                supplier.get('email', ''),
                products_count,
                status
            ))
    
    def on_supplier_select(self, event):
        """Evento de seleção de fornecedor"""
        selection = self.suppliers_tree.selection()
        if selection:
            item = self.suppliers_tree.item(selection[0])
            name = item['values'][1]
            self.selected_supplier = self.manager.get_supplier_by_name(name)
            
            if self.selected_supplier:
                self.selected_supplier_label.configure(
                    text=f"✅ Selecionado: {self.selected_supplier['name']}",
                    text_color=COLORS["success"]
                )
        else:
            self.selected_supplier = None
            self.selected_supplier_label.configure(
                text="❌ Nenhum fornecedor selecionado",
                text_color=COLORS["error"]
            )
    
    def show_add_supplier_dialog(self):
        """Mostrar diálogo de adicionar fornecedor"""
        dialog = SupplierDialog(self.root_window, self.manager, title="Novo Fornecedor")
        self.root_window.wait_window(dialog.dialog)
        
        if dialog.result:
            self.load_suppliers_data()
            self.show_message("Fornecedor adicionado com sucesso!", "success")
    
    def edit_selected_supplier(self, event=None):
        """Editar fornecedor selecionado"""
        if not self.selected_supplier:
            self.show_message("Selecione um fornecedor para editar.", "warning")
            return
        
        dialog = SupplierDialog(
            self.root_window, 
            self.manager, 
            self.selected_supplier, 
            title="Editar Fornecedor"
        )
        self.root_window.wait_window(dialog.dialog)
        
        if dialog.result:
            self.load_suppliers_data()
            self.show_message("Fornecedor atualizado com sucesso!", "success")
    
    def on_status_filter_change(self, value=None):
        """Filtrar fornecedores por status"""
        self.load_suppliers_data()
    
    def on_search_change(self, *args):
        """Filtrar fornecedores por busca"""
        self.load_suppliers_data()
    
    def clear_search(self):
        """Limpar campo de busca"""
        self.search_var.set("")
        self.status_filter.set("Todos")
        self.load_suppliers_data()
    
    def refresh(self):
        """Atualizar dados da view"""
        self.load_suppliers_data()

    def edit_supplier(self, event=None):
        """Editar fornecedor selecionado"""
        selection = self.suppliers_tree.selection()
        if not selection:
            self.show_message("Selecione um fornecedor para editar.", "warning")
            return
            
        item = self.suppliers_tree.item(selection[0])
        supplier_name = item['values'][1]  # Nome está na segunda coluna
        
        # Buscar fornecedor pelo nome
        supplier = None
        for s in self.manager.suppliers:
            if s.get('name') == supplier_name:
                supplier = s
                break
        
        if supplier:
            # Usar o diálogo de fornecedor existente
            dialog = SupplierDialog(
                self.root_window, 
                self.manager, 
                supplier, 
                title="Editar Fornecedor"
            )
            self.root_window.wait_window(dialog.dialog)
            
            if dialog.result:
                self.load_suppliers_data()
                self.show_message("Fornecedor atualizado com sucesso!", "success")
        else:
            self.show_message("Fornecedor não encontrado", "error")

    def add_supplier(self):
        """Adicionar novo fornecedor"""
        self.show_message("Adição de fornecedor em desenvolvimento", "info")

    def delete_supplier(self):
        """Excluir fornecedor selecionado"""
        selection = self.suppliers_tree.selection()
        if not selection:
            self.show_message("Selecione um fornecedor para excluir.", "warning")
            return
            
        item = self.suppliers_tree.item(selection[0])
        supplier_name = item['values'][1]
        
        if self.confirm_action(f"Tem certeza que deseja excluir o fornecedor '{supplier_name}'?"):
            self.show_message("Exclusão de fornecedor em desenvolvimento", "info") 