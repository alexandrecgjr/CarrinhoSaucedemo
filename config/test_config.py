"""
Configurações centralizadas para os testes de automação
"""

class TestConfig:
    """Configurações centralizadas para os testes"""
    
    # URLs
    BASE_URL = "https://www.saucedemo.com/"
    LOGIN_URL = f"{BASE_URL}"
    PRODUCTS_URL = f"{BASE_URL}inventory.html"
    CART_URL = f"{BASE_URL}cart.html"
    CHECKOUT_URL = f"{BASE_URL}checkout-step-one.html"
    
    # Timeouts
    DEFAULT_TIMEOUT = 10
    SHORT_TIMEOUT = 5
    LONG_TIMEOUT = 20
    
    # Dados de teste
    TEST_DATA_FILE = "data/users.json"
    
    # Diretórios
    SCREENSHOTS_DIR = "screenshots"
    REPORTS_DIR = "reports"
    LOGS_DIR = "logs"
    
    # Taxa de imposto esperada
    TAXA_IMPOSTO_ESPERADA = 0.08  # 8%
    
    # Tolerância para validações de preço
    TOLERANCIA_PRECO = 0.01
    
    # Configurações do navegador
    BROWSER_HEADLESS = False
    BROWSER_WINDOW_SIZE = "--window-size=1920,1080"
    
    # Configurações de teste
    QUANTIDADE_PRODUTOS_PADRAO = 2
    MAX_TENTATIVAS_RETRY = 3
