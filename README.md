# 🛒 Automação de Testes - Sauce Demo

Projeto de automação de testes para validar o fluxo completo de compra no ambiente demo do Sauce Demo (https://www.saucedemo.com/).

## 📋 Descrição

Este projeto implementa testes automatizados usando **Python**, **Selenium**, **Pytest** e **BDD (Behave)** para validar:

- ✅ Login com diferentes tipos de usuários
- ✅ Seleção aleatória de produtos
- ✅ Validação de preços e impostos (8%)
- ✅ Fluxo completo de checkout
- ✅ Geração de relatórios HTML e Allure
- ✅ Captura de screenshots em caso de falha
- ✅ Testes data-driven com múltiplos usuários
- ✅ **BDD (Behavior Driven Development)** com Gherkin

## 🚀 Funcionalidades

### Usuários Testados
- **standard_user**: Usuário padrão válido
- **locked_out_user**: Usuário bloqueado
- **problem_user**: Usuário com problemas de interface
- **performance_glitch_user**: Usuário com problemas de performance
- **error_user**: Usuário que gera erros
- **visual_user**: Usuário com problemas visuais

### Fluxo de Teste
1. **Login** → Acesso com credenciais válidas
2. **Seleção de Produtos** → 2 produtos aleatórios adicionados ao carrinho
3. **Validação de Preços** → Confirmação do subtotal e taxa de imposto (8%)
4. **Checkout** → Preenchimento de dados pessoais
5. **Finalização** → Confirmação da compra

## 📁 Estrutura do Projeto

```
CarrinhoSaucedemo/
├── features/                     # 🆕 Arquivos BDD (Gherkin)
│   ├── fluxo_compra.feature     # Cenários de teste em linguagem natural
│   └── steps/                   # Implementação dos steps BDD
│       ├── __init__.py
│       ├── common_steps.py      # Setup e teardown
│       ├── login_steps.py       # Steps de login
│       ├── product_steps.py     # Steps de produtos
│       ├── cart_steps.py        # Steps do carrinho
│       └── checkout_steps.py    # Steps de checkout
├── pages/                       # Page Object Model
│   ├── login_page.py           # Página de login
│   ├── products_page.py        # Página de produtos
│   ├── cart_page.py            # Página do carrinho
│   └── checkout_page.py        # Página de checkout
├── utils/
│   └── webdriver_config.py     # Configuração do WebDriver
├── reports/                     # Relatórios gerados
│   ├── behave_report.txt       # 🆕 Relatório Behave
│   ├── allure-results/         # Resultados Allure
│   └── allure-report/          # Relatório Allure HTML
├── screenshots/                 # Screenshots capturados
├── test_sauce_demo.py          # Testes Pytest (legado)
├── run_tests.py                # Script de execução Pytest
├── run_bdd_tests.py            # 🆕 Script de execução BDD
├── behave.ini                  # 🆕 Configuração Behave
├── requirements.txt            # Dependências atualizadas
└── README.md                   # Este arquivo
```

## 🛠️ Tecnologias Utilizadas

### 🆕 **BDD (Behavior Driven Development)**
- **Behave 1.2.6**: Framework BDD para Python
- **Gherkin**: Linguagem para escrita de cenários
- **allure-behave 2.13.2**: Integração Allure com Behave

### **Automação Web**
- **Selenium 4.15.2**: Automação de navegador
- **WebDriver Manager 4.0.1**: Gerenciamento automático de drivers
- **Chrome Options**: Configurações anti-detecção

### **Frameworks de Teste**
- **Pytest 7.4.3**: Framework de testes (implementação original)
- **Behave 1.2.6**: Framework BDD (implementação atual)

### **Relatórios e Evidências**
- **Allure 2.13.2**: Relatórios avançados
- **pytest-html 4.1.1**: Relatórios HTML básicos
- **Screenshots automáticos**: Captura em caso de falha

### **Utilitários**
- **Faker**: Geração de dados fake
- **Pillow**: Processamento de imagens
- **pytest-xdist**: Execução paralela

## ⚙️ Instalação

1. **Clone o repositório:**
```bash
git clone https://github.com/alexandrecgjr/CarrinhoSaucedemo.git
cd CarrinhoSaucedemo
```

2. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

3. **Verifique a instalação:**
```bash
python -c "import selenium, behave; print('Dependências instaladas com sucesso!')"
```

## 🎯 Como Executar

### 🆕 **Execução BDD (Recomendado)**
```bash
# Executar todos os testes BDD
python run_bdd_tests.py

# Executar cenários específicos
behave features/fluxo_compra.feature --tags=@fluxo_completo --verbose

# Executar apenas validações
behave features/fluxo_compra.feature --tags=@validacao_produtos --verbose
```

### **Execução Pytest (Legado)**
```bash
# Executar testes Pytest
python run_tests.py

# Executar com Pytest direto
pytest test_sauce_demo.py -v

# Executar com relatório HTML
pytest test_sauce_demo.py --html=reports/report.html --self-contained-html
```

### **Executar Testes Específicos**

#### BDD (Behave)
```bash
# Apenas fluxo completo
behave --tags=@fluxo_completo

# Apenas validações
behave --tags=@validacao_produtos

# Apenas login bloqueado
behave --tags=@login_bloqueado
```

#### Pytest (Legado)
```bash
# Apenas testes de login
pytest test_sauce_demo.py::TestSauceDemo::test_login_usuarios_validos -v

# Apenas fluxo completo
pytest test_sauce_demo.py::TestSauceDemo::test_fluxo_completo_compra -v
```

## 📊 Relatórios

### 🆕 **Relatório Behave**
- **Localização**: `reports/behave_report.txt`
- **Conteúdo**: Resumo detalhado dos cenários BDD
- **Formato**: Texto estruturado

### **Relatório Allure**
- **Localização**: `reports/allure-report/`
- **Conteúdo**: Relatório detalhado com screenshots, logs, métricas
- **Visualização**: `allure open reports/allure-report`

### **Relatório HTML (Pytest)**
- **Localização**: `reports/report.html`
- **Conteúdo**: Resumo dos testes Pytest
- **Visualização**: Abrir no navegador

### **Screenshots**
- **Localização**: `screenshots/`
- **Captura**: Automática em caso de falha
- **Nomenclatura**: `falha_[nome_cenario]_[timestamp].png`

## 🆕 **Cenários BDD Implementados**

### **Fluxo Completo de Compra**
```gherkin
@fluxo_completo @usuario_valido
Cenário: Fluxo completo de compra com usuário válido
  Dado que estou na página de login do Sauce Demo
  Quando faço login com usuário "standard_user" e senha "secret_sauce"
  E seleciono dois produtos aleatórios
  E adiciono os produtos ao carrinho
  E verifico que os produtos foram adicionados corretamente
  E navego para o carrinho
  E verifico o preço total dos produtos
  E clico em "Checkout"
  E preencho as informações de checkout
  E verifico o resumo da compra
  E confirmo a compra
  Então devo ver a mensagem de sucesso "Thank you for your order!"
```

## 🔧 Configurações

### **WebDriver**
- **Navegador**: Chrome (padrão)
- **Modo**: Headless (configurável)
- **Timeout**: 10 segundos (configurável)
- **Anti-detecção**: Configurações implementadas

### **Behave (BDD)**
- **Formato**: Pretty (configurável)
- **Logs**: Nível INFO
- **Screenshots**: Automáticos em falhas
- **Tags**: Organização por tipos de teste

### **Pytest (Legado)**
- **Paralelização**: Suportada via pytest-xdist
- **Retry**: Configurável para testes instáveis
- **Markers**: Organização por tipos de teste

## 🐛 Troubleshooting

### **Problemas Comuns**

1. **Chrome não encontrado:**
```bash
# Instalar ChromeDriver
pip install webdriver-manager
```

2. **Erro de timeout:**
```bash
# Aumentar timeout nos testes
# Editar utils/webdriver_config.py
```

3. **Falha no login:**
```bash
# Verificar credenciais no feature file
# Verificar conectividade com saucedemo.com
```

4. **Relatório não gerado:**
```bash
# Verificar permissões de escrita
# Verificar se diretório reports/ existe
```

5. **Behave não encontrado:**
```bash
# Instalar Behave
pip install behave==1.2.6
```

### **Logs e Debug**
```bash
# Executar BDD com logs detalhados
behave --verbose --log-cli-level=DEBUG

# Executar Pytest com logs detalhados
pytest test_sauce_demo.py -v -s --log-cli-level=DEBUG
```

## 📝 **Melhorias Implementadas**

### **🆕 BDD (Behavior Driven Development)**
- ✅ Implementação completa com Behave
- ✅ Cenários escritos em Gherkin
- ✅ Steps organizados por funcionalidade
- ✅ 100% de sucesso nos testes

### **🆕 Correções de Bugs**
- ✅ **Cálculo de preços corrigido**: Soma todos os produtos no carrinho
- ✅ **Fluxo de checkout corrigido**: Implementação completa do processo
- ✅ **Steps não implementados**: Todos os steps agora funcionais

### **🆕 Arquitetura Melhorada**
- ✅ **Separação de responsabilidades**: Steps organizados por módulo
- ✅ **Configuração robusta**: WebDriver com fallbacks
- ✅ **Relatórios avançados**: Behave + Allure integrados

## 👥 Autor

- **Alexandre C**
