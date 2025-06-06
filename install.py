#!/usr/bin/env python3
"""
Instalação automática das dependências do Sistema de Controle de Estoque
"""

import subprocess
import sys
import os

def run_command(command):
    """Execute a command and return success status"""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {command}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar: {command}")
        print(f"   {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} encontrado")
        return True
    else:
        print(f"❌ Python 3.8+ é necessário. Versão atual: {version.major}.{version.minor}.{version.micro}")
        return False

def install_dependencies():
    """Install required dependencies"""
    print("📦 Instalando dependências...")
    
    # Upgrade pip first
    if not run_command("python -m pip install --upgrade pip"):
        return False
    
    # Install requirements
    if not run_command("pip install -r requirements.txt"):
        return False
    
    return True

def create_directories():
    """Create necessary directories"""
    directories = ["data", "assets", "backups"]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"📁 Criada pasta: {directory}")
        else:
            print(f"📁 Pasta já existe: {directory}")

def main():
    """Main installation function"""
    print("🚀 Sistema de Controle de Estoque v2.0 - Instalação")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        print("\n❌ Instalação cancelada devido à versão incompatível do Python")
        return False
    
    # Create directories
    print("\n📁 Criando diretórios...")
    create_directories()
    
    # Install dependencies
    print("\n📦 Instalando dependências...")
    if not install_dependencies():
        print("\n❌ Falha na instalação das dependências")
        return False
    
    print("\n✅ Instalação concluída com sucesso!")
    print("\n🎯 Para executar o sistema:")
    print("   python main.py")
    print("\n📚 Documentação completa no README.md")
    
    return True

if __name__ == "__main__":
    success = main()
    
    if success:
        input("\nPressione Enter para sair...")
    else:
        input("\nPressione Enter para sair...")
        sys.exit(1) 