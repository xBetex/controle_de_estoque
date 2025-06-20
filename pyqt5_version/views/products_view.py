"""
Products view for PyQt5 Inventory Management System
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QLineEdit, QFrame, QHeaderView, QAbstractItemView, QComboBox)
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QFont

from config import *
from utils import format_currency, MessageBox

class ProductsView(QWidget):
    """Products management view"""
    
    def __init__(self, inventory_manager, parent=None):
        super().__init__(parent)
        self.inventory_manager = inventory_manager
        self.parent_window = parent
        
        self.setup_ui()
        self.refresh()
    
    def setup_ui(self):
        """Setup products view UI"""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(20)
        
        # Header
        self.create_header(main_layout)
        
        # Search and filters
        self.create_search_section(main_layout)
        
        # Products table
        self.create_table(main_layout)
        
        # Apply styles
        self.apply_styles()
    
    def create_header(self, parent_layout):
        """Create header section"""
        header_frame = QFrame()
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        # Title
        title_label = QLabel("Gerenciamento de Produtos")
        title_label.setFont(FONTS['title'])
        title_label.setStyleSheet(f"color: {COLORS['text_primary']};")
        
        # Action buttons
        self.add_btn = QPushButton(ICONS['add'] + " Adicionar Produto")
        self.add_btn.setObjectName("primary_button")
        self.add_btn.clicked.connect(self.add_product)
        
        self.edit_btn = QPushButton(ICONS['edit'] + " Editar")
        self.edit_btn.setObjectName("secondary_button")
        self.edit_btn.clicked.connect(self.edit_product)
        self.edit_btn.setEnabled(False)
        
        self.delete_btn = QPushButton(ICONS['delete'] + " Excluir")
        self.delete_btn.setObjectName("secondary_button")
        self.delete_btn.clicked.connect(self.delete_product)
        self.delete_btn.setEnabled(False)
        
        # Layout
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.add_btn)
        header_layout.addWidget(self.edit_btn)
        header_layout.addWidget(self.delete_btn)
        
        parent_layout.addWidget(header_frame)
    
    def create_search_section(self, parent_layout):
        """Create search and filter section"""
        search_frame = QFrame()
        search_frame.setObjectName("search_frame")
        search_layout = QHBoxLayout(search_frame)
        search_layout.setContentsMargins(15, 10, 15, 10)
        
        # Search input
        search_label = QLabel(ICONS['search'] + " Buscar:")
        search_label.setFont(FONTS['body'])
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Digite o nome, código ou descrição do produto...")
        self.search_input.textChanged.connect(self.on_search_changed)
        
        # Supplier filter
        supplier_label = QLabel("👥 Fornecedor:")
        supplier_label.setFont(FONTS['body'])
        
        self.supplier_filter = QLineEdit()
        self.supplier_filter.setPlaceholderText("Digite o nome ou código do fornecedor...")
        self.supplier_filter.textChanged.connect(self.on_filter_changed)
        
        # Refresh button
        refresh_btn = QPushButton(ICONS['refresh'] + " Atualizar")
        refresh_btn.setObjectName("secondary_button")
        refresh_btn.clicked.connect(self.refresh)
        
        # Layout
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(supplier_label)
        search_layout.addWidget(self.supplier_filter)
        search_layout.addWidget(refresh_btn)
        
        parent_layout.addWidget(search_frame)
    
    def create_table(self, parent_layout):
        """Create products table"""
        # Table widget
        self.table = QTableWidget()
        self.table.setObjectName("data_table")
        
        # Configure table
        columns = PRODUCT_COLUMNS
        self.table.setColumnCount(len(columns))
        self.table.setHorizontalHeaderLabels([col['title'] for col in columns])
        
        # Table properties
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)
        
        # Header properties
        header = self.table.horizontalHeader()
        header.setStretchLastSection(True)
        for i, col in enumerate(columns):
            header.resizeSection(i, col['width'])
        
        # Connect selection change
        self.table.selectionModel().selectionChanged.connect(self.on_selection_changed)
        
        parent_layout.addWidget(self.table)
    
    def apply_styles(self):
        """Apply styles to the view"""
        self.setStyleSheet(f"""
            QPushButton#primary_button {{
                {STYLES['button_primary']}
            }}
            
            QPushButton#secondary_button {{
                {STYLES['button_secondary']}
            }}
            
            QLineEdit {{
                {STYLES['input_field']}
            }}
            
            QFrame#search_frame {{
                {STYLES['card']}
            }}
            
            QTableWidget#data_table {{
                {STYLES['table']}
            }}
        """)
    
    def refresh(self):
        """Refresh products table"""
        try:
            # Apply current filters
            self.apply_filters()
                
        except Exception as e:
            MessageBox.show_error(self, "Erro", f"Erro ao carregar produtos: {e}")
    
    def add_product_row(self, product):
        """Add product row to table"""
        row = self.table.rowCount()
        self.table.insertRow(row)
        
        # Product data
        items = [
            product.get('code', ''),
            product.get('name', ''),
            product.get('category', ''),
            product.get('supplier', ''),
            str(product.get('quantity', 0)),
            format_currency(product.get('price', 0)),
            format_currency(product.get('price', 0) * product.get('quantity', 0))
        ]
        
        # Add items to row
        for col, item_text in enumerate(items):
            item = QTableWidgetItem(item_text)
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Make read-only
            self.table.setItem(row, col, item)
    
    @pyqtSlot()
    def on_selection_changed(self):
        """Handle table selection change"""
        has_selection = len(self.table.selectionModel().selectedRows()) > 0
        self.edit_btn.setEnabled(has_selection)
        self.delete_btn.setEnabled(has_selection)
    

    
    @pyqtSlot(str)
    def on_search_changed(self, text):
        """Handle search text change"""
        self.apply_filters()
    
    @pyqtSlot(str)
    def on_filter_changed(self, text):
        """Handle supplier filter change"""
        self.apply_filters()
    
    def apply_filters(self):
        """Apply search and supplier filters"""
        try:
            search_text = self.search_input.text().strip()
            supplier_query = self.supplier_filter.text().strip()
            
            # Get all products
            all_products = self.inventory_manager.get_all_products()
            filtered_products = all_products
            
            # Apply supplier filter first
            if supplier_query:
                filtered_products = self.inventory_manager.get_products_by_supplier(supplier_query)
            
            # Apply search filter to the already filtered products
            if search_text:
                filtered_products = [p for p in filtered_products
                                   if (search_text.lower() in p.get('name', '').lower() or
                                       search_text.lower() in p.get('code', '').lower() or
                                       search_text.lower() in p.get('description', '').lower())]
            
            self.load_products(filtered_products)
                
        except Exception as e:
            MessageBox.show_error(self, "Erro", f"Erro ao aplicar filtros: {e}")
    
    def load_products(self, products):
        """Load products into table"""
        try:
            # Clear table
            self.table.setRowCount(0)
            
            # Populate table
            for product in products:
                self.add_product_row(product)
                
        except Exception as e:
            MessageBox.show_error(self, "Erro", f"Erro ao carregar produtos: {e}")
    
    def get_selected_product(self):
        """Get selected product"""
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            return None
        
        row = selected_rows[0].row()
        code = self.table.item(row, 0).text()  # Code is in first column
        return self.inventory_manager.get_product(code)
    
    @pyqtSlot()
    def add_product(self):
        """Add new product"""
        # For now, show a simple message
        # In full implementation, this would open a product dialog
        MessageBox.show_info(
            self, 
            "Adicionar Produto", 
            "Funcionalidade de adicionar produto será implementada em breve."
        )
    
    @pyqtSlot()
    def edit_product(self):
        """Edit selected product"""
        product = self.get_selected_product()
        if not product:
            return
        
        # For now, show a simple message
        MessageBox.show_info(
            self, 
            "Editar Produto", 
            f"Funcionalidade de editar produto '{product['name']}' será implementada em breve."
        )
    
    @pyqtSlot()
    def delete_product(self):
        """Delete selected product"""
        product = self.get_selected_product()
        if not product:
            return
        
        # Confirm deletion
        if MessageBox.ask_confirmation(
            self,
            "Confirmar Exclusão",
            f"Tem certeza que deseja excluir o produto '{product['name']}'?\n\nEsta ação não pode ser desfeita."
        ):
            try:
                success = self.inventory_manager.delete_product(product['code'])
                if success:
                    MessageBox.show_success(self, "Sucesso", "Produto excluído com sucesso!")
                    self.refresh()
                else:
                    MessageBox.show_error(self, "Erro", "Erro ao excluir produto.")
            except Exception as e:
                MessageBox.show_error(self, "Erro", f"Erro ao excluir produto: {e}") 