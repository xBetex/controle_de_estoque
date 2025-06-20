"""
Settings view for PyQt5 Inventory Management System
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from config import FONTS, COLORS

class SettingsView(QWidget):
    """Application settings view"""
    
    def __init__(self, inventory_manager, parent=None):
        super().__init__(parent)
        self.inventory_manager = inventory_manager
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup settings view UI"""
        layout = QVBoxLayout(self)
        
        title = QLabel("Configurações do Sistema")
        title.setFont(FONTS['title'])
        title.setStyleSheet(f"color: {COLORS['text_primary']};")
        
        content = QLabel("Vista de configurações será implementada aqui.")
        content.setAlignment(Qt.AlignCenter)
        content.setStyleSheet(f"color: {COLORS['text_secondary']};")
        
        layout.addWidget(title)
        layout.addWidget(content)
        layout.addStretch()
    
    def refresh(self):
        """Refresh view"""
        pass 