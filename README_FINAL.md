# 📦 Sistema de Controle de Estoque Avançado v2.0

## 🎯 Visão Geral

Sistema completo de controle de estoque desenvolvido em Python com interface gráfica moderna usando CustomTkinter. O sistema oferece funcionalidades avançadas de gestão de produtos, fornecedores, categorias, movimentações e relatórios, com arquitetura modular e interface intuitiva.

## ✨ Características Principais

### 🏗️ Arquitetura Modular
- **Separação clara de responsabilidades** com padrão MVC
- **Componentes reutilizáveis** e facilmente extensíveis
- **Sistema de views independentes** para cada funcionalidade
- **Gerenciamento centralizado de dados** com InventoryManager

### 🎨 Interface Moderna
- **Design responsivo** com CustomTkinter
- **Tema escuro/claro** configurável
- **Ícones e indicadores visuais** intuitivos
- **Navegação por abas** e menu lateral
- **Feedback visual** para todas as ações

### 📊 Funcionalidades Completas

#### 📦 Gestão de Produtos
- ✅ Cadastro completo com código, nome, categoria, preço
- ✅ Controle de estoque mínimo e alertas automáticos
- ✅ Busca avançada por múltiplos campos
- ✅ Edição em tempo real com validação
- ✅ Histórico de movimentações por produto

#### 🏢 Gestão de Fornecedores
- ✅ Cadastro com dados de contato completos
- ✅ Status ativo/inativo com filtros
- ✅ Busca por nome, contato, telefone, email
- ✅ Contagem automática de produtos por fornecedor
- ✅ Integração com sistema de produtos

#### 📂 Gestão de Categorias
- ✅ Organização hierárquica de produtos
- ✅ Descrições detalhadas
- ✅ Contagem automática de produtos por categoria
- ✅ Edição e exclusão com validação

#### 📈 Controle de Movimentações
- ✅ Registro automático de entradas e saídas
- ✅ Filtros por data (Hoje, Semana, Mês, Ano)
- ✅ Filtros por tipo (Entrada/Saída)
- ✅ Histórico completo com motivos
- ✅ Estatísticas em tempo real

#### 📋 Inventário Inteligente
- ✅ Visão consolidada do estoque
- ✅ Indicadores visuais de status (Normal/Baixo/Sem estoque)
- ✅ Cálculo automático de valores totais
- ✅ Filtros por status e busca textual
- ✅ Alertas de reposição

#### 📊 Dashboard e Relatórios
- ✅ Visão geral com métricas principais
- ✅ Gráficos de estoque e movimentações
- ✅ Relatórios de produtos em falta
- ✅ Análise de valor do inventário
- ✅ Estatísticas por categoria e fornecedor

### 🔍 Sistema de Filtros Avançado
- **Busca em tempo real** com tecla Enter
- **Filtros combinados** (status + texto)
- **Filtros por data** com períodos predefinidos
- **Interface sem popups** automáticos
- **Feedback visual** do número de resultados

## 🚀 Instalação e Configuração

### Pré-requisitos
```bash
Python 3.8+
pip (gerenciador de pacotes Python)
```

### Instalação Automática
```bash
# Clone o repositório
git clone [URL_DO_REPOSITORIO]
cd "Controle de Estoque"

# Execute o instalador automático
python install.py
```

### Instalação Manual
```bash
# Instalar dependências
pip install -r requirements.txt

# Ou instalar individualmente:
pip install customtkinter
pip install pillow
pip install tkinter
```

### Primeira Execução
```bash
# Gerar dados de teste (opcional)
python reset_database.py

# Executar o sistema
python main_modular.py
```

## 📁 Estrutura do Projeto

```
Controle de Estoque/
├── 📁 views/                    # Interface gráfica
│   ├── main_window.py          # Janela principal
│   ├── base_view.py            # Classe base para views
│   ├── dashboard_view.py       # Dashboard principal
│   ├── products_view.py        # Gestão de produtos
│   ├── suppliers_view.py       # Gestão de fornecedores
│   ├── categories_view.py      # Gestão de categorias
│   ├── movements_view.py       # Controle de movimentações
│   └── inventory_view.py       # Inventário consolidado
├── 📁 models/                   # Lógica de negócio
│   └── __init__.py             # InventoryManager
├── 📁 dialogs/                  # Diálogos modais
│   └── __init__.py             # ProductDialog, SupplierDialog, etc.
├── 📁 config/                   # Configurações
│   └── __init__.py             # Constantes e configurações
├── 📁 utils/                    # Utilitários
│   └── __init__.py             # Funções auxiliares
├── 📁 data/                     # Base de dados JSON
│   ├── products.json           # Produtos
│   ├── suppliers.json          # Fornecedores
│   ├── categories.json         # Categorias
│   ├── movements.json          # Movimentações
│   └── settings.json           # Configurações
├── 📁 docs/                     # Documentação
│   ├── MODULARIZACAO_COMPLETA.md
│   ├── CORREÇÕES_FINAIS.md
│   ├── MELHORIAS_FILTROS.md
│   ├── FIXES_APPLIED.md
│   ├── README_MODULAR.md
│   ├── README_LINUX_MINT.md
│   └── COMO_EDITAR.md
├── 📁 logs/                     # Logs do sistema
├── 📁 backups/                  # Backups automáticos
├── main_modular.py             # Ponto de entrada
├── reset_database.py           # Gerador de dados de teste
├── install.py                  # Instalador automático
├── requirements.txt            # Dependências
└── README_FINAL.md            # Esta documentação
```

## 🎮 Como Usar

### 1. Iniciando o Sistema
```bash
python main_modular.py
```

### 2. Navegação Principal
- **Dashboard**: Visão geral e métricas
- **Produtos**: Gestão completa de produtos
- **Fornecedores**: Cadastro e controle de fornecedores
- **Categorias**: Organização de produtos
- **Movimentações**: Histórico de entradas/saídas
- **Inventário**: Visão consolidada do estoque

### 3. Funcionalidades por Tela

#### 📦 Produtos
- **Adicionar**: Botão "Novo Produto" → Preencher formulário
- **Editar**: Duplo clique no produto ou botão "Editar"
- **Buscar**: Digite no campo de pesquisa + Enter ou botão "Filtrar"
- **Filtrar**: Use os botões "Filtrar" e "Limpar"

#### 🏢 Fornecedores
- **Filtros**: Status (Ativo/Inativo) + Busca textual
- **Busca**: Nome, contato, telefone, email
- **Edição**: Duplo clique ou botão "Editar"
- **Status**: Visualização de contatos e produtos por fornecedor

#### 📈 Movimentações
- **Filtros por Data**: Hoje, Última Semana, Último Mês, Último Ano
- **Filtros por Tipo**: Entrada, Saída, Todos
- **Aplicar**: Botão "Aplicar Filtros"
- **Estatísticas**: Resumo automático na interface

#### 📋 Inventário
- **Status**: Normal, Estoque Baixo, Sem Estoque
- **Busca**: Código, nome, categoria
- **Valores**: Cálculo automático de valores totais
- **Cores**: Indicadores visuais por status

### 4. Atalhos de Teclado
- **Enter**: Aplica filtros em campos de busca
- **Duplo clique**: Edita item selecionado
- **Esc**: Fecha diálogos

## 🔧 Configuração Avançada

### Personalização de Tema
```python
# Em config/__init__.py
THEME_MODE = "dark"  # ou "light"
COLOR_THEME = "blue"  # ou "green", "dark-blue"
```

### Configuração de Estoque
```python
# Limite de estoque baixo
DEFAULT_SETTINGS = {
    "low_stock_threshold": 5,
    "currency": "BRL",
    "auto_backup": True
}
```

### Backup Automático
O sistema cria backups automáticos dos dados em `backups/` a cada 7 dias.

## 🛠️ Desenvolvimento

### Adicionando Nova View
1. Criar arquivo em `views/nova_view.py`
2. Herdar de `BaseView`
3. Implementar `create_widgets()`
4. Adicionar ao menu principal

### Exemplo de Nova View
```python
from views.base_view import BaseView

class NovaView(BaseView):
    def __init__(self, parent, manager):
        super().__init__(parent, manager)
    
    def create_widgets(self):
        self.create_header("🆕 Nova Funcionalidade", "Descrição")
        # Implementar interface...
```

### Adicionando Novo Diálogo
```python
from dialogs import BaseDialog

class NovoDialog(BaseDialog):
    def create_widgets(self):
        # Implementar formulário...
        pass
    
    def save(self):
        # Implementar salvamento...
        pass
```

## 🐛 Solução de Problemas

### Problemas Comuns

#### Erro de Importação
```bash
# Verificar instalação das dependências
pip install -r requirements.txt

# Verificar versão do Python
python --version  # Deve ser 3.8+
```

#### Erro de Permissão
```bash
# Windows: Executar como administrador
# Linux: Verificar permissões da pasta
chmod 755 "Controle de Estoque"
```

#### Interface não Carrega
```bash
# Resetar configurações
python reset_database.py

# Verificar logs
cat logs/app.log
```

### Logs e Debug
- Logs salvos em `logs/app.log`
- Modo debug: Alterar `DEBUG = True` em `config/__init__.py`
- Teste de componentes: `python test_startup.py`

## 📈 Melhorias Implementadas

### v2.0 - Arquitetura Modular
- ✅ Refatoração completa para arquitetura MVC
- ✅ Separação de responsabilidades
- ✅ Sistema de views independentes
- ✅ Gerenciamento centralizado de dados

### v2.1 - Correções e Estabilidade
- ✅ Correção de erros de geometria (grid/pack)
- ✅ Implementação de métodos faltantes
- ✅ Melhoria na edição de produtos
- ✅ Correção de filtros de movimentação

### v2.2 - Sistema de Filtros Avançado
- ✅ Filtros por data em movimentações
- ✅ Busca textual em inventário
- ✅ Botões de filtro manuais (sem popups)
- ✅ Tecla Enter para aplicar filtros
- ✅ Feedback visual de resultados

### v2.3 - Melhorias na Interface
- ✅ Correção de campos de contato em fornecedores
- ✅ Filtros de status ativo/inativo
- ✅ Melhoria na exibição de dados
- ✅ Otimização de performance

## 🤝 Contribuição

### Como Contribuir
1. Fork do projeto
2. Criar branch para feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit das mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para branch (`git push origin feature/nova-funcionalidade`)
5. Criar Pull Request

### Padrões de Código
- **PEP 8** para formatação Python
- **Docstrings** para documentação de funções
- **Type hints** quando possível
- **Comentários** em português para clareza

## 📄 Licença

Este projeto está sob licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 📞 Suporte

### Documentação Adicional
- 📖 [Guia de Modularização](docs/MODULARIZACAO_COMPLETA.md)
- 🔧 [Correções Aplicadas](docs/CORREÇÕES_FINAIS.md)
- 🔍 [Sistema de Filtros](docs/MELHORIAS_FILTROS.md)
- 🐧 [Instalação Linux](docs/README_LINUX_MINT.md)
- ✏️ [Como Editar](docs/COMO_EDITAR.md)

### Contato
- **Issues**: Use o sistema de issues do GitHub
- **Discussões**: Seção de discussões do repositório
- **Email**: [seu-email@exemplo.com]

---

## 🎉 Agradecimentos

Obrigado por usar o Sistema de Controle de Estoque Avançado! Este projeto foi desenvolvido com foco na usabilidade, performance e extensibilidade.

**Versão**: 2.3  
**Última Atualização**: Dezembro 2024  
**Status**: ✅ Produção

---

*Desenvolvido com ❤️ em Python* 