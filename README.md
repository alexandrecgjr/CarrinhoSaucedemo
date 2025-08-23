# 🛒 Automação de Testes - Sauce Demo

Projeto de automação de testes para validar o fluxo completo de compra no ambiente demo do Sauce Demo (https://www.saucedemo.com/).

## 📋 Descrição

Este projeto implementa testes automatizados usando Python, Selenium e Pytest para validar:

- ✅ Login com diferentes tipos de usuários
- ✅ Seleção aleatória de produtos
- ✅ Validação de preços e impostos (8%)
- ✅ Fluxo completo de checkout
- ✅ Geração de relatórios HTML e Allure
- ✅ Captura de screenshots em caso de falha
- ✅ Testes data-driven com múltiplos usuários

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
├── data/
│   └── users.json                 # Dados de teste (usuários e checkout)
├── pages/
│   ├── login_page.py             # Página de login
│   ├── products_page.py          # Página de produtos
│   ├── cart_page.py              # Página do carrinho
│   └── checkout_page.py          # Página de checkout
├── utils/
│   ├── webdriver_config.py       # Configuração do WebDriver
│   ├── report_utils.py           # Utilitários de relatório
│   └── test_data_loader.py       # Carregador de dados de teste
├── reports/                      # Relatórios gerados
├── screenshots/                  # Screenshots capturados
├── test_fluxo_completo_compra.py # Testes principais
├── run_tests.py                  # Script de execução
├── requirements.txt              # Dependências
└── README.md                     # Este arquivo
```

## 🛠️ Pré-requisitos

- Python 3.8 ou superior
- Chrome/Chromium instalado
- pip (gerenciador de pacotes Python)

## ⚙️ Instalação

1. **Clone o repositório:**
```bash
git clone <url-do-repositorio>
cd CarrinhoSaucedemo
```

2. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

3. **Verifique a instalação:**
```bash
python -c "import selenium; print('Selenium instalado com sucesso!')"
```

## 🎯 Como Executar

### Execução Simples
```bash
python run_tests.py
```

### Execução com Pytest Direto
```bash
# Executar todos os testes
pytest test_fluxo_completo_compra.py -v

# Executar com relatório HTML
pytest test_fluxo_completo_compra.py --html=reports/report.html --self-contained-html

# Executar com Allure
pytest test_fluxo_completo_compra.py --alluredir=reports/allure-results
allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allure-report
```

### Executar Testes Específicos
```bash
# Apenas testes de login
pytest test_fluxo_completo_compra.py::TestFluxoCompletoCompra::test_login_usuarios_validos -v

# Apenas fluxo completo
pytest test_fluxo_completo_compra.py::TestFluxoCompletoCompra::test_fluxo_completo_compra -v
```

## 📊 Relatórios

### Relatório HTML
- **Localização**: `reports/report.html`
- **Conteúdo**: Resumo dos testes, status, duração, erros
- **Visualização**: Abrir no navegador

### Relatório Allure
- **Localização**: `reports/allure-report/`
- **Conteúdo**: Relatório detalhado com screenshots, logs, métricas
- **Visualização**: `allure open reports/allure-report`

### Screenshots
- **Localização**: `screenshots/`
- **Captura**: Automática em caso de falha
- **Nomenclatura**: `falha_[nome_teste]_[timestamp].png`

## 📝 Dados de Teste

### Arquivo users.json
```json
{
  "usuarios": [
    {
      "username": "standard_user",
      "password": "secret_sauce",
      "tipo": "valido",
      "descricao": "Usuário padrão válido"
    }
  ],
  "dados_checkout": [
    {
      "first_name": "João",
      "last_name": "Silva",
      "zip_code": "12345-678"
    }
  ]
}
```

### Adicionar Novos Usuários
1. Edite o arquivo `data/users.json`
2. Adicione novos usuários na seção "usuarios"
3. Adicione novos dados de checkout na seção "dados_checkout"

## 🔧 Configurações

### WebDriver
- **Navegador**: Chrome (padrão)
- **Modo**: Headless (configurável)
- **Timeout**: 10 segundos (configurável)

### Testes
- **Paralelização**: Suportada via pytest-xdist
- **Retry**: Configurável para testes instáveis
- **Markers**: Organização por tipos de teste

## 🐛 Troubleshooting

### Problemas Comuns

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
# Verificar credenciais em data/users.json
# Verificar conectividade com saucedemo.com
```

4. **Relatório não gerado:**
```bash
# Verificar permissões de escrita
# Verificar se diretório reports/ existe
```

### Logs e Debug
```bash
# Executar com logs detalhados
pytest test_fluxo_completo_compra.py -v -s --log-cli-level=DEBUG

# Verificar logs do navegador
# Implementado em utils/report_utils.py
```

## 📈 Métricas e KPIs

### Métricas Coletadas
- **Tempo de execução** por teste
- **Taxa de sucesso** geral
- **Screenshots** de falhas
- **Logs** de console e performance
- **Dados de teste** utilizados

### Relatórios Disponíveis
- **HTML**: Resumo executivo
- **Allure**: Relatório detalhado
- **JSON**: Dados estruturados
- **JUnit XML**: Compatível com CI/CD

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👥 Autores

- **Seu Nome** - *Desenvolvimento inicial* - [SeuGitHub](https://github.com/seugithub)

## 🙏 Agradecimentos

- Sauce Labs pelo ambiente de teste demo
- Comunidade Python/Selenium
- Contribuidores do projeto

---

**Última atualização**: Dezembro 2024
**Versão**: 1.0.0


