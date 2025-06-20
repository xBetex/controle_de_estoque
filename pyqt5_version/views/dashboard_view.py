"""
Dashboard view for PyQt5 Inventory Management System
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QFrame, QGridLayout, QScrollArea)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont

from config import *
from utils import format_currency

class StatCard(QFrame):
    """Statistics card widget"""
    
    def __init__(self, title: str, value: str, icon: str, color: str = None):
        super().__init__()
        self.title = title
        self.value = value
        self.icon = icon
        self.color = color or COLORS['primary']
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup card UI"""
        self.setObjectName("stat_card")
        self.setFixedHeight(120)
        
        # Layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)
        
        # Icon
        icon_label = QLabel(self.icon)
        icon_label.setFont(QFont("Arial", 32))
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setFixedSize(60, 60)
        icon_label.setStyleSheet(f"""
            QLabel {{
                color: {self.color};
                background-color: rgba({self._hex_to_rgb(self.color)}, 0.1);
                border-radius: 30px;
            }}
        """)
        
        # Text content
        text_layout = QVBoxLayout()
        text_layout.setSpacing(5)
        
        value_label = QLabel(self.value)
        value_label.setFont(QFont("Arial", 18, QFont.Bold))
        value_label.setStyleSheet(f"color: {COLORS['text_primary']};")
        
        title_label = QLabel(self.title)
        title_label.setFont(FONTS['caption'])
        title_label.setStyleSheet(f"color: {COLORS['text_secondary']};")
        
        text_layout.addWidget(value_label)
        text_layout.addWidget(title_label)
        text_layout.addStretch()
        
        # Add to main layout
        layout.addWidget(icon_label)
        layout.addLayout(text_layout)
        layout.addStretch()
        
        # Apply card styling
        self.setStyleSheet(f"""
            QFrame#stat_card {{
                {STYLES['card']}
                min-width: 200px;
            }}
        """)
    
    def _hex_to_rgb(self, hex_color: str) -> str:
        """Convert hex color to RGB values"""
        hex_color = hex_color.lstrip('#')
        return ', '.join(str(int(hex_color[i:i+2], 16)) for i in (0, 2, 4))
    
    def update_value(self, new_value: str):
        """Update card value"""
        self.value = new_value
        # Find and update the value label
        for child in self.findChildren(QLabel):
            if child.font().bold():
                child.setText(new_value)
                break

class DashboardView(QWidget):
    """Dashboard view showing overview statistics"""
    
    def __init__(self, inventory_manager, parent=None):
        super().__init__(parent)
        self.inventory_manager = inventory_manager
        self.stat_cards = {}
        
        self.setup_ui()
        self.refresh()
        
        # Auto-refresh timer
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh)
        self.refresh_timer.start(30000)  # Refresh every 30 seconds
    
    def setup_ui(self):
        """Setup dashboard UI"""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(20)
        
        # Title
        title_label = QLabel("Dashboard - Visão Geral")
        title_label.setFont(FONTS['title'])
        title_label.setStyleSheet(f"color: {COLORS['text_primary']};")
        main_layout.addWidget(title_label)
        
        # Scroll area for content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Content widget
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(30)
        
        # Statistics cards
        self.create_stats_section(content_layout)
        
        # Quick actions section
        self.create_quick_actions_section(content_layout)
        
        # Recent activity section
        self.create_recent_activity_section(content_layout)
        
        # Alerts section
        self.create_alerts_section(content_layout)
        
        # Set content widget to scroll area
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)
    
    def create_stats_section(self, parent_layout):
        """Create statistics cards section"""
        # Section title
        section_title = QLabel("Estatísticas Gerais")
        section_title.setFont(FONTS['heading'])
        section_title.setStyleSheet(f"color: {COLORS['text_primary']};")
        parent_layout.addWidget(section_title)
        
        # Cards grid
        cards_frame = QFrame()
        cards_layout = QGridLayout(cards_frame)
        cards_layout.setSpacing(20)
        
        # Create stat cards
        card_configs = [
            ('total_products', 'Total de Produtos', '0', ICONS['products'], COLORS['primary']),
            ('total_items', 'Itens em Estoque', '0', ICONS['inventory'], COLORS['info']),
            ('total_value', 'Valor Total', 'R$ 0,00', ICONS['reports'], COLORS['success']),
            ('low_stock', 'Estoque Baixo', '0', ICONS['warning'], COLORS['warning']),
            ('total_suppliers', 'Fornecedores', '0', ICONS['suppliers'], COLORS['primary']),
            ('total_categories', 'Categorias', '0', ICONS['categories'], COLORS['info'])
        ]
        
        row, col = 0, 0
        for card_id, title, initial_value, icon, color in card_configs:
            card = StatCard(title, initial_value, icon, color)
            self.stat_cards[card_id] = card
            
            cards_layout.addWidget(card, row, col)
            col += 1
            if col >= 3:  # 3 cards per row
                col = 0
                row += 1
        
        parent_layout.addWidget(cards_frame)
    
    def create_quick_actions_section(self, parent_layout):
        """Create quick actions section"""
        # Section title
        section_title = QLabel("Ações Rápidas")
        section_title.setFont(FONTS['heading'])
        section_title.setStyleSheet(f"color: {COLORS['text_primary']};")
        parent_layout.addWidget(section_title)
        
        # Quick actions frame
        actions_frame = QFrame()
        actions_frame.setObjectName("actions_frame")
        actions_layout = QHBoxLayout(actions_frame)
        actions_layout.setSpacing(15)
        
        # Quick action buttons would go here
        # For now, just a placeholder
        placeholder_label = QLabel("Ações rápidas serão implementadas aqui")
        placeholder_label.setAlignment(Qt.AlignCenter)
        placeholder_label.setStyleSheet(f"color: {COLORS['text_secondary']};")
        actions_layout.addWidget(placeholder_label)
        
        actions_frame.setStyleSheet(f"""
            QFrame#actions_frame {{
                {STYLES['card']}
                min-height: 80px;
            }}
        """)
        
        parent_layout.addWidget(actions_frame)
    
    def create_recent_activity_section(self, parent_layout):
        """Create recent activity section"""
        # Section title
        section_title = QLabel("Atividade Recente")
        section_title.setFont(FONTS['heading'])
        section_title.setStyleSheet(f"color: {COLORS['text_primary']};")
        parent_layout.addWidget(section_title)
        
        # Activity frame
        self.activity_frame = QFrame()
        self.activity_frame.setObjectName("activity_frame")
        self.activity_layout = QVBoxLayout(self.activity_frame)
        self.activity_layout.setSpacing(10)
        
        self.activity_frame.setStyleSheet(f"""
            QFrame#activity_frame {{
                {STYLES['card']}
                min-height: 200px;
            }}
        """)
        
        parent_layout.addWidget(self.activity_frame)
    
    def create_alerts_section(self, parent_layout):
        """Create alerts section"""
        # Section title
        section_title = QLabel("Alertas")
        section_title.setFont(FONTS['heading'])
        section_title.setStyleSheet(f"color: {COLORS['text_primary']};")
        parent_layout.addWidget(section_title)
        
        # Alerts frame
        self.alerts_frame = QFrame()
        self.alerts_frame.setObjectName("alerts_frame")
        self.alerts_layout = QVBoxLayout(self.alerts_frame)
        self.alerts_layout.setSpacing(10)
        
        self.alerts_frame.setStyleSheet(f"""
            QFrame#alerts_frame {{
                {STYLES['card']}
                min-height: 150px;
            }}
        """)
        
        parent_layout.addWidget(self.alerts_frame)
    
    def refresh(self):
        """Refresh dashboard data"""
        try:
            # Get statistics from inventory manager
            stats = self.inventory_manager.get_dashboard_stats()
            
            # Update stat cards
            if 'total_products' in self.stat_cards:
                self.stat_cards['total_products'].update_value(str(stats['total_products']))
                
            if 'total_items' in self.stat_cards:
                self.stat_cards['total_items'].update_value(str(stats['total_items']))
                
            if 'total_value' in self.stat_cards:
                self.stat_cards['total_value'].update_value(
                    format_currency(stats['total_value'])
                )
                
            if 'low_stock' in self.stat_cards:
                self.stat_cards['low_stock'].update_value(str(stats['low_stock_count']))
                
            if 'total_suppliers' in self.stat_cards:
                self.stat_cards['total_suppliers'].update_value(str(stats['total_suppliers']))
                
            if 'total_categories' in self.stat_cards:
                self.stat_cards['total_categories'].update_value(str(stats['total_categories']))
            
            # Update recent activity
            self.update_recent_activity()
            
            # Update alerts
            self.update_alerts()
            
        except Exception as e:
            print(f"Error refreshing dashboard: {e}")
    
    def update_recent_activity(self):
        """Update recent activity section"""
        # Clear existing activity items
        for i in reversed(range(self.activity_layout.count())):
            child = self.activity_layout.itemAt(i).widget()
            if child:
                child.setParent(None)
        
        # Get recent movements
        recent_movements = self.inventory_manager.get_all_movements()[:5]  # Last 5 movements
        
        if not recent_movements:
            no_activity_label = QLabel("Nenhuma atividade recente")
            no_activity_label.setAlignment(Qt.AlignCenter)
            no_activity_label.setStyleSheet(f"color: {COLORS['text_secondary']};")
            self.activity_layout.addWidget(no_activity_label)
        else:
            for movement in recent_movements:
                activity_item = self.create_activity_item(movement)
                self.activity_layout.addWidget(activity_item)
        
        self.activity_layout.addStretch()
    
    def create_activity_item(self, movement):
        """Create activity item widget"""
        item_frame = QFrame()
        item_layout = QHBoxLayout(item_frame)
        item_layout.setContentsMargins(10, 5, 10, 5)
        
        # Movement type icon
        icon = ICONS['movements']
        if movement['type'] == 'entrada':
            icon = '📥'
        elif movement['type'] == 'saída':
            icon = '📤'
        
        icon_label = QLabel(icon)
        icon_label.setFont(QFont("Arial", 16))
        icon_label.setFixedSize(30, 30)
        icon_label.setAlignment(Qt.AlignCenter)
        
        # Movement description
        from utils import format_date
        description = f"{movement['type'].capitalize()} - {movement['product_code']} ({movement['quantity']} unidades)"
        date_str = format_date(movement['date'], format_to="%d/%m/%Y %H:%M")
        
        desc_label = QLabel(description)
        desc_label.setFont(FONTS['body'])
        desc_label.setStyleSheet(f"color: {COLORS['text_primary']};")
        
        date_label = QLabel(date_str)
        date_label.setFont(FONTS['caption'])
        date_label.setStyleSheet(f"color: {COLORS['text_secondary']};")
        
        # Layout
        item_layout.addWidget(icon_label)
        item_layout.addWidget(desc_label)
        item_layout.addStretch()
        item_layout.addWidget(date_label)
        
        return item_frame
    
    def update_alerts(self):
        """Update alerts section"""
        # Clear existing alerts
        for i in reversed(range(self.alerts_layout.count())):
            child = self.alerts_layout.itemAt(i).widget()
            if child:
                child.setParent(None)
        
        # Get low stock products
        low_stock_products = self.inventory_manager.get_low_stock_products()
        
        if not low_stock_products:
            no_alerts_label = QLabel("✅ Nenhum alerta no momento")
            no_alerts_label.setAlignment(Qt.AlignCenter)
            no_alerts_label.setStyleSheet(f"color: {COLORS['success']};")
            self.alerts_layout.addWidget(no_alerts_label)
        else:
            # Show low stock alert
            alert_text = f"⚠️ {len(low_stock_products)} produto(s) com estoque baixo"
            alert_label = QLabel(alert_text)
            alert_label.setFont(FONTS['body'])
            alert_label.setStyleSheet(f"""
                color: {COLORS['warning']};
                background-color: rgba(255, 152, 0, 0.1);
                padding: 10px;
                border-radius: 5px;
                border-left: 4px solid {COLORS['warning']};
            """)
            self.alerts_layout.addWidget(alert_label)
        
        self.alerts_layout.addStretch() 