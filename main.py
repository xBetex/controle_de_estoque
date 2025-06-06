import json
import os
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Optional

# Configure matplotlib backend before importing
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for Linux compatibility
import matplotlib.pyplot as plt

try:
    import customtkinter as ctk
    from tkinter import messagebox, filedialog
    import tkinter as tk
    from tkinter import ttk
    from PIL import Image, ImageTk
    from tkcalendar import DateEntry
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import pandas as pd
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Please install dependencies: pip install -r requirements.txt")
    sys.exit(1)

# Configure CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Data files
DATA_DIR = "data"
PRODUCTS_FILE = os.path.join(DATA_DIR, "products.json")
MOVEMENTS_FILE = os.path.join(DATA_DIR, "movements.json")
SUPPLIERS_FILE = os.path.join(DATA_DIR, "suppliers.json")
CATEGORIES_FILE = os.path.join(DATA_DIR, "categories.json")
SETTINGS_FILE = os.path.join(DATA_DIR, "settings.json")

class InventoryManager:
    """Main inventory management class"""
    
    def __init__(self):
        self.create_data_directory()
        self.products = self.load_data(PRODUCTS_FILE, [])
        self.movements = self.load_data(MOVEMENTS_FILE, [])
        self.suppliers = self.load_data(SUPPLIERS_FILE, [])
        self.categories = self.load_data(CATEGORIES_FILE, [])
        self.settings = self.load_data(SETTINGS_FILE, self.default_settings())
    
    def create_data_directory(self):
        """Create data directory if it doesn't exist"""
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
    
    def default_settings(self):
        """Default application settings"""
        return {
            "theme": "dark",
            "language": "pt-BR",
            "low_stock_threshold": 5,
            "currency": "BRL",
            "backup_enabled": True,
            "auto_backup": True,
            "auto_backup_days": 7,
            "default_category": "",
            "theme_mode": "dark",
            "color_theme": "blue"
        }
    
    def load_data(self, filename: str, default: any) -> any:
        """Load data from JSON file"""
        try:
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return default
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            return default
    
    def save_data(self, data: any, filename: str) -> bool:
        """Save data to JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving {filename}: {e}")
            return False
    
    def add_product(self, product_data: Dict) -> bool:
        """Add a new product"""
        # Check if product code already exists
        if any(p['code'] == product_data['code'] for p in self.products):
            return False
            
        product_data['created_at'] = datetime.now().isoformat()
        product_data['updated_at'] = datetime.now().isoformat()
        self.products.append(product_data)
        
        # Record initial stock movement
        self.add_movement("entrada", product_data['code'], 
                         product_data['quantity'], "Cadastro inicial")
        
        return self.save_data(self.products, PRODUCTS_FILE)
    
    def update_product(self, code: str, updates: Dict) -> bool:
        """Update an existing product"""
        product = self.get_product(code)
        if not product:
            return False
        
        product.update(updates)
        product['updated_at'] = datetime.now().isoformat()
        return self.save_data(self.products, PRODUCTS_FILE)
    
    def delete_product(self, code: str) -> bool:
        """Delete a product"""
        self.products = [p for p in self.products if p['code'] != code]
        return self.save_data(self.products, PRODUCTS_FILE)
    
    def get_product(self, code: str) -> Optional[Dict]:
        """Get product by code"""
        return next((p for p in self.products if p['code'] == code), None)
    
    def update_stock(self, code: str, quantity_change: int, reason: str = "") -> bool:
        """Update product stock"""
        product = self.get_product(code)
        if not product:
            return False
        
        new_quantity = product['quantity'] + quantity_change
        if new_quantity < 0:
            return False
        
        product['quantity'] = new_quantity
        product['updated_at'] = datetime.now().isoformat()
        
        # Record movement
        movement_type = "entrada" if quantity_change > 0 else "saída"
        self.add_movement(movement_type, code, abs(quantity_change), reason)
        
        return self.save_data(self.products, PRODUCTS_FILE)
    
    def add_movement(self, movement_type: str, product_code: str, 
                    quantity: int, reason: str = "") -> bool:
        """Add stock movement record"""
        movement = {
            'id': len(self.movements) + 1,
            'date': datetime.now().isoformat(),
            'type': movement_type,
            'product_code': product_code,
            'quantity': quantity,
            'reason': reason,
            'user': "admin"  # You can implement user system later
        }
        
        self.movements.append(movement)
        return self.save_data(self.movements, MOVEMENTS_FILE)
    
    def get_low_stock_products(self) -> List[Dict]:
        """Get products with low stock"""
        threshold = self.settings.get('low_stock_threshold', 5)
        return [p for p in self.products if p['quantity'] <= threshold]
    
    def get_total_inventory_value(self) -> float:
        """Calculate total inventory value"""
        return sum(p['price'] * p['quantity'] for p in self.products)
    
    def search_products(self, query: str) -> List[Dict]:
        """Search products by name, code, or description"""
        query = query.lower()
        return [p for p in self.products if 
                query in p['name'].lower() or 
                query in p['code'].lower() or 
                query in p.get('description', '').lower()]

class ModernInventoryApp:
    """Modern inventory management application"""
    
    def __init__(self):
        self.manager = InventoryManager()
        self.setup_main_window()
        self.create_styles()
        self.create_sidebar()
        self.create_main_content()
        self.show_dashboard()
    
    def setup_main_window(self):
        """Setup the main application window"""
        self.root = ctk.CTk()
        self.root.title("Sistema de Controle de Estoque Avançado v2.0")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 700)
        
        # Configure grid
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        
        # Set window icon (if available)
        try:
            self.root.iconbitmap("assets/icon.ico")
        except:
            pass
    
    def create_styles(self):
        """Create custom styles and colors"""
        self.colors = {
            'primary': '#1f538d',
            'secondary': '#2d5aa0',
            'success': '#28a745',
            'danger': '#dc3545',
            'warning': '#ffc107',
            'info': '#17a2b8',
            'dark': '#343a40',
            'light': '#f8f9fa'
        }
    
    def create_sidebar(self):
        """Create the sidebar navigation"""
        self.sidebar = ctk.CTkFrame(self.root, width=250, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(10, weight=1)
        
        # Logo/Title
        title_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        title_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        
        logo_label = ctk.CTkLabel(
            title_frame,
            text="📦 SISTEMA DE\nESTOQUE",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#4CAF50"
        )
        logo_label.pack()
        
        version_label = ctk.CTkLabel(
            title_frame,
            text="v2.0 - Professional",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        version_label.pack(pady=(0, 10))
        
        # Navigation buttons
        nav_buttons = [
            ("🏠 Dashboard", self.show_dashboard),
            ("📊 Produtos", self.show_products),
            ("📦 Estoque", self.show_inventory),
            ("🔄 Movimentações", self.show_movements),
            ("👥 Fornecedores", self.show_suppliers),
            ("📁 Categorias", self.show_categories),
            ("📈 Relatórios", self.show_reports),
            ("⚙️ Configurações", self.show_settings),
            ("💾 Backup", self.show_backup),
            ("❓ Ajuda", self.show_help)
        ]
        
        self.nav_buttons = []
        for i, (text, command) in enumerate(nav_buttons, 1):
            btn = ctk.CTkButton(
                self.sidebar,
                text=text,
                command=command,
                width=200,
                height=45,
                font=ctk.CTkFont(size=16),
                anchor="w",
                fg_color="transparent",
                text_color=("gray10", "gray90"),
                hover_color=("gray80", "gray20")
            )
            btn.grid(row=i, column=0, padx=20, pady=5, sticky="ew")
            self.nav_buttons.append(btn)
    
    def create_main_content(self):
        """Create the main content area"""
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
    
    def clear_main_content(self):
        """Clear the main content area"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def show_dashboard(self):
        """Show the dashboard"""
        self.clear_main_content()
        
        # Dashboard container
        dashboard = ctk.CTkScrollableFrame(self.main_frame)
        dashboard.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        # Dashboard title
        title = ctk.CTkLabel(
            dashboard,
            text="📊 Dashboard do Sistema",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title.pack(pady=(0, 20))
        
        # Stats cards
        stats_frame = ctk.CTkFrame(dashboard)
        stats_frame.pack(fill="x", pady=10)
        
        # Calculate statistics
        total_products = len(self.manager.products)
        total_value = self.manager.get_total_inventory_value()
        low_stock_count = len(self.manager.get_low_stock_products())
        recent_movements = len([m for m in self.manager.movements 
                              if datetime.fromisoformat(m['date']).date() == datetime.now().date()])
        
        stats = [
            ("Total de Produtos", total_products, "📦", "#4CAF50"),
            ("Valor do Estoque", f"R$ {total_value:,.2f}", "💰", "#2196F3"),
            ("Produtos em Falta", low_stock_count, "⚠️", "#FF9800"),
            ("Movimentações Hoje", recent_movements, "📈", "#9C27B0")
        ]
        
        for i, (title, value, icon, color) in enumerate(stats):
            card = self.create_stat_card(stats_frame, title, value, icon, color)
            card.grid(row=0, column=i, padx=10, pady=10, sticky="ew")
        
        stats_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Recent activities
        activities_frame = ctk.CTkFrame(dashboard)
        activities_frame.pack(fill="both", expand=True, pady=20)
        
        activities_title = ctk.CTkLabel(
            activities_frame,
            text="📋 Atividades Recentes",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        activities_title.pack(pady=10)
        
        # Activities list
        activities_list = ctk.CTkTextbox(activities_frame, height=300, font=ctk.CTkFont(size=14))
        activities_list.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Show recent movements
        recent_movements = sorted(self.manager.movements, 
                                key=lambda x: x['date'], reverse=True)[:10]
        
        for movement in recent_movements:
            date = datetime.fromisoformat(movement['date'])
            product = self.manager.get_product(movement['product_code'])
            product_name = product['name'] if product else "Produto não encontrado"
            
            activity_text = f"[{date.strftime('%d/%m/%Y %H:%M')}] "
            activity_text += f"{movement['type'].upper()} - "
            activity_text += f"{product_name} (Qtd: {movement['quantity']})\n"
            
            activities_list.insert("end", activity_text)
    
    def create_stat_card(self, parent, title, value, icon, color):
        """Create a statistics card"""
        card = ctk.CTkFrame(parent)
        
        # Icon
        icon_label = ctk.CTkLabel(
            card,
            text=icon,
            font=ctk.CTkFont(size=40),
            text_color=color
        )
        icon_label.pack(pady=(10, 5))
        
        # Value
        value_label = ctk.CTkLabel(
            card,
            text=str(value),
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=color
        )
        value_label.pack()
        
        # Title
        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=16),
            text_color="gray"
        )
        title_label.pack(pady=(0, 10))
        
        return card
    
    def show_products(self):
        """Show products management"""
        self.clear_main_content()
        
        # Products container
        products_frame = ctk.CTkFrame(self.main_frame)
        products_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        products_frame.grid_rowconfigure(2, weight=1)
        products_frame.grid_columnconfigure(0, weight=1)
        
        # Title and controls
        header_frame = ctk.CTkFrame(products_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        
        title = ctk.CTkLabel(
            header_frame,
            text="📊 Gerenciamento de Produtos",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title.pack(side="left")
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        buttons_frame.pack(side="right")
        
        edit_btn = ctk.CTkButton(
            buttons_frame,
            text="✏️ Editar",
            command=self.edit_selected_product,
            width=120,
            height=40,
            font=ctk.CTkFont(size=16),
            fg_color="#FF9800"
        )
        edit_btn.pack(side="left", padx=(0, 10))
        
        stock_btn = ctk.CTkButton(
            buttons_frame,
            text="🔄 Ajustar Estoque",
            command=self.adjust_stock_dialog,
            width=150,
            height=40,
            font=ctk.CTkFont(size=16),
            fg_color="#9C27B0"
        )
        stock_btn.pack(side="left", padx=(0, 10))
        
        add_btn = ctk.CTkButton(
            buttons_frame,
            text="➕ Novo Produto",
            command=self.show_add_product_dialog,
            width=170,
            height=40,
            font=ctk.CTkFont(size=16)
        )
        add_btn.pack(side="left")
        
        # Search frame
        search_frame = ctk.CTkFrame(products_frame, fg_color="transparent")
        search_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        
        ctk.CTkLabel(search_frame, text="🔍 Pesquisar:", font=ctk.CTkFont(size=16)).pack(side="left", padx=(0, 10))
        
        self.search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(
            search_frame,
            textvariable=self.search_var,
            placeholder_text="Digite o nome, código ou descrição...",
            width=350,
            height=35,
            font=ctk.CTkFont(size=14)
        )
        search_entry.pack(side="left", padx=(0, 10))
        search_entry.bind('<KeyRelease>', self.on_search_products)
        
        # Selection status
        self.selected_product_label = ctk.CTkLabel(
            search_frame,
            text="❌ Nenhum produto selecionado",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#FF6B6B"
        )
        self.selected_product_label.pack(side="right", padx=(10, 0))
        
        # Products table
        self.create_products_table(products_frame)
    
    def create_products_table(self, parent):
        """Create products table"""
        # Table frame
        table_frame = ctk.CTkFrame(parent)
        table_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)
        
        # Create treeview
        columns = ('code', 'name', 'category', 'price', 'quantity', 'supplier', 'status')
        
        # Configure treeview style for larger fonts
        style = ttk.Style()
        style.configure("Treeview", font=('TkDefaultFont', 12))
        style.configure("Treeview.Heading", font=('TkDefaultFont', 14, 'bold'))
        style.map("Treeview", background=[('selected', '#0078D4')], foreground=[('selected', 'white')])
        
        self.products_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Define headings
        headings = {
            'code': 'Código',
            'name': 'Nome',
            'category': 'Categoria',
            'price': 'Preço (R$)',
            'quantity': 'Quantidade',
            'supplier': 'Fornecedor',
            'status': 'Status'
        }
        
        for col, heading in headings.items():
            self.products_tree.heading(col, text=heading)
            if col == 'price':
                self.products_tree.column(col, width=100, anchor='e')
            elif col == 'quantity':
                self.products_tree.column(col, width=80, anchor='center')
            elif col == 'code':
                self.products_tree.column(col, width=100)
            else:
                self.products_tree.column(col, width=150)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.products_tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=self.products_tree.xview)
        
        self.products_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack table and scrollbars
        self.products_tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # Context menu
        self.create_products_context_menu()
        
        # Bind selection event to show selected item info
        self.products_tree.bind('<<TreeviewSelect>>', self.on_product_select)
        
        # Bind double click to edit
        self.products_tree.bind('<Double-1>', lambda e: self.edit_selected_product())
        
        # Bind keyboard shortcuts
        self.products_tree.bind('<Control-e>', lambda e: self.edit_selected_product())
        self.products_tree.bind('<Control-E>', lambda e: self.edit_selected_product())
        
        # Load products
        self.load_products_table()
    
    def load_products_table(self, products=None):
        """Load products into the table"""
        # Clear existing items
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)
        
        # Use filtered products or all products
        products_to_show = products if products is not None else self.manager.products
        
        # Add products to table
        for product in products_to_show:
            # Determine status
            if product['quantity'] <= 0:
                status = "❌ Sem estoque"
            elif product['quantity'] <= self.manager.settings.get('low_stock_threshold', 5):
                status = "⚠️ Estoque baixo"
            else:
                status = "✅ Disponível"
            
            values = (
                product['code'],
                product['name'],
                product.get('category', ''),
                f"{product['price']:.2f}",
                product['quantity'],
                product.get('supplier', ''),
                status
            )
            
            self.products_tree.insert('', 'end', values=values)
    
    def create_products_context_menu(self):
        """Create context menu for products table"""
        self.products_context_menu = tk.Menu(self.root, tearoff=0)
        self.products_context_menu.add_command(label="✏️ Editar", command=self.edit_selected_product)
        self.products_context_menu.add_command(label="🔄 Ajustar Estoque", command=self.adjust_stock_dialog)
        self.products_context_menu.add_separator()
        self.products_context_menu.add_command(label="🗑️ Excluir", command=self.delete_selected_product)
        
        self.products_tree.bind("<Button-3>", self.show_products_context_menu)
    
    def show_products_context_menu(self, event):
        """Show context menu for products"""
        try:
            self.products_context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.products_context_menu.grab_release()
    
    def on_product_select(self, event):
        """Handle product selection"""
        selection = self.products_tree.selection()
        if hasattr(self, 'selected_product_label'):
            if selection:
                item = self.products_tree.item(selection[0])
                product_name = item['values'][1]
                self.selected_product_label.configure(
                    text=f"✅ Selecionado: {product_name}",
                    text_color="#4CAF50"
                )
            else:
                self.selected_product_label.configure(
                    text="❌ Nenhum produto selecionado",
                    text_color="#FF6B6B"
                )
    
    def on_search_products(self, event=None):
        """Handle product search"""
        query = self.search_var.get()
        if query.strip():
            filtered_products = self.manager.search_products(query)
            self.load_products_table(filtered_products)
        else:
            self.load_products_table()
    
    def show_add_product_dialog(self):
        """Show add product dialog"""
        dialog = ProductDialog(self.root, self.manager, title="Novo Produto")
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            self.load_products_table()
            self.show_dashboard()  # Refresh dashboard stats
    
    def edit_selected_product(self):
        """Edit selected product"""
        selection = self.products_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Por favor, selecione um produto na tabela para editar.\n\n💡 Dica: Clique em uma linha da tabela primeiro.")
            return
        
        item = self.products_tree.item(selection[0])
        product_code = item['values'][0]
        product = self.manager.get_product(product_code)
        
        if product:
            dialog = ProductDialog(self.root, self.manager, product=product, title="Editar Produto")
            self.root.wait_window(dialog.dialog)
            
            if dialog.result:
                self.load_products_table()
                self.show_dashboard()
    
    def delete_selected_product(self):
        """Delete selected product"""
        selection = self.products_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um produto para excluir.")
            return
        
        item = self.products_tree.item(selection[0])
        product_code = item['values'][0]
        product_name = item['values'][1]
        
        if messagebox.askyesno("Confirmar", f"Deseja realmente excluir o produto '{product_name}'?"):
            if self.manager.delete_product(product_code):
                messagebox.showinfo("Sucesso", "Produto excluído com sucesso!")
                self.load_products_table()
                self.show_dashboard()
            else:
                messagebox.showerror("Erro", "Erro ao excluir produto.")
    
    def adjust_stock_dialog(self):
        """Show stock adjustment dialog"""
        selection = self.products_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Por favor, selecione um produto na tabela para ajustar o estoque.\n\n💡 Dica: Clique em uma linha da tabela primeiro.")
            return
        
        item = self.products_tree.item(selection[0])
        product_code = item['values'][0]
        product = self.manager.get_product(product_code)
        
        if product:
            dialog = StockAdjustmentDialog(self.root, self.manager, product)
            self.root.wait_window(dialog.dialog)
            
            if dialog.result:
                self.load_products_table()
                self.show_dashboard()
    
    def show_inventory(self):
        """Show inventory overview"""
        self.clear_main_content()
        
        # Inventory container
        inventory_frame = ctk.CTkFrame(self.main_frame)
        inventory_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        inventory_frame.grid_rowconfigure(3, weight=1)
        inventory_frame.grid_columnconfigure(0, weight=1)
        
        # Title
        title = ctk.CTkLabel(
            inventory_frame,
            text="📦 Visão Geral do Estoque",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title.grid(row=0, column=0, pady=20)
        
        # Summary cards
        summary_frame = ctk.CTkFrame(inventory_frame)
        summary_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        
        # Calculate inventory summary
        total_items = sum(p['quantity'] for p in self.manager.products)
        total_value = self.manager.get_total_inventory_value()
        low_stock_items = len(self.manager.get_low_stock_products())
        out_of_stock = len([p for p in self.manager.products if p['quantity'] == 0])
        
        summaries = [
            ("Total de Itens", total_items, "📦", "#4CAF50"),
            ("Valor Total", f"R$ {total_value:,.2f}", "💰", "#2196F3"),
            ("Estoque Baixo", low_stock_items, "⚠️", "#FF9800"),
            ("Sem Estoque", out_of_stock, "❌", "#F44336")
        ]
        
        for i, (title_text, value, icon, color) in enumerate(summaries):
            card = self.create_stat_card(summary_frame, title_text, value, icon, color)
            card.grid(row=0, column=i, padx=10, pady=10, sticky="ew")
        
        summary_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Filter options
        filter_frame = ctk.CTkFrame(inventory_frame, fg_color="transparent")
        filter_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=10)
        
        ctk.CTkLabel(filter_frame, text="Filtrar por:", font=ctk.CTkFont(size=16)).pack(side="left", padx=(0, 10))
        
        self.inventory_filter = ctk.StringVar(value="todos")
        filters = [
            ("Todos", "todos"),
            ("Estoque Baixo", "baixo"),
            ("Sem Estoque", "zero"),
            ("Disponível", "disponivel")
        ]
        
        for text, value in filters:
            rb = ctk.CTkRadioButton(
                filter_frame,
                text=text,
                variable=self.inventory_filter,
                value=value,
                command=self.filter_inventory,
                font=ctk.CTkFont(size=14)
            )
            rb.pack(side="left", padx=10)
        
        # Inventory table
        self.create_inventory_table(inventory_frame)
        
        # Load initial data
        self.filter_inventory()
    
    def create_inventory_table(self, parent):
        """Create inventory table"""
        table_frame = ctk.CTkFrame(parent)
        table_frame.grid(row=3, column=0, sticky="nsew", padx=20, pady=10)
        
        # Create treeview for inventory
        columns = ('code', 'name', 'quantity', 'min_stock', 'location', 'last_update', 'status')
        
        # Configure treeview style
        style = ttk.Style()
        style.configure("Inventory.Treeview", font=('TkDefaultFont', 12))
        style.configure("Inventory.Treeview.Heading", font=('TkDefaultFont', 14, 'bold'))
        
        self.inventory_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15, style="Inventory.Treeview")
        
        # Define headings
        headings = {
            'code': 'Código',
            'name': 'Produto',
            'quantity': 'Quantidade',
            'min_stock': 'Estoque Mín.',
            'location': 'Localização',
            'last_update': 'Última Atualização',
            'status': 'Status'
        }
        
        for col, heading in headings.items():
            self.inventory_tree.heading(col, text=heading)
            if col == 'quantity':
                self.inventory_tree.column(col, width=100, anchor='center')
            elif col == 'min_stock':
                self.inventory_tree.column(col, width=100, anchor='center')
            elif col == 'code':
                self.inventory_tree.column(col, width=80)
            elif col == 'last_update':
                self.inventory_tree.column(col, width=150)
            else:
                self.inventory_tree.column(col, width=120)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.inventory_tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=self.inventory_tree.xview)
        
        self.inventory_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack table and scrollbars
        self.inventory_tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
    
    def filter_inventory(self):
        """Filter inventory based on selected filter"""
        filter_value = self.inventory_filter.get()
        
        # Clear existing items
        for item in self.inventory_tree.get_children():
            self.inventory_tree.delete(item)
        
        # Filter products
        if filter_value == "baixo":
            products = self.manager.get_low_stock_products()
        elif filter_value == "zero":
            products = [p for p in self.manager.products if p['quantity'] == 0]
        elif filter_value == "disponivel":
            products = [p for p in self.manager.products if p['quantity'] > self.manager.settings.get('low_stock_threshold', 5)]
        else:  # todos
            products = self.manager.products
        
        # Add products to table
        for product in products:
            # Determine status
            if product['quantity'] <= 0:
                status = "❌ Sem estoque"
            elif product['quantity'] <= self.manager.settings.get('low_stock_threshold', 5):
                status = "⚠️ Estoque baixo"
            else:
                status = "✅ Disponível"
            
            # Format last update
            try:
                from datetime import datetime
                last_update = datetime.fromisoformat(product.get('updated_at', '')).strftime('%d/%m/%Y %H:%M')
            except:
                last_update = "N/A"
            
            values = (
                product['code'],
                product['name'][:30] + ('...' if len(product['name']) > 30 else ''),
                product['quantity'],
                self.manager.settings.get('low_stock_threshold', 5),
                product.get('location', 'N/A'),
                last_update,
                status
            )
            
            self.inventory_tree.insert('', 'end', values=values)
    
    def show_movements(self):
        """Show stock movements"""
        self.clear_main_content()
        
        # Movements container
        movements_frame = ctk.CTkFrame(self.main_frame)
        movements_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        movements_frame.grid_rowconfigure(3, weight=1)
        movements_frame.grid_columnconfigure(0, weight=1)
        
        # Title and controls
        header_frame = ctk.CTkFrame(movements_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        
        title = ctk.CTkLabel(
            header_frame,
            text="📈 Histórico de Movimentações",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title.pack(side="left")
        
        export_btn = ctk.CTkButton(
            header_frame,
            text="📋 Exportar",
            command=self.export_movements,
            width=120,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        export_btn.pack(side="right", padx=(10, 0))
        
        # Filters
        filter_frame = ctk.CTkFrame(movements_frame, fg_color="transparent")
        filter_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        
        # Date filter
        ctk.CTkLabel(filter_frame, text="Período:", font=ctk.CTkFont(size=16)).pack(side="left", padx=(0, 10))
        
        self.movements_period = ctk.StringVar(value="30")
        periods = [
            ("Hoje", "1"),
            ("7 dias", "7"),
            ("30 dias", "30"),
            ("Todos", "all")
        ]
        
        for text, value in periods:
            rb = ctk.CTkRadioButton(
                filter_frame,
                text=text,
                variable=self.movements_period,
                value=value,
                command=self.filter_movements,
                font=ctk.CTkFont(size=14)
            )
            rb.pack(side="left", padx=10)
        
        # Type filter
        ctk.CTkLabel(filter_frame, text="Tipo:", font=ctk.CTkFont(size=16)).pack(side="left", padx=(20, 10))
        
        self.movements_type = ctk.StringVar(value="todos")
        types = [
            ("Todos", "todos"),
            ("Entradas", "entrada"),
            ("Saídas", "saida")
        ]
        
        for text, value in types:
            rb = ctk.CTkRadioButton(
                filter_frame,
                text=text,
                variable=self.movements_type,
                value=value,
                command=self.filter_movements,
                font=ctk.CTkFont(size=14)
            )
            rb.pack(side="left", padx=10)
        
        # Search
        search_frame = ctk.CTkFrame(movements_frame, fg_color="transparent")
        search_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=10)
        
        ctk.CTkLabel(search_frame, text="🔍 Pesquisar:", font=ctk.CTkFont(size=16)).pack(side="left", padx=(0, 10))
        
        self.movements_search = ctk.StringVar()
        search_entry = ctk.CTkEntry(
            search_frame,
            textvariable=self.movements_search,
            placeholder_text="Digite o código do produto ou motivo...",
            width=350,
            height=35,
            font=ctk.CTkFont(size=14)
        )
        search_entry.pack(side="left", padx=(0, 10))
        search_entry.bind('<KeyRelease>', self.filter_movements)
        
        # Movements table
        self.create_movements_table(movements_frame)
        
        # Load initial data
        self.filter_movements()
    
    def create_movements_table(self, parent):
        """Create movements table"""
        table_frame = ctk.CTkFrame(parent)
        table_frame.grid(row=3, column=0, sticky="nsew", padx=20, pady=10)
        
        # Create treeview for movements
        columns = ('date', 'type', 'product_code', 'product_name', 'quantity', 'reason', 'user')
        
        # Configure treeview style
        style = ttk.Style()
        style.configure("Movements.Treeview", font=('TkDefaultFont', 12))
        style.configure("Movements.Treeview.Heading", font=('TkDefaultFont', 14, 'bold'))
        
        self.movements_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15, style="Movements.Treeview")
        
        # Define headings
        headings = {
            'date': 'Data/Hora',
            'type': 'Tipo',
            'product_code': 'Código',
            'product_name': 'Produto',
            'quantity': 'Quantidade',
            'reason': 'Motivo',
            'user': 'Usuário'
        }
        
        for col, heading in headings.items():
            self.movements_tree.heading(col, text=heading)
            if col == 'date':
                self.movements_tree.column(col, width=150)
            elif col == 'type':
                self.movements_tree.column(col, width=80, anchor='center')
            elif col == 'product_code':
                self.movements_tree.column(col, width=80)
            elif col == 'quantity':
                self.movements_tree.column(col, width=80, anchor='center')
            elif col == 'user':
                self.movements_tree.column(col, width=100)
            else:
                self.movements_tree.column(col, width=150)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.movements_tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=self.movements_tree.xview)
        
        self.movements_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack table and scrollbars
        self.movements_tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
    
    def filter_movements(self, event=None):
        """Filter movements based on criteria"""
        period = self.movements_period.get()
        movement_type = self.movements_type.get()
        search_query = self.movements_search.get().lower()
        
        # Clear existing items
        for item in self.movements_tree.get_children():
            self.movements_tree.delete(item)
        
        # Filter by period
        if period != "all":
            from datetime import datetime, timedelta
            days = int(period)
            cutoff_date = datetime.now() - timedelta(days=days)
            filtered_movements = [
                m for m in self.manager.movements
                if datetime.fromisoformat(m['date']) >= cutoff_date
            ]
        else:
            filtered_movements = self.manager.movements
        
        # Filter by type
        if movement_type != "todos":
            filtered_movements = [
                m for m in filtered_movements
                if m['type'] == movement_type
            ]
        
        # Filter by search query
        if search_query:
            filtered_movements = [
                m for m in filtered_movements
                if search_query in m['product_code'].lower() or
                   search_query in m.get('reason', '').lower()
            ]
        
        # Sort by date (most recent first)
        filtered_movements.sort(key=lambda x: x['date'], reverse=True)
        
        # Add movements to table
        for movement in filtered_movements:
            # Get product name
            product = self.manager.get_product(movement['product_code'])
            product_name = product['name'][:25] + ('...' if len(product['name']) > 25 else '') if product else "Produto não encontrado"
            
            # Format date
            try:
                date_obj = datetime.fromisoformat(movement['date'])
                formatted_date = date_obj.strftime('%d/%m/%Y %H:%M')
            except:
                formatted_date = movement['date']
            
            # Format type with icon
            type_icon = "⬆️" if movement['type'] == "entrada" else "⬇️"
            type_text = f"{type_icon} {movement['type'].title()}"
            
            values = (
                formatted_date,
                type_text,
                movement['product_code'],
                product_name,
                movement['quantity'],
                movement.get('reason', 'N/A')[:30],
                movement.get('user', 'N/A')
            )
            
            self.movements_tree.insert('', 'end', values=values)
    
    def export_movements(self):
        """Export movements to file"""
        try:
            from tkinter import filedialog
            import csv
            from datetime import datetime
            
            # Get filtered movements
            period = self.movements_period.get()
            movement_type = self.movements_type.get()
            
            if period != "all":
                from datetime import timedelta
                days = int(period)
                cutoff_date = datetime.now() - timedelta(days=days)
                movements = [
                    m for m in self.manager.movements
                    if datetime.fromisoformat(m['date']) >= cutoff_date
                ]
            else:
                movements = self.manager.movements
            
            if movement_type != "todos":
                movements = [m for m in movements if m['type'] == movement_type]
            
            # Ask for save location
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Exportar Movimentações"
            )
            
            if filename:
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    
                    # Write header
                    writer.writerow(['Data/Hora', 'Tipo', 'Código', 'Produto', 'Quantidade', 'Motivo', 'Usuário'])
                    
                    # Write data
                    for movement in movements:
                        product = self.manager.get_product(movement['product_code'])
                        product_name = product['name'] if product else "Produto não encontrado"
                        
                        date_obj = datetime.fromisoformat(movement['date'])
                        formatted_date = date_obj.strftime('%d/%m/%Y %H:%M:%S')
                        
                        writer.writerow([
                            formatted_date,
                            movement['type'].title(),
                            movement['product_code'],
                            product_name,
                            movement['quantity'],
                            movement.get('reason', ''),
                            movement.get('user', '')
                        ])
                
                messagebox.showinfo("Sucesso", f"Movimentações exportadas para:\n{filename}")
        
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar movimentações:\n{str(e)}")
    
    def show_suppliers(self):
        """Show suppliers management"""
        self.clear_main_content()
        
        # Suppliers container
        suppliers_frame = ctk.CTkFrame(self.main_frame)
        suppliers_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        suppliers_frame.grid_rowconfigure(2, weight=1)
        suppliers_frame.grid_columnconfigure(0, weight=1)
        
        # Title and controls
        header_frame = ctk.CTkFrame(suppliers_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        
        title = ctk.CTkLabel(
            header_frame,
            text="👥 Gerenciamento de Fornecedores",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title.pack(side="left")
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        buttons_frame.pack(side="right")
        
        edit_supplier_btn = ctk.CTkButton(
            buttons_frame,
            text="✏️ Editar",
            command=self.edit_selected_supplier,
            width=120,
            height=40,
            font=ctk.CTkFont(size=16),
            fg_color="#FF9800"
        )
        edit_supplier_btn.pack(side="left", padx=(0, 10))
        
        add_supplier_btn = ctk.CTkButton(
            buttons_frame,
            text="➕ Novo Fornecedor",
            command=self.show_add_supplier_dialog,
            width=170,
            height=40,
            font=ctk.CTkFont(size=16)
        )
        add_supplier_btn.pack(side="left")
        
        # Search frame
        search_frame = ctk.CTkFrame(suppliers_frame, fg_color="transparent")
        search_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        
        ctk.CTkLabel(search_frame, text="🔍 Pesquisar:", font=ctk.CTkFont(size=16)).pack(side="left", padx=(0, 10))
        
        self.suppliers_search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(
            search_frame,
            textvariable=self.suppliers_search_var,
            placeholder_text="Digite o nome, email ou telefone...",
            width=350,
            height=35,
            font=ctk.CTkFont(size=14)
        )
        search_entry.pack(side="left", padx=(0, 10))
        search_entry.bind('<KeyRelease>', self.on_search_suppliers)
        
        # Selection status
        self.selected_supplier_label = ctk.CTkLabel(
            search_frame,
            text="❌ Nenhum fornecedor selecionado",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#FF6B6B"
        )
        self.selected_supplier_label.pack(side="right", padx=(10, 0))
        
        # Suppliers table
        self.create_suppliers_table(suppliers_frame)
        
        # Load suppliers
        self.load_suppliers_table()
    
    def create_suppliers_table(self, parent):
        """Create suppliers table"""
        table_frame = ctk.CTkFrame(parent)
        table_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)
        
        # Create treeview
        columns = ('name', 'contact', 'phone', 'email', 'products_count', 'status')
        
        # Configure treeview style
        style = ttk.Style()
        style.configure("Suppliers.Treeview", font=('TkDefaultFont', 12))
        style.configure("Suppliers.Treeview.Heading", font=('TkDefaultFont', 14, 'bold'))
        
        self.suppliers_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15, style="Suppliers.Treeview")
        
        # Define headings
        headings = {
            'name': 'Nome',
            'contact': 'Contato',
            'phone': 'Telefone',
            'email': 'Email',
            'products_count': 'Produtos',
            'status': 'Status'
        }
        
        for col, heading in headings.items():
            self.suppliers_tree.heading(col, text=heading)
            if col == 'products_count':
                self.suppliers_tree.column(col, width=80, anchor='center')
            elif col == 'phone':
                self.suppliers_tree.column(col, width=120)
            elif col == 'status':
                self.suppliers_tree.column(col, width=100, anchor='center')
            else:
                self.suppliers_tree.column(col, width=150)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.suppliers_tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=self.suppliers_tree.xview)
        
        self.suppliers_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack table and scrollbars
        self.suppliers_tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # Context menu
        self.create_suppliers_context_menu()
        
        # Bind selection event
        self.suppliers_tree.bind('<<TreeviewSelect>>', self.on_supplier_select)
        
        # Bind double click to edit
        self.suppliers_tree.bind('<Double-1>', lambda e: self.edit_selected_supplier())
        
        # Bind keyboard shortcuts
        self.suppliers_tree.bind('<Control-e>', lambda e: self.edit_selected_supplier())
        self.suppliers_tree.bind('<Control-E>', lambda e: self.edit_selected_supplier())
    
    def create_suppliers_context_menu(self):
        """Create context menu for suppliers table"""
        self.suppliers_context_menu = tk.Menu(self.root, tearoff=0)
        self.suppliers_context_menu.add_command(label="✏️ Editar", command=self.edit_selected_supplier)
        self.suppliers_context_menu.add_command(label="📋 Ver Produtos", command=self.view_supplier_products)
        self.suppliers_context_menu.add_separator()
        self.suppliers_context_menu.add_command(label="🗑️ Excluir", command=self.delete_selected_supplier)
        
        self.suppliers_tree.bind("<Button-3>", self.show_suppliers_context_menu)
    
    def show_suppliers_context_menu(self, event):
        """Show context menu for suppliers"""
        try:
            self.suppliers_context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.suppliers_context_menu.grab_release()
    
    def load_suppliers_table(self, suppliers=None):
        """Load suppliers into the table"""
        # Clear existing items
        for item in self.suppliers_tree.get_children():
            self.suppliers_tree.delete(item)
        
        # Use filtered suppliers or all suppliers
        suppliers_to_show = suppliers if suppliers is not None else self.manager.suppliers
        
        # Add suppliers to table
        for supplier in suppliers_to_show:
            # Count products for this supplier
            products_count = len([p for p in self.manager.products if p.get('supplier') == supplier['name']])
            
            # Determine status
            status = "✅ Ativo" if supplier.get('active', True) else "❌ Inativo"
            
            values = (
                supplier['name'],
                supplier.get('contact', ''),
                supplier.get('phone', ''),
                supplier.get('email', ''),
                products_count,
                status
            )
            
            self.suppliers_tree.insert('', 'end', values=values)
    
    def on_supplier_select(self, event):
        """Handle supplier selection"""
        selection = self.suppliers_tree.selection()
        if hasattr(self, 'selected_supplier_label'):
            if selection:
                item = self.suppliers_tree.item(selection[0])
                supplier_name = item['values'][0]
                self.selected_supplier_label.configure(
                    text=f"✅ Selecionado: {supplier_name}",
                    text_color="#4CAF50"
                )
            else:
                self.selected_supplier_label.configure(
                    text="❌ Nenhum fornecedor selecionado",
                    text_color="#FF6B6B"
                )
    
    def on_search_suppliers(self, event=None):
        """Handle supplier search"""
        query = self.suppliers_search_var.get().lower()
        if query.strip():
            filtered_suppliers = [
                s for s in self.manager.suppliers
                if query in s['name'].lower() or
                   query in s.get('contact', '').lower() or
                   query in s.get('phone', '').lower() or
                   query in s.get('email', '').lower()
            ]
            self.load_suppliers_table(filtered_suppliers)
        else:
            self.load_suppliers_table()
    
    def show_add_supplier_dialog(self):
        """Show add supplier dialog"""
        dialog = SupplierDialog(self.root, self.manager, title="Novo Fornecedor")
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            self.load_suppliers_table()
    
    def edit_selected_supplier(self):
        """Edit selected supplier"""
        selection = self.suppliers_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Por favor, selecione um fornecedor na tabela para editar.\n\n💡 Dica: Clique em uma linha da tabela primeiro.")
            return
        
        item = self.suppliers_tree.item(selection[0])
        supplier_name = item['values'][0]
        supplier = next((s for s in self.manager.suppliers if s['name'] == supplier_name), None)
        
        if supplier:
            dialog = SupplierDialog(self.root, self.manager, supplier=supplier, title="Editar Fornecedor")
            self.root.wait_window(dialog.dialog)
            
            if dialog.result:
                self.load_suppliers_table()
    
    def delete_selected_supplier(self):
        """Delete selected supplier"""
        selection = self.suppliers_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um fornecedor para excluir.")
            return
        
        item = self.suppliers_tree.item(selection[0])
        supplier_name = item['values'][0]
        
        if messagebox.askyesno("Confirmar", f"Deseja realmente excluir o fornecedor '{supplier_name}'?"):
            self.manager.suppliers = [s for s in self.manager.suppliers if s['name'] != supplier_name]
            self.manager.save_data(self.manager.suppliers, SUPPLIERS_FILE)
            messagebox.showinfo("Sucesso", "Fornecedor excluído com sucesso!")
            self.load_suppliers_table()
    
    def view_supplier_products(self):
        """View products from selected supplier"""
        selection = self.suppliers_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um fornecedor.")
            return
        
        item = self.suppliers_tree.item(selection[0])
        supplier_name = item['values'][0]
        
        # Filter products by supplier and show in products view
        self.show_products()
        # Set search to filter by supplier
        self.search_var.set(supplier_name)
        self.on_search_products()
    
    def show_categories(self):
        """Show categories management"""
        self.clear_main_content()
        
        # Categories container
        categories_frame = ctk.CTkFrame(self.main_frame)
        categories_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        categories_frame.grid_rowconfigure(3, weight=1)
        categories_frame.grid_columnconfigure(0, weight=1)
        
        # Title and controls
        header_frame = ctk.CTkFrame(categories_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        
        title = ctk.CTkLabel(
            header_frame,
            text="📁 Gerenciamento de Categorias",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title.pack(side="left")
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        buttons_frame.pack(side="right")
        
        edit_category_btn = ctk.CTkButton(
            buttons_frame,
            text="✏️ Editar",
            command=self.edit_selected_category,
            width=120,
            height=40,
            font=ctk.CTkFont(size=16),
            fg_color="#FF9800"
        )
        edit_category_btn.pack(side="left", padx=(0, 10))
        
        add_category_btn = ctk.CTkButton(
            buttons_frame,
            text="➕ Nova Categoria",
            command=self.show_add_category_dialog,
            width=170,
            height=40,
            font=ctk.CTkFont(size=16)
        )
        add_category_btn.pack(side="left")
        
        # Quick stats
        stats_frame = ctk.CTkFrame(categories_frame)
        stats_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        
        # Calculate category stats
        categories_count = len(self.manager.categories)
        products_with_category = len([p for p in self.manager.products if p.get('category')])
        products_without_category = len(self.manager.products) - products_with_category
        
        stats = [
            ("Total Categorias", categories_count, "📁", "#4CAF50"),
            ("Produtos Categorizados", products_with_category, "✅", "#2196F3"),
            ("Sem Categoria", products_without_category, "❓", "#FF9800")
        ]
        
        for i, (title_text, value, icon, color) in enumerate(stats):
            card = self.create_stat_card(stats_frame, title_text, value, icon, color)
            card.grid(row=0, column=i, padx=10, pady=10, sticky="ew")
        
        stats_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Selection status frame
        status_frame = ctk.CTkFrame(categories_frame, fg_color="transparent")
        status_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=5)
        
        self.selected_category_label = ctk.CTkLabel(
            status_frame,
            text="❌ Nenhuma categoria selecionada",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#FF6B6B"
        )
        self.selected_category_label.pack(side="right")
        
        # Categories table
        self.create_categories_table(categories_frame)
        
        # Load categories
        self.load_categories_table()
    
    def create_categories_table(self, parent):
        """Create categories table"""
        table_frame = ctk.CTkFrame(parent)
        table_frame.grid(row=3, column=0, sticky="nsew", padx=20, pady=10)
        
        # Create treeview
        columns = ('name', 'description', 'products_count', 'color', 'status')
        
        # Configure treeview style
        style = ttk.Style()
        style.configure("Categories.Treeview", font=('TkDefaultFont', 12))
        style.configure("Categories.Treeview.Heading", font=('TkDefaultFont', 14, 'bold'))
        
        self.categories_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15, style="Categories.Treeview")
        
        # Define headings
        headings = {
            'name': 'Nome',
            'description': 'Descrição',
            'products_count': 'Produtos',
            'color': 'Cor',
            'status': 'Status'
        }
        
        for col, heading in headings.items():
            self.categories_tree.heading(col, text=heading)
            if col == 'products_count':
                self.categories_tree.column(col, width=80, anchor='center')
            elif col == 'color':
                self.categories_tree.column(col, width=80, anchor='center')
            elif col == 'status':
                self.categories_tree.column(col, width=100, anchor='center')
            else:
                self.categories_tree.column(col, width=200)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.categories_tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=self.categories_tree.xview)
        
        self.categories_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack table and scrollbars
        self.categories_tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # Context menu
        self.create_categories_context_menu()
        
        # Bind selection event
        self.categories_tree.bind('<<TreeviewSelect>>', self.on_category_select)
        
        # Bind double click to edit
        self.categories_tree.bind('<Double-1>', lambda e: self.edit_selected_category())
        
        # Bind keyboard shortcuts
        self.categories_tree.bind('<Control-e>', lambda e: self.edit_selected_category())
        self.categories_tree.bind('<Control-E>', lambda e: self.edit_selected_category())
    
    def create_categories_context_menu(self):
        """Create context menu for categories table"""
        self.categories_context_menu = tk.Menu(self.root, tearoff=0)
        self.categories_context_menu.add_command(label="✏️ Editar", command=self.edit_selected_category)
        self.categories_context_menu.add_command(label="📋 Ver Produtos", command=self.view_category_products)
        self.categories_context_menu.add_separator()
        self.categories_context_menu.add_command(label="🗑️ Excluir", command=self.delete_selected_category)
        
        self.categories_tree.bind("<Button-3>", self.show_categories_context_menu)
    
    def show_categories_context_menu(self, event):
        """Show context menu for categories"""
        try:
            self.categories_context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.categories_context_menu.grab_release()
    
    def load_categories_table(self):
        """Load categories into the table"""
        # Clear existing items
        for item in self.categories_tree.get_children():
            self.categories_tree.delete(item)
        
        # Add categories to table
        for category in self.manager.categories:
            # Count products for this category
            products_count = len([p for p in self.manager.products if p.get('category') == category['name']])
            
            # Status
            status = "✅ Ativa" if category.get('active', True) else "❌ Inativa"
            
            # Color indicator
            color_indicator = f"●" if category.get('color') else "○"
            
            values = (
                category['name'],
                category.get('description', '')[:50],
                products_count,
                color_indicator,
                status
            )
            
            self.categories_tree.insert('', 'end', values=values)
    
    def on_category_select(self, event):
        """Handle category selection"""
        selection = self.categories_tree.selection()
        if hasattr(self, 'selected_category_label'):
            if selection:
                item = self.categories_tree.item(selection[0])
                category_name = item['values'][0]
                self.selected_category_label.configure(
                    text=f"✅ Selecionada: {category_name}",
                    text_color="#4CAF50"
                )
            else:
                self.selected_category_label.configure(
                    text="❌ Nenhuma categoria selecionada",
                    text_color="#FF6B6B"
                )
    
    def show_add_category_dialog(self):
        """Show add category dialog"""
        dialog = CategoryDialog(self.root, self.manager, title="Nova Categoria")
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            self.load_categories_table()
    
    def edit_selected_category(self):
        """Edit selected category"""
        selection = self.categories_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Por favor, selecione uma categoria na tabela para editar.\n\n💡 Dica: Clique em uma linha da tabela primeiro.")
            return
        
        item = self.categories_tree.item(selection[0])
        category_name = item['values'][0]
        category = next((c for c in self.manager.categories if c['name'] == category_name), None)
        
        if category:
            dialog = CategoryDialog(self.root, self.manager, category=category, title="Editar Categoria")
            self.root.wait_window(dialog.dialog)
            
            if dialog.result:
                self.load_categories_table()
    
    def delete_selected_category(self):
        """Delete selected category"""
        selection = self.categories_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione uma categoria para excluir.")
            return
        
        item = self.categories_tree.item(selection[0])
        category_name = item['values'][0]
        
        # Check if category has products
        products_count = len([p for p in self.manager.products if p.get('category') == category_name])
        
        if products_count > 0:
            if not messagebox.askyesno("Confirmar", 
                f"A categoria '{category_name}' possui {products_count} produto(s).\n"
                "Os produtos ficarão sem categoria. Deseja continuar?"):
                return
        
        if messagebox.askyesno("Confirmar", f"Deseja realmente excluir a categoria '{category_name}'?"):
            # Remove category from products
            for product in self.manager.products:
                if product.get('category') == category_name:
                    product['category'] = ""
            
            # Remove category
            self.manager.categories = [c for c in self.manager.categories if c['name'] != category_name]
            
            # Save changes
            self.manager.save_data(self.manager.categories, CATEGORIES_FILE)
            self.manager.save_data(self.manager.products, PRODUCTS_FILE)
            
            messagebox.showinfo("Sucesso", "Categoria excluída com sucesso!")
            self.load_categories_table()
    
    def view_category_products(self):
        """View products from selected category"""
        selection = self.categories_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione uma categoria.")
            return
        
        item = self.categories_tree.item(selection[0])
        category_name = item['values'][0]
        
        # Switch to products view and filter by category
        self.show_products()
        self.search_var.set(category_name)
        self.on_search_products()
    
    def show_reports(self):
        """Show reports"""
        self.clear_main_content()
        
        # Reports container
        reports_frame = ctk.CTkFrame(self.main_frame)
        reports_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        reports_frame.grid_rowconfigure(2, weight=1)
        reports_frame.grid_columnconfigure(0, weight=1)
        
        # Title
        title = ctk.CTkLabel(
            reports_frame,
            text="📊 Relatórios e Análises",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title.grid(row=0, column=0, pady=20)
        
        # Report buttons
        buttons_frame = ctk.CTkFrame(reports_frame)
        buttons_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        
        report_buttons = [
            ("📋 Produtos em Falta", self.generate_low_stock_report, "#FF9800"),
            ("💰 Valor do Estoque", self.generate_inventory_value_report, "#4CAF50"),
            ("📈 Movimentações", self.generate_movements_report, "#2196F3"),
            ("📊 Por Categoria", self.generate_category_report, "#9C27B0"),
            ("👥 Por Fornecedor", self.generate_supplier_report, "#FF5722"),
            ("📅 Relatório Mensal", self.generate_monthly_report, "#607D8B")
        ]
        
        for i, (text, command, color) in enumerate(report_buttons):
            btn = ctk.CTkButton(
                buttons_frame,
                text=text,
                command=command,
                width=180,
                height=50,
                font=ctk.CTkFont(size=14),
                fg_color=color,
                hover_color=self.darken_color(color)
            )
            btn.grid(row=i//3, column=i%3, padx=10, pady=10, sticky="ew")
        
        # Configure grid columns
        buttons_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Report display area
        self.report_display = ctk.CTkTextbox(reports_frame, height=400, font=ctk.CTkFont(size=12))
        self.report_display.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)
        
        # Show default report
        self.generate_summary_report()
    
    def darken_color(self, hex_color):
        """Darken a hex color for hover effect"""
        try:
            # Remove '#' if present
            hex_color = hex_color.lstrip('#')
            # Convert to RGB
            rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            # Darken by 20%
            darkened = tuple(max(0, int(c * 0.8)) for c in rgb)
            # Convert back to hex
            return f"#{darkened[0]:02x}{darkened[1]:02x}{darkened[2]:02x}"
        except:
            return "#666666"
    
    def generate_summary_report(self):
        """Generate summary report"""
        self.report_display.delete("1.0", "end")
        
        report = "📊 RESUMO GERAL DO ESTOQUE\n"
        report += "=" * 50 + "\n\n"
        
        # Basic stats
        total_products = len(self.manager.products)
        total_items = sum(p['quantity'] for p in self.manager.products)
        total_value = self.manager.get_total_inventory_value()
        low_stock_count = len(self.manager.get_low_stock_products())
        
        report += f"📦 Total de Produtos: {total_products}\n"
        report += f"📊 Total de Itens: {total_items:,}\n"
        report += f"💰 Valor Total: R$ {total_value:,.2f}\n"
        report += f"⚠️  Produtos com Estoque Baixo: {low_stock_count}\n\n"
        
        # Categories breakdown
        categories = {}
        for product in self.manager.products:
            cat = product.get('category', 'Sem categoria')
            if cat not in categories:
                categories[cat] = {'count': 0, 'value': 0}
            categories[cat]['count'] += 1
            categories[cat]['value'] += product['price'] * product['quantity']
        
        report += "📁 PRODUTOS POR CATEGORIA:\n"
        report += "-" * 30 + "\n"
        for cat, data in categories.items():
            report += f"{cat}: {data['count']} produto(s) - R$ {data['value']:,.2f}\n"
        
        report += "\n"
        
        # Recent movements
        recent_movements = sorted(self.manager.movements, key=lambda x: x['date'], reverse=True)[:10]
        report += "🔄 MOVIMENTAÇÕES RECENTES:\n"
        report += "-" * 30 + "\n"
        for movement in recent_movements:
            date_obj = datetime.fromisoformat(movement['date'])
            formatted_date = date_obj.strftime('%d/%m/%Y %H:%M')
            type_icon = "⬆️" if movement['type'] == "entrada" else "⬇️"
            report += f"{type_icon} {formatted_date} - {movement['product_code']} ({movement['quantity']})\n"
        
        self.report_display.insert("1.0", report)
    
    def generate_low_stock_report(self):
        """Generate low stock report"""
        self.report_display.delete("1.0", "end")
        
        low_stock_products = self.manager.get_low_stock_products()
        threshold = self.manager.settings.get('low_stock_threshold', 5)
        
        report = f"⚠️  PRODUTOS COM ESTOQUE BAIXO (≤ {threshold} unidades)\n"
        report += "=" * 60 + "\n\n"
        
        if not low_stock_products:
            report += "✅ Nenhum produto com estoque baixo!\n"
        else:
            report += f"Total de produtos: {len(low_stock_products)}\n\n"
            
            for product in sorted(low_stock_products, key=lambda x: x['quantity']):
                status = "❌ SEM ESTOQUE" if product['quantity'] == 0 else f"⚠️  {product['quantity']} unid."
                report += f"• {product['name']} ({product['code']})\n"
                report += f"  Status: {status}\n"
                report += f"  Fornecedor: {product.get('supplier', 'N/A')}\n"
                report += f"  Localização: {product.get('location', 'N/A')}\n"
                report += "-" * 40 + "\n"
        
        self.report_display.insert("1.0", report)
    
    def generate_inventory_value_report(self):
        """Generate inventory value report"""
        self.report_display.delete("1.0", "end")
        
        total_value = self.manager.get_total_inventory_value()
        
        report = "💰 RELATÓRIO DE VALOR DO ESTOQUE\n"
        report += "=" * 50 + "\n\n"
        
        report += f"Valor Total do Estoque: R$ {total_value:,.2f}\n\n"
        
        # Value by category
        categories = {}
        for product in self.manager.products:
            cat = product.get('category', 'Sem categoria')
            if cat not in categories:
                categories[cat] = 0
            categories[cat] += product['price'] * product['quantity']
        
        report += "📁 VALOR POR CATEGORIA:\n"
        report += "-" * 30 + "\n"
        
        sorted_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)
        for cat, value in sorted_categories:
            percentage = (value / total_value * 100) if total_value > 0 else 0
            report += f"{cat}: R$ {value:,.2f} ({percentage:.1f}%)\n"
        
        report += "\n"
        
        # Top 10 most valuable products
        products_by_value = sorted(
            self.manager.products,
            key=lambda x: x['price'] * x['quantity'],
            reverse=True
        )[:10]
        
        report += "🏆 TOP 10 PRODUTOS MAIS VALIOSOS:\n"
        report += "-" * 40 + "\n"
        
        for i, product in enumerate(products_by_value, 1):
            total_product_value = product['price'] * product['quantity']
            report += f"{i:2d}. {product['name'][:30]}\n"
            report += f"     Qtd: {product['quantity']} x R$ {product['price']:.2f} = R$ {total_product_value:,.2f}\n"
        
        self.report_display.insert("1.0", report)
    
    def generate_movements_report(self):
        """Generate movements report"""
        self.report_display.delete("1.0", "end")
        
        movements = self.manager.movements
        
        report = "📈 RELATÓRIO DE MOVIMENTAÇÕES\n"
        report += "=" * 50 + "\n\n"
        
        if not movements:
            report += "Nenhuma movimentação registrada.\n"
        else:
            # Statistics by period
            today = datetime.now()
            week_ago = today - timedelta(days=7)
            month_ago = today - timedelta(days=30)
            
            movements_today = [m for m in movements if datetime.fromisoformat(m['date']).date() == today.date()]
            movements_week = [m for m in movements if datetime.fromisoformat(m['date']) >= week_ago]
            movements_month = [m for m in movements if datetime.fromisoformat(m['date']) >= month_ago]
            
            report += f"📅 MOVIMENTAÇÕES POR PERÍODO:\n"
            report += f"Hoje: {len(movements_today)}\n"
            report += f"Últimos 7 dias: {len(movements_week)}\n"
            report += f"Últimos 30 dias: {len(movements_month)}\n"
            report += f"Total: {len(movements)}\n\n"
            
            # By type
            entradas = [m for m in movements if m['type'] == 'entrada']
            saidas = [m for m in movements if m['type'] == 'saida']
            
            report += f"📊 POR TIPO:\n"
            report += f"⬆️  Entradas: {len(entradas)}\n"
            report += f"⬇️  Saídas: {len(saidas)}\n\n"
            
            # Recent movements
            recent = sorted(movements, key=lambda x: x['date'], reverse=True)[:15]
            report += f"🔄 MOVIMENTAÇÕES RECENTES:\n"
            report += "-" * 40 + "\n"
            
            for movement in recent:
                date_obj = datetime.fromisoformat(movement['date'])
                formatted_date = date_obj.strftime('%d/%m/%Y %H:%M')
                type_icon = "⬆️" if movement['type'] == "entrada" else "⬇️"
                
                product = self.manager.get_product(movement['product_code'])
                product_name = product['name'][:25] if product else "Produto não encontrado"
                
                report += f"{type_icon} {formatted_date}\n"
                report += f"   {product_name} (Qtd: {movement['quantity']})\n"
                report += f"   Motivo: {movement.get('reason', 'N/A')}\n"
                report += "-" * 30 + "\n"
        
        self.report_display.insert("1.0", report)
    
    def generate_category_report(self):
        """Generate category report"""
        self.report_display.delete("1.0", "end")
        
        report = "📊 RELATÓRIO POR CATEGORIA\n"
        report += "=" * 50 + "\n\n"
        
        categories_data = {}
        products_without_category = []
        
        for product in self.manager.products:
            category = product.get('category', '')
            if not category:
                products_without_category.append(product)
            else:
                if category not in categories_data:
                    categories_data[category] = {
                        'products': [],
                        'total_quantity': 0,
                        'total_value': 0
                    }
                categories_data[category]['products'].append(product)
                categories_data[category]['total_quantity'] += product['quantity']
                categories_data[category]['total_value'] += product['price'] * product['quantity']
        
        # Categories with products
        if categories_data:
            for category, data in sorted(categories_data.items()):
                report += f"📁 {category.upper()}\n"
                report += f"   Produtos: {len(data['products'])}\n"
                report += f"   Quantidade Total: {data['total_quantity']:,}\n"
                report += f"   Valor Total: R$ {data['total_value']:,.2f}\n"
                
                # Top products in category
                top_products = sorted(data['products'], key=lambda x: x['price'] * x['quantity'], reverse=True)[:3]
                report += f"   Top Produtos:\n"
                for product in top_products:
                    value = product['price'] * product['quantity']
                    report += f"     • {product['name'][:25]} - R$ {value:,.2f}\n"
                report += "\n"
        
        # Products without category
        if products_without_category:
            report += f"❓ PRODUTOS SEM CATEGORIA ({len(products_without_category)})\n"
            report += "-" * 40 + "\n"
            for product in products_without_category[:10]:  # Show first 10
                report += f"• {product['name']} ({product['code']})\n"
            
            if len(products_without_category) > 10:
                report += f"... e mais {len(products_without_category) - 10} produto(s)\n"
        
        self.report_display.insert("1.0", report)
    
    def generate_supplier_report(self):
        """Generate supplier report"""
        self.report_display.delete("1.0", "end")
        
        report = "👥 RELATÓRIO POR FORNECEDOR\n"
        report += "=" * 50 + "\n\n"
        
        suppliers_data = {}
        products_without_supplier = []
        
        for product in self.manager.products:
            supplier = product.get('supplier', '')
            if not supplier:
                products_without_supplier.append(product)
            else:
                if supplier not in suppliers_data:
                    suppliers_data[supplier] = {
                        'products': [],
                        'total_quantity': 0,
                        'total_value': 0
                    }
                suppliers_data[supplier]['products'].append(product)
                suppliers_data[supplier]['total_quantity'] += product['quantity']
                suppliers_data[supplier]['total_value'] += product['price'] * product['quantity']
        
        # Suppliers with products
        if suppliers_data:
            sorted_suppliers = sorted(suppliers_data.items(), key=lambda x: x[1]['total_value'], reverse=True)
            
            for supplier, data in sorted_suppliers:
                report += f"👥 {supplier.upper()}\n"
                report += f"   Produtos: {len(data['products'])}\n"
                report += f"   Quantidade Total: {data['total_quantity']:,}\n"
                report += f"   Valor Total: R$ {data['total_value']:,.2f}\n"
                
                # List products
                report += f"   Produtos:\n"
                for product in data['products']:
                    value = product['price'] * product['quantity']
                    report += f"     • {product['name'][:30]} - {product['quantity']} unid. - R$ {value:,.2f}\n"
                report += "\n"
        
        # Products without supplier
        if products_without_supplier:
            report += f"❓ PRODUTOS SEM FORNECEDOR ({len(products_without_supplier)})\n"
            report += "-" * 40 + "\n"
            for product in products_without_supplier[:10]:  # Show first 10
                report += f"• {product['name']} ({product['code']})\n"
            
            if len(products_without_supplier) > 10:
                report += f"... e mais {len(products_without_supplier) - 10} produto(s)\n"
        
        self.report_display.insert("1.0", report)
    
    def generate_monthly_report(self):
        """Generate monthly report"""
        self.report_display.delete("1.0", "end")
        
        now = datetime.now()
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        report = f"📅 RELATÓRIO MENSAL - {now.strftime('%B %Y').upper()}\n"
        report += "=" * 60 + "\n\n"
        
        # Monthly movements
        monthly_movements = [
            m for m in self.manager.movements
            if datetime.fromisoformat(m['date']) >= month_start
        ]
        
        entradas = [m for m in monthly_movements if m['type'] == 'entrada']
        saidas = [m for m in monthly_movements if m['type'] == 'saida']
        
        report += f"📊 MOVIMENTAÇÕES DO MÊS:\n"
        report += f"⬆️  Entradas: {len(entradas)}\n"
        report += f"⬇️  Saídas: {len(saidas)}\n"
        report += f"📈 Total: {len(monthly_movements)}\n\n"
        
        # Daily breakdown
        daily_stats = {}
        for movement in monthly_movements:
            date = datetime.fromisoformat(movement['date']).date()
            if date not in daily_stats:
                daily_stats[date] = {'entradas': 0, 'saidas': 0}
            daily_stats[date][movement['type'] + 's'] += 1
        
        if daily_stats:
            report += f"📅 MOVIMENTAÇÕES POR DIA:\n"
            report += "-" * 30 + "\n"
            for date in sorted(daily_stats.keys(), reverse=True)[:10]:  # Last 10 days
                stats = daily_stats[date]
                formatted_date = date.strftime('%d/%m/%Y')
                report += f"{formatted_date}: ⬆️ {stats['entradas']} ⬇️ {stats['saidas']}\n"
        
        # Current status
        total_value = self.manager.get_total_inventory_value()
        low_stock_count = len(self.manager.get_low_stock_products())
        
        report += f"\n📊 STATUS ATUAL:\n"
        report += f"💰 Valor Total do Estoque: R$ {total_value:,.2f}\n"
        report += f"⚠️  Produtos com Estoque Baixo: {low_stock_count}\n"
        report += f"📦 Total de Produtos: {len(self.manager.products)}\n"
        
        self.report_display.insert("1.0", report)
    
    def show_settings(self):
        """Show application settings"""
        self.clear_main_content()
        
        # Settings container
        settings_frame = ctk.CTkFrame(self.main_frame)
        settings_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        settings_frame.grid_rowconfigure(1, weight=1)
        settings_frame.grid_columnconfigure(0, weight=1)
        
        # Title
        title = ctk.CTkLabel(
            settings_frame,
            text="⚙️ Configurações do Sistema",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title.grid(row=0, column=0, pady=20)
        
        # Settings content frame
        content_frame = ctk.CTkScrollableFrame(settings_frame)
        content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        
        # General Settings Section
        general_frame = ctk.CTkFrame(content_frame)
        general_frame.pack(fill="x", pady=10)
        
        general_title = ctk.CTkLabel(
            general_frame,
            text="🔧 Configurações Gerais",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        general_title.pack(pady=(10, 5))
        
        # Low Stock Threshold
        threshold_frame = ctk.CTkFrame(general_frame, fg_color="transparent")
        threshold_frame.pack(fill="x", padx=20, pady=5)
        
        threshold_label = ctk.CTkLabel(
            threshold_frame,
            text="Limite de Estoque Baixo:",
            font=ctk.CTkFont(size=14)
        )
        threshold_label.pack(side="left")
        
        self.threshold_var = ctk.StringVar(value=str(self.manager.settings.get('low_stock_threshold', 5)))
        threshold_entry = ctk.CTkEntry(
            threshold_frame,
            textvariable=self.threshold_var,
            width=100,
            font=ctk.CTkFont(size=14)
        )
        threshold_entry.pack(side="right", padx=(10, 0))
        
        # Auto Backup
        backup_frame = ctk.CTkFrame(general_frame, fg_color="transparent")
        backup_frame.pack(fill="x", padx=20, pady=5)
        
        self.auto_backup_var = ctk.BooleanVar(value=self.manager.settings.get('auto_backup', True))
        backup_checkbox = ctk.CTkCheckBox(
            backup_frame,
            text="Backup Automático Diário",
            variable=self.auto_backup_var,
            font=ctk.CTkFont(size=14)
        )
        backup_checkbox.pack(side="left")
        
        # Default Category
        category_frame = ctk.CTkFrame(general_frame, fg_color="transparent")
        category_frame.pack(fill="x", padx=20, pady=5)
        
        category_label = ctk.CTkLabel(
            category_frame,
            text="Categoria Padrão:",
            font=ctk.CTkFont(size=14)
        )
        category_label.pack(side="left")
        
        category_names = [cat['name'] for cat in self.manager.categories if cat.get('active', True)]
        category_names.insert(0, "Nenhuma")
        
        self.default_category_var = ctk.StringVar(value=self.manager.settings.get('default_category', 'Nenhuma'))
        category_combo = ctk.CTkComboBox(
            category_frame,
            values=category_names,
            variable=self.default_category_var,
            width=200,
            font=ctk.CTkFont(size=14)
        )
        category_combo.pack(side="right", padx=(10, 0))
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        buttons_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=20)
        
        # Save button
        save_btn = ctk.CTkButton(
            buttons_frame,
            text="💾 Salvar Configurações",
            command=self.save_settings,
            width=200,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        save_btn.pack(side="right")
    
    def save_settings(self):
        """Save settings"""
        try:
            # Validate threshold  
            try:
                threshold = int(self.threshold_var.get())
                if threshold < 0:
                    messagebox.showerror("Erro", "O limite deve ser um número positivo!")
                    return
            except ValueError:
                messagebox.showerror("Erro", "O limite deve ser um número válido!")
                return
            
            # Update settings
            self.manager.settings.update({
                'low_stock_threshold': threshold,
                'auto_backup': self.auto_backup_var.get(),
                'default_category': self.default_category_var.get() if self.default_category_var.get() != 'Nenhuma' else ''
            })
            
            # Save to file
            self.manager.save_data(self.manager.settings, SETTINGS_FILE)
            
            messagebox.showinfo("Sucesso", "Configurações salvas com sucesso!")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar configurações: {str(e)}")
    
    def show_backup(self):
        """Show backup options"""
        self.clear_main_content()
        
        # Backup container
        backup_frame = ctk.CTkFrame(self.main_frame)
        backup_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        backup_frame.grid_rowconfigure(2, weight=1)
        backup_frame.grid_columnconfigure(0, weight=1)
        
        # Title
        title = ctk.CTkLabel(
            backup_frame,
            text="💾 Backup e Restauração",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title.grid(row=0, column=0, pady=20)
        
        # Backup options frame
        options_frame = ctk.CTkFrame(backup_frame)
        options_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        
        # Manual Backup Section
        manual_frame = ctk.CTkFrame(options_frame)
        manual_frame.pack(fill="x", padx=20, pady=20)
        
        manual_title = ctk.CTkLabel(
            manual_frame,
            text="🔧 Backup Manual",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        manual_title.pack(pady=(10, 15))
        
        manual_desc = ctk.CTkLabel(
            manual_frame,
            text="Crie um backup completo de todos os dados do sistema",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        manual_desc.pack(pady=(0, 15))
        
        backup_buttons_frame = ctk.CTkFrame(manual_frame, fg_color="transparent")
        backup_buttons_frame.pack(fill="x", padx=20, pady=10)
        
        create_backup_btn = ctk.CTkButton(
            backup_buttons_frame,
            text="💾 Criar Backup Completo",
            command=self.create_full_backup,
            width=250,
            height=50,
            font=ctk.CTkFont(size=16)
        )
        create_backup_btn.pack(side="left", padx=(0, 20))
        
        quick_backup_btn = ctk.CTkButton(
            backup_buttons_frame,
            text="⚡ Backup Rápido",
            command=self.create_quick_backup,
            width=200,
            height=50,
            font=ctk.CTkFont(size=16),
            fg_color="#FF9800"
        )
        quick_backup_btn.pack(side="left")
        
        # Restore Section
        restore_frame = ctk.CTkFrame(options_frame)
        restore_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        restore_title = ctk.CTkLabel(
            restore_frame,
            text="🔄 Restaurar Backup",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        restore_title.pack(pady=(10, 15))
        
        restore_desc = ctk.CTkLabel(
            restore_frame,
            text="Restaure dados de um arquivo de backup anterior",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        restore_desc.pack(pady=(0, 15))
        
        restore_buttons_frame = ctk.CTkFrame(restore_frame, fg_color="transparent")
        restore_buttons_frame.pack(fill="x", padx=20, pady=10)
        
        restore_btn = ctk.CTkButton(
            restore_buttons_frame,
            text="📥 Restaurar Backup",
            command=self.restore_backup,
            width=200,
            height=50,
            font=ctk.CTkFont(size=16),
            fg_color="#F44336"
        )
        restore_btn.pack(side="left", padx=(0, 20))
        
        # Auto Backup Section
        auto_frame = ctk.CTkFrame(options_frame)
        auto_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        auto_title = ctk.CTkLabel(
            auto_frame,
            text="⏰ Backup Automático",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        auto_title.pack(pady=(10, 15))
        
        # Auto backup status
        auto_enabled = self.manager.settings.get('auto_backup', True)
        status_text = "✅ Ativado" if auto_enabled else "❌ Desativado"
        status_color = "#4CAF50" if auto_enabled else "#F44336"
        
        status_label = ctk.CTkLabel(
            auto_frame,
            text=f"Status: {status_text}",
            font=ctk.CTkFont(size=14),
            text_color=status_color
        )
        status_label.pack()
        
        auto_toggle_btn = ctk.CTkButton(
            auto_frame,
            text="🔄 Alternar Backup Automático",
            command=self.toggle_auto_backup,
            width=250,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        auto_toggle_btn.pack(pady=15)
        
        # Backup Log
        log_frame = ctk.CTkFrame(backup_frame)
        log_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)
        
        log_title = ctk.CTkLabel(
            log_frame,
            text="📋 Log de Backups",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        log_title.pack(pady=(10, 5))
        
        self.backup_log = ctk.CTkTextbox(log_frame, height=250, font=ctk.CTkFont(size=12))
        self.backup_log.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Load backup log
        self.load_backup_log()
    
    def create_full_backup(self):
        """Create a full backup with all data"""
        try:
            # Get current timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            default_filename = f"backup_completo_{timestamp}.json"
            
            filename = filedialog.asksaveasfilename(
                title="Salvar Backup Completo",
                defaultextension=".json",
                initialvalue=default_filename,
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if filename:
                # Compile all data
                backup_data = {
                    'backup_info': {
                        'type': 'full',
                        'created_at': datetime.now().isoformat(),
                        'version': '1.0',
                        'description': 'Backup completo do sistema'
                    },
                    'products': self.manager.products,
                    'movements': self.manager.movements,
                    'suppliers': self.manager.suppliers,
                    'categories': self.manager.categories,
                    'settings': self.manager.settings
                }
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(backup_data, f, indent=2, ensure_ascii=False)
                
                # Log the backup
                log_entry = f"✅ {datetime.now().strftime('%d/%m/%Y %H:%M')} - Backup completo criado: {os.path.basename(filename)}"
                self.add_backup_log(log_entry)
                
                messagebox.showinfo("Sucesso", f"Backup completo criado com sucesso!\n\nArquivo: {filename}")
                
        except Exception as e:
            error_msg = f"❌ {datetime.now().strftime('%d/%m/%Y %H:%M')} - Erro ao criar backup: {str(e)}"
            self.add_backup_log(error_msg)
            messagebox.showerror("Erro", f"Erro ao criar backup: {str(e)}")
    
    def create_quick_backup(self):
        """Create a quick backup (products and movements only)"""
        try:
            # Create backup directory if it doesn't exist
            backup_dir = "backups"
            os.makedirs(backup_dir, exist_ok=True)
            
            # Get current timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(backup_dir, f"backup_rapido_{timestamp}.json")
            
            # Quick backup data (essential data only)
            backup_data = {
                'backup_info': {
                    'type': 'quick',
                    'created_at': datetime.now().isoformat(),
                    'version': '1.0',
                    'description': 'Backup rápido (produtos e movimentações)'
                },
                'products': self.manager.products,
                'movements': self.manager.movements
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, indent=2, ensure_ascii=False)
            
            # Log the backup
            log_entry = f"⚡ {datetime.now().strftime('%d/%m/%Y %H:%M')} - Backup rápido criado: {os.path.basename(filename)}"
            self.add_backup_log(log_entry)
            
            messagebox.showinfo("Sucesso", f"Backup rápido criado com sucesso!\n\nArquivo: {filename}")
            
        except Exception as e:
            error_msg = f"❌ {datetime.now().strftime('%d/%m/%Y %H:%M')} - Erro ao criar backup rápido: {str(e)}"
            self.add_backup_log(error_msg)
            messagebox.showerror("Erro", f"Erro ao criar backup rápido: {str(e)}")
    
    def restore_backup(self):
        """Restore data from backup file"""
        # Warning message
        if not messagebox.askyesno("Atenção", 
            "⚠️ A restauração irá SOBRESCREVER todos os dados atuais!\n\n"
            "Esta ação não pode ser desfeita.\n"
            "Recomendamos criar um backup dos dados atuais antes de continuar.\n\n"
            "Deseja continuar?"):
            return
        
        try:
            filename = filedialog.askopenfilename(
                title="Selecionar Arquivo de Backup",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if filename:
                with open(filename, 'r', encoding='utf-8') as f:
                    backup_data = json.load(f)
                
                # Validate backup file
                if 'backup_info' not in backup_data:
                    messagebox.showerror("Erro", "Arquivo de backup inválido!")
                    return
                
                backup_type = backup_data['backup_info'].get('type', 'unknown')
                
                # Restore data based on backup type
                if backup_type == 'full':
                    # Full restore
                    if all(key in backup_data for key in ['products', 'movements', 'suppliers', 'categories', 'settings']):
                        self.manager.products = backup_data['products']
                        self.manager.movements = backup_data['movements']
                        self.manager.suppliers = backup_data['suppliers']
                        self.manager.categories = backup_data['categories']
                        self.manager.settings = backup_data['settings']
                        
                        # Save all data
                        self.manager.save_data(self.manager.products, PRODUCTS_FILE)
                        self.manager.save_data(self.manager.movements, MOVEMENTS_FILE)
                        self.manager.save_data(self.manager.suppliers, SUPPLIERS_FILE)
                        self.manager.save_data(self.manager.categories, CATEGORIES_FILE)
                        self.manager.save_data(self.manager.settings, SETTINGS_FILE)
                        
                        log_entry = f"🔄 {datetime.now().strftime('%d/%m/%Y %H:%M')} - Backup completo restaurado: {os.path.basename(filename)}"
                        
                    else:
                        messagebox.showerror("Erro", "Backup completo inválido! Dados faltando.")
                        return
                        
                elif backup_type == 'quick':
                    # Quick restore (products and movements only)
                    if all(key in backup_data for key in ['products', 'movements']):
                        self.manager.products = backup_data['products']
                        self.manager.movements = backup_data['movements']
                        
                        # Save data
                        self.manager.save_data(self.manager.products, PRODUCTS_FILE)
                        self.manager.save_data(self.manager.movements, MOVEMENTS_FILE)
                        
                        log_entry = f"⚡ {datetime.now().strftime('%d/%m/%Y %H:%M')} - Backup rápido restaurado: {os.path.basename(filename)}"
                        
                    else:
                        messagebox.showerror("Erro", "Backup rápido inválido! Dados faltando.")
                        return
                        
                else:
                    messagebox.showerror("Erro", f"Tipo de backup desconhecido: {backup_type}")
                    return
                
                # Log the restore
                self.add_backup_log(log_entry)
                
                messagebox.showinfo("Sucesso", 
                    f"Backup restaurado com sucesso!\n\n"
                    f"Tipo: {backup_type.title()}\n"
                    f"Arquivo: {os.path.basename(filename)}\n\n"
                    "Reinicie o programa para aplicar as mudanças.")
                
        except Exception as e:
            error_msg = f"❌ {datetime.now().strftime('%d/%m/%Y %H:%M')} - Erro ao restaurar backup: {str(e)}"
            self.add_backup_log(error_msg)
            messagebox.showerror("Erro", f"Erro ao restaurar backup: {str(e)}")
    
    def toggle_auto_backup(self):
        """Toggle automatic backup setting"""
        try:
            current_setting = self.manager.settings.get('auto_backup', True)
            new_setting = not current_setting
            
            self.manager.settings['auto_backup'] = new_setting
            self.manager.save_data(self.manager.settings, SETTINGS_FILE)
            
            status = "ativado" if new_setting else "desativado"
            log_entry = f"⚙️ {datetime.now().strftime('%d/%m/%Y %H:%M')} - Backup automático {status}"
            self.add_backup_log(log_entry)
            
            messagebox.showinfo("Configuração Alterada", f"Backup automático {status} com sucesso!")
            
            # Refresh the view
            self.show_backup()
            
        except Exception as e:
            error_msg = f"❌ {datetime.now().strftime('%d/%m/%Y %H:%M')} - Erro ao alterar configuração: {str(e)}"
            self.add_backup_log(error_msg)
            messagebox.showerror("Erro", f"Erro ao alterar configuração: {str(e)}")
    
    def add_backup_log(self, message):
        """Add message to backup log"""
        try:
            log_file = os.path.join("data", "backup_log.txt")
            
            # Ensure data directory exists
            os.makedirs("data", exist_ok=True)
            
            # Append to log file
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"{message}\n")
                
        except Exception as e:
            print(f"Error writing to backup log: {e}")
    
    def load_backup_log(self):
        """Load and display backup log"""
        try:
            log_file = os.path.join("data", "backup_log.txt")
            
            if os.path.exists(log_file):
                with open(log_file, 'r', encoding='utf-8') as f:
                    log_content = f.read()
                
                # Show last 50 lines
                lines = log_content.strip().split('\n')
                recent_lines = lines[-50:] if len(lines) > 50 else lines
                
                self.backup_log.delete("1.0", "end")
                self.backup_log.insert("1.0", '\n'.join(recent_lines))
            else:
                self.backup_log.delete("1.0", "end")
                self.backup_log.insert("1.0", "📋 Nenhum log de backup encontrado.\n\nOs logs aparecerão aqui conforme você criar ou restaurar backups.")
                
        except Exception as e:
            self.backup_log.delete("1.0", "end")
            self.backup_log.insert("1.0", f"❌ Erro ao carregar log: {str(e)}")
    
    def show_help(self):
        """Show help information"""
        self.clear_main_content()
        
        # Help container
        help_frame = ctk.CTkFrame(self.main_frame)
        help_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        help_frame.grid_rowconfigure(1, weight=1)
        help_frame.grid_columnconfigure(0, weight=1)
        
        # Title
        title = ctk.CTkLabel(
            help_frame,
            text="❓ Ajuda e Suporte",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title.grid(row=0, column=0, pady=20)
        
        # Help content frame
        content_frame = ctk.CTkScrollableFrame(help_frame)
        content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        
        # System Info Section
        info_frame = ctk.CTkFrame(content_frame)
        info_frame.pack(fill="x", pady=10)
        
        info_title = ctk.CTkLabel(
            info_frame,
            text="ℹ️ Informações do Sistema",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        info_title.pack(pady=(10, 15))
        
        # Version info
        version_info = f"""
📦 Sistema de Controle de Estoque
🔢 Versão: 2.0.0
🐍 Python: {sys.version.split()[0]}
💻 Sistema: {os.name}
📁 Diretório de Dados: {os.path.abspath('data')}
        """.strip()
        
        version_label = ctk.CTkLabel(
            info_frame,
            text=version_info,
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        version_label.pack(padx=20, pady=10)
        
        # Quick Start Guide
        guide_frame = ctk.CTkFrame(content_frame)
        guide_frame.pack(fill="x", pady=10)
        
        guide_title = ctk.CTkLabel(
            guide_frame,
            text="🚀 Guia Rápido",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        guide_title.pack(pady=(10, 15))
        
        guide_text = """
1. 📦 PRODUTOS:
   • Clique em "Produtos" para gerenciar seu inventário
   • Use "➕ Novo Produto" para adicionar itens
   • Clique com botão direito para editar ou excluir

2. 📊 ESTOQUE:
   • Visualize níveis de estoque em "Inventário"
   • Ajuste quantidades em "Produtos" → Botão direito → "Ajustar Estoque"
   • Configure alertas de estoque baixo em "Configurações"

3. 📈 MOVIMENTAÇÕES:
   • Acompanhe entradas e saídas em "Movimentações"
   • Exporte relatórios usando o botão "📤 Exportar"
   • Filtre por período ou tipo de movimento

4. 👥 FORNECEDORES:
   • Gerencie fornecedores em "Fornecedores"
   • Vincule produtos aos fornecedores
   • Acompanhe dados de contato

5. 📁 CATEGORIAS:
   • Organize produtos por categoria
   • Crie e edite categorias conforme necessário
   • Visualize relatórios por categoria

6. 📊 RELATÓRIOS:
   • Acesse análises detalhadas em "Relatórios"
   • Gere relatórios por categoria, fornecedor ou período
   • Monitore valor total do estoque

7. 💾 BACKUP:
   • Faça backups regulares em "Backup"
   • Use "Backup Rápido" para salvar produtos e movimentações
   • Use "Backup Completo" para salvar todos os dados
        """.strip()
        
        guide_label = ctk.CTkLabel(
            guide_frame,
            text=guide_text,
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        guide_label.pack(padx=20, pady=10, anchor="w")
        
        # Keyboard Shortcuts
        shortcuts_frame = ctk.CTkFrame(content_frame)
        shortcuts_frame.pack(fill="x", pady=10)
        
        shortcuts_title = ctk.CTkLabel(
            shortcuts_frame,
            text="⌨️ Atalhos do Teclado",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        shortcuts_title.pack(pady=(10, 15))
        
        shortcuts_text = """
• Ctrl + N = Novo produto
• Ctrl + S = Salvar/Buscar
• Ctrl + F = Buscar
• Ctrl + E = Exportar
• F1 = Ajuda
• F5 = Atualizar
• Esc = Cancelar/Fechar
• Enter = Confirmar/Buscar
• Tab = Navegar entre campos
• Botão direito = Menu de contexto
        """.strip()
        
        shortcuts_label = ctk.CTkLabel(
            shortcuts_frame,
            text=shortcuts_text,
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        shortcuts_label.pack(padx=20, pady=10, anchor="w")
        
        # FAQ Section
        faq_frame = ctk.CTkFrame(content_frame)
        faq_frame.pack(fill="x", pady=10)
        
        faq_title = ctk.CTkLabel(
            faq_frame,
            text="❓ Perguntas Frequentes",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        faq_title.pack(pady=(10, 15))
        
        faq_text = """
Q: Como alterar a quantidade de um produto?
A: Vá em "Produtos" → botão direito no produto → "Ajustar Estoque"

Q: Como definir o limite de estoque baixo?
A: Acesse "Configurações" e altere o "Limite de Estoque Baixo"

Q: Como fazer backup dos dados?
A: Use "Backup" → "Criar Backup Completo" ou "Backup Rápido"

Q: Como importar produtos de outro sistema?
A: Use "Backup" → "Restaurar Backup" com arquivo JSON compatível

Q: O que fazer se perder dados?
A: Restaure o último backup em "Backup" → "Restaurar Backup"

Q: Como exportar relatórios?
A: Em "Movimentações", use o botão "📤 Exportar" para salvar em CSV

Q: Como categorizar produtos?
A: Crie categorias em "Categorias" e edite produtos para atribuí-las

Q: Como contactar fornecedores?
A: Veja dados de contato em "Fornecedores" → clique duplo no fornecedor
        """.strip()
        
        faq_label = ctk.CTkLabel(
            faq_frame,
            text=faq_text,
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        faq_label.pack(padx=20, pady=10, anchor="w")
        
        # Troubleshooting
        trouble_frame = ctk.CTkFrame(content_frame)
        trouble_frame.pack(fill="x", pady=10)
        
        trouble_title = ctk.CTkLabel(
            trouble_frame,
            text="🔧 Solução de Problemas",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        trouble_title.pack(pady=(10, 15))
        
        trouble_text = """
PROBLEMA: Programa não inicia
SOLUÇÃO: Verifique se todas as dependências estão instaladas:
         pip install -r requirements.txt

PROBLEMA: Erro ao salvar dados
SOLUÇÃO: Verifique permissões da pasta 'data' e espaço em disco

PROBLEMA: Interface não aparece corretamente
SOLUÇÃO: Atualize o CustomTkinter: pip install --upgrade customtkinter

PROBLEMA: Erro de encoding no Linux
SOLUÇÃO: Defina a variável de ambiente: export LANG=pt_BR.UTF-8

PROBLEMA: Gráficos não aparecem
SOLUÇÃO: Instale matplotlib: pip install matplotlib

PROBLEMA: Backup não funciona
SOLUÇÃO: Verifique permissões de escrita na pasta de destino

PROBLEMA: Dados corrompidos
SOLUÇÃO: Restaure o último backup válido

Para problemas persistentes:
1. Feche o programa completamente
2. Faça backup dos dados
3. Reinicie o programa
4. Se necessário, reinstale as dependências
        """.strip()
        
        trouble_label = ctk.CTkLabel(
            trouble_frame,
            text=trouble_text,
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        trouble_label.pack(padx=20, pady=10, anchor="w")
        
        # Support Section
        support_frame = ctk.CTkFrame(content_frame)
        support_frame.pack(fill="x", pady=10)
        
        support_title = ctk.CTkLabel(
            support_frame,
            text="📞 Suporte e Contato",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        support_title.pack(pady=(10, 15))
        
        support_text = """
💻 Sistema desenvolvido para controle eficiente de estoque
📧 Para suporte técnico e dúvidas, consulte a documentação
🔄 Mantenha sempre backups atualizados dos seus dados
📊 Use os relatórios para análises e tomada de decisões
🎯 Configure alertas de estoque baixo para melhor gestão

DICAS DE USO:
• Faça backup diário (pode ser configurado como automático)
• Mantenha fornecedores e categorias organizados
• Use códigos únicos para cada produto
• Revise periodicamente os relatórios de estoque
• Configure o limite de estoque baixo conforme sua necessidade
        """.strip()
        
        support_label = ctk.CTkLabel(
            support_frame,
            text=support_text,
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        support_label.pack(padx=20, pady=10, anchor="w")
    
    def run(self):
        """Run the application"""
        self.root.mainloop()


class ProductDialog:
    """Dialog for adding/editing products"""
    
    def __init__(self, parent, manager, product=None, title="Produto"):
        self.manager = manager
        self.product = product
        self.result = False
        
        # Create dialog
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("500x600")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (600 // 2)
        self.dialog.geometry(f"500x600+{x}+{y}")
        
        self.create_widgets()
        
        if product:
            self.populate_fields()
    
    def create_widgets(self):
        """Create dialog widgets"""
        # Main frame
        main_frame = ctk.CTkScrollableFrame(self.dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Form fields
        fields = [
            ("Código *", "code", "entry"),
            ("Nome *", "name", "entry"),
            ("Descrição", "description", "textbox"),
            ("Preço (R$) *", "price", "entry"),
            ("Quantidade *", "quantity", "entry"),
            ("Fornecedor", "supplier", "entry"),
            ("Categoria", "category", "entry"),
            ("Localização", "location", "entry"),
            ("Código de Barras", "barcode", "entry"),
            ("Peso (kg)", "weight", "entry"),
            ("Dimensões", "dimensions", "entry")
        ]
        
        self.fields = {}
        
        for label_text, field_name, field_type in fields:
            # Field frame
            field_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
            field_frame.pack(fill="x", pady=5)
            
            # Label
            label = ctk.CTkLabel(field_frame, text=label_text, anchor="w", font=ctk.CTkFont(size=14))
            label.pack(fill="x")
            
            # Field
            if field_type == "entry":
                field = ctk.CTkEntry(field_frame, height=40, font=ctk.CTkFont(size=14))
            elif field_type == "textbox":
                field = ctk.CTkTextbox(field_frame, height=100, font=ctk.CTkFont(size=14))
            
            field.pack(fill="x", pady=(5, 0))
            self.fields[field_name] = field
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=20)
        
        # Cancel button
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="Cancelar",
            command=self.cancel,
            fg_color="gray",
            width=120,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        cancel_btn.pack(side="right", padx=(10, 0))
        
        # Save button
        save_btn = ctk.CTkButton(
            buttons_frame,
            text="Salvar",
            command=self.save,
            width=120,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        save_btn.pack(side="right")
    
    def populate_fields(self):
        """Populate fields with product data"""
        if not self.product:
            return
        
        field_mapping = {
            'code': 'code',
            'name': 'name',
            'description': 'description',
            'price': 'price',
            'quantity': 'quantity',
            'supplier': 'supplier',
            'category': 'category',
            'location': 'location',
            'barcode': 'barcode',
            'weight': 'weight',
            'dimensions': 'dimensions'
        }
        
        for field_name, product_key in field_mapping.items():
            if field_name in self.fields and product_key in self.product:
                field = self.fields[field_name]
                value = str(self.product[product_key])
                
                if isinstance(field, ctk.CTkEntry):
                    field.insert(0, value)
                elif isinstance(field, ctk.CTkTextbox):
                    field.insert("1.0", value)
    
    def save(self):
        """Save product"""
        try:
            # Get field values
            data = {}
            for field_name, field in self.fields.items():
                if isinstance(field, ctk.CTkEntry):
                    data[field_name] = field.get().strip()
                elif isinstance(field, ctk.CTkTextbox):
                    data[field_name] = field.get("1.0", "end-1c").strip()
            
            # Validate required fields
            required_fields = ['code', 'name', 'price', 'quantity']
            for field in required_fields:
                if not data.get(field):
                    messagebox.showerror("Erro", f"O campo {field} é obrigatório!")
                    return
            
            # Convert numeric fields
            try:
                data['price'] = float(data['price'])
                data['quantity'] = int(data['quantity'])
                if data.get('weight'):
                    data['weight'] = float(data['weight'])
            except ValueError:
                messagebox.showerror("Erro", "Preço, Quantidade e Peso devem ser números válidos!")
                return
            
            # Save product
            if self.product:
                # Update existing product
                if self.manager.update_product(self.product['code'], data):
                    messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")
                    self.result = True
                    self.dialog.destroy()
                else:
                    messagebox.showerror("Erro", "Erro ao atualizar produto!")
            else:
                # Add new product
                if self.manager.add_product(data):
                    messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
                    self.result = True
                    self.dialog.destroy()
                else:
                    messagebox.showerror("Erro", "Código de produto já existe!")
        
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar produto: {str(e)}")
    
    def cancel(self):
        """Cancel dialog"""
        self.dialog.destroy()


class StockAdjustmentDialog:
    """Dialog for stock adjustments"""
    
    def __init__(self, parent, manager, product):
        self.manager = manager
        self.product = product
        self.result = False
        
        # Create dialog
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Ajustar Estoque")
        self.dialog.geometry("400x300")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (300 // 2)
        self.dialog.geometry(f"400x300+{x}+{y}")
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create dialog widgets"""
        # Main frame
        main_frame = ctk.CTkFrame(self.dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Product info
        info_frame = ctk.CTkFrame(main_frame)
        info_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            info_frame,
            text=f"Produto: {self.product['name']}",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=5)
        
        ctk.CTkLabel(
            info_frame,
            text=f"Estoque Atual: {self.product['quantity']} unidades",
            font=ctk.CTkFont(size=16)
        ).pack(pady=5)
        
        # Adjustment type
        ctk.CTkLabel(main_frame, text="Tipo de Ajuste:", font=ctk.CTkFont(size=16)).pack(anchor="w", pady=(0, 5))
        
        self.adjustment_type = ctk.StringVar(value="add")
        
        type_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        type_frame.pack(fill="x", pady=(0, 10))
        
        ctk.CTkRadioButton(
            type_frame,
            text="➕ Adicionar ao estoque",
            variable=self.adjustment_type,
            value="add",
            font=ctk.CTkFont(size=14)
        ).pack(anchor="w")
        
        ctk.CTkRadioButton(
            type_frame,
            text="➖ Remover do estoque",
            variable=self.adjustment_type,
            value="remove",
            font=ctk.CTkFont(size=14)
        ).pack(anchor="w")
        
        # Quantity
        ctk.CTkLabel(main_frame, text="Quantidade:", font=ctk.CTkFont(size=16)).pack(anchor="w", pady=(10, 5))
        self.quantity_entry = ctk.CTkEntry(main_frame, placeholder_text="Digite a quantidade...", height=35, font=ctk.CTkFont(size=14))
        self.quantity_entry.pack(fill="x", pady=(0, 10))
        
        # Reason
        ctk.CTkLabel(main_frame, text="Motivo:", font=ctk.CTkFont(size=16)).pack(anchor="w", pady=(0, 5))
        self.reason_entry = ctk.CTkEntry(main_frame, placeholder_text="Motivo do ajuste (opcional)", height=35, font=ctk.CTkFont(size=14))
        self.reason_entry.pack(fill="x", pady=(0, 20))
        
        # Buttons
        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(fill="x")
        
        ctk.CTkButton(
            buttons_frame,
            text="Cancelar",
            command=self.cancel,
            fg_color="gray",
            width=120,
            height=40,
            font=ctk.CTkFont(size=14)
        ).pack(side="right", padx=(10, 0))
        
        ctk.CTkButton(
            buttons_frame,
            text="Aplicar",
            command=self.apply_adjustment,
            width=120,
            height=40,
            font=ctk.CTkFont(size=14)
        ).pack(side="right")
    
    def apply_adjustment(self):
        """Apply stock adjustment"""
        try:
            quantity = int(self.quantity_entry.get())
            if quantity <= 0:
                messagebox.showerror("Erro", "Quantidade deve ser maior que zero!")
                return
            
            adjustment_type = self.adjustment_type.get()
            if adjustment_type == "remove":
                quantity = -quantity
            
            reason = self.reason_entry.get().strip() or "Ajuste manual"
            
            if self.manager.update_stock(self.product['code'], quantity, reason):
                messagebox.showinfo("Sucesso", "Estoque ajustado com sucesso!")
                self.result = True
                self.dialog.destroy()
            else:
                messagebox.showerror("Erro", "Erro ao ajustar estoque! Verifique se há estoque suficiente.")
        
        except ValueError:
            messagebox.showerror("Erro", "Quantidade deve ser um número inteiro!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao ajustar estoque: {str(e)}")
    
    def cancel(self):
        """Cancel dialog"""
        self.dialog.destroy()


class CategoryDialog:
    """Dialog for adding/editing categories"""
    
    def __init__(self, parent, manager, category=None, title="Categoria"):
        self.manager = manager
        self.category = category
        self.result = False
        
        # Create dialog
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("450x350")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (450 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (350 // 2)
        self.dialog.geometry(f"450x350+{x}+{y}")
        
        self.create_widgets()
        
        if category:
            self.populate_fields()
    
    def create_widgets(self):
        """Create dialog widgets"""
        # Main frame
        main_frame = ctk.CTkScrollableFrame(self.dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Form fields
        fields = [
            ("Nome *", "name", "entry"),
            ("Descrição", "description", "textbox"),
            ("Cor (hex)", "color", "entry")
        ]
        
        self.fields = {}
        
        for label_text, field_name, field_type in fields:
            # Field frame
            field_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
            field_frame.pack(fill="x", pady=5)
            
            # Label
            label = ctk.CTkLabel(field_frame, text=label_text, anchor="w", font=ctk.CTkFont(size=14))
            label.pack(fill="x")
            
            # Field
            if field_type == "entry":
                if field_name == "color":
                    field = ctk.CTkEntry(field_frame, height=35, font=ctk.CTkFont(size=14), placeholder_text="#FF0000")
                else:
                    field = ctk.CTkEntry(field_frame, height=35, font=ctk.CTkFont(size=14))
            elif field_type == "textbox":
                field = ctk.CTkTextbox(field_frame, height=80, font=ctk.CTkFont(size=14))
            
            field.pack(fill="x", pady=(5, 0))
            self.fields[field_name] = field
        
        # Active checkbox
        self.active_var = ctk.BooleanVar(value=True)
        active_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        active_frame.pack(fill="x", pady=10)
        
        active_checkbox = ctk.CTkCheckBox(
            active_frame,
            text="Categoria Ativa",
            variable=self.active_var,
            font=ctk.CTkFont(size=14)
        )
        active_checkbox.pack(anchor="w")
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=20)
        
        # Cancel button
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="Cancelar",
            command=self.cancel,
            fg_color="gray",
            width=120,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        cancel_btn.pack(side="right", padx=(10, 0))
        
        # Save button
        save_btn = ctk.CTkButton(
            buttons_frame,
            text="Salvar",
            command=self.save,
            width=120,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        save_btn.pack(side="right")
    
    def populate_fields(self):
        """Populate fields with category data"""
        if not self.category:
            return
        
        field_mapping = {
            'name': 'name',
            'description': 'description',
            'color': 'color'
        }
        
        for field_name, category_key in field_mapping.items():
            if field_name in self.fields and category_key in self.category:
                field = self.fields[field_name]
                value = str(self.category[category_key])
                
                if isinstance(field, ctk.CTkEntry):
                    field.insert(0, value)
                elif isinstance(field, ctk.CTkTextbox):
                    field.insert("1.0", value)
        
        self.active_var.set(self.category.get('active', True))
    
    def save(self):
        """Save category"""
        try:
            # Get field values
            data = {}
            for field_name, field in self.fields.items():
                if isinstance(field, ctk.CTkEntry):
                    data[field_name] = field.get().strip()
                elif isinstance(field, ctk.CTkTextbox):
                    data[field_name] = field.get("1.0", "end-1c").strip()
            
            # Validate required fields
            if not data.get('name'):
                messagebox.showerror("Erro", "O campo Nome é obrigatório!")
                return
            
            # Validate color format if provided
            if data.get('color'):
                color = data['color']
                if not color.startswith('#') or len(color) != 7:
                    messagebox.showerror("Erro", "Cor deve estar no formato #RRGGBB (ex: #FF0000)")
                    return
            
            # Add active status
            data['active'] = self.active_var.get()
            
            # Save category
            if self.category:
                # Update existing category
                for i, category in enumerate(self.manager.categories):
                    if category['name'] == self.category['name']:
                        # Update products if category name changed
                        old_name = self.category['name']
                        new_name = data['name']
                        if old_name != new_name:
                            for product in self.manager.products:
                                if product.get('category') == old_name:
                                    product['category'] = new_name
                            self.manager.save_data(self.manager.products, PRODUCTS_FILE)
                        
                        self.manager.categories[i] = data
                        break
                messagebox.showinfo("Sucesso", "Categoria atualizada com sucesso!")
            else:
                # Check if category name already exists
                if any(c['name'] == data['name'] for c in self.manager.categories):
                    messagebox.showerror("Erro", "Nome de categoria já existe!")
                    return
                
                # Add new category
                self.manager.categories.append(data)
                messagebox.showinfo("Sucesso", "Categoria cadastrada com sucesso!")
            
            # Save to file
            self.manager.save_data(self.manager.categories, CATEGORIES_FILE)
            self.result = True
            self.dialog.destroy()
        
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar categoria: {str(e)}")
    
    def cancel(self):
        """Cancel dialog"""
        self.dialog.destroy()


class SupplierDialog:
    """Dialog for adding/editing suppliers"""
    
    def __init__(self, parent, manager, supplier=None, title="Fornecedor"):
        self.manager = manager
        self.supplier = supplier
        self.result = False
        
        # Create dialog
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("500x400")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (400 // 2)
        self.dialog.geometry(f"500x400+{x}+{y}")
        
        self.create_widgets()
        
        if supplier:
            self.populate_fields()
    
    def create_widgets(self):
        """Create dialog widgets"""
        # Main frame
        main_frame = ctk.CTkScrollableFrame(self.dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Form fields
        fields = [
            ("Nome *", "name", "entry"),
            ("Pessoa de Contato", "contact", "entry"),
            ("Telefone", "phone", "entry"),
            ("Email", "email", "entry"),
            ("Endereço", "address", "textbox"),
            ("CNPJ", "cnpj", "entry"),
            ("Observações", "notes", "textbox")
        ]
        
        self.fields = {}
        
        for label_text, field_name, field_type in fields:
            # Field frame
            field_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
            field_frame.pack(fill="x", pady=5)
            
            # Label
            label = ctk.CTkLabel(field_frame, text=label_text, anchor="w", font=ctk.CTkFont(size=14))
            label.pack(fill="x")
            
            # Field
            if field_type == "entry":
                field = ctk.CTkEntry(field_frame, height=35, font=ctk.CTkFont(size=14))
            elif field_type == "textbox":
                field = ctk.CTkTextbox(field_frame, height=80, font=ctk.CTkFont(size=14))
            
            field.pack(fill="x", pady=(5, 0))
            self.fields[field_name] = field
        
        # Active checkbox
        self.active_var = ctk.BooleanVar(value=True)
        active_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        active_frame.pack(fill="x", pady=10)
        
        active_checkbox = ctk.CTkCheckBox(
            active_frame,
            text="Fornecedor Ativo",
            variable=self.active_var,
            font=ctk.CTkFont(size=14)
        )
        active_checkbox.pack(anchor="w")
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=20)
        
        # Cancel button
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="Cancelar",
            command=self.cancel,
            fg_color="gray",
            width=120,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        cancel_btn.pack(side="right", padx=(10, 0))
        
        # Save button
        save_btn = ctk.CTkButton(
            buttons_frame,
            text="Salvar",
            command=self.save,
            width=120,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        save_btn.pack(side="right")
    
    def populate_fields(self):
        """Populate fields with supplier data"""
        if not self.supplier:
            return
        
        field_mapping = {
            'name': 'name',
            'contact': 'contact',
            'phone': 'phone',
            'email': 'email',
            'address': 'address',
            'cnpj': 'cnpj',
            'notes': 'notes'
        }
        
        for field_name, supplier_key in field_mapping.items():
            if field_name in self.fields and supplier_key in self.supplier:
                field = self.fields[field_name]
                value = str(self.supplier[supplier_key])
                
                if isinstance(field, ctk.CTkEntry):
                    field.insert(0, value)
                elif isinstance(field, ctk.CTkTextbox):
                    field.insert("1.0", value)
        
        self.active_var.set(self.supplier.get('active', True))
    
    def save(self):
        """Save supplier"""
        try:
            # Get field values
            data = {}
            for field_name, field in self.fields.items():
                if isinstance(field, ctk.CTkEntry):
                    data[field_name] = field.get().strip()
                elif isinstance(field, ctk.CTkTextbox):
                    data[field_name] = field.get("1.0", "end-1c").strip()
            
            # Validate required fields
            if not data.get('name'):
                messagebox.showerror("Erro", "O campo Nome é obrigatório!")
                return
            
            # Add active status
            data['active'] = self.active_var.get()
            
            # Save supplier
            if self.supplier:
                # Update existing supplier
                for i, supplier in enumerate(self.manager.suppliers):
                    if supplier['name'] == self.supplier['name']:
                        self.manager.suppliers[i] = data
                        break
                messagebox.showinfo("Sucesso", "Fornecedor atualizado com sucesso!")
            else:
                # Check if supplier name already exists
                if any(s['name'] == data['name'] for s in self.manager.suppliers):
                    messagebox.showerror("Erro", "Nome de fornecedor já existe!")
                    return
                
                # Add new supplier
                self.manager.suppliers.append(data)
                messagebox.showinfo("Sucesso", "Fornecedor cadastrado com sucesso!")
            
            # Save to file
            self.manager.save_data(self.manager.suppliers, SUPPLIERS_FILE)
            self.result = True
            self.dialog.destroy()
        
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar fornecedor: {str(e)}")
    
    def cancel(self):
        """Cancel dialog"""
        self.dialog.destroy()


if __name__ == "__main__":
    try:
        app = ModernInventoryApp()
        app.run()
    except KeyboardInterrupt:
        print("\n🔄 Programa interrompido pelo usuário")
    except Exception as e:
        print(f"❌ Erro ao executar o programa: {e}")
        print("💡 Tente executar com: python3 -v main.py para mais detalhes")
        import traceback
        traceback.print_exc() 