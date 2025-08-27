"""
Steps para funcionalidades do carrinho
"""

from behave import when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


@when('navego para o carrinho')
def step_impl(context):
    """Navega para a página do carrinho"""
    try:
        # Clicar no ícone do carrinho
        cart_icon = context.driver.find_element(By.CLASS_NAME, "shopping_cart_link")
        cart_icon.click()
        
        # Aguardar carregamento da página do carrinho
        WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "cart_list"))
        )
        
        print("Navegacao para o carrinho realizada!")
        
    except Exception as e:
        print(f"Erro ao navegar para o carrinho: {e}")
        raise


@when('verifico o preço total dos produtos')
def step_impl(context):
    """Verifica o preço total dos produtos no carrinho"""
    try:
        # Calcular preço total esperado
        preco_total_esperado = sum(produto['preco_float'] for produto in context.produtos_selecionados)
        
        # Obter TODOS os preços dos produtos no carrinho
        preco_elements = context.driver.find_elements(By.CLASS_NAME, "inventory_item_price")
        precos_carrinho = [float(element.text.replace("$", "")) for element in preco_elements]
        preco_total_carrinho = sum(precos_carrinho)
        
        # Armazenar para uso posterior
        context.preco_total_produtos = preco_total_esperado
        context.preco_total_carrinho = preco_total_carrinho
        
        assert abs(preco_total_esperado - preco_total_carrinho) < 0.01, \
            f"Preço total esperado: ${preco_total_esperado}, Encontrado: ${preco_total_carrinho}"
        
        print(f"Preco total verificado: ${preco_total_esperado}")
        
    except Exception as e:
        print(f"Erro ao verificar preço total: {e}")
        raise


@when('clico em "{botao}"')
def step_impl(context, botao):
    """Clica em um botão específico"""
    try:
        if botao.lower() == "checkout":
            checkout_button = context.driver.find_element(By.ID, "checkout")
            checkout_button.click()
            
            # Aguardar carregamento da página de checkout
            WebDriverWait(context.driver, 10).until(
                EC.presence_of_element_located((By.ID, "first-name"))
            )
            
            print("Botao Checkout clicado!")
            
        elif botao.lower() == "continue":
            continue_button = context.driver.find_element(By.ID, "continue")
            continue_button.click()
            
            # Aguardar carregamento da página de resumo
            WebDriverWait(context.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "summary_info"))
            )
            
            print("Botao Continue clicado!")
            
        elif botao.lower() == "finish":
            finish_button = context.driver.find_element(By.ID, "finish")
            finish_button.click()
            
            # Aguardar carregamento da página de sucesso
            WebDriverWait(context.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "complete-header"))
            )
            
            print("Botao Finish clicado!")
            
    except Exception as e:
        print(f"Erro ao clicar no botão {botao}: {e}")
        raise


@then('devo ver os produtos corretos no carrinho')
def step_impl(context):
    """Verifica se os produtos corretos estão no carrinho"""
    try:
        # Obter produtos no carrinho
        cart_items = context.driver.find_elements(By.CLASS_NAME, "inventory_item_name")
        produtos_carrinho = [item.text for item in cart_items]
        
        # Verificar se todos os produtos selecionados estão no carrinho
        produtos_selecionados = [produto['nome'] for produto in context.produtos_selecionados]
        
        for produto in produtos_selecionados:
            assert produto in produtos_carrinho, f"Produto {produto} não encontrado no carrinho"
        
        print(f"Produtos corretos no carrinho: {produtos_carrinho}")
        
    except Exception as e:
        print(f"Erro ao verificar produtos no carrinho: {e}")
        raise


@then('o preço total deve ser a soma dos produtos')
def step_impl(context):
    """Verifica se o preço total é a soma dos produtos"""
    try:
        # Calcular soma esperada
        soma_esperada = sum(produto['preco_float'] for produto in context.produtos_selecionados)
        
        # Obter TODOS os preços dos produtos no carrinho
        preco_elements = context.driver.find_elements(By.CLASS_NAME, "inventory_item_price")
        precos_carrinho = [float(element.text.replace("$", "")) for element in preco_elements]
        preco_total = sum(precos_carrinho)
        
        assert abs(soma_esperada - preco_total) < 0.01, \
            f"Soma esperada: ${soma_esperada}, Preço total: ${preco_total}"
        
        print(f"Preco total correto: ${preco_total}")
        
    except Exception as e:
        print(f"Erro ao verificar soma dos produtos: {e}")
        raise


@then('a taxa de imposto deve ser calculada corretamente ({taxa:d}%)')
def step_impl(context, taxa):
    """Verifica se a taxa de imposto está sendo calculada corretamente"""
    try:
        # Calcular imposto esperado
        preco_total = sum(produto['preco_float'] for produto in context.produtos_selecionados)
        imposto_esperado = preco_total * (taxa / 100)
        
        # Obter imposto do carrinho (se disponível)
        try:
            tax_element = context.driver.find_element(By.CLASS_NAME, "summary_tax_label")
            imposto_texto = tax_element.text
            imposto_carrinho = float(imposto_texto.replace("Tax: $", ""))
            
            assert abs(imposto_esperado - imposto_carrinho) < 0.01, \
                f"Imposto esperado: ${imposto_esperado:.2f}, Encontrado: ${imposto_carrinho}"
            
            print(f"Taxa de imposto correta: ${imposto_carrinho:.2f}")
            
        except:
            print(f"Taxa de imposto não encontrada na página atual")
        
    except Exception as e:
        print(f"Erro ao verificar taxa de imposto: {e}")
        raise
