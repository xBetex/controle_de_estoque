"""
View de ajuda
"""

import customtkinter as ctk
from views.base_view import BaseView
from config import FONT_SIZES, COLORS, APP_TITLE, APP_VERSION

class HelpView(BaseView):
    """View de ajuda do sistema"""
    
    def create_widgets(self):
        """Criar widgets da view de ajuda"""
        self.frame = ctk.CTkScrollableFrame(self.parent)
        
        # Cabeçalho
        self.create_header("❓ Ajuda e Documentação", "Guia de uso do sistema")
        
        # Conteúdo da ajuda
        self.create_help_content()
    
    def create_help_content(self):
        """Criar conteúdo da ajuda"""
        # Seção Sobre
        about_frame = ctk.CTkFrame(self.frame)
        about_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            about_frame,
            text="Sobre o Sistema",
            font=ctk.CTkFont(size=FONT_SIZES["subheading"], weight="bold")
        ).pack(pady=(20, 10))
        
        about_text = f"""
{APP_TITLE}
Versão: {APP_VERSION}

Sistema completo de controle de estoque desenvolvido em Python com interface moderna.
Permite gerenciar produtos, fornecedores, categorias e movimentações de estoque.
        """
        
        ctk.CTkLabel(
            about_frame,
            text=about_text.strip(),
            font=ctk.CTkFont(size=FONT_SIZES["text"]),
            justify="left"
        ).pack(pady=(0, 20))
        
        # Seção Como Usar
        usage_frame = ctk.CTkFrame(self.frame)
        usage_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            usage_frame,
            text="Como Usar",
            font=ctk.CTkFont(size=FONT_SIZES["subheading"], weight="bold")
        ).pack(pady=(20, 10))
        
        usage_text = """
🏠 DASHBOARD
- Visualize estatísticas gerais do seu estoque
- Acompanhe atividades recentes
- Monitore produtos com estoque baixo

📦 PRODUTOS
- Cadastre novos produtos
- Edite informações existentes
- Ajuste quantidades em estoque
- Pesquise produtos por nome ou código

📊 MOVIMENTAÇÕES
- Visualize histórico de entradas e saídas
- Filtre por tipo de movimentação
- Acompanhe razões das movimentações

🏢 FORNECEDORES
- Cadastre fornecedores
- Gerencie informações de contato
- Vincule produtos aos fornecedores

🏷️ CATEGORIAS
- Organize produtos por categoria
- Facilite a busca e organização

📈 RELATÓRIOS
- Gere relatórios detalhados
- Analise dados por categoria/fornecedor
- Exporte informações
        """
        
        ctk.CTkLabel(
            usage_frame,
            text=usage_text.strip(),
            font=ctk.CTkFont(size=FONT_SIZES["text"]),
            justify="left"
        ).pack(pady=(0, 20))
        
        # Seção Atalhos
        shortcuts_frame = ctk.CTkFrame(self.frame)
        shortcuts_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            shortcuts_frame,
            text="Dicas e Atalhos",
            font=ctk.CTkFont(size=FONT_SIZES["subheading"], weight="bold")
        ).pack(pady=(20, 10))
        
        shortcuts_text = """
✨ DICAS IMPORTANTES:

• Duplo clique em qualquer item das listas para editar
• Use o botão direito do mouse para acessar menus de contexto
• Configure alertas de estoque baixo em Configurações
• Faça backups regulares dos seus dados
• Use a pesquisa para encontrar produtos rapidamente

🔄 ATALHOS:
• Ctrl+N: Novo produto (quando na aba Produtos)
• F5: Atualizar dados
• Esc: Fechar diálogos

⚠️ IMPORTANTE:
• Sempre faça backup antes de grandes alterações
• Mantenha os dados atualizados
• Configure o estoque mínimo para cada produto
        """
        
        ctk.CTkLabel(
            shortcuts_frame,
            text=shortcuts_text.strip(),
            font=ctk.CTkFont(size=FONT_SIZES["text"]),
            justify="left"
        ).pack(pady=(0, 20))
        
        # Seção de Suporte
        support_frame = ctk.CTkFrame(self.frame)
        support_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            support_frame,
            text="Suporte e Contato",
            font=ctk.CTkFont(size=FONT_SIZES["subheading"], weight="bold")
        ).pack(pady=(20, 10))
        
        support_text = """
📧 Suporte técnico: suporte@estoque.com
🌐 Site: www.estoque.com
📱 WhatsApp: (11) 99999-9999

Para reportar bugs ou sugestões, entre em contato conosco.
Sua opinião é importante para melhorarmos o sistema!
        """
        
        ctk.CTkLabel(
            support_frame,
            text=support_text.strip(),
            font=ctk.CTkFont(size=FONT_SIZES["text"]),
            justify="left"
        ).pack(pady=(0, 20))
    
    def refresh(self):
        """Atualizar dados da view"""
        pass  # Conteúdo estático 