"""
Página de Login do Sauce Demo
Contém os elementos e métodos para interagir com a página de login
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    """Classe que representa a página de login do Sauce Demo"""
    
    # Locators (localizadores dos elementos)
    CAMPO_USUARIO = (By.ID, "user-name")
    CAMPO_SENHA = (By.ID, "password")
    BOTAO_LOGIN = (By.ID, "login-button")
    MENSAGEM_ERRO = (By.CLASS_NAME, "error-message-container")
    
    def __init__(self, driver):
        """
        Inicializa a página de login
        
        Args:
            driver: Instância do WebDriver
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def acessar_pagina_login(self, url):
        """
        Acessa a página de login
        
        Args:
            url: URL da página de login
        """
        self.driver.get(url)
        print(f"Página de login acessada: {url}")
    
    def preencher_usuario(self, usuario):
        """
        Preenche o campo de usuário
        
        Args:
            usuario: Nome do usuário
        """
        campo_usuario = self.wait.until(
            EC.element_to_be_clickable(self.CAMPO_USUARIO)
        )
        campo_usuario.clear()
        campo_usuario.send_keys(usuario)
        print(f"Usuário preenchido: {usuario}")
    
    def preencher_senha(self, senha):
        """
        Preenche o campo de senha
        
        Args:
            senha: Senha do usuário
        """
        campo_senha = self.wait.until(
            EC.element_to_be_clickable(self.CAMPO_SENHA)
        )
        campo_senha.clear()
        campo_senha.send_keys(senha)
        print("Senha preenchida")
    
    def clicar_botao_login(self):
        """Clica no botão de login"""
        botao_login = self.wait.until(
            EC.element_to_be_clickable(self.BOTAO_LOGIN)
        )
        botao_login.click()
        print("Botão de login clicado")
    
    def fazer_login(self, usuario, senha):
        """
        Realiza o processo completo de login
        
        Args:
            usuario: Nome do usuário
            senha: Senha do usuário
        """
        self.preencher_usuario(usuario)
        self.preencher_senha(senha)
        self.clicar_botao_login()
    
    def verificar_se_login_foi_bem_sucedido(self):
        """
        Verifica se o login foi bem-sucedido
        (verifica se não está mais na página de login)
        
        Returns:
            bool: True se o login foi bem-sucedido, False caso contrário
        """
        try:
            # Se ainda estiver na página de login, o login falhou
            self.wait.until(EC.presence_of_element_located(self.BOTAO_LOGIN))
            return False
        except:
            return True
    
    def obter_mensagem_erro(self):
        """
        Obtém a mensagem de erro, se houver
        
        Returns:
            str: Mensagem de erro ou string vazia se não houver erro
        """
        try:
            elemento_erro = self.driver.find_element(*self.MENSAGEM_ERRO)
            return elemento_erro.text
        except:
            return ""
    
    def verificar_se_usuario_bloqueado(self):
        """
        Verifica se o usuário está bloqueado
        
        Returns:
            bool: True se o usuário está bloqueado, False caso contrário
        """
        try:
            mensagem_erro = self.obter_mensagem_erro()
            return "locked out" in mensagem_erro.lower()
        except:
            return False
