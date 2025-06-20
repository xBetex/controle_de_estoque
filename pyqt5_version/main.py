#!/usr/bin/env python3
"""
Sistema de Controle de Estoque - Versão PyQt5
Main entry point for the inventory management system
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Main application entry point"""
    try:
        # Import main window
        from views.main_window import main as run_app
        
        # Run the application
        run_app()
        
    except ImportError as e:
        print(f"Erro ao importar módulos: {e}")
        print("Certifique-se de que o PyQt5 está instalado:")
        print("pip install PyQt5")
        input("Pressione Enter para sair...")
        sys.exit(1)
    except Exception as e:
        print(f"Erro crítico na aplicação: {e}")
        import traceback
        traceback.print_exc()
        input("Pressione Enter para sair...")
        sys.exit(1)

if __name__ == "__main__":
    main() 