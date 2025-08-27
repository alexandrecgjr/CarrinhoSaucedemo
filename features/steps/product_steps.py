"""
Steps para funcionalidades de produtos
"""

from behave import when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time


@when('seleciono dois produtos aleatórios')
def step_impl(context):
    """Seleciona dois produtos aleatórios da lista"""
    try:
        # Aguardar carregamento da lista de produtos
        WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "inventory_list"))
        )
        
        # Encontrar todos os produtos
        produtos = context.driver.find_elements(By.CLASS_NAME, "inventory_item")
        
        # Selecionar dois produtos aleatórios
        produtos_selecionados = random.sample(produtos, 2)
        
        # Armazenar informações dos produtos selecionados
        context.produtos_selecionados = []
        
        for produto in produtos_selecionados:
            nome = produto.find_element(By.CLASS_NAME, "inventory_item_name").text
            preco = produto.find_element(By.CLASS_NAME, "inventory_item_price").text
            preco_float = float(preco.replace("$", ""))
            
            context.produtos_selecionados.append({
                'nome': nome,
                'preco': preco,
                'preco_float': preco_float,
                'elemento': produto
            })
        
        print(f"Produtos selecionados: {[p['nome'] for p in context.produtos_selecionados]}")
        
    except Exception as e:
        print(f"Erro ao selecionar produtos: {e}")
        raise


@when('adiciono os produtos ao carrinho')
def step_impl(context):
    """Adiciona os produtos selecionados ao carrinho"""
    try:
        for produto in context.produtos_selecionados:
            # Encontrar o botão "Add to cart" para este produto
            botao_add = produto['elemento'].find_element(By.CLASS_NAME, "btn_inventory")
            
            # Clicar no botão
            botao_add.click()
            
            # Aguardar um pouco
            time.sleep(1)
        
        print("Produtos adicionados ao carrinho!")
        
    except Exception as e:
        print(f"Erro ao adicionar produtos ao carrinho: {e}")
        raise


@when('verifico que os produtos foram adicionados corretamente')
def step_impl(context):
    """Verifica se os produtos foram adicionados ao carrinho"""
    try:
        # Verificar o contador do carrinho
        cart_badge = context.driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
        quantidade = int(cart_badge.text)
        
        assert quantidade == 2, f"Quantidade esperada: 2, Encontrada: {quantidade}"
        print(f"Carrinho contem {quantidade} produtos")
        
    except Exception as e:
        print(f"Erro ao verificar produtos no carrinho: {e}")
        raise


@then('devo ver que exatamente dois produtos foram selecionados')
def step_impl(context):
    """Verifica se exatamente dois produtos foram selecionados"""
    try:
        assert len(context.produtos_selecionados) == 2, f"Esperado: 2 produtos, Encontrado: {len(context.produtos_selecionados)}"
        print(f"Exatamente {len(context.produtos_selecionados)} produtos selecionados")
        
    except Exception as e:
        print(f"Erro ao verificar quantidade de produtos: {e}")
        raise


@then('os produtos devem ter preços válidos')
def step_impl(context):
    """Verifica se os produtos têm preços válidos"""
    try:
        for produto in context.produtos_selecionados:
            preco = produto['preco_float']
            assert preco > 0, f"Preço deve ser maior que zero: {preco}"
            assert isinstance(preco, float), f"Preço deve ser float: {type(preco)}"
        
        print("Todos os produtos tem precos validos")
        
    except Exception as e:
        print(f"Erro ao verificar preços: {e}")
        raise
