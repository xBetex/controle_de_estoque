# 📦 Sistema de Controle de Estoque Avançado v2.0

Um sistema moderno e profissional para gerenciamento de estoque com interface gráfica intuitiva.

## ✨ Características Principais

### 🎯 Funcionalidades Implementadas
- **Dashboard Interativo**: Visão geral com estatísticas em tempo real
- **Gerenciamento de Produtos**: CRUD completo com interface moderna
- **Controle de Estoque**: Ajustes de entrada e saída com histórico
- **Busca Avançada**: Pesquisa por nome, código ou descrição
- **Interface Responsiva**: Layout adaptável e moderno

### 🚀 Funcionalidades em Desenvolvimento
- **Relatórios Avançados**: Gráficos e análises detalhadas
- **Gestão de Fornecedores**: Controle completo de fornecedores
- **Categorias**: Organização por categorias
- **Movimentações**: Histórico detalhado de todas as operações
- **Backup Automático**: Sistema de backup e recuperação
- **Configurações**: Personalização completa do sistema

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+**
- **CustomTkinter**: Interface gráfica moderna
- **Matplotlib**: Gráficos e visualizações
- **Pandas**: Manipulação de dados
- **PIL (Pillow)**: Processamento de imagens
- **JSON**: Armazenamento de dados

## 📋 Pré-requisitos

- Python 3.8 ou superior
- Pip (gerenciador de pacotes Python)

## 🚀 Instalação

1. **Clone ou baixe o projeto**
   ```bash
   git clone [URL_DO_REPOSITORIO]
   cd controle-estoque
   ```

2. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

3. **Execute o sistema**
   ```bash
   python main.py
   ```

## 📊 Como Usar

### 1. **Dashboard**
- Visualize estatísticas gerais do estoque
- Acompanhe produtos com estoque baixo
- Veja as atividades recentes

### 2. **Gerenciamento de Produtos**
- **Adicionar**: Clique em "➕ Novo Produto" para cadastrar
- **Editar**: Clique com botão direito em um produto → "✏️ Editar"
- **Ajustar Estoque**: Clique com botão direito → "🔄 Ajustar Estoque"
- **Excluir**: Clique com botão direito → "🗑️ Excluir"

### 3. **Busca de Produtos**
- Use a barra de pesquisa para encontrar produtos rapidamente
- Busque por nome, código ou descrição

## 📁 Estrutura dos Dados

O sistema armazena os dados em arquivos JSON na pasta `data/`:

- `products.json`: Informações dos produtos
- `movements.json`: Histórico de movimentações
- `suppliers.json`: Dados dos fornecedores
- `categories.json`: Categorias dos produtos
- `settings.json`: Configurações do sistema

## 🔧 Configurações

### Personalização do Sistema
- **Tema**: Claro, escuro ou automático
- **Limite de Estoque Baixo**: Configurável (padrão: 5 unidades)
- **Backup Automático**: Ativação e frequência configuráveis

## 📈 Campos de Produto

### Obrigatórios
- **Código**: Identificador único do produto
- **Nome**: Nome descritivo do produto
- **Preço**: Valor unitário em R$
- **Quantidade**: Quantidade em estoque

### Opcionais
- **Descrição**: Descrição detalhada
- **Fornecedor**: Nome do fornecedor
- **Categoria**: Categoria do produto
- **Localização**: Local de armazenamento
- **Código de Barras**: Para leitura automática
- **Peso**: Peso em quilogramas
- **Dimensões**: Dimensões do produto

## 🎨 Interface

### Design Moderno
- **Dark Mode**: Interface escura por padrão
- **Ícones Intuitivos**: Navegação visual clara
- **Cores Contextuais**: Status visuais (verde=disponível, amarelo=baixo, vermelho=esgotado)
- **Layout Responsivo**: Adapta-se ao tamanho da janela

### Navegação
- **Sidebar**: Menu lateral com todas as funcionalidades
- **Breadcrumbs**: Navegação hierárquica
- **Atalhos**: Teclas de atalho para ações comuns

## 🔒 Segurança

- **Confirmações**: Diálogos de confirmação para ações críticas
- **Validação**: Validação de dados de entrada
- **Backup**: Sistema de backup automático (em desenvolvimento)

## 📊 Relatórios (Em Desenvolvimento)

- **Produtos em Falta**: Lista de produtos com estoque baixo
- **Valor do Estoque**: Valor total inventariado
- **Movimentações**: Relatório de entradas e saídas
- **Gráficos**: Visualizações estatísticas

## 🐛 Solução de Problemas

### Erro de Dependências
```bash
pip install --upgrade -r requirements.txt
```

### Erro de Permissão na Pasta
- Certifique-se que tem permissão de escrita na pasta do projeto
- Execute como administrador se necessário

### Interface não Carrega
- Verifique se o CustomTkinter está atualizado
- Reinstale as dependências

## 🔄 Atualizações Futuras

### Versão 2.1 (Planejada)
- [ ] Sistema completo de relatórios
- [ ] Gestão de fornecedores
- [ ] Categorias dinâmicas
- [ ] Import/Export Excel
- [ ] Código de barras

### Versão 2.2 (Planejada)
- [ ] Sistema multi-usuário
- [ ] Permissões de acesso
- [ ] Backup na nuvem
- [ ] API REST
- [ ] Mobile app

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👨‍💻 Desenvolvedor

Desenvolvido com ❤️ usando Python e CustomTkinter

---

**Versão:** 2.0.0  
**Status:** Em Desenvolvimento Ativo  
**Última Atualização:** Dezembro 2024 