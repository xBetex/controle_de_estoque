"""
Módulo de diálogos para o Sistema de Controle de Estoque
"""

import customtkinter as ctk
from tkinter import messagebox
from typing import Dict, Optional
from config import FONT_SIZES
from utils import center_window, validate_required_fields, validate_numeric_fields

class ProductDialog:
    """Diálogo para adicionar/editar produtos"""
    
    def __init__(self, parent, manager, product=None, title="Produto"):
        self.manager = manager
        self.product = product
        self.result = False
        
        # Criar diálogo
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("500x700")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Centralizar diálogo
        center_window(self.dialog, 500, 700)
        
        self.create_widgets()
        
        if product:
            self.populate_fields()
    
    def create_widgets(self):
        """Criar widgets do diálogo"""
        # Frame principal
        main_frame = ctk.CTkScrollableFrame(self.dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Campos do formulário
        fields = [
            ("Código *", "code", "entry"),
            ("Nome *", "name", "entry"),
            ("Descrição", "description", "textbox"),
            ("Preço (R$) *", "price", "entry"),
            ("Quantidade *", "quantity", "entry"),
            ("Fornecedor", "supplier", "entry"),
            ("Categoria", "category", "entry"),
            ("Localização", "location", "entry"),
            ("Código de Barras", "barcode", "entry"),
            ("Peso (kg)", "weight", "entry"),
            ("Dimensões", "dimensions", "entry"),
            ("Estoque Mínimo", "min_stock", "entry")
        ]
        
        self.fields = {}
        
        for label_text, field_name, field_type in fields:
            # Frame do campo
            field_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
            field_frame.pack(fill="x", pady=5)
            
            # Label
            label = ctk.CTkLabel(
                field_frame, 
                text=label_text, 
                anchor="w", 
                font=ctk.CTkFont(size=FONT_SIZES["label"])
            )
            label.pack(fill="x")
            
            # Campo
            if field_type == "entry":
                field = ctk.CTkEntry(
                    field_frame, 
                    height=40, 
                    font=ctk.CTkFont(size=FONT_SIZES["text"])
                )
            elif field_type == "textbox":
                field = ctk.CTkTextbox(
                    field_frame, 
                    height=100, 
                    font=ctk.CTkFont(size=FONT_SIZES["text"])
                )
            
            field.pack(fill="x", pady=(5, 0))
            self.fields[field_name] = field
        
        # Frame dos botões
        buttons_frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=20)
        
        # Botão cancelar
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="Cancelar",
            command=self.cancel,
            fg_color="gray",
            width=120,
            height=40,
            font=ctk.CTkFont(size=FONT_SIZES["button"])
        )
        cancel_btn.pack(side="right", padx=(10, 0))
        
        # Botão salvar
        save_btn = ctk.CTkButton(
            buttons_frame,
            text="Salvar",
            command=self.save,
            width=120,
            height=40,
            font=ctk.CTkFont(size=FONT_SIZES["button"])
        )
        save_btn.pack(side="right")
    
    def populate_fields(self):
        """Preencher campos com dados do produto"""
        if not self.product:
            return
        
        field_mapping = {
            'code': 'code',
            'name': 'name',
            'description': 'description',
            'price': 'price',
            'quantity': 'quantity',
            'supplier': 'supplier',
            'category': 'category',
            'location': 'location',
            'barcode': 'barcode',
            'weight': 'weight',
            'dimensions': 'dimensions',
            'min_stock': 'min_stock'
        }
        
        for field_name, product_key in field_mapping.items():
            if field_name in self.fields and product_key in self.product:
                field = self.fields[field_name]
                value = str(self.product[product_key])
                
                if isinstance(field, ctk.CTkEntry):
                    field.insert(0, value)
                elif isinstance(field, ctk.CTkTextbox):
                    field.insert("1.0", value)
    
    def save(self):
        """Salvar produto"""
        try:
            # Obter valores dos campos
            data = {}
            for field_name, field in self.fields.items():
                if isinstance(field, ctk.CTkEntry):
                    data[field_name] = field.get().strip()
                elif isinstance(field, ctk.CTkTextbox):
                    data[field_name] = field.get("1.0", "end-1c").strip()
            
            # Validar campos obrigatórios
            required_fields = ['code', 'name', 'price', 'quantity']
            missing_field = validate_required_fields(data, required_fields)
            if missing_field:
                messagebox.showerror("Erro", f"O campo '{missing_field}' é obrigatório!")
                return
            
            # Validar campos numéricos
            numeric_fields = {
                'price': float,
                'quantity': int,
                'weight': float,
                'min_stock': int
            }
            invalid_field = validate_numeric_fields(data, numeric_fields)
            if invalid_field:
                messagebox.showerror("Erro", f"O campo '{invalid_field}' deve ser um número válido!")
                return
            
            # Converter campos numéricos
            data['price'] = float(data['price'])
            data['quantity'] = int(data['quantity'])
            if data.get('weight'):
                data['weight'] = float(data['weight'])
            if data.get('min_stock'):
                data['min_stock'] = int(data['min_stock'])
            else:
                data['min_stock'] = 0
            
            # Salvar produto
            if self.product:
                # Atualizar produto existente
                if self.manager.update_product(self.product['code'], data):
                    messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")
                    self.result = True
                    self.dialog.destroy()
                else:
                    messagebox.showerror("Erro", "Erro ao atualizar produto!")
            else:
                # Adicionar novo produto
                if self.manager.add_product(data):
                    messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
                    self.result = True
                    self.dialog.destroy()
                else:
                    messagebox.showerror("Erro", "Código de produto já existe!")
        
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar produto: {str(e)}")
    
    def cancel(self):
        """Cancelar diálogo"""
        self.dialog.destroy()


class StockAdjustmentDialog:
    """Diálogo para ajuste de estoque"""
    
    def __init__(self, parent, manager, product):
        self.manager = manager
        self.product = product
        self.result = False
        
        # Criar diálogo
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Ajustar Estoque")
        self.dialog.geometry("450x400")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Centralizar diálogo
        center_window(self.dialog, 450, 400)
        
        self.create_widgets()
    
    def create_widgets(self):
        """Criar widgets do diálogo"""
        # Frame principal
        main_frame = ctk.CTkFrame(self.dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Informações do produto
        info_frame = ctk.CTkFrame(main_frame)
        info_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            info_frame,
            text=f"Produto: {self.product['name']}",
            font=ctk.CTkFont(size=FONT_SIZES["subheading"], weight="bold")
        ).pack(pady=5)
        
        ctk.CTkLabel(
            info_frame,
            text=f"Código: {self.product['code']}",
            font=ctk.CTkFont(size=FONT_SIZES["text"])
        ).pack(pady=2)
        
        ctk.CTkLabel(
            info_frame,
            text=f"Estoque Atual: {self.product['quantity']} unidades",
            font=ctk.CTkFont(size=FONT_SIZES["button"], weight="bold")
        ).pack(pady=5)
        
        # Tipo de ajuste
        ctk.CTkLabel(
            main_frame, 
            text="Tipo de Ajuste:", 
            font=ctk.CTkFont(size=FONT_SIZES["button"])
        ).pack(anchor="w", pady=(0, 5))
        
        self.adjustment_type = ctk.StringVar(value="add")
        
        type_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        type_frame.pack(fill="x", pady=(0, 10))
        
        ctk.CTkRadioButton(
            type_frame,
            text="➕ Adicionar ao estoque",
            variable=self.adjustment_type,
            value="add",
            font=ctk.CTkFont(size=FONT_SIZES["text"])
        ).pack(anchor="w", pady=2)
        
        ctk.CTkRadioButton(
            type_frame,
            text="➖ Remover do estoque",
            variable=self.adjustment_type,
            value="remove",
            font=ctk.CTkFont(size=FONT_SIZES["text"])
        ).pack(anchor="w", pady=2)
        
        # Quantidade
        ctk.CTkLabel(
            main_frame, 
            text="Quantidade:", 
            font=ctk.CTkFont(size=FONT_SIZES["button"])
        ).pack(anchor="w", pady=(10, 5))
        
        self.quantity_entry = ctk.CTkEntry(
            main_frame, 
            placeholder_text="Digite a quantidade...", 
            height=40, 
            font=ctk.CTkFont(size=FONT_SIZES["text"])
        )
        self.quantity_entry.pack(fill="x", pady=(0, 10))
        
        # Motivo
        ctk.CTkLabel(
            main_frame, 
            text="Motivo:", 
            font=ctk.CTkFont(size=FONT_SIZES["button"])
        ).pack(anchor="w", pady=(0, 5))
        
        self.reason_entry = ctk.CTkEntry(
            main_frame, 
            placeholder_text="Motivo do ajuste (opcional)", 
            height=40, 
            font=ctk.CTkFont(size=FONT_SIZES["text"])
        )
        self.reason_entry.pack(fill="x", pady=(0, 20))
        
        # Botões
        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(fill="x")
        
        ctk.CTkButton(
            buttons_frame,
            text="Cancelar",
            command=self.cancel,
            fg_color="gray",
            width=120,
            height=40,
            font=ctk.CTkFont(size=FONT_SIZES["button"])
        ).pack(side="right", padx=(10, 0))
        
        ctk.CTkButton(
            buttons_frame,
            text="Aplicar",
            command=self.apply_adjustment,
            width=120,
            height=40,
            font=ctk.CTkFont(size=FONT_SIZES["button"])
        ).pack(side="right")
    
    def apply_adjustment(self):
        """Aplicar ajuste de estoque"""
        try:
            quantity_str = self.quantity_entry.get().strip()
            if not quantity_str:
                messagebox.showerror("Erro", "Por favor, digite a quantidade!")
                return
                
            quantity = int(quantity_str)
            if quantity <= 0:
                messagebox.showerror("Erro", "Quantidade deve ser maior que zero!")
                return
            
            adjustment_type = self.adjustment_type.get()
            if adjustment_type == "remove":
                quantity = -quantity
                
                # Verificar se há estoque suficiente
                if self.product['quantity'] + quantity < 0:
                    messagebox.showerror("Erro", "Estoque insuficiente para esta operação!")
                    return
            
            reason = self.reason_entry.get().strip() or "Ajuste manual"
            
            if self.manager.update_stock(self.product['code'], quantity, reason):
                messagebox.showinfo("Sucesso", "Estoque ajustado com sucesso!")
                self.result = True
                self.dialog.destroy()
            else:
                messagebox.showerror("Erro", "Erro ao ajustar estoque!")
        
        except ValueError:
            messagebox.showerror("Erro", "Quantidade deve ser um número inteiro válido!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao ajustar estoque: {str(e)}")
    
    def cancel(self):
        """Cancelar diálogo"""
        self.dialog.destroy()


class SupplierDialog:
    """Diálogo para adicionar/editar fornecedores"""
    
    def __init__(self, parent, manager, supplier=None, title="Fornecedor"):
        self.manager = manager
        self.supplier = supplier
        self.result = False
        
        # Criar diálogo
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("500x600")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Centralizar diálogo
        center_window(self.dialog, 500, 600)
        
        self.create_widgets()
        
        if supplier:
            self.populate_fields()
    
    def create_widgets(self):
        """Criar widgets do diálogo"""
        # Frame principal
        main_frame = ctk.CTkScrollableFrame(self.dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Campos do formulário
        fields = [
            ("Nome *", "name", "entry"),
            ("Email", "email", "entry"),
            ("Telefone", "phone", "entry"),
            ("Endereço", "address", "textbox"),
            ("CNPJ/CPF", "document", "entry"),
            ("Contato", "contact_person", "entry"),
            ("Observações", "notes", "textbox")
        ]
        
        self.fields = {}
        
        for label_text, field_name, field_type in fields:
            # Frame do campo
            field_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
            field_frame.pack(fill="x", pady=5)
            
            # Label
            label = ctk.CTkLabel(
                field_frame, 
                text=label_text, 
                anchor="w", 
                font=ctk.CTkFont(size=FONT_SIZES["label"])
            )
            label.pack(fill="x")
            
            # Campo
            if field_type == "entry":
                field = ctk.CTkEntry(
                    field_frame, 
                    height=40, 
                    font=ctk.CTkFont(size=FONT_SIZES["text"])
                )
            elif field_type == "textbox":
                field = ctk.CTkTextbox(
                    field_frame, 
                    height=80, 
                    font=ctk.CTkFont(size=FONT_SIZES["text"])
                )
            
            field.pack(fill="x", pady=(5, 0))
            self.fields[field_name] = field
        
        # Checkbox ativo
        self.active_var = ctk.BooleanVar(value=True)
        active_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        active_frame.pack(fill="x", pady=10)
        
        active_checkbox = ctk.CTkCheckBox(
            active_frame,
            text="Fornecedor Ativo",
            variable=self.active_var,
            font=ctk.CTkFont(size=FONT_SIZES["text"])
        )
        active_checkbox.pack(anchor="w")
        
        # Frame dos botões
        buttons_frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=20)
        
        # Botão cancelar
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="Cancelar",
            command=self.cancel,
            fg_color="gray",
            width=120,
            height=40,
            font=ctk.CTkFont(size=FONT_SIZES["button"])
        )
        cancel_btn.pack(side="right", padx=(10, 0))
        
        # Botão salvar
        save_btn = ctk.CTkButton(
            buttons_frame,
            text="Salvar",
            command=self.save,
            width=120,
            height=40,
            font=ctk.CTkFont(size=FONT_SIZES["button"])
        )
        save_btn.pack(side="right")
    
    def populate_fields(self):
        """Preencher campos com dados do fornecedor"""
        if not self.supplier:
            return
        
        field_mapping = {
            'name': 'name',
            'email': 'email',
            'phone': 'phone',
            'address': 'address',
            'document': 'document',
            'contact_person': 'contact_person',
            'notes': 'notes'
        }
        
        for field_name, supplier_key in field_mapping.items():
            if field_name in self.fields and supplier_key in self.supplier:
                field = self.fields[field_name]
                value = str(self.supplier[supplier_key])
                
                if isinstance(field, ctk.CTkEntry):
                    field.insert(0, value)
                elif isinstance(field, ctk.CTkTextbox):
                    field.insert("1.0", value)
        
        # Status ativo
        if 'active' in self.supplier:
            self.active_var.set(self.supplier['active'])
    
    def save(self):
        """Salvar fornecedor"""
        try:
            # Obter valores dos campos
            data = {}
            for field_name, field in self.fields.items():
                if isinstance(field, ctk.CTkEntry):
                    data[field_name] = field.get().strip()
                elif isinstance(field, ctk.CTkTextbox):
                    data[field_name] = field.get("1.0", "end-1c").strip()
            
            data['active'] = self.active_var.get()
            
            # Validar campos obrigatórios
            if not data.get('name'):
                messagebox.showerror("Erro", "O campo 'Nome' é obrigatório!")
                return
            
            # Salvar fornecedor
            if self.supplier:
                # Atualizar fornecedor existente
                if self.manager.update_supplier(self.supplier['id'], data):
                    messagebox.showinfo("Sucesso", "Fornecedor atualizado com sucesso!")
                    self.result = True
                    self.dialog.destroy()
                else:
                    messagebox.showerror("Erro", "Erro ao atualizar fornecedor!")
            else:
                # Adicionar novo fornecedor
                if self.manager.add_supplier(data):
                    messagebox.showinfo("Sucesso", "Fornecedor cadastrado com sucesso!")
                    self.result = True
                    self.dialog.destroy()
                else:
                    messagebox.showerror("Erro", "Fornecedor já existe!")
        
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar fornecedor: {str(e)}")
    
    def cancel(self):
        """Cancelar diálogo"""
        self.dialog.destroy()


class CategoryDialog:
    """Diálogo para adicionar/editar categorias"""
    
    def __init__(self, parent, manager, category=None, title="Categoria"):
        self.manager = manager
        self.category = category
        self.result = False
        
        # Criar diálogo
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("450x400")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Centralizar diálogo
        center_window(self.dialog, 450, 400)
        
        self.create_widgets()
        
        if category:
            self.populate_fields()
    
    def create_widgets(self):
        """Criar widgets do diálogo"""
        # Frame principal
        main_frame = ctk.CTkScrollableFrame(self.dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Campos do formulário
        fields = [
            ("Nome *", "name", "entry"),
            ("Descrição", "description", "textbox"),
            ("Cor (hex)", "color", "entry")
        ]
        
        self.fields = {}
        
        for label_text, field_name, field_type in fields:
            # Frame do campo
            field_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
            field_frame.pack(fill="x", pady=5)
            
            # Label
            label = ctk.CTkLabel(
                field_frame, 
                text=label_text, 
                anchor="w", 
                font=ctk.CTkFont(size=FONT_SIZES["label"])
            )
            label.pack(fill="x")
            
            # Campo
            if field_type == "entry":
                if field_name == "color":
                    field = ctk.CTkEntry(
                        field_frame, 
                        height=40, 
                        font=ctk.CTkFont(size=FONT_SIZES["text"]), 
                        placeholder_text="#FF0000"
                    )
                else:
                    field = ctk.CTkEntry(
                        field_frame, 
                        height=40, 
                        font=ctk.CTkFont(size=FONT_SIZES["text"])
                    )
            elif field_type == "textbox":
                field = ctk.CTkTextbox(
                    field_frame, 
                    height=80, 
                    font=ctk.CTkFont(size=FONT_SIZES["text"])
                )
            
            field.pack(fill="x", pady=(5, 0))
            self.fields[field_name] = field
        
        # Checkbox ativo
        self.active_var = ctk.BooleanVar(value=True)
        active_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        active_frame.pack(fill="x", pady=10)
        
        active_checkbox = ctk.CTkCheckBox(
            active_frame,
            text="Categoria Ativa",
            variable=self.active_var,
            font=ctk.CTkFont(size=FONT_SIZES["text"])
        )
        active_checkbox.pack(anchor="w")
        
        # Frame dos botões
        buttons_frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=20)
        
        # Botão cancelar
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="Cancelar",
            command=self.cancel,
            fg_color="gray",
            width=120,
            height=40,
            font=ctk.CTkFont(size=FONT_SIZES["button"])
        )
        cancel_btn.pack(side="right", padx=(10, 0))
        
        # Botão salvar
        save_btn = ctk.CTkButton(
            buttons_frame,
            text="Salvar",
            command=self.save,
            width=120,
            height=40,
            font=ctk.CTkFont(size=FONT_SIZES["button"])
        )
        save_btn.pack(side="right")
    
    def populate_fields(self):
        """Preencher campos com dados da categoria"""
        if not self.category:
            return
        
        field_mapping = {
            'name': 'name',
            'description': 'description',
            'color': 'color'
        }
        
        for field_name, category_key in field_mapping.items():
            if field_name in self.fields and category_key in self.category:
                field = self.fields[field_name]
                value = str(self.category[category_key])
                
                if isinstance(field, ctk.CTkEntry):
                    field.insert(0, value)
                elif isinstance(field, ctk.CTkTextbox):
                    field.insert("1.0", value)
        
        # Status ativo
        if 'active' in self.category:
            self.active_var.set(self.category['active'])
    
    def save(self):
        """Salvar categoria"""
        try:
            # Obter valores dos campos
            data = {}
            for field_name, field in self.fields.items():
                if isinstance(field, ctk.CTkEntry):
                    data[field_name] = field.get().strip()
                elif isinstance(field, ctk.CTkTextbox):
                    data[field_name] = field.get("1.0", "end-1c").strip()
            
            data['active'] = self.active_var.get()
            
            # Validar campos obrigatórios
            if not data.get('name'):
                messagebox.showerror("Erro", "O campo 'Nome' é obrigatório!")
                return
            
            # Validar cor (se fornecida)
            if data.get('color') and not data['color'].startswith('#'):
                data['color'] = '#' + data['color']
            
            # Salvar categoria
            if self.category:
                # Atualizar categoria existente
                if self.manager.update_category(self.category['id'], data):
                    messagebox.showinfo("Sucesso", "Categoria atualizada com sucesso!")
                    self.result = True
                    self.dialog.destroy()
                else:
                    messagebox.showerror("Erro", "Erro ao atualizar categoria!")
            else:
                # Adicionar nova categoria
                if self.manager.add_category(data):
                    messagebox.showinfo("Sucesso", "Categoria cadastrada com sucesso!")
                    self.result = True
                    self.dialog.destroy()
                else:
                    messagebox.showerror("Erro", "Categoria já existe!")
        
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar categoria: {str(e)}")
    
    def cancel(self):
        """Cancelar diálogo"""
        self.dialog.destroy() 