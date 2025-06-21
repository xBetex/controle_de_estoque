# Sistema de Controle de Estoque

Sistema completo para gerenciamento de estoque desenvolvido em Python com PyQt6.

## 📋 Funcionalidades

- **Dashboard** com indicadores em tempo real
- **Cadastro de Produtos** com código, categoria, fornecedor e preços
- **Gestão de Categorias** para organização dos produtos
- **Cadastro de Fornecedores** com dados completos
- **Movimentações de Estoque** (entradas e saídas)
- **Relatórios** com exportação em Excel, CSV e PDF
- **Controle de Estoque Mínimo** com alertas
- **Backup automático** do banco de dados
- **Sistema de Logs** para auditoria

## 🚀 Como Executar

### Pré-requisitos

- Python 3.8 ou superior
- Pip (gerenciador de pacotes do Python)

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Executar o Sistema

```bash
python main.py
```

Ou no Windows:
```bash
python.exe main.py
```

## 📦 Dependências

- **PyQt6** - Interface gráfica
- **sqlite3** - Banco de dados (incluído no Python)
- **pandas** - Manipulação de dados para relatórios
- **openpyxl** - Exportação para Excel
- **reportlab** - Geração de PDFs
- **Pillow** - Manipulação de imagens

## 🗂️ Estrutura do Projeto

```
pyqt6_version/
├── main.py                 # Arquivo principal
├── requirements.txt        # Dependências
├── config/                 # Configurações
│   └── settings.py
├── models/                 # Modelos de dados
│   ├── __init__.py
│   ├── base.py
│   ├── produto.py
│   ├── categoria.py
│   ├── fornecedor.py
│   ├── movimentacao.py
│   └── usuario.py
├── views/                  # Interfaces gráficas
│   ├── __init__.py
│   ├── main_window.py
│   ├── dashboard_window.py
│   ├── produtos_window.py
│   ├── categorias_window.py
│   ├── fornecedores_window.py
│   ├── movimentacoes_window.py
│   └── relatorios_window.py
├── utils/                  # Utilitários
│   ├── __init__.py
│   ├── database.py
│   ├── logger.py
│   ├── export.py
│   └── validators.py
├── data/                   # Banco de dados
├── logs/                   # Arquivos de log
├── exports/                # Relatórios exportados
├── backups/                # Backups do banco
└── assets/                 # Recursos (ícones, imagens)
```

## 💾 Banco de Dados

O sistema utiliza SQLite com as seguintes tabelas:

- **produtos** - Cadastro de produtos
- **categorias** - Categorias dos produtos
- **fornecedores** - Cadastro de fornecedores
- **movimentacoes** - Histórico de movimentações
- **usuarios** - Usuários do sistema (funcionalidade básica)

## 🖥️ Principais Telas

### Dashboard
- Indicadores de estoque
- Produtos em falta
- Últimas movimentações
- Valor total do estoque

### Cadastro de Produtos
- Código único do produto
- Nome e descrição
- Categoria e fornecedor
- Preços de compra e venda
- Controle de estoque mínimo e atual
- Localização no estoque

### Movimentações
- Registrar entradas e saídas
- Controle automático do estoque
- Histórico completo
- Filtros por período e tipo

### Relatórios
- Lista de produtos
- Movimentações por período
- Produtos em falta
- Valor do estoque
- Resumo mensal
- Exportação em múltiplos formatos

## 🔧 Configurações

As configurações do sistema estão no arquivo `config/settings.py`:

- Caminhos dos diretórios
- Configurações do banco de dados
- Parâmetros de logging
- Configurações de backup

## 📊 Relatórios e Exportações

O sistema permite exportar dados em:
- **Excel (.xlsx)** - Formato mais completo
- **CSV** - Para integração com outros sistemas
- **PDF** - Para impressão e apresentação

## 🔒 Backup e Segurança

- Backup automático do banco de dados
- Sistema de logs para auditoria
- Validação de dados de entrada
- Controle de integridade referencial

## 🛠️ Desenvolvimento

### Adicionar Nova Funcionalidade

1. Criar modelo em `models/` se necessário
2. Criar interface em `views/`
3. Adicionar no menu principal em `views/main_window.py`
4. Testar funcionalidade

### Personalizar Interface

As interfaces utilizam PyQt6 com estilos CSS aplicados diretamente nos componentes.

## 📝 Logs

Os logs do sistema são salvos em `logs/sistema.log` com rotação automática.

## ❓ Solução de Problemas

### Erro de Dependências
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Erro de Permissão no Banco
Verifique se o diretório `data/` tem permissão de escrita.

### Interface não Aparece
Verifique se o PyQt6 foi instalado corretamente:
```bash
python -c "import PyQt6; print('PyQt6 OK')"
```

## 📄 Licença

Sistema desenvolvido para controle de estoque empresarial.

## 🤝 Suporte

Para suporte técnico ou dúvidas sobre o sistema, consulte os logs em `logs/sistema.log` para identificar possíveis erros.

---

**Versão:** 1.0.0  
**Desenvolvido em:** Python 3.x + PyQt6 