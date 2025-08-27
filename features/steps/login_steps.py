"""
Steps para funcionalidades de login
"""

from behave import when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


@when('faço login com usuário "{username}" e senha "{password}"')
def step_impl(context, username, password):
    """Realiza login com usuário e senha específicos"""
    # Localizar elementos
    username_field = context.driver.find_element(By.ID, "user-name")
    password_field = context.driver.find_element(By.ID, "password")
    login_button = context.driver.find_element(By.ID, "login-button")
    
    # Limpar campos e preencher
    username_field.clear()
    username_field.send_keys(username)
    
    password_field.clear()
    password_field.send_keys(password)
    
    # Clicar no botão de login
    login_button.click()
    
    # Aguardar carregamento
    time.sleep(2)


@then('devo ver a mensagem de erro "{mensagem}"')
def step_impl(context, mensagem):
    """Verifica se a mensagem de erro está presente"""
    try:
        # Aguardar elemento de erro
        error_element = WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "error-message-container"))
        )
        
        # Verificar se a mensagem contém o texto esperado
        assert mensagem in error_element.text, f"Mensagem esperada: '{mensagem}', Encontrada: '{error_element.text}'"
        print(f"Mensagem de erro encontrada: {error_element.text}")
        
    except Exception as e:
        print(f"Erro ao verificar mensagem: {e}")
        raise


@then('devo estar logado com sucesso')
def step_impl(context):
    """Verifica se o login foi bem-sucedido"""
    try:
        # Verificar se estamos na página de produtos
        WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "inventory_list"))
        )
        
        # Verificar se o botão do menu está presente
        menu_button = context.driver.find_element(By.ID, "react-burger-menu-btn")
        assert menu_button.is_displayed(), "Menu button não está visível"
        
        print("Login realizado com sucesso!")
        
    except Exception as e:
        print(f"Erro ao verificar login: {e}")
        raise


@then('devo ver a mensagem de sucesso "{mensagem}"')
def step_impl(context, mensagem):
    """Verifica se a mensagem de sucesso está presente"""
    try:
        # Aguardar elemento de sucesso
        success_element = WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "complete-header"))
        )
        
        # Verificar se a mensagem contém o texto esperado
        assert mensagem in success_element.text, f"Mensagem esperada: '{mensagem}', Encontrada: '{success_element.text}'"
        print(f"Mensagem de sucesso encontrada: {success_element.text}")
        
    except Exception as e:
        print(f"Erro ao verificar mensagem de sucesso: {e}")
        raise
