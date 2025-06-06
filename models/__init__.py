"""
Módulo de modelos para o Sistema de Controle de Estoque
"""

from datetime import datetime
from typing import List, Dict, Optional
from config import *
from utils import load_json_data, save_json_data, create_directory

class InventoryManager:
    """Gerenciador principal do estoque"""
    
    def __init__(self):
        self.create_data_directories()
        self.products = load_json_data(PRODUCTS_FILE, [])
        self.movements = load_json_data(MOVEMENTS_FILE, [])
        self.suppliers = load_json_data(SUPPLIERS_FILE, [])
        self.categories = load_json_data(CATEGORIES_FILE, [])
        self.settings = load_json_data(SETTINGS_FILE, DEFAULT_SETTINGS)
    
    def create_data_directories(self):
        """Cria diretórios necessários se não existirem"""
        for directory in [DATA_DIR, LOGS_DIR, BACKUPS_DIR, ASSETS_DIR]:
            create_directory(directory)
    
    # PRODUTOS
    def add_product(self, product_data: Dict) -> bool:
        """Adiciona um novo produto"""
        # Verifica se o código já existe
        if any(p['code'] == product_data['code'] for p in self.products):
            return False
            
        product_data['created_at'] = datetime.now().isoformat()
        product_data['updated_at'] = datetime.now().isoformat()
        self.products.append(product_data)
        
        # Registra movimento inicial
        self.add_movement("entrada", product_data['code'], 
                         product_data['quantity'], "Cadastro inicial")
        
        return save_json_data(self.products, PRODUCTS_FILE)
    
    def update_product(self, code: str, updates: Dict) -> bool:
        """Atualiza um produto existente"""
        product = self.get_product(code)
        if not product:
            return False
        
        product.update(updates)
        product['updated_at'] = datetime.now().isoformat()
        return save_json_data(self.products, PRODUCTS_FILE)
    
    def delete_product(self, code: str) -> bool:
        """Remove um produto"""
        self.products = [p for p in self.products if p['code'] != code]
        return save_json_data(self.products, PRODUCTS_FILE)
    
    def get_product(self, code: str) -> Optional[Dict]:
        """Busca produto por código"""
        return next((p for p in self.products if p['code'] == code), None)
    
    def search_products(self, query: str) -> List[Dict]:
        """Busca produtos por nome, código ou descrição"""
        query = query.lower()
        return [p for p in self.products if 
                query in p['name'].lower() or 
                query in p['code'].lower() or 
                query in p.get('description', '').lower()]
    
    def get_products_by_category(self, category: str) -> List[Dict]:
        """Busca produtos por categoria"""
        return [p for p in self.products if p.get('category', '').lower() == category.lower()]
    
    def get_products_by_supplier(self, supplier: str) -> List[Dict]:
        """Busca produtos por fornecedor"""
        return [p for p in self.products if p.get('supplier', '').lower() == supplier.lower()]
    
    # ESTOQUE
    def update_stock(self, code: str, quantity_change: int, reason: str = "") -> bool:
        """Atualiza estoque de um produto"""
        product = self.get_product(code)
        if not product:
            return False
        
        new_quantity = product['quantity'] + quantity_change
        if new_quantity < 0:
            return False
        
        product['quantity'] = new_quantity
        product['updated_at'] = datetime.now().isoformat()
        
        # Registra movimento
        movement_type = "entrada" if quantity_change > 0 else "saída"
        self.add_movement(movement_type, code, abs(quantity_change), reason)
        
        return save_json_data(self.products, PRODUCTS_FILE)
    
    def get_low_stock_products(self) -> List[Dict]:
        """Busca produtos com estoque baixo"""
        threshold = self.settings.get('low_stock_threshold', 5)
        return [p for p in self.products if p['quantity'] <= threshold]
    
    def get_out_of_stock_products(self) -> List[Dict]:
        """Busca produtos sem estoque"""
        return [p for p in self.products if p['quantity'] == 0]
    
    def get_total_inventory_value(self) -> float:
        """Calcula valor total do estoque"""
        return sum(p['price'] * p['quantity'] for p in self.products)
    
    def get_total_items_count(self) -> int:
        """Conta total de itens em estoque"""
        return sum(p['quantity'] for p in self.products)
    
    # MOVIMENTAÇÕES
    def add_movement(self, movement_type: str, product_code: str, 
                    quantity: int, reason: str = "") -> bool:
        """Adiciona registro de movimentação"""
        movement = {
            'id': len(self.movements) + 1,
            'date': datetime.now().isoformat(),
            'type': movement_type,
            'product_code': product_code,
            'quantity': quantity,
            'reason': reason,
            'user': "admin"  # Implementar sistema de usuários futuramente
        }
        
        self.movements.append(movement)
        return save_json_data(self.movements, MOVEMENTS_FILE)
    
    def get_movements_by_date_range(self, start_date: str, end_date: str) -> List[Dict]:
        """Busca movimentações por período"""
        movements = []
        for movement in self.movements:
            movement_date = movement['date'][:10]  # Pega apenas a data (YYYY-MM-DD)
            if start_date <= movement_date <= end_date:
                movements.append(movement)
        return movements
    
    def get_movements_by_type(self, movement_type: str) -> List[Dict]:
        """Busca movimentações por tipo"""
        return [m for m in self.movements if m['type'] == movement_type]
    
    def get_movements_by_product(self, product_code: str) -> List[Dict]:
        """Busca movimentações de um produto específico"""
        return [m for m in self.movements if m['product_code'] == product_code]
    
    # FORNECEDORES
    def add_supplier(self, supplier_data: Dict) -> bool:
        """Adiciona novo fornecedor"""
        # Verifica se já existe fornecedor com mesmo nome
        if any(s['name'].lower() == supplier_data['name'].lower() for s in self.suppliers):
            return False
            
        supplier_data['id'] = len(self.suppliers) + 1
        supplier_data['created_at'] = datetime.now().isoformat()
        supplier_data['updated_at'] = datetime.now().isoformat()
        self.suppliers.append(supplier_data)
        
        return save_json_data(self.suppliers, SUPPLIERS_FILE)
    
    def update_supplier(self, supplier_id: int, updates: Dict) -> bool:
        """Atualiza fornecedor existente"""
        supplier = self.get_supplier_by_id(supplier_id)
        if not supplier:
            return False
        
        supplier.update(updates)
        supplier['updated_at'] = datetime.now().isoformat()
        return save_json_data(self.suppliers, SUPPLIERS_FILE)
    
    def delete_supplier(self, supplier_id: int) -> bool:
        """Remove fornecedor"""
        self.suppliers = [s for s in self.suppliers if s.get('id') != supplier_id]
        return save_json_data(self.suppliers, SUPPLIERS_FILE)
    
    def get_supplier_by_id(self, supplier_id: int) -> Optional[Dict]:
        """Busca fornecedor por ID"""
        return next((s for s in self.suppliers if s.get('id') == supplier_id), None)
    
    def get_supplier_by_name(self, name: str) -> Optional[Dict]:
        """Busca fornecedor por nome"""
        return next((s for s in self.suppliers if s['name'].lower() == name.lower()), None)
    
    def search_suppliers(self, query: str) -> List[Dict]:
        """Busca fornecedores por nome, email ou telefone"""
        query = query.lower()
        return [s for s in self.suppliers if 
                query in s['name'].lower() or 
                query in s.get('email', '').lower() or 
                query in s.get('phone', '').lower()]
    
    # CATEGORIAS
    def add_category(self, category_data: Dict) -> bool:
        """Adiciona nova categoria"""
        # Verifica se já existe categoria com mesmo nome
        if any(c['name'].lower() == category_data['name'].lower() for c in self.categories):
            return False
            
        category_data['id'] = len(self.categories) + 1
        category_data['created_at'] = datetime.now().isoformat()
        category_data['updated_at'] = datetime.now().isoformat()
        self.categories.append(category_data)
        
        return save_json_data(self.categories, CATEGORIES_FILE)
    
    def update_category(self, category_id: int, updates: Dict) -> bool:
        """Atualiza categoria existente"""
        category = self.get_category_by_id(category_id)
        if not category:
            return False
        
        category.update(updates)
        category['updated_at'] = datetime.now().isoformat()
        return save_json_data(self.categories, CATEGORIES_FILE)
    
    def delete_category(self, category_id: int) -> bool:
        """Remove categoria"""
        self.categories = [c for c in self.categories if c.get('id') != category_id]
        return save_json_data(self.categories, CATEGORIES_FILE)
    
    def get_category_by_id(self, category_id: int) -> Optional[Dict]:
        """Busca categoria por ID"""
        return next((c for c in self.categories if c.get('id') == category_id), None)
    
    def get_category_by_name(self, name: str) -> Optional[Dict]:
        """Busca categoria por nome"""
        return next((c for c in self.categories if c['name'].lower() == name.lower()), None)
    
    # CONFIGURAÇÕES
    def update_settings(self, new_settings: Dict) -> bool:
        """Atualiza configurações"""
        self.settings.update(new_settings)
        return save_json_data(self.settings, SETTINGS_FILE)
    
    def get_setting(self, key: str, default=None):
        """Busca configuração específica"""
        return self.settings.get(key, default)
    
    # RELATÓRIOS E ESTATÍSTICAS
    def get_dashboard_stats(self) -> Dict:
        """Obtém estatísticas para o dashboard"""
        return {
            'total_products': len(self.products),
            'total_items': self.get_total_items_count(),
            'total_value': self.get_total_inventory_value(),
            'low_stock_count': len(self.get_low_stock_products()),
            'out_of_stock_count': len(self.get_out_of_stock_products()),
            'total_suppliers': len(self.suppliers),
            'total_categories': len(self.categories),
            'recent_movements': self.movements[-10:] if self.movements else []
        }
    
    def get_inventory_summary(self) -> Dict:
        """Obtém resumo do inventário"""
        return {
            'by_category': self._group_products_by_category(),
            'by_supplier': self._group_products_by_supplier(),
            'stock_levels': self._group_products_by_stock_level()
        }
    
    def _group_products_by_category(self) -> Dict:
        """Agrupa produtos por categoria"""
        result = {}
        for product in self.products:
            category = product.get('category', 'Sem categoria')
            if category not in result:
                result[category] = {'count': 0, 'value': 0}
            result[category]['count'] += product['quantity']
            result[category]['value'] += product['price'] * product['quantity']
        return result
    
    def _group_products_by_supplier(self) -> Dict:
        """Agrupa produtos por fornecedor"""
        result = {}
        for product in self.products:
            supplier = product.get('supplier', 'Sem fornecedor')
            if supplier not in result:
                result[supplier] = {'count': 0, 'value': 0}
            result[supplier]['count'] += product['quantity']
            result[supplier]['value'] += product['price'] * product['quantity']
        return result
    
    def _group_products_by_stock_level(self) -> Dict:
        """Agrupa produtos por nível de estoque"""
        threshold = self.settings.get('low_stock_threshold', 5)
        result = {
            'sem_estoque': 0,
            'estoque_baixo': 0,
            'estoque_normal': 0
        }
        
        for product in self.products:
            qty = product['quantity']
            if qty == 0:
                result['sem_estoque'] += 1
            elif qty <= threshold:
                result['estoque_baixo'] += 1
            else:
                result['estoque_normal'] += 1
        
        return result 