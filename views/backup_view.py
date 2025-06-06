"""
View de backup
"""

import customtkinter as ctk
from views.base_view import BaseView
from config import FONT_SIZES, COLORS

class BackupView(BaseView):
    """View de backup do sistema"""
    
    def create_widgets(self):
        """Criar widgets da view de backup"""
        self.frame = ctk.CTkScrollableFrame(self.parent)
        
        # Cabeçalho
        self.create_header("💾 Backup e Restauração", "Gerenciamento de backups do sistema")
        
        # Seções de backup
        self.create_backup_sections()
    
    def create_backup_sections(self):
        """Criar seções de backup"""
        # Seção de Criar Backup
        create_frame = ctk.CTkFrame(self.frame)
        create_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            create_frame,
            text="Criar Backup",
            font=ctk.CTkFont(size=FONT_SIZES["subheading"], weight="bold")
        ).pack(pady=(20, 10))
        
        ctk.CTkLabel(
            create_frame,
            text="Faça backup dos seus dados para não perder informações importantes.",
            font=ctk.CTkFont(size=FONT_SIZES["text"]),
            text_color="gray"
        ).pack(pady=(0, 20))
        
        # Botões de backup
        buttons_frame = ctk.CTkFrame(create_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        ctk.CTkButton(
            buttons_frame,
            text="📦 Backup Completo",
            command=self.create_full_backup,
            height=50,
            font=ctk.CTkFont(size=FONT_SIZES["button"])
        ).pack(side="left", padx=(0, 10), fill="x", expand=True)
        
        ctk.CTkButton(
            buttons_frame,
            text="⚡ Backup Rápido",
            command=self.create_quick_backup,
            height=50,
            font=ctk.CTkFont(size=FONT_SIZES["button"])
        ).pack(side="left", padx=(10, 0), fill="x", expand=True)
        
        # Seção de Configurações
        config_frame = ctk.CTkFrame(self.frame)
        config_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            config_frame,
            text="Configurações de Backup",
            font=ctk.CTkFont(size=FONT_SIZES["subheading"], weight="bold")
        ).pack(pady=(20, 10))
        
        # Auto backup
        auto_frame = ctk.CTkFrame(config_frame, fg_color="transparent")
        auto_frame.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkLabel(auto_frame, text="Backup Automático:").pack(side="left")
        
        current_auto = self.manager.settings.get('auto_backup', True)
        status_text = "✅ Ativado" if current_auto else "❌ Desativado"
        ctk.CTkLabel(auto_frame, text=status_text).pack(side="right")
        
        # Seção de Status
        status_frame = ctk.CTkFrame(self.frame)
        status_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            status_frame,
            text="Status do Sistema",
            font=ctk.CTkFont(size=FONT_SIZES["subheading"], weight="bold")
        ).pack(pady=(20, 10))
        
        # Informações do sistema
        info_text = f"""
Sistema funcionando normalmente
Total de produtos: {len(self.manager.products)}
Total de movimentações: {len(self.manager.movements)}
Total de fornecedores: {len(self.manager.suppliers)}
Total de categorias: {len(self.manager.categories)}
        """
        
        ctk.CTkLabel(
            status_frame,
            text=info_text.strip(),
            font=ctk.CTkFont(size=FONT_SIZES["text"]),
            justify="left"
        ).pack(pady=(0, 20))
    
    def create_full_backup(self):
        """Criar backup completo"""
        try:
            # Simular criação de backup
            import shutil
            import os
            from datetime import datetime
            
            # Criar diretório de backup se não existir
            backup_dir = "backups"
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
            
            # Nome do backup
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"backup_completo_{timestamp}"
            backup_path = os.path.join(backup_dir, backup_name)
            
            # Copiar diretório de dados
            if os.path.exists("data"):
                shutil.copytree("data", backup_path)
                self.show_message(f"Backup completo criado com sucesso!\nLocal: {backup_path}", "success")
            else:
                self.show_message("Nenhum dado encontrado para backup.", "warning")
                
        except Exception as e:
            self.show_message(f"Erro ao criar backup: {str(e)}", "error")
    
    def create_quick_backup(self):
        """Criar backup rápido"""
        try:
            import json
            import os
            from datetime import datetime
            
            # Criar diretório de backup se não existir
            backup_dir = "backups"
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
            
            # Nome do backup
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(backup_dir, f"backup_rapido_{timestamp}.json")
            
            # Dados para backup
            backup_data = {
                "products": self.manager.products,
                "movements": self.manager.movements,
                "suppliers": self.manager.suppliers,
                "categories": self.manager.categories,
                "settings": self.manager.settings,
                "backup_date": datetime.now().isoformat()
            }
            
            # Salvar backup
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, indent=2, ensure_ascii=False)
            
            self.show_message(f"Backup rápido criado com sucesso!\nLocal: {backup_file}", "success")
            
        except Exception as e:
            self.show_message(f"Erro ao criar backup rápido: {str(e)}", "error")
    
    def refresh(self):
        """Atualizar dados da view"""
        # Recriar widgets para atualizar informações
        if hasattr(self, 'frame'):
            for widget in self.frame.winfo_children():
                widget.destroy()
            self.create_backup_sections() 