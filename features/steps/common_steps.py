"""
Steps comuns para BDD - Setup e Teardown
"""

from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from datetime import datetime


@given('que estou na página de login do Sauce Demo')
def step_impl(context):
    """Configura o driver e navega para a página de login"""
    # Configurar Chrome Options
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Configurações anti-detecção
    chrome_options.add_experimental_option(
        "prefs", {
            "profile.password_manager_leak_detection": False,
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False
        }
    )
    
    # Inicializar WebDriver
    try:
        service = Service(ChromeDriverManager().install())
        context.driver = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        print(f"Erro ao inicializar ChromeDriverManager: {e}")
        context.driver = webdriver.Chrome(options=chrome_options)
    
    # Executar script para remover webdriver
    context.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    # Navegar para a página
    context.driver.get("https://www.saucedemo.com/")
    context.base_url = "https://www.saucedemo.com/"
    
    # Aguardar carregamento
    time.sleep(2)


@when('aguardo {segundos:d} segundos')
def step_impl(context, segundos):
    """Aguarda um número específico de segundos"""
    time.sleep(segundos)


@then('tirei um screenshot')
def step_impl(context, name=None):
    """Tira um screenshot da página atual"""
    if not name:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        name = f"screenshot_{timestamp}"
    
    # Criar diretório se não existir
    os.makedirs("screenshots", exist_ok=True)
    
    # Salvar screenshot
    screenshot_path = f"screenshots/{name}.png"
    context.driver.save_screenshot(screenshot_path)
    print(f"Screenshot salvo: {screenshot_path}")


def after_scenario(context, scenario):
    """Executado após cada cenário"""
    if hasattr(context, 'driver') and context.driver:
        # Tirar screenshot em caso de falha
        if scenario.status == "failed":
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_name = f"falha_{scenario.name.replace(' ', '_')}_{timestamp}"
            step_impl(context, screenshot_name)
        
        # Fechar driver
        context.driver.quit()


def after_all(context):
    """Executado após todos os cenários"""
    print("Todos os cenarios BDD foram executados!")
    print("Screenshots disponiveis em: screenshots/")
    print("Relatorios disponiveis em: reports/")
