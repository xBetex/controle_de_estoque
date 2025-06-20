# Sistema de Controle de Estoque - PyQt5

Uma versão moderna e profissional do sistema de controle de estoque, desenvolvida com **PyQt5** e arquitetura modular.

## 🎯 Características

### ✨ Interface Moderna
- **Interface nativa do PyQt5** com aparência profissional
- **Design Material Design** inspirado nas diretrizes do Google
- **Sidebar de navegação** intuitiva com ícones
- **Tabelas avançadas** com ordenação, filtros e seleção
- **Tema responsivo** que se adapta ao sistema operacional

### 🏗️ Arquitetura Modular
```
pyqt5_version/
├── config/           # Configurações e constantes
├── models/           # Modelos de dados e lógica de negócio
├── utils/            # Utilitários e funções auxiliares
├── views/            # Interfaces de usuário (views)
├── main.py           # Ponto de entrada da aplicação
├── requirements.txt  # Dependências do projeto
└── README.md         # Esta documentação
```

### 📊 Funcionalidades Principais

#### Dashboard Inteligente
- **Cartões de estatísticas** em tempo real
- **Alertas automáticos** para estoque baixo
- **Atividades recentes** com histórico
- **Atualização automática** a cada 30 segundos

#### Gerenciamento de Produtos
- **CRUD completo** (Criar, Ler, Atualizar, Deletar)
- **Busca avançada** por nome, código ou descrição
- **Filtros dinâmicos** por categoria, fornecedor, estoque
- **Validação de dados** com regras de negócio

#### Controle de Estoque
- **Movimentações automáticas** com histórico completo
- **Alertas de estoque baixo** configuráveis
- **Relatórios de entrada/saída** detalhados
- **Auditoria completa** de todas as operações

#### Fornecedores e Categorias
- **Gestão completa** de fornecedores
- **Categorização hierárquica** de produtos
- **Relatórios por fornecedor/categoria**
- **Validação de email e telefone**

## 🚀 Instalação e Execução

### Pré-requisitos
- **Python 3.7+** instalado
- **pip** para gerenciamento de pacotes

### 1. Instalação das Dependências
```bash
cd pyqt5_version
pip install -r requirements.txt
```

### 2. Geração de Dados de Exemplo (Opcional)
```bash
python generate_sample_data.py
```

### 3. Execução do Sistema
```bash
python main.py
```

## 📦 Dependências

| Dependência | Versão | Propósito |
|-------------|--------|-----------|
| **PyQt5** | ≥5.15.0 | Interface gráfica moderna |
| **matplotlib** | ≥3.7.0 | Gráficos e relatórios |
| **pandas** | ≥2.0.0 | Manipulação de dados |
| **openpyxl** | ≥3.1.0 | Export/import Excel |
| **reportlab** | ≥4.0.0 | Geração de relatórios PDF |
| **numpy** | ≥1.24.0 | Cálculos matemáticos |

## 🏛️ Arquitetura do Sistema

### Padrão MVC (Model-View-Controller)

#### **Models** (`models/`)
- `InventoryManager`: Classe principal com lógica de negócio
- **Signals PyQt5** para comunicação reativa entre componentes
- **Persistência em JSON** para simplicidade e portabilidade
- **Validação de dados** integrada

#### **Views** (`views/`)
- `MainWindow`: Janela principal com navegação
- `DashboardView`: Dashboard com estatísticas
- `ProductsView`: Gerenciamento de produtos
- `InventoryView`: Controle de estoque
- `MovementsView`: Histórico de movimentações
- Outras views especializadas...

#### **Configuration** (`config/`)
- **Constantes do sistema** (cores, fontes, tamanhos)
- **Estilos CSS** para componentes
- **Configurações de validação**
- **Definições de colunas** das tabelas

#### **Utils** (`utils/`)
- **Funções utilitárias** reutilizáveis
- **Formatação** de dados (moeda, data, telefone)
- **Validação** de campos
- **MessageBox** e **FileDialog** customizados

## 🎨 Design System

### Cores Principais
- **Primary**: `#1976D2` (Azul Material)
- **Success**: `#4CAF50` (Verde)
- **Warning**: `#FF9800` (Laranja)
- **Error**: `#F44336` (Vermelho)
- **Info**: `#2196F3` (Azul claro)

### Tipografia
- **Títulos**: Arial Bold 16px
- **Subtítulos**: Arial Bold 14px
- **Corpo**: Arial Regular 10px
- **Legendas**: Arial Regular 9px

### Componentes Padronizados
- **Botões primários/secundários** com hover effects
- **Campos de entrada** com focus states
- **Tabelas** com alternating rows e seleção
- **Cards** com sombras e bordas arredondadas

## 🔧 Configuração Avançada

### Personalização de Temas
Edite o arquivo `config/__init__.py` para personalizar:
- Cores do sistema
- Fontes e tamanhos
- Estilos CSS
- Ícones e emojis

### Banco de Dados
O sistema usa **JSON** por padrão, mas pode ser facilmente adaptado para:
- SQLite
- PostgreSQL
- MySQL
- MongoDB

### Localização
Atualmente em **Português (pt-BR)**, mas preparado para:
- Inglês (en-US)
- Espanhol (es-ES)
- Outros idiomas

## 🔒 Vantagens do PyQt5

### Comparado ao CustomTkinter:

| Aspecto | PyQt5 | CustomTkinter |
|---------|-------|---------------|
| **Performance** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Aparência** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Widgets** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Estabilidade** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Documentação** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Comunidade** | ⭐⭐⭐⭐⭐ | ⭐⭐ |

### Principais Benefícios:
- ✅ **Interface nativa** do sistema operacional
- ✅ **Performance superior** para tabelas grandes
- ✅ **Widgets avançados** (QTableWidget, QTreeView, etc.)
- ✅ **Sistema de sinais/slots** robusto
- ✅ **Suporte completo** a threading
- ✅ **Internacionalização** built-in
- ✅ **Estabilidade comprovada** em aplicações empresariais

## 🛠️ Desenvolvimento

### Estrutura de Commits
```
feat: nova funcionalidade
fix: correção de bug
docs: documentação
style: formatação
refactor: refatoração
test: testes
chore: manutenção
```

### Próximas Funcionalidades
- [ ] Sistema de usuários e permissões
- [ ] Relatórios avançados com gráficos
- [ ] Export/import de dados
- [ ] Backup automático
- [ ] API REST
- [ ] Versão web complementar
- [ ] App mobile de consulta

## 📞 Suporte

### Problemas Comuns

**Erro de importação do PyQt5:**
```bash
pip install PyQt5
# ou
conda install pyqt
```

**Fonte não encontrada:**
- O sistema usa fontes padrão do sistema
- Em Linux, instale: `sudo apt-get install fonts-liberation`

**Performance lenta:**
- Verifique a versão do Python (recomendado 3.8+)
- Use SSD para armazenamento de dados
- Monitore o uso de memória

## 📄 Licença

Este projeto é distribuído sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🤝 Contribuição

Contribuições são bem-vindas! Por favor:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'feat: adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

---

**Desenvolvido com ❤️ usando PyQt5**

*Sistema moderno, profissional e escalável para controle de estoque empresarial.* 