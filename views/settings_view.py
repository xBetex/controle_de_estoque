"""
View de configurações
"""

import customtkinter as ctk
from views.base_view import BaseView
from config import FONT_SIZES, COLORS

class SettingsView(BaseView):
    """View de configurações do sistema"""
    
    def create_widgets(self):
        """Criar widgets da view de configurações"""
        self.frame = ctk.CTkScrollableFrame(self.parent)
        
        # Cabeçalho
        self.create_header("⚙️ Configurações", "Ajustes e preferências do sistema")
        
        # Seções de configuração
        self.create_settings_sections()
        
        # Botão salvar
        self.create_save_button()
    
    def create_settings_sections(self):
        """Criar seções de configurações"""
        # Configurações Gerais
        general_frame = ctk.CTkFrame(self.frame)
        general_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            general_frame,
            text="Configurações Gerais",
            font=ctk.CTkFont(size=FONT_SIZES["subheading"], weight="bold")
        ).pack(pady=(20, 10))
        
        # Limite de estoque baixo
        stock_frame = ctk.CTkFrame(general_frame, fg_color="transparent")
        stock_frame.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkLabel(stock_frame, text="Limite de Estoque Baixo:").pack(side="left")
        self.stock_limit_var = ctk.StringVar(value=str(self.manager.settings.get('low_stock_threshold', 5)))
        ctk.CTkEntry(stock_frame, textvariable=self.stock_limit_var, width=100).pack(side="right")
        
        # Tema
        theme_frame = ctk.CTkFrame(general_frame, fg_color="transparent")
        theme_frame.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkLabel(theme_frame, text="Tema:").pack(side="left")
        self.theme_var = ctk.StringVar(value=self.manager.settings.get('theme_mode', 'dark'))
        ctk.CTkOptionMenu(
            theme_frame, 
            variable=self.theme_var, 
            values=["dark", "light"], 
            width=120
        ).pack(side="right")
        
        # Configurações de Backup
        backup_frame = ctk.CTkFrame(self.frame)
        backup_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            backup_frame,
            text="Configurações de Backup",
            font=ctk.CTkFont(size=FONT_SIZES["subheading"], weight="bold")
        ).pack(pady=(20, 10))
        
        # Auto backup
        auto_backup_frame = ctk.CTkFrame(backup_frame, fg_color="transparent")
        auto_backup_frame.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkLabel(auto_backup_frame, text="Backup Automático:").pack(side="left")
        self.auto_backup_var = ctk.BooleanVar(value=self.manager.settings.get('auto_backup', True))
        ctk.CTkCheckBox(auto_backup_frame, text="", variable=self.auto_backup_var).pack(side="right")
        
        # Dias para backup
        backup_days_frame = ctk.CTkFrame(backup_frame, fg_color="transparent")
        backup_days_frame.pack(fill="x", padx=20, pady=(5, 20))
        
        ctk.CTkLabel(backup_days_frame, text="Intervalo de Backup (dias):").pack(side="left")
        self.backup_days_var = ctk.StringVar(value=str(self.manager.settings.get('auto_backup_days', 7)))
        ctk.CTkEntry(backup_days_frame, textvariable=self.backup_days_var, width=100).pack(side="right")
    
    def create_save_button(self):
        """Criar botão de salvar"""
        save_btn = ctk.CTkButton(
            self.frame,
            text="💾 Salvar Configurações",
            command=self.save_settings,
            height=50,
            font=ctk.CTkFont(size=FONT_SIZES["button"], weight="bold")
        )
        save_btn.pack(pady=30)
    
    def save_settings(self):
        """Salvar configurações"""
        try:
            # Atualizar configurações
            new_settings = self.manager.settings.copy()
            new_settings['low_stock_threshold'] = int(self.stock_limit_var.get())
            new_settings['theme_mode'] = self.theme_var.get()
            new_settings['auto_backup'] = self.auto_backup_var.get()
            new_settings['auto_backup_days'] = int(self.backup_days_var.get())
            
            # Salvar
            if self.manager.update_settings(new_settings):
                self.show_message("Configurações salvas com sucesso!", "success")
                
                # Aplicar tema se mudou
                if new_settings['theme_mode'] != self.manager.settings.get('theme_mode'):
                    ctk.set_appearance_mode(new_settings['theme_mode'])
            else:
                self.show_message("Erro ao salvar configurações!", "error")
                
        except ValueError:
            self.show_message("Verifique os valores numéricos inseridos!", "warning")
    
    def refresh(self):
        """Atualizar dados da view"""
        # Recarregar valores atuais
        self.stock_limit_var.set(str(self.manager.settings.get('low_stock_threshold', 5)))
        self.theme_var.set(self.manager.settings.get('theme_mode', 'dark'))
        self.auto_backup_var.set(self.manager.settings.get('auto_backup', True))
        self.backup_days_var.set(str(self.manager.settings.get('auto_backup_days', 7))) 