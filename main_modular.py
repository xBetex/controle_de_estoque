"""
Sistema de Controle de Estoque Modularizado
"""

import sys
import os

try:
    from views.main_window import MainWindow
except ImportError as e:
    print(f"Erro ao importar módulos: {e}")
    print("Verifique se todos os arquivos estão no local correto")
    input("Pressione Enter para sair...")
    sys.exit(1)

def main():
    """Função principal da aplicação"""
    try:
        # Criar e executar aplicação
        app = MainWindow()
        app.run()
        
    except Exception as e:
        print(f"Erro crítico na aplicação: {e}")
        import traceback
        traceback.print_exc()
        input("Pressione Enter para sair...")

if __name__ == "__main__":
    main() 