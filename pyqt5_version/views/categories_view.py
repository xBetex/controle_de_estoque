"""
Categories view for PyQt5 Inventory Management System
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from config import FONTS, COLORS

class CategoriesView(QWidget):
    """Categories management view"""
    
    def __init__(self, inventory_manager, parent=None):
        super().__init__(parent)
        self.inventory_manager = inventory_manager
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup categories view UI"""
        layout = QVBoxLayout(self)
        
        title = QLabel("Gerenciamento de Categorias")
        title.setFont(FONTS['title'])
        title.setStyleSheet(f"color: {COLORS['text_primary']};")
        
        content = QLabel("Vista de categorias será implementada aqui.")
        content.setAlignment(Qt.AlignCenter)
        content.setStyleSheet(f"color: {COLORS['text_secondary']};")
        
        layout.addWidget(title)
        layout.addWidget(content)
        layout.addStretch()
    
    def refresh(self):
        """Refresh view"""
        pass 