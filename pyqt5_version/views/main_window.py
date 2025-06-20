"""
Main window for PyQt5 Inventory Management System
"""

import sys
from PyQt5.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
                             QPushButton, QLabel, QFrame, QStackedWidget,
                             QApplication, QSplashScreen, QButtonGroup)
from PyQt5.QtCore import Qt, QTimer, pyqtSlot
from PyQt5.QtGui import QFont, QPixmap

from config import *
from models import InventoryManager
from utils import MessageBox

# Import views
from .dashboard_view import DashboardView
from .products_view import ProductsView
from .inventory_view import InventoryView
from .movements_view import MovementsView
from .suppliers_view import SuppliersView
from .categories_view import CategoriesView
from .reports_view import ReportsView
from .settings_view import SettingsView

class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.inventory_manager = InventoryManager()
        self.current_view = None
        self.views = {}
        
        self.setup_window()
        self.create_layout()
        self.create_sidebar()
        self.create_content_area()
        self.apply_styles()
        self.show_dashboard()
        
        # Connect signals
        self.connect_signals()
    
    def setup_window(self):
        """Setup main window properties"""
        self.setWindowTitle(APP_TITLE)
        self.setGeometry(100, 100, *DEFAULT_WINDOW_SIZE)
        self.setMinimumSize(*MIN_WINDOW_SIZE)
        
        # Center window on screen
        self.center_window()
    
    def center_window(self):
        """Center window on screen"""
        screen = QApplication.desktop().screenGeometry()
        window = self.geometry()
        x = (screen.width() - window.width()) // 2
        y = (screen.height() - window.height()) // 2
        self.move(x, y)
    
    def create_layout(self):
        """Create main layout"""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main horizontal layout
        self.main_layout = QHBoxLayout(central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
    
    def create_sidebar(self):
        """Create navigation sidebar"""
        # Sidebar frame
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(SIDEBAR_WIDTH)
        self.sidebar.setObjectName("sidebar")
        
        # Sidebar layout
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)
        
        # Logo/Title
        title_frame = QFrame()
        title_frame.setFixedHeight(80)
        title_layout = QVBoxLayout(title_frame)
        
        logo_label = QLabel("📦")
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setFont(QFont("Arial", 24))
        logo_label.setObjectName("logo")
        
        title_label = QLabel("Estoque")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(FONTS['title'])
        title_label.setObjectName("title")
        
        title_layout.addWidget(logo_label)
        title_layout.addWidget(title_label)
        sidebar_layout.addWidget(title_frame)
        
        # Navigation buttons
        self.nav_buttons = QButtonGroup(self)
        nav_items = [
            ('dashboard', ICONS['dashboard'] + ' Dashboard', self.show_dashboard),
            ('products', ICONS['products'] + ' Produtos', self.show_products),
            ('inventory', ICONS['inventory'] + ' Estoque', self.show_inventory),
            ('movements', ICONS['movements'] + ' Movimentações', self.show_movements),
            ('suppliers', ICONS['suppliers'] + ' Fornecedores', self.show_suppliers),
            ('categories', ICONS['categories'] + ' Categorias', self.show_categories),
            ('reports', ICONS['reports'] + ' Relatórios', self.show_reports),
            ('settings', ICONS['settings'] + ' Configurações', self.show_settings),
        ]
        
        self.nav_button_widgets = {}
        for view_name, text, callback in nav_items:
            btn = QPushButton(text)
            btn.setObjectName("nav_button")
            btn.setCheckable(True)
            btn.clicked.connect(callback)
            btn.setFont(FONTS['button'])
            
            self.nav_buttons.addButton(btn)
            self.nav_button_widgets[view_name] = btn
            sidebar_layout.addWidget(btn)
        
        # Spacer
        sidebar_layout.addStretch()
        
        # Exit button
        exit_btn = QPushButton(ICONS['help'] + " Sair")
        exit_btn.setObjectName("exit_button")
        exit_btn.clicked.connect(self.close)
        exit_btn.setFont(FONTS['button'])
        sidebar_layout.addWidget(exit_btn)
        
        # Add sidebar to main layout
        self.main_layout.addWidget(self.sidebar)
    
    def create_content_area(self):
        """Create main content area"""
        # Content frame
        self.content_frame = QFrame()
        self.content_frame.setObjectName("content_area")
        
        # Content layout
        self.content_layout = QVBoxLayout(self.content_frame)
        self.content_layout.setContentsMargins(20, 20, 20, 20)
        
        # Stacked widget for views
        self.stacked_widget = QStackedWidget()
        self.content_layout.addWidget(self.stacked_widget)
        
        # Add content area to main layout
        self.main_layout.addWidget(self.content_frame)
    
    def apply_styles(self):
        """Apply stylesheet to the window"""
        self.setStyleSheet(f"""
            {STYLES['main_window']}
            
            QFrame#sidebar {{
                {STYLES['sidebar']}
            }}
            
            QLabel#logo {{
                color: white;
                font-size: 32px;
                margin: 10px;
            }}
            
            QLabel#title {{
                color: white;
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 20px;
            }}
            
            QPushButton#nav_button {{
                {STYLES['nav_button']}
            }}
            
            QPushButton#exit_button {{
                {STYLES['nav_button']}
                background-color: #D32F2F;
                margin: 10px;
                border-radius: 5px;
            }}
            
            QPushButton#exit_button:hover {{
                background-color: #B71C1C;
            }}
            
            QFrame#content_area {{
                {STYLES['content_area']}
                margin: 10px;
            }}
        """)
    
    def connect_signals(self):
        """Connect inventory manager signals"""
        self.inventory_manager.product_added.connect(self.on_data_changed)
        self.inventory_manager.product_updated.connect(self.on_data_changed)
        self.inventory_manager.product_deleted.connect(self.on_data_changed)
        self.inventory_manager.movement_added.connect(self.on_data_changed)
        self.inventory_manager.supplier_added.connect(self.on_data_changed)
        self.inventory_manager.category_added.connect(self.on_data_changed)
    
    @pyqtSlot()
    def on_data_changed(self):
        """Handle data changes"""
        # Refresh current view if it has a refresh method
        if self.current_view and hasattr(self.current_view, 'refresh'):
            self.current_view.refresh()
    
    def set_active_nav_button(self, view_name: str):
        """Set active navigation button"""
        for name, btn in self.nav_button_widgets.items():
            btn.setChecked(name == view_name)
    
    def show_view(self, view_class, view_name: str):
        """Show a specific view"""
        # Create view if it doesn't exist
        if view_name not in self.views:
            self.views[view_name] = view_class(self.inventory_manager, self)
            self.stacked_widget.addWidget(self.views[view_name])
        
        # Show the view
        self.current_view = self.views[view_name]
        self.stacked_widget.setCurrentWidget(self.current_view)
        self.set_active_nav_button(view_name)
        
        # Refresh view if it has refresh method
        if hasattr(self.current_view, 'refresh'):
            self.current_view.refresh()
    
    # Navigation methods
    def show_dashboard(self):
        """Show dashboard view"""
        self.show_view(DashboardView, 'dashboard')
    
    def show_products(self):
        """Show products view"""
        self.show_view(ProductsView, 'products')
    
    def show_inventory(self):
        """Show inventory view"""
        self.show_view(InventoryView, 'inventory')
    
    def show_movements(self):
        """Show movements view"""
        self.show_view(MovementsView, 'movements')
    
    def show_suppliers(self):
        """Show suppliers view"""
        self.show_view(SuppliersView, 'suppliers')
    
    def show_categories(self):
        """Show categories view"""
        self.show_view(CategoriesView, 'categories')
    
    def show_reports(self):
        """Show reports view"""
        self.show_view(ReportsView, 'reports')
    
    def show_settings(self):
        """Show settings view"""
        self.show_view(SettingsView, 'settings')
    
    def closeEvent(self, event):
        """Handle window close event"""
        # Ask for confirmation
        if MessageBox.ask_confirmation(
            self, 
            "Confirmar Saída", 
            "Tem certeza que deseja sair do sistema?"
        ):
            event.accept()
        else:
            event.ignore()

def create_splash_screen():
    """Create splash screen"""
    splash_pixmap = QPixmap(400, 300)
    splash_pixmap.fill(Qt.white)
    
    splash = QSplashScreen(splash_pixmap)
    splash.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.SplashScreen)
    
    # Add text to splash screen
    splash.showMessage(
        "Carregando Sistema de Controle de Estoque...",
        Qt.AlignBottom | Qt.AlignCenter,
        Qt.black
    )
    
    return splash

def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)
    app.setOrganizationName(APP_ORGANIZATION)
    
    # Show splash screen
    splash = create_splash_screen()
    splash.show()
    
    # Process events to show splash
    app.processEvents()
    
    # Simulate loading time
    QTimer.singleShot(2000, splash.close)
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Close splash when main window is shown
    splash.finish(window)
    
    # Start event loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 