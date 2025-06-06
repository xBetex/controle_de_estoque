# Sistema de Controle de Estoque - Linux Mint

## 🐧 Guia de Instalação e Configuração para Linux Mint

Este guia foi criado especificamente para resolver problemas comuns no Linux Mint e garantir que o sistema funcione perfeitamente.

## 🚀 Instalação Rápida

```bash
# Baixar e executar o script de instalação otimizado
./start_mint.sh
```

## 📋 Pré-requisitos

### Dependências do Sistema
O script de instalação cuidará automaticamente destas dependências, mas você pode instalá-las manualmente se necessário:

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv python3-dev python3-tk \
                   python3-pil python3-pil.imagetk libgtk-3-dev libcairo2-dev \
                   libgirepository1.0-dev pkg-config build-essential curl git
```

### Python 3.7+
```bash
python3 --version  # Deve ser 3.7 ou superior
```

## 🔧 Instalação Manual

Se você preferir fazer a instalação manualmente:

### 1. Criar Ambiente Virtual
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Instalar Dependências Python
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configurar Variáveis de Ambiente
```bash
export LANG=pt_BR.UTF-8
export LC_ALL=pt_BR.UTF-8
export DISPLAY=${DISPLAY:-:0}
export MPLBACKEND=TkAgg
```

### 4. Executar o Sistema
```bash
python3 main.py
```

## 🐛 Solução de Problemas Comuns

### Problema: "ModuleNotFoundError: No module named 'tkinter'"
**Solução:**
```bash
sudo apt install python3-tk python3-dev
```

### Problema: "ImportError: cannot import name 'FigureCanvasTkinter'"
**Solução:**
```bash
# Já corrigido no código - usa FigureCanvasTkAgg
pip install --upgrade matplotlib
```

### Problema: Erro de encoding UTF-8
**Solução:**
```bash
# Adicionar ao ~/.bashrc
echo 'export LANG=pt_BR.UTF-8' >> ~/.bashrc
echo 'export LC_ALL=pt_BR.UTF-8' >> ~/.bashrc
source ~/.bashrc
```

### Problema: Interface não aparece ou trava
**Solução:**
```bash
# Instalar dependências de GUI
sudo apt install libgtk-3-dev libcairo2-dev
# Verificar display
echo $DISPLAY
# Se vazio, definir:
export DISPLAY=:0
```

### Problema: "Permission denied" ao executar scripts
**Solução:**
```bash
chmod +x start_mint.sh
chmod +x *.sh
```

### Problema: Erro com CustomTkinter
**Solução:**
```bash
# Desinstalar e reinstalar
pip uninstall customtkinter
pip install --no-cache-dir customtkinter>=5.2.0
```

### Problema: Matplotlib não funciona
**Solução:**
```bash
# Configurar backend
export MPLBACKEND=TkAgg
# Ou instalar dependências adicionais
sudo apt install python3-matplotlib
```

### Problema: Erro com PIL/Pillow
**Solução:**
```bash
sudo apt install python3-pil python3-pil.imagetk
pip install --upgrade Pillow
```

## 🖥️ Configurações Específicas do Linux Mint

### Para Linux Mint 20.x (Ubuntu 20.04 base)
```bash
# Dependências adicionais que podem ser necessárias
sudo apt install python3.8-dev python3.8-venv
```

### Para Linux Mint 21.x (Ubuntu 22.04 base)
```bash
# Dependências adicionais que podem ser necessárias
sudo apt install python3.10-dev python3.10-venv
```

### Para sistemas com Wayland
```bash
# Se estiver usando Wayland em vez de X11
export GDK_BACKEND=x11
export QT_QPA_PLATFORM=xcb
```

## 🔧 Scripts Úteis

### Verificar Instalação
```bash
./start_mint.sh --verify
```

### Apenas Executar (sem instalar)
```bash
./start_mint.sh --run
```

### Instalar Dependências Apenas
```bash
./start_mint.sh --install
```

### Criar Atalho no Desktop
```bash
./start_mint.sh --desktop
```

## 📁 Estrutura de Arquivos

```
projeto/
├── main.py                 # Arquivo principal
├── start_mint.sh           # Script de instalação Linux Mint
├── requirements.txt        # Dependências Python
├── README_LINUX_MINT.md    # Este arquivo
├── data/                   # Dados do sistema
│   ├── products.json       # Produtos
│   ├── movements.json      # Movimentações
│   ├── suppliers.json      # Fornecedores
│   ├── categories.json     # Categorias
│   └── settings.json       # Configurações
├── backups/                # Backups automáticos
├── logs/                   # Logs do sistema
└── venv/                   # Ambiente virtual Python
```

## 🔄 Atualizações e Manutenção

### Atualizar Dependências
```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

### Fazer Backup
```bash
# Use a função de backup integrada no sistema
# Ou copie manualmente:
cp -r data/ backup_$(date +%Y%m%d)/
```

### Limpar Cache Python
```bash
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -name "*.pyc" -delete
```

## 🆘 Suporte e Debug

### Log de Erros
Se encontrar problemas, verifique:
```bash
# Executar com debug
python3 -v main.py

# Verificar logs do sistema
journalctl --user -f
```

### Informações do Sistema
```bash
# Versão do Linux Mint
cat /etc/os-release

# Versão do Python
python3 --version

# Módulos instalados
pip list
```

### Teste de Módulos
```bash
python3 -c "
import tkinter as tk
import customtkinter as ctk
import PIL
import matplotlib
import pandas
print('✅ Todos os módulos funcionando!')
"
```

## 📞 Ajuda Adicional

Se você ainda estiver com problemas:

1. **Verifique as dependências:** Execute `./start_mint.sh --verify`
2. **Reinstale completamente:** Remova a pasta `venv` e execute `./start_mint.sh`
3. **Consulte os logs:** Verifique arquivos de log em `logs/`
4. **Teste individual:** Execute os comandos de teste acima

## 🔒 Permissões

O sistema precisa de permissões para:
- Ler/escrever na pasta `data/`
- Criar backups na pasta `backups/`
- Escrever logs na pasta `logs/`

```bash
# Garantir permissões corretas
chmod -R 755 .
chmod +x *.sh
```

## 🎯 Dicas de Performance

Para melhor performance no Linux Mint:

1. **Use SSD:** Para melhor I/O de dados
2. **RAM:** Mínimo 4GB recomendado
3. **Python:** Use a versão mais recente disponível
4. **Ambiente virtual:** Sempre use para isolamento

---

**Versão:** 2.0  
**Testado em:** Linux Mint 20.x, 21.x  
**Python:** 3.7+  
**Última atualização:** Dezembro 2024 