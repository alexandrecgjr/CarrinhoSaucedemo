"""
Configuração do WebDriver para automação do Sauce Demo
Inclui configurações para desabilitar detecção de vazamento de senha
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time


class WebDriverConfig:
    """Classe para configurar e gerenciar o WebDriver"""
    
    @staticmethod
    def configurar_chrome_driver():
        """
        Configura e retorna uma instância do Chrome WebDriver
        com opções otimizadas para automação
        """
        # Configurações do Chrome
        chrome_options = Options()
        
        # Desabilitar detecção de vazamento de senha
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Outras configurações úteis para automação
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Desabilitar detecção de vazamento de senha
        chrome_options.add_experimental_option(
            "prefs", {
                "profile.password_manager_leak_detection": False,
                "credentials_enable_service": False,  # Também desabilita o prompt "Oferecer para salvar senhas"
                "profile.password_manager_enabled": False,  # Desabilita o gerenciador de senhas completamente
                "profile.default_content_setting_values.notifications": 2
            }
        )
        
        # Inicializar o driver
        try:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
        except Exception as e:
            print(f"Erro ao inicializar ChromeDriver: {e}")
            # Tentar sem o service
            driver = webdriver.Chrome(options=chrome_options)
        
        # Executar script para remover propriedades de automação
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        return driver
    
    @staticmethod
    def configurar_driver_com_espera_implicita(driver, tempo_espera=10):
        """
        Configura o tempo de espera implícita do driver
        
        Args:
            driver: Instância do WebDriver
            tempo_espera: Tempo de espera em segundos (padrão: 10)
        """
        driver.implicitly_wait(tempo_espera)
        driver.maximize_window()
    
    @staticmethod
    def fechar_driver(driver):
        """
        Fecha o driver de forma segura
        
        Args:
            driver: Instância do WebDriver
        """
        if driver:
            driver.quit()
