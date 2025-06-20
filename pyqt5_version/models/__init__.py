"""
Models module for PyQt5 Inventory Management System
"""

from datetime import datetime
from typing import List, Dict, Optional
from PyQt5.QtCore import QObject, pyqtSignal

from config import *
from utils import load_json_data, save_json_data, create_directory

class InventoryManager(QObject):
    """Main inventory manager with PyQt5 signals"""
    
    # Signals for data changes
    product_added = pyqtSignal(dict)
    product_updated = pyqtSignal(str, dict)
    product_deleted = pyqtSignal(str)
    
    stock_updated = pyqtSignal(str, int)
    movement_added = pyqtSignal(dict)
    
    supplier_added = pyqtSignal(dict)
    supplier_updated = pyqtSignal(int, dict)
    supplier_deleted = pyqtSignal(int)
    
    category_added = pyqtSignal(dict)
    category_updated = pyqtSignal(int, dict)
    category_deleted = pyqtSignal(int)
    
    settings_updated = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.create_data_directories()
        self.load_all_data()
    
    def create_data_directories(self):
        """Create necessary directories if they don't exist"""
        for directory in [DATA_DIR, LOGS_DIR, BACKUPS_DIR, ASSETS_DIR, EXPORTS_DIR]:
            create_directory(directory)
    
    def load_all_data(self):
        """Load all data from files"""
        self.products = load_json_data(PRODUCTS_FILE, [])
        self.movements = load_json_data(MOVEMENTS_FILE, [])
        self.suppliers = load_json_data(SUPPLIERS_FILE, [])
        self.categories = load_json_data(CATEGORIES_FILE, [])
        self.settings = load_json_data(SETTINGS_FILE, DEFAULT_SETTINGS)
    
    # PRODUCT MANAGEMENT
    def add_product(self, product_data: Dict) -> bool:
        """Add a new product"""
        # Check if product code already exists
        if any(p['code'] == product_data['code'] for p in self.products):
            return False
        
        # Add metadata
        product_data['created_at'] = datetime.now().isoformat()
        product_data['updated_at'] = datetime.now().isoformat()
        
        # Ensure required fields have default values
        product_data.setdefault('description', '')
        product_data.setdefault('category', '')
        product_data.setdefault('supplier', '')
        product_data.setdefault('min_stock', 0)
        product_data.setdefault('location', '')
        
        self.products.append(product_data)
        
        # Record initial stock movement
        if product_data.get('quantity', 0) > 0:
            self.add_movement("entrada", product_data['code'], 
                             product_data['quantity'], "Cadastro inicial")
        
        # Save and emit signal
        success = save_json_data(self.products, PRODUCTS_FILE)
        if success:
            self.product_added.emit(product_data)
        
        return success
    
    def update_product(self, code: str, updates: Dict) -> bool:
        """Update an existing product"""
        product = self.get_product(code)
        if not product:
            return False
        
        # Store old quantity for stock movement tracking
        old_quantity = product.get('quantity', 0)
        
        # Update product data
        product.update(updates)
        product['updated_at'] = datetime.now().isoformat()
        
        # Check if quantity changed and record movement
        new_quantity = product.get('quantity', 0)
        if new_quantity != old_quantity:
            quantity_change = new_quantity - old_quantity
            movement_type = "entrada" if quantity_change > 0 else "saída"
            self.add_movement(movement_type, code, abs(quantity_change), 
                             "Ajuste de estoque via edição")
        
        # Save and emit signal
        success = save_json_data(self.products, PRODUCTS_FILE)
        if success:
            self.product_updated.emit(code, product)
        
        return success
    
    def delete_product(self, code: str) -> bool:
        """Delete a product"""
        # Check if product exists
        product = self.get_product(code)
        if not product:
            return False
        
        # Remove product
        self.products = [p for p in self.products if p['code'] != code]
        
        # Save and emit signal
        success = save_json_data(self.products, PRODUCTS_FILE)
        if success:
            self.product_deleted.emit(code)
        
        return success
    
    def get_product(self, code: str) -> Optional[Dict]:
        """Get product by code"""
        return next((p for p in self.products if p['code'] == code), None)
    
    def get_all_products(self) -> List[Dict]:
        """Get all products"""
        return self.products.copy()
    
    def search_products(self, query: str) -> List[Dict]:
        """Search products by name, code, or description"""
        if not query:
            return self.products.copy()
        
        query = query.lower()
        return [p for p in self.products if query in p['name'].lower() or 
                query in p['code'].lower() or 
                query in p.get('description', '').lower()]
    
    def get_products_by_supplier(self, supplier_query: str) -> List[Dict]:
        """Get products filtered by supplier name or code"""
        if not supplier_query or supplier_query.strip() == "":
            return self.products.copy()
        
        query = supplier_query.lower().strip()
        filtered_products = []
        
        for product in self.products:
            supplier_name = product.get('supplier', '').lower()
            supplier_code = str(product.get('supplier_code', '')).lower()
            
            # Check if query matches supplier name or code
            if (query in supplier_name or 
                query in supplier_code or 
                supplier_name == query or 
                supplier_code == query):
                filtered_products.append(product)
        
        return filtered_products
    
    def get_low_stock_products(self) -> List[Dict]:
        """Get products with low stock"""
        threshold = self.settings.get('low_stock_threshold', 5)
        return [p for p in self.products if p.get('quantity', 0) <= threshold]
    
    def get_total_inventory_value(self) -> float:
        """Calculate total inventory value"""
        return sum(p.get('price', 0) * p.get('quantity', 0) for p in self.products)
    
    def get_total_items_count(self) -> int:
        """Get total count of items in inventory"""
        return sum(p.get('quantity', 0) for p in self.products)
    
    # MOVEMENT MANAGEMENT
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
            'user': "admin"
        }
        
        self.movements.append(movement)
        
        # Save and emit signal
        success = save_json_data(self.movements, MOVEMENTS_FILE)
        if success:
            self.movement_added.emit(movement)
        
        return success
    
    def get_all_movements(self) -> List[Dict]:
        """Get all movements"""
        return sorted(self.movements, key=lambda x: x['date'], reverse=True)
    
    # SUPPLIER MANAGEMENT
    def add_supplier(self, supplier_data: Dict) -> bool:
        """Add new supplier"""
        # Check if supplier with same name already exists
        if any(s['name'].lower() == supplier_data['name'].lower() for s in self.suppliers):
            return False
        
        # Add metadata
        supplier_data['id'] = len(self.suppliers) + 1
        supplier_data['created_at'] = datetime.now().isoformat()
        supplier_data['updated_at'] = datetime.now().isoformat()
        
        self.suppliers.append(supplier_data)
        
        # Save and emit signal
        success = save_json_data(self.suppliers, SUPPLIERS_FILE)
        if success:
            self.supplier_added.emit(supplier_data)
        
        return success
    
    def get_all_suppliers(self) -> List[Dict]:
        """Get all suppliers"""
        return self.suppliers.copy()
    
    # CATEGORY MANAGEMENT
    def add_category(self, category_data: Dict) -> bool:
        """Add new category"""
        # Check if category with same name already exists
        if any(c['name'].lower() == category_data['name'].lower() for c in self.categories):
            return False
        
        # Add metadata
        category_data['id'] = len(self.categories) + 1
        category_data['created_at'] = datetime.now().isoformat()
        category_data['updated_at'] = datetime.now().isoformat()
        
        self.categories.append(category_data)
        
        # Save and emit signal
        success = save_json_data(self.categories, CATEGORIES_FILE)
        if success:
            self.category_added.emit(category_data)
        
        return success
    
    def get_all_categories(self) -> List[Dict]:
        """Get all categories"""
        return self.categories.copy()
    
    # SETTINGS MANAGEMENT
    def update_settings(self, new_settings: Dict) -> bool:
        """Update application settings"""
        self.settings.update(new_settings)
        
        # Save and emit signal
        success = save_json_data(self.settings, SETTINGS_FILE)
        if success:
            self.settings_updated.emit(self.settings)
        
        return success
    
    def get_setting(self, key: str, default=None):
        """Get a specific setting value"""
        return self.settings.get(key, default)
    
    def get_all_settings(self) -> Dict:
        """Get all settings"""
        return self.settings.copy()
    
    # DASHBOARD STATISTICS
    def get_dashboard_stats(self) -> Dict:
        """Get dashboard statistics"""
        total_products = len(self.products)
        total_items = self.get_total_items_count()
        total_value = self.get_total_inventory_value()
        low_stock_count = len(self.get_low_stock_products())
        
        return {
            'total_products': total_products,
            'total_items': total_items,
            'total_value': total_value,
            'low_stock_count': low_stock_count,
            'total_suppliers': len(self.suppliers),
            'total_categories': len(self.categories)
        } 