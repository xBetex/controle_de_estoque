"""
View do Dashboard do sistema
"""

import customtkinter as ctk
from datetime import datetime
from views.base_view import BaseView
from config import FONT_SIZES, COLORS

class DashboardView(BaseView):
    """View do dashboard principal"""
    
    def create_widgets(self):
        """Criar widgets do dashboard"""
        # Frame já criado na BaseView, não precisa recriar
        
        # Cabeçalho
        self.create_header("🏠 Dashboard", "Visão geral do sistema")
        
        # Cards de estatísticas
        self.create_stats_section()
        
        # Gráficos e resumos
        self.create_charts_section()
    
    def create_stats_section(self):
        """Criar seção de estatísticas"""
        stats_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        stats_frame.pack(fill="x", padx=20, pady=10)
        
        # Obter estatísticas
        stats = self.get_dashboard_stats()
        
        # Cards de estatísticas
        cards_data = [
            ("📦", "Total Produtos", str(stats['total_products']), "primary"),
            ("📋", "Categorias", str(stats['total_categories']), "secondary"),
            ("🏢", "Fornecedores", str(stats['total_suppliers']), "success"),
            ("⚠️", "Estoque Baixo", str(stats['low_stock']), "warning"),
            ("❌", "Sem Estoque", str(stats['no_stock']), "error")
        ]
        
        for i, (icon, title, value, color) in enumerate(cards_data):
            card = self.create_stat_card(stats_frame, title, value, icon, color)
            card.pack(side="left", fill="x", expand=True, padx=5, pady=10)
    
    def create_activities_section(self):
        """Criar seção de atividades recentes"""
        activities_frame = ctk.CTkFrame(self.frame)
        activities_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Título
        activities_title = ctk.CTkLabel(
            activities_frame,
            text="📋 Atividades Recentes",
            font=ctk.CTkFont(size=FONT_SIZES["subheading"], weight="bold")
        )
        activities_title.pack(pady=(20, 10))
        
        # Lista de atividades
        self.activities_list = ctk.CTkTextbox(
            activities_frame, 
            height=300, 
            font=ctk.CTkFont(size=FONT_SIZES["text"])
        )
        self.activities_list.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Carregar atividades
        self.load_recent_activities()
    
    def calculate_stats(self):
        """Calcular estatísticas para o dashboard"""
        total_products = len(self.manager.products)
        total_value = self.manager.get_total_inventory_value()
        low_stock_count = len(self.manager.get_low_stock_products())
        
        # Movimentações de hoje
        today = datetime.now().date()
        recent_movements = len([
            m for m in self.manager.movements 
            if datetime.fromisoformat(m['date']).date() == today
        ])
        
        return {
            'total_products': total_products,
            'total_value': total_value,
            'low_stock_count': low_stock_count,
            'recent_movements': recent_movements
        }
    
    def load_recent_activities(self):
        """Carregar atividades recentes"""
        # Limpar lista
        self.activities_list.delete("1.0", "end")
        
        # Obter movimentações recentes
        recent_movements = sorted(
            self.manager.movements, 
            key=lambda x: x['date'], 
            reverse=True
        )[:10]
        
        if not recent_movements:
            self.activities_list.insert("1.0", "Nenhuma atividade recente encontrada.")
            return
        
        # Adicionar movimentações à lista
        for movement in recent_movements:
            date = datetime.fromisoformat(movement['date'])
            product = self.manager.get_product(movement['product_code'])
            product_name = product['name'] if product else "Produto não encontrado"
            
            activity_text = f"[{date.strftime('%d/%m/%Y %H:%M')}] "
            activity_text += f"{movement['type'].upper()} - "
            activity_text += f"{product_name} (Qtd: {movement['quantity']})"
            
            if movement.get('reason'):
                activity_text += f" - {movement['reason']}"
            
            activity_text += "\n"
            
            self.activities_list.insert("end", activity_text)
    
    def refresh(self):
        """Atualizar dados do dashboard"""
        if hasattr(self, 'activities_list'):
            self.load_recent_activities()
        
        # Atualizar estatísticas se necessário
        # As estatísticas serão atualizadas na próxima visualização 

    def get_dashboard_stats(self):
        """Obter estatísticas para o dashboard"""
        try:
            total_products = len(self.manager.products)
            total_categories = len(self.manager.categories)
            total_suppliers = len(self.manager.suppliers)
            
            # Calcular produtos com estoque baixo e sem estoque
            low_stock = 0
            no_stock = 0
            
            for product in self.manager.products:
                quantity = product.get('quantity', 0)
                min_stock = product.get('min_stock', 0)
                
                if quantity == 0:
                    no_stock += 1
                elif quantity <= min_stock:
                    low_stock += 1
            
            return {
                'total_products': total_products,
                'total_categories': total_categories,
                'total_suppliers': total_suppliers,
                'low_stock': low_stock,
                'no_stock': no_stock
            }
        except Exception as e:
            # Retornar valores padrão em caso de erro
            return {
                'total_products': 0,
                'total_categories': 0,
                'total_suppliers': 0,
                'low_stock': 0,
                'no_stock': 0
            }

    def create_charts_section(self):
        """Criar seção de gráficos e resumos"""
        charts_frame = ctk.CTkFrame(self.frame)
        charts_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Título da seção
        ctk.CTkLabel(
            charts_frame,
            text="📊 Resumo Detalhado",
            font=ctk.CTkFont(size=FONT_SIZES["subheading"], weight="bold")
        ).pack(pady=20)
        
        # Informações adicionais
        info_text = """
        • Use o menu lateral para navegar entre as diferentes seções
        • Produtos: Gerencie seu catálogo de produtos
        • Estoque: Controle quantidades e movimentações
        • Relatórios: Analise dados e gere relatórios
        """
        
        ctk.CTkLabel(
            charts_frame,
            text=info_text,
            font=ctk.CTkFont(size=FONT_SIZES["text"]),
            justify="left"
        ).pack(pady=10) 