"""
View de movimentações de estoque
"""

import customtkinter as ctk
from tkinter import ttk
from datetime import datetime
from views.base_view import BaseView
from config import FONT_SIZES, COLORS

class MovementsView(BaseView):
    """View de movimentações de estoque"""
    
    def __init__(self, parent, manager):
        super().__init__(parent, manager)
        self.movements_tree = None
        self.filter_type_var = None
    
    def create_widgets(self):
        """Criar widgets da view de movimentações"""
        # Frame já criado na BaseView, não precisa recriar
        
        # Cabeçalho
        self.create_header("📊 Movimentações de Estoque", "Histórico de entradas e saídas")
        
        # Filtros
        self.create_filters_section()
        
        # Tabela de movimentações
        self.create_movements_table()
        
        # Carregar dados
        self.load_movements_data()
    
    def create_filters_section(self):
        """Criar seção de filtros"""
        filters_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        filters_frame.pack(fill="x", padx=20, pady=10)
        
        # Linha superior de filtros
        top_filters = ctk.CTkFrame(filters_frame, fg_color="transparent")
        top_filters.pack(fill="x", pady=(0, 10))
        
        # Filtro por tipo
        ctk.CTkLabel(
            top_filters, 
            text="Tipo:", 
            font=ctk.CTkFont(size=FONT_SIZES["label"])
        ).pack(side="left", padx=(0, 5))
        
        self.filter_type_var = ctk.StringVar(value="Todos")
        type_menu = ctk.CTkOptionMenu(
            top_filters,
            variable=self.filter_type_var,
            values=["Todos", "Entrada", "Saída"],
            width=120
        )
        type_menu.pack(side="left", padx=(0, 20))
        
        # Linha inferior de filtros (data)
        bottom_filters = ctk.CTkFrame(filters_frame, fg_color="transparent")
        bottom_filters.pack(fill="x")
        
        # Filtro por período
        ctk.CTkLabel(
            bottom_filters, 
            text="Período:", 
            font=ctk.CTkFont(size=FONT_SIZES["label"])
        ).pack(side="left", padx=(0, 5))
        
        self.filter_period_var = ctk.StringVar(value="Todos")
        period_menu = ctk.CTkOptionMenu(
            bottom_filters,
            variable=self.filter_period_var,
            values=["Todos", "Hoje", "Última Semana", "Último Mês", "Último Ano"],
            width=150
        )
        period_menu.pack(side="left", padx=(0, 10))
        
        # Botão aplicar filtros
        filter_btn = self.create_action_button(
            bottom_filters, "Aplicar Filtros", self.apply_filters,
            color="primary", icon="🔍"
        )
        filter_btn.pack(side="left", padx=(0, 10))
        
        # Botão limpar filtros
        clear_btn = self.create_action_button(
            bottom_filters, "Limpar", self.clear_filters,
            color="secondary", icon="🗑️"
        )
        clear_btn.pack(side="left", padx=(0, 20))
        
        # Estatísticas
        self.create_movements_summary(bottom_filters)
    
    def create_movements_summary(self, parent):
        """Criar resumo das movimentações"""
        summary_frame = ctk.CTkFrame(parent)
        summary_frame.pack(side="right", padx=(20, 0))
        
        stats = self.calculate_movements_stats()
        
        summary_text = f"Total: {stats['total']} | Entradas: {stats['entradas']} | Saídas: {stats['saidas']}"
        
        ctk.CTkLabel(
            summary_frame,
            text=summary_text,
            font=ctk.CTkFont(size=FONT_SIZES["text"]),
            fg_color="transparent"
        ).pack(padx=10, pady=5)
    
    def create_movements_table(self):
        """Criar tabela de movimentações"""
        table_frame = ctk.CTkFrame(self.frame)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Colunas
        columns = ('date', 'type', 'product_name', 'product_code', 'quantity', 'reason')
        
        # Treeview
        self.movements_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Cabeçalhos
        headers = {
            'date': 'Data/Hora',
            'type': 'Tipo',
            'product_name': 'Produto',
            'product_code': 'Código',
            'quantity': 'Quantidade',
            'reason': 'Motivo'
        }
        
        for col, header in headers.items():
            self.movements_tree.heading(col, text=header, anchor='w')
            if col in ['quantity']:
                self.movements_tree.column(col, anchor='center', width=80)
            elif col in ['type']:
                self.movements_tree.column(col, anchor='center', width=80)
            elif col in ['date']:
                self.movements_tree.column(col, anchor='w', width=140)
            else:
                self.movements_tree.column(col, anchor='w', width=120)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.movements_tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=self.movements_tree.xview)
        self.movements_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack em vez de grid
        self.movements_tree.pack(side="left", fill="both", expand=True)
        v_scrollbar.pack(side="right", fill="y")
        
        # Frame para scrollbar horizontal
        h_frame = ctk.CTkFrame(table_frame, fg_color="transparent")
        h_frame.pack(side="bottom", fill="x")
        h_scrollbar = ttk.Scrollbar(h_frame, orient="horizontal", command=self.movements_tree.xview)
        h_scrollbar.pack(fill="x")
        self.movements_tree.configure(xscrollcommand=h_scrollbar.set)
    
    def load_movements_data(self, filter_type=None, filter_period=None):
        """Carregar dados das movimentações (melhorado)"""
        # Limpar tabela
        for item in self.movements_tree.get_children():
            self.movements_tree.delete(item)
        
        try:
            # Verificar se há movimentações
            if not hasattr(self.manager, 'movements') or not self.manager.movements:
                print("Nenhuma movimentação encontrada")
                # Adicionar linha indicando que não há dados
                self.movements_tree.insert('', 'end', values=(
                    "---", "---", "Nenhuma movimentação encontrada", "---", "---", "---"
                ))
                return
            
            # Filtrar movimentações
            movements = self.manager.movements.copy()
            print(f"Total de movimentações: {len(movements)}")
            
            # Filtrar por período primeiro
            if filter_period and filter_period != "Todos":
                movements = self.filter_movements_by_period(movements, filter_period)
                print(f"Movimentações após filtro por período '{filter_period}': {len(movements)}")
            
            # Filtrar por tipo
            if filter_type and filter_type != "Todos":
                # Filtrar por tipo, considerando variações
                filter_lower = filter_type.lower()
                if filter_lower == "entrada":
                    movements = [m for m in movements if m.get('type', '').lower() in ['entrada', 'in', 'input']]
                elif filter_lower == "saída":
                    movements = [m for m in movements if m.get('type', '').lower() in ['saída', 'saida', 'out', 'output']]
                
                print(f"Movimentações após filtro por tipo '{filter_type}': {len(movements)}")
            
            # Ordenar por data (mais recentes primeiro)
            movements = sorted(movements, key=lambda x: x.get('date', ''), reverse=True)
            
            # Adicionar movimentações à tabela
            for movement in movements:
                # Obter dados do produto
                product_code = movement.get('product_code', '')
                product = self.manager.get_product(product_code) if product_code else None
                product_name = product.get('name', 'Produto não encontrado') if product else "Produto não encontrado"
                
                # Formatar data
                date_str = movement.get('date', '')
                try:
                    if date_str:
                        date_obj = datetime.fromisoformat(date_str)
                        formatted_date = date_obj.strftime('%d/%m/%Y %H:%M')
                    else:
                        formatted_date = "Data não informada"
                except:
                    formatted_date = str(date_str)
                
                # Determinar cor por tipo
                movement_type = movement.get('type', '').lower()
                tag = movement_type
                
                # Inserir na tabela
                self.movements_tree.insert('', 'end', values=(
                    formatted_date,
                    movement.get('type', '').title(),
                    product_name,
                    product_code,
                    movement.get('quantity', 0),
                    movement.get('reason', '')
                ), tags=(tag,))
            
            # Configurar cores por tag
            self.movements_tree.tag_configure('entrada', background='#e8f5e8')
            self.movements_tree.tag_configure('saída', background='#ffebee')
            self.movements_tree.tag_configure('saida', background='#ffebee')  # Variação sem acento
            
        except Exception as e:
            print(f"Erro ao carregar movimentações: {e}")
            self.show_message(f"Erro ao carregar movimentações: {e}", "error")
    
    def apply_filters(self):
        """Aplicar todos os filtros selecionados"""
        try:
            filter_type = self.filter_type_var.get()
            filter_period = self.filter_period_var.get()
            self.load_movements_data(filter_type, filter_period)
        except Exception as e:
            print(f"Erro ao aplicar filtros: {e}")
            self.show_message(f"Erro ao aplicar filtros: {e}", "error")
    
    def clear_filters(self):
        """Limpar todos os filtros"""
        self.filter_type_var.set("Todos")
        self.filter_period_var.set("Todos")
        self.load_movements_data()
    
    def filter_movements_by_period(self, movements, period):
        """Filtrar movimentações por período"""
        if period == "Todos":
            return movements
        
        from datetime import datetime, timedelta
        
        now = datetime.now()
        filtered = []
        
        for movement in movements:
            try:
                date_str = movement.get('date', '')
                if not date_str:
                    continue
                    
                # Parse da data
                movement_date = datetime.fromisoformat(date_str)
                
                # Aplicar filtro por período
                if period == "Hoje":
                    if movement_date.date() == now.date():
                        filtered.append(movement)
                elif period == "Última Semana":
                    if movement_date >= now - timedelta(days=7):
                        filtered.append(movement)
                elif period == "Último Mês":
                    if movement_date >= now - timedelta(days=30):
                        filtered.append(movement)
                elif period == "Último Ano":
                    if movement_date >= now - timedelta(days=365):
                        filtered.append(movement)
            except Exception as e:
                print(f"Erro ao processar data da movimentação: {e}")
                continue
        
        return filtered
    
    def filter_movements(self, value=None):
        """Filtrar movimentações por tipo (melhorado)"""
        try:
            filter_type = self.filter_type_var.get() if self.filter_type_var else "Todos"
            print(f"Filtro selecionado: {filter_type}")  # Debug
            self.load_movements_data(filter_type)
            
            # Atualizar estatísticas após filtro
            stats = self.calculate_movements_stats()
            print(f"Estatísticas: {stats}")  # Debug
            
        except Exception as e:
            print(f"Erro no filtro: {e}")
            self.show_message(f"Erro ao filtrar movimentações: {e}", "error")
    
    def calculate_movements_stats(self):
        """Calcular estatísticas das movimentações"""
        total = len(self.manager.movements)
        entradas = len([m for m in self.manager.movements if m['type'] == 'entrada'])
        saidas = len([m for m in self.manager.movements if m['type'] == 'saída'])
        
        return {
            'total': total,
            'entradas': entradas,
            'saidas': saidas
        }
    
    def refresh(self):
        """Atualizar dados da view"""
        self.load_movements_data() 