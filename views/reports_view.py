"""
View de relatórios
"""

import customtkinter as ctk
from views.base_view import BaseView
from config import FONT_SIZES, COLORS

class ReportsView(BaseView):
    """View de relatórios do sistema"""
    
    def create_widgets(self):
        """Criar widgets da view de relatórios"""
        # Frame já criado na BaseView, não precisa recriar
        
        # Cabeçalho
        self.create_header("📈 Relatórios", "Análises e relatórios do sistema")
        
        # Cards de relatórios
        self.create_reports_cards()
    
    def create_reports_cards(self):
        """Criar cards de relatórios disponíveis"""
        reports_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        reports_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Lista de relatórios disponíveis
        reports_data = [
            ("📊 Relatório de Estoque", "Situação atual do estoque", self.generate_stock_report),
            ("📈 Relatório de Movimentações", "Histórico de entradas e saídas", self.generate_movements_report),
            ("💰 Relatório Financeiro", "Valores e custos dos produtos", self.generate_financial_report),
            ("🏢 Relatório de Fornecedores", "Análise de fornecedores", self.generate_suppliers_report),
            ("🏷️ Relatório por Categorias", "Produtos agrupados por categoria", self.generate_categories_report),
            ("⚠️ Produtos com Estoque Baixo", "Itens que precisam de reposição", self.generate_low_stock_report)
        ]
        
        # Criar cards em duas colunas usando pack
        for i, (title, description, command) in enumerate(reports_data):
            row_frame = ctk.CTkFrame(reports_frame, fg_color="transparent")
            row_frame.pack(fill="x", pady=5)
            
            report_card = self.create_report_card(row_frame, title, description, command)
            # Usar pack em vez de grid
            report_card.pack(side="left", fill="x", expand=True, padx=5)
    
    def create_report_card(self, parent, title, description, command):
        """Criar card de relatório"""
        card = ctk.CTkFrame(parent)
        
        # Título
        ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=FONT_SIZES["subheading"], weight="bold")
        ).pack(pady=(20, 5))
        
        # Descrição
        ctk.CTkLabel(
            card,
            text=description,
            font=ctk.CTkFont(size=FONT_SIZES["text"]),
            text_color="gray"
        ).pack(pady=(0, 10))
        
        # Botão
        ctk.CTkButton(
            card,
            text="Gerar Relatório",
            command=command,
            height=40
        ).pack(pady=(0, 20))
        
        return card
    
    def show_general_summary(self):
        """Mostrar resumo geral"""
        stats = self.manager.get_dashboard_stats()
        
        summary = f"""
RESUMO GERAL DO ESTOQUE

Total de Produtos: {stats['total_products']}
Valor Total: R$ {stats['total_value']:,.2f}
Produtos em Falta: {stats['low_stock_count']}
Movimentações Hoje: {stats['recent_movements']}

Produtos por Status:
- Normal: {stats['total_products'] - stats['low_stock_count']}
- Estoque Baixo: {stats['low_stock_count']}
"""
        
        self.show_report_dialog("Resumo Geral", summary)
    
    def show_low_stock(self):
        """Mostrar produtos com estoque baixo"""
        low_stock_products = self.manager.get_low_stock_products()
        
        if not low_stock_products:
            self.show_message("Não há produtos com estoque baixo!", "info")
            return
        
        report = "PRODUTOS COM ESTOQUE BAIXO\n\n"
        for product in low_stock_products:
            report += f"• {product['name']} ({product['code']}) - Qtd: {product['quantity']}\n"
        
        self.show_report_dialog("Estoque Baixo", report)
    
    def show_inventory_value(self):
        """Mostrar relatório de valor do estoque"""
        total_value = self.manager.get_total_inventory_value()
        products_by_value = sorted(
            self.manager.products,
            key=lambda p: p['price'] * p['quantity'],
            reverse=True
        )[:10]
        
        report = f"VALOR DO ESTOQUE\n\nValor Total: R$ {total_value:,.2f}\n\n"
        report += "TOP 10 PRODUTOS POR VALOR:\n"
        
        for product in products_by_value:
            value = product['price'] * product['quantity']
            report += f"• {product['name']} - R$ {value:,.2f}\n"
        
        self.show_report_dialog("Valor do Estoque", report)
    
    def show_movements_report(self):
        """Mostrar relatório de movimentações"""
        movements = self.manager.movements
        entradas = len([m for m in movements if m['type'] == 'entrada'])
        saidas = len([m for m in movements if m['type'] == 'saída'])
        
        report = f"""
RELATÓRIO DE MOVIMENTAÇÕES

Total de Movimentações: {len(movements)}
Entradas: {entradas}
Saídas: {saidas}

Últimas 10 Movimentações:
"""
        
        recent_movements = sorted(movements, key=lambda x: x['date'], reverse=True)[:10]
        for movement in recent_movements:
            product = self.manager.get_product(movement['product_code'])
            product_name = product['name'] if product else "Produto não encontrado"
            report += f"• {movement['type'].title()} - {product_name} (Qtd: {movement['quantity']})\n"
        
        self.show_report_dialog("Movimentações", report)
    
    def show_category_report(self):
        """Mostrar relatório por categoria"""
        categories_stats = {}
        
        for product in self.manager.products:
            category = product.get('category', 'Sem Categoria')
            if category not in categories_stats:
                categories_stats[category] = {'count': 0, 'value': 0}
            
            categories_stats[category]['count'] += 1
            categories_stats[category]['value'] += product['price'] * product['quantity']
        
        report = "RELATÓRIO POR CATEGORIA\n\n"
        for category, stats in categories_stats.items():
            report += f"• {category}: {stats['count']} produtos - R$ {stats['value']:,.2f}\n"
        
        self.show_report_dialog("Por Categoria", report)
    
    def show_supplier_report(self):
        """Mostrar relatório por fornecedor"""
        suppliers_stats = {}
        
        for product in self.manager.products:
            supplier = product.get('supplier', 'Sem Fornecedor')
            if supplier not in suppliers_stats:
                suppliers_stats[supplier] = {'count': 0, 'value': 0}
            
            suppliers_stats[supplier]['count'] += 1
            suppliers_stats[supplier]['value'] += product['price'] * product['quantity']
        
        report = "RELATÓRIO POR FORNECEDOR\n\n"
        for supplier, stats in suppliers_stats.items():
            report += f"• {supplier}: {stats['count']} produtos - R$ {stats['value']:,.2f}\n"
        
        self.show_report_dialog("Por Fornecedor", report)
    
    def show_report_dialog(self, title, content):
        """Mostrar diálogo com relatório"""
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title(f"Relatório - {title}")
        dialog.geometry("600x500")
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # Área de texto
        text_area = ctk.CTkTextbox(dialog, font=ctk.CTkFont(family="Courier", size=12))
        text_area.pack(fill="both", expand=True, padx=20, pady=20)
        text_area.insert("1.0", content)
        text_area.configure(state="disabled")
        
        # Botão fechar
        ctk.CTkButton(
            dialog,
            text="Fechar",
            command=dialog.destroy,
            width=120
        ).pack(pady=(0, 20))
    
    def refresh(self):
        """Atualizar dados da view"""
        pass  # Relatórios são gerados dinamicamente 

    def generate_stock_report(self):
        """Gerar relatório de estoque"""
        self.show_general_summary()

    def generate_movements_report(self):
        """Gerar relatório de movimentações"""
        self.show_movements_report()

    def generate_financial_report(self):
        """Gerar relatório financeiro"""
        self.show_inventory_value()

    def generate_suppliers_report(self):
        """Gerar relatório de fornecedores"""
        self.show_supplier_report()

    def generate_categories_report(self):
        """Gerar relatório por categorias"""
        self.show_category_report()

    def generate_low_stock_report(self):
        """Gerar relatório de estoque baixo"""
        self.show_low_stock() 