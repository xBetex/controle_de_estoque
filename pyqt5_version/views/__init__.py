"""
Views module for PyQt5 Inventory Management System
"""

from .main_window import MainWindow
from .dashboard_view import DashboardView
from .products_view import ProductsView
from .inventory_view import InventoryView
from .movements_view import MovementsView
from .suppliers_view import SuppliersView
from .categories_view import CategoriesView
from .reports_view import ReportsView
from .settings_view import SettingsView

__all__ = [
    'MainWindow',
    'DashboardView',
    'ProductsView',
    'InventoryView',
    'MovementsView',
    'SuppliersView',
    'CategoriesView',
    'ReportsView',
    'SettingsView'
] 