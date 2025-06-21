# -*- coding: utf-8 -*-
"""
Estilos visuais para a aplicação - Tema Alto Contraste
"""

def get_high_contrast_style():
    """
    Retorna CSS para tema de alto contraste
    Cores fortes, contornos marcados, excelente legibilidade
    """
    return """
    /* === CONFIGURAÇÕES GLOBAIS === */
    QWidget {
        background-color: #000000;
        color: #FFFFFF;
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 10pt;
        font-weight: 500;
    }

    QMainWindow {
        background-color: #000000;
        color: #FFFFFF;
    }

    /* === BOTÕES === */
    QPushButton {
        background-color: #0066CC;
        color: #FFFFFF;
        border: 2px solid #FFFFFF;
        border-radius: 6px;
        padding: 8px 16px;
        font-weight: bold;
        font-size: 10pt;
        min-height: 20px;
    }

    QPushButton:hover {
        background-color: #0080FF;
        border-color: #FFFF00;
        color: #000000;
    }

    QPushButton:pressed {
        background-color: #004499;
        border-color: #FF0000;
    }

    QPushButton:disabled {
        background-color: #333333;
        color: #666666;
        border-color: #444444;
    }

    /* Botões de ação primária */
    QPushButton[class="primary"] {
        background-color: #00AA00;
        border-color: #FFFFFF;
    }

    QPushButton[class="primary"]:hover {
        background-color: #00DD00;
        color: #000000;
        border-color: #FFFF00;
    }

    /* Botões de perigo */
    QPushButton[class="danger"] {
        background-color: #CC0000;
        border-color: #FFFFFF;
    }

    QPushButton[class="danger"]:hover {
        background-color: #FF0000;
        border-color: #FFFF00;
    }

    /* === CAMPOS DE ENTRADA === */
    QLineEdit, QTextEdit, QPlainTextEdit {
        background-color: #FFFFFF;
        color: #000000;
        border: 3px solid #0066CC;
        border-radius: 6px;
        padding: 6px;
        font-size: 10pt;
        font-weight: bold;
    }

    QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
        border-color: #FFFF00;
        background-color: #FFFFCC;
    }

    QLineEdit:disabled, QTextEdit:disabled, QPlainTextEdit:disabled {
        background-color: #CCCCCC;
        color: #666666;
        border-color: #999999;
    }

    /* === COMBO BOXES === */
    QComboBox {
        background-color: #FFFFFF;
        color: #000000;
        border: 3px solid #0066CC;
        border-radius: 6px;
        padding: 6px;
        font-weight: bold;
        min-width: 120px;
    }

    QComboBox:hover {
        border-color: #FFFF00;
        background-color: #FFFFCC;
    }

    QComboBox::drop-down {
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 25px;
        border-left: 2px solid #0066CC;
        background-color: #0066CC;
    }

    QComboBox::down-arrow {
        width: 12px;
        height: 12px;
        background-color: #FFFFFF;
    }

    QComboBox QAbstractItemView {
        background-color: #FFFFFF;
        color: #000000;
        border: 2px solid #0066CC;
        selection-background-color: #0066CC;
        selection-color: #FFFFFF;
    }

    /* === SPIN BOXES === */
    QSpinBox, QDoubleSpinBox {
        background-color: #FFFFFF;
        color: #000000;
        border: 3px solid #0066CC;
        border-radius: 6px;
        padding: 6px;
        font-weight: bold;
    }

    QSpinBox:focus, QDoubleSpinBox:focus {
        border-color: #FFFF00;
        background-color: #FFFFCC;
    }

    /* === TABELAS === */
    QTableWidget {
        background-color: #FFFFFF;
        color: #000000;
        gridline-color: #000000;
        border: 3px solid #0066CC;
        selection-background-color: #0066CC;
        selection-color: #FFFFFF;
        font-weight: bold;
    }

    QTableWidget::item {
        padding: 8px;
        border-bottom: 1px solid #CCCCCC;
    }

    QTableWidget::item:selected {
        background-color: #0066CC;
        color: #FFFFFF;
    }

    QHeaderView::section {
        background-color: #000000;
        color: #FFFFFF;
        padding: 10px;
        border: 2px solid #FFFFFF;
        font-weight: bold;
        font-size: 10pt;
    }

    /* === TABS === */
    QTabWidget::pane {
        border: 3px solid #0066CC;
        background-color: #000000;
        top: -1px;
    }

    QTabBar::tab {
        background-color: #333333;
        color: #FFFFFF;
        border: 2px solid #0066CC;
        padding: 10px 20px;
        margin: 2px;
        font-weight: bold;
    }

    QTabBar::tab:selected {
        background-color: #0066CC;
        color: #FFFFFF;
        border-color: #FFFF00;
    }

    QTabBar::tab:hover {
        background-color: #0080FF;
        border-color: #FFFF00;
    }

    /* === MENUS === */
    QMenuBar {
        background-color: #000000;
        color: #FFFFFF;
        border-bottom: 2px solid #0066CC;
        font-weight: bold;
    }

    QMenuBar::item {
        background-color: transparent;
        padding: 8px 16px;
    }

    QMenuBar::item:selected {
        background-color: #0066CC;
        color: #FFFFFF;
    }

    QMenu {
        background-color: #FFFFFF;
        color: #000000;
        border: 3px solid #0066CC;
        font-weight: bold;
    }

    QMenu::item {
        padding: 8px 24px;
    }

    QMenu::item:selected {
        background-color: #0066CC;
        color: #FFFFFF;
    }

    /* === TOOLBAR === */
    QToolBar {
        background-color: #000000;
        border: 2px solid #0066CC;
        spacing: 4px;
        padding: 4px;
    }

    QToolButton {
        background-color: #0066CC;
        color: #FFFFFF;
        border: 2px solid #FFFFFF;
        border-radius: 6px;
        padding: 8px;
        font-weight: bold;
    }

    QToolButton:hover {
        background-color: #0080FF;
        border-color: #FFFF00;
    }

    /* === STATUS BAR === */
    QStatusBar {
        background-color: #000000;
        color: #FFFFFF;
        border-top: 2px solid #0066CC;
        font-weight: bold;
    }

    /* === LABELS === */
    QLabel {
        color: #FFFFFF;
        font-weight: bold;
    }

    QLabel[class="title"] {
        color: #FFFF00;
        font-size: 14pt;
        font-weight: bold;
    }

    QLabel[class="subtitle"] {
        color: #00DDDD;
        font-size: 12pt;
        font-weight: bold;
    }

    QLabel[class="warning"] {
        color: #FFFF00;
        background-color: #CC6600;
        border: 2px solid #FFFFFF;
        padding: 8px;
        border-radius: 6px;
        font-weight: bold;
    }

    QLabel[class="error"] {
        color: #FFFFFF;
        background-color: #CC0000;
        border: 2px solid #FFFFFF;
        padding: 8px;
        border-radius: 6px;
        font-weight: bold;
    }

    QLabel[class="success"] {
        color: #000000;
        background-color: #00AA00;
        border: 2px solid #FFFFFF;
        padding: 8px;
        border-radius: 6px;
        font-weight: bold;
    }

    /* === GROUP BOXES === */
    QGroupBox {
        font-weight: bold;
        border: 3px solid #0066CC;
        border-radius: 8px;
        margin-top: 12px;
        padding-top: 8px;
        color: #FFFFFF;
    }

    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 8px 0 8px;
        color: #FFFF00;
        font-weight: bold;
        font-size: 11pt;
    }

    /* === SCROLL BARS === */
    QScrollBar:vertical {
        background-color: #333333;
        width: 18px;
        border: 2px solid #0066CC;
        border-radius: 6px;
    }

    QScrollBar::handle:vertical {
        background-color: #0066CC;
        border: 2px solid #FFFFFF;
        border-radius: 6px;
        min-height: 30px;
    }

    QScrollBar::handle:vertical:hover {
        background-color: #0080FF;
    }

    QScrollBar:horizontal {
        background-color: #333333;
        height: 18px;
        border: 2px solid #0066CC;
        border-radius: 6px;
    }

    QScrollBar::handle:horizontal {
        background-color: #0066CC;
        border: 2px solid #FFFFFF;
        border-radius: 6px;
        min-width: 30px;
    }

    QScrollBar::handle:horizontal:hover {
        background-color: #0080FF;
    }

    /* === PROGRESS BARS === */
    QProgressBar {
        border: 3px solid #0066CC;
        border-radius: 6px;
        text-align: center;
        font-weight: bold;
        color: #000000;
        background-color: #FFFFFF;
    }

    QProgressBar::chunk {
        background-color: #00AA00;
        border-radius: 3px;
    }

    /* === CHECK BOXES === */
    QCheckBox {
        color: #FFFFFF;
        font-weight: bold;
        spacing: 8px;
    }

    QCheckBox::indicator {
        width: 18px;
        height: 18px;
        border: 3px solid #0066CC;
        border-radius: 4px;
        background-color: #FFFFFF;
    }

    QCheckBox::indicator:checked {
        background-color: #00AA00;
        border-color: #FFFFFF;
    }

    QCheckBox::indicator:hover {
        border-color: #FFFF00;
    }

    /* === RADIO BUTTONS === */
    QRadioButton {
        color: #FFFFFF;
        font-weight: bold;
        spacing: 8px;
    }

    QRadioButton::indicator {
        width: 18px;
        height: 18px;
        border: 3px solid #0066CC;
        border-radius: 12px;
        background-color: #FFFFFF;
    }

    QRadioButton::indicator:checked {
        background-color: #00AA00;
        border-color: #FFFFFF;
    }

    QRadioButton::indicator:hover {
        border-color: #FFFF00;
    }

    /* === DATE EDIT === */
    QDateEdit {
        background-color: #FFFFFF;
        color: #000000;
        border: 3px solid #0066CC;
        border-radius: 6px;
        padding: 6px;
        font-weight: bold;
    }

    QDateEdit:focus {
        border-color: #FFFF00;
        background-color: #FFFFCC;
    }

    QDateEdit::drop-down {
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 25px;
        border-left: 2px solid #0066CC;
        background-color: #0066CC;
    }

    QCalendarWidget {
        background-color: #FFFFFF;
        color: #000000;
        border: 3px solid #0066CC;
    }

    QCalendarWidget QToolButton {
        background-color: #0066CC;
        color: #FFFFFF;
        font-weight: bold;
    }

    QCalendarWidget QAbstractItemView:enabled {
        background-color: #FFFFFF;
        color: #000000;
        selection-background-color: #0066CC;
        selection-color: #FFFFFF;
    }

    /* === SPLITTER === */
    QSplitter::handle {
        background-color: #0066CC;
        border: 2px solid #FFFFFF;
    }

    QSplitter::handle:horizontal {
        width: 8px;
    }

    QSplitter::handle:vertical {
        height: 8px;
    }

    /* === CLASSES ESPECIAIS === */
    
    /* Cards de Dashboard */
    QFrame[class="dashboard-card"] {
        background-color: #1A1A1A;
        border: 3px solid #0066CC;
        border-radius: 10px;
        padding: 15px;
        margin: 5px;
    }

    /* Indicadores */
    QLabel[class="indicator-value"] {
        color: #00DD00;
        font-size: 24pt;
        font-weight: bold;
    }

    QLabel[class="indicator-label"] {
        color: #CCCCCC;
        font-size: 10pt;
        font-weight: bold;
    }

    /* Alertas críticos */
    QLabel[class="critical"] {
        color: #FFFFFF;
        background-color: #FF0000;
        border: 3px solid #FFFFFF;
        font-weight: bold;
        padding: 10px;
        border-radius: 8px;
    }

    /* === MESSAGE BOXES === */
    QMessageBox {
        background-color: #000000;
        color: #FFFFFF;
        font-weight: bold;
    }

    QMessageBox QPushButton {
        min-width: 80px;
        padding: 8px 16px;
    }
    """


def get_app_style():
    """Retorna o estilo principal da aplicação"""
    return get_high_contrast_style()


# Cores do sistema (para uso no código Python)
COLORS = {
    'background': '#000000',
    'text': '#FFFFFF',
    'primary': '#0066CC',
    'primary_hover': '#0080FF',
    'success': '#00AA00',
    'warning': '#FFFF00',
    'danger': '#CC0000',
    'info': '#00DDDD',
    'light': '#FFFFFF',
    'dark': '#333333',
    'border': '#0066CC',
    'focus': '#FFFF00',
    'entrada': (150, 255, 150),  # Verde claro para entradas
    'saida': (255, 150, 150),    # Rosa claro para saídas
    'critico': '#FF0000',        # Vermelho para crítico
    'alerta': '#FFAA00'          # Laranja para alerta
} 