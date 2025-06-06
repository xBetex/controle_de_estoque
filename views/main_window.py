"""
Janela principal da aplicação de controle de estoque
"""

import customtkinter as ctk
from typing import Dict, Any
import sys

# Configure matplotlib backend before importing
import matplotlib
matplotlib.use('Agg')

from models import InventoryManager
from config import *
from views.dashboard_view import DashboardView
from views.products_view import ProductsView
from views.inventory_view import InventoryView
from views.movements_view import MovementsView
from views.suppliers_view import SuppliersView
from views.categories_view import CategoriesView
from views.reports_view import ReportsView
from views.settings_view import SettingsView
from views.backup_view import BackupView
from views.help_view import HelpView

class MainWindow:
    """Janela principal da aplicação"""
    
    def __init__(self):
        self.manager = InventoryManager()
        self.current_view = None
        self.views = {}
        
        self.setup_main_window()
        self.create_sidebar()
        self.create_main_content()
        self.show_dashboard()
    
    def setup_main_window(self):
        """Configurar janela principal"""
        # Configure CustomTkinter
        ctk.set_appearance_mode(THEME_MODE)
        ctk.set_default_color_theme(COLOR_THEME)
        
        self.root = ctk.CTk()
        self.root.title(APP_TITLE)
        self.root.geometry(DEFAULT_WINDOW_SIZE)
        self.root.minsize(*MIN_WINDOW_SIZE)
        
        # Configure grid
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        
        # Set window icon (if available)
        try:
            icon_path = os.path.join(ASSETS_DIR, "icon.ico")
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except:
            pass
    
    def create_sidebar(self):
        """Criar barra lateral de navegação"""
        # Sidebar frame
        self.sidebar = ctk.CTkFrame(self.root, width=SIDEBAR_WIDTH, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(20, weight=1)
        
        # Logo/título
        logo_label = ctk.CTkLabel(
            self.sidebar, 
            text="📦 Estoque", 
            font=ctk.CTkFont(size=FONT_SIZES["title"], weight="bold")
        )
        logo_label.grid(row=0, column=0, padx=20, pady=(20, 30))
        
        # Botões de navegação
        nav_buttons = [
            ("🏠 Dashboard", self.show_dashboard),
            ("📋 Produtos", self.show_products),
            ("📦 Estoque", self.show_inventory),
            ("📊 Movimentações", self.show_movements),
            ("🏢 Fornecedores", self.show_suppliers),
            ("🏷️ Categorias", self.show_categories),
            ("📈 Relatórios", self.show_reports),
            ("⚙️ Configurações", self.show_settings),
            ("💾 Backup", self.show_backup),
            ("❓ Ajuda", self.show_help)
        ]
        
        self.nav_buttons = {}
        for i, (text, command) in enumerate(nav_buttons, 1):
            btn = ctk.CTkButton(
                self.sidebar,
                text=text,
                command=command,
                width=SIDEBAR_WIDTH - 40,
                height=50,
                anchor="w",
                font=ctk.CTkFont(size=FONT_SIZES["button"])
            )
            btn.grid(row=i, column=0, padx=20, pady=5)
            self.nav_buttons[text] = btn
        
        # Botão de sair
        exit_btn = ctk.CTkButton(
            self.sidebar,
            text="🚪 Sair",
            command=self.root.quit,
            width=SIDEBAR_WIDTH - 40,
            height=50,
            anchor="w",
            fg_color="darkred",
            hover_color="red",
            font=ctk.CTkFont(size=FONT_SIZES["button"])
        )
        exit_btn.grid(row=21, column=0, padx=20, pady=(20, 20))
    
    def create_main_content(self):
        """Criar área de conteúdo principal"""
        self.main_content = ctk.CTkFrame(self.root, corner_radius=0)
        self.main_content.grid(row=0, column=1, sticky="nsew", padx=(2, 0))
        self.main_content.grid_rowconfigure(0, weight=1)
        self.main_content.grid_columnconfigure(0, weight=1)
    
    def clear_main_content(self):
        """Limpar conteúdo principal"""
        # Destruir view atual se existir
        if hasattr(self, 'current_view') and self.current_view:
            self.current_view.destroy()
        
        # Limpar todas as views armazenadas para forçar recriação
        self.views.clear()
        
        # Limpar widgets filhos
        for widget in self.main_content.winfo_children():
            widget.destroy()
    
    def highlight_nav_button(self, active_text: str):
        """Destacar botão de navegação ativo"""
        for text, button in self.nav_buttons.items():
            if text == active_text:
                button.configure(fg_color=COLORS["primary"])
            else:
                button.configure(fg_color=["#3B8ED0", "#1F6AA5"])  # Default colors
    
    def show_dashboard(self):
        """Mostrar dashboard"""
        self.clear_main_content()
        self.highlight_nav_button("🏠 Dashboard")
        
        if "dashboard" not in self.views:
            self.views["dashboard"] = DashboardView(self.main_content, self.manager)
        
        self.current_view = self.views["dashboard"]
        self.current_view.show()
    
    def show_products(self):
        """Mostrar produtos"""
        self.clear_main_content()
        self.highlight_nav_button("📋 Produtos")
        
        if "products" not in self.views:
            self.views["products"] = ProductsView(self.main_content, self.manager, self.root)
        
        self.current_view = self.views["products"]
        self.current_view.show()
    
    def show_inventory(self):
        """Mostrar estoque"""
        self.clear_main_content()
        self.highlight_nav_button("📦 Estoque")
        
        if "inventory" not in self.views:
            self.views["inventory"] = InventoryView(self.main_content, self.manager)
        
        self.current_view = self.views["inventory"]
        self.current_view.show()
    
    def show_movements(self):
        """Mostrar movimentações"""
        self.clear_main_content()
        self.highlight_nav_button("📊 Movimentações")
        
        if "movements" not in self.views:
            self.views["movements"] = MovementsView(self.main_content, self.manager)
        
        self.current_view = self.views["movements"]
        self.current_view.show()
    
    def show_suppliers(self):
        """Mostrar fornecedores"""
        self.clear_main_content()
        self.highlight_nav_button("🏢 Fornecedores")
        
        if "suppliers" not in self.views:
            self.views["suppliers"] = SuppliersView(self.main_content, self.manager, self.root)
        
        self.current_view = self.views["suppliers"]
        self.current_view.show()
    
    def show_categories(self):
        """Mostrar categorias"""
        self.clear_main_content()
        self.highlight_nav_button("🏷️ Categorias")
        
        if "categories" not in self.views:
            self.views["categories"] = CategoriesView(self.main_content, self.manager, self.root)
        
        self.current_view = self.views["categories"]
        self.current_view.show()
    
    def show_reports(self):
        """Mostrar relatórios"""
        self.clear_main_content()
        self.highlight_nav_button("📈 Relatórios")
        
        if "reports" not in self.views:
            self.views["reports"] = ReportsView(self.main_content, self.manager)
        
        self.current_view = self.views["reports"]
        self.current_view.show()
    
    def show_settings(self):
        """Mostrar configurações"""
        self.clear_main_content()
        self.highlight_nav_button("⚙️ Configurações")
        
        if "settings" not in self.views:
            self.views["settings"] = SettingsView(self.main_content, self.manager)
        
        self.current_view = self.views["settings"]
        self.current_view.show()
    
    def show_backup(self):
        """Mostrar backup"""
        self.clear_main_content()
        self.highlight_nav_button("💾 Backup")
        
        if "backup" not in self.views:
            self.views["backup"] = BackupView(self.main_content, self.manager)
        
        self.current_view = self.views["backup"]
        self.current_view.show()
    
    def show_help(self):
        """Mostrar ajuda"""
        self.clear_main_content()
        self.highlight_nav_button("❓ Ajuda")
        
        if "help" not in self.views:
            self.views["help"] = HelpView(self.main_content, self.manager)
        
        self.current_view = self.views["help"]
        self.current_view.show()
    
    def run(self):
        """Executar aplicação"""
        self.root.mainloop() 