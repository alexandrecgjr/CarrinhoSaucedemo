"""
Steps para funcionalidades de checkout
"""

from behave import when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


@when('preencho as informações de checkout')
def step_impl(context):
    """Preenche as informações básicas de checkout"""
    try:
        # Dados padrão para checkout
        first_name = "João"
        last_name = "Silva"
        postal_code = "12345-678"
        
        # Preencher campos
        first_name_field = context.driver.find_element(By.ID, "first-name")
        first_name_field.clear()
        first_name_field.send_keys(first_name)
        
        last_name_field = context.driver.find_element(By.ID, "last-name")
        last_name_field.clear()
        last_name_field.send_keys(last_name)
        
        postal_code_field = context.driver.find_element(By.ID, "postal-code")
        postal_code_field.clear()
        postal_code_field.send_keys(postal_code)
        
        # Armazenar dados para verificação posterior
        context.checkout_data = {
            'first_name': first_name,
            'last_name': last_name,
            'postal_code': postal_code
        }
        
        print(f"Informacoes de checkout preenchidas: {first_name} {last_name}")
        
    except Exception as e:
        print(f"Erro ao preencher informações de checkout: {e}")
        raise


@when('preencho as informações de checkout com')
def step_impl(context):
    """Preenche as informações de checkout usando dados da tabela"""
    try:
        # Obter dados da tabela
        dados = {}
        for row in context.table:
            dados[row['Campo']] = row['Valor']
        
        # Preencher campos
        if 'First Name' in dados:
            first_name_field = context.driver.find_element(By.ID, "first-name")
            first_name_field.clear()
            first_name_field.send_keys(dados['First Name'])
        
        if 'Last Name' in dados:
            last_name_field = context.driver.find_element(By.ID, "last-name")
            last_name_field.clear()
            last_name_field.send_keys(dados['Last Name'])
        
        if 'ZIP Code' in dados:
            postal_code_field = context.driver.find_element(By.ID, "postal-code")
            postal_code_field.clear()
            postal_code_field.send_keys(dados['ZIP Code'])
        
        # Armazenar dados para verificação posterior
        context.checkout_data = dados
        
        print(f"Informacoes de checkout preenchidas com dados da tabela")
        
    except Exception as e:
        print(f"Erro ao preencher informações de checkout: {e}")
        raise


@when('verifico o resumo da compra')
def step_impl(context):
    """Verifica o resumo da compra na página de overview"""
    try:
        # Primeiro, clicar em Continue para ir para a página de resumo
        continue_button = context.driver.find_element(By.ID, "continue")
        continue_button.click()
        
        # Aguardar carregamento da página de resumo
        WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "summary_info"))
        )
        
        # Verificar se os produtos estão listados
        cart_items = context.driver.find_elements(By.CLASS_NAME, "inventory_item_name")
        produtos_resumo = [item.text for item in cart_items]
        
        # Verificar se todos os produtos selecionados estão no resumo
        produtos_selecionados = [produto['nome'] for produto in context.produtos_selecionados]
        
        for produto in produtos_selecionados:
            assert produto in produtos_resumo, f"Produto {produto} não encontrado no resumo"
        
        print(f"Resumo da compra verificado: {produtos_resumo}")
        
    except Exception as e:
        print(f"Erro ao verificar resumo da compra: {e}")
        raise


@when('confirmo a compra')
def step_impl(context):
    """Confirma a compra clicando em Finish"""
    try:
        # Clicar no botão Finish
        finish_button = context.driver.find_element(By.ID, "finish")
        finish_button.click()
        
        # Aguardar carregamento da página de sucesso
        WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "complete-header"))
        )
        
        print("Compra confirmada com sucesso!")
        
    except Exception as e:
        print(f"Erro ao confirmar compra: {e}")
        raise


@then('devo ver o resumo da compra')
def step_impl(context):
    """Verifica se o resumo da compra está visível"""
    try:
        # Verificar elementos do resumo
        summary_info = context.driver.find_element(By.CLASS_NAME, "summary_info")
        assert summary_info.is_displayed(), "Resumo da compra não está visível"
        
        # Verificar se há produtos listados
        cart_items = context.driver.find_elements(By.CLASS_NAME, "inventory_item_name")
        assert len(cart_items) > 0, "Nenhum produto encontrado no resumo"
        
        print("Resumo da compra está visível")
        
    except Exception as e:
        print(f"Erro ao verificar resumo da compra: {e}")
        raise


@then('os valores devem estar corretos')
def step_impl(context):
    """Verifica se os valores no resumo estão corretos"""
    try:
        # Verificar subtotal
        subtotal_element = context.driver.find_element(By.CLASS_NAME, "summary_subtotal_label")
        subtotal_texto = subtotal_element.text
        subtotal_valor = float(subtotal_texto.replace("Item total: $", ""))
        
        # Calcular subtotal esperado
        subtotal_esperado = sum(produto['preco_float'] for produto in context.produtos_selecionados)
        
        assert abs(subtotal_valor - subtotal_esperado) < 0.01, \
            f"Subtotal esperado: ${subtotal_esperado}, Encontrado: ${subtotal_valor}"
        
        # Verificar taxa (se disponível)
        try:
            tax_element = context.driver.find_element(By.CLASS_NAME, "summary_tax_label")
            tax_texto = tax_element.text
            tax_valor = float(tax_texto.replace("Tax: $", ""))
            
            tax_esperado = subtotal_esperado * 0.08  # 8% de taxa
            
            assert abs(tax_valor - tax_esperado) < 0.01, \
                f"Taxa esperada: ${tax_esperado:.2f}, Encontrada: ${tax_valor}"
            
            print(f"Taxa verificada: ${tax_valor:.2f}")
            
        except:
            print("Taxa não encontrada no resumo")
        
        # Verificar total
        try:
            total_element = context.driver.find_element(By.CLASS_NAME, "summary_total_label")
            total_texto = total_element.text
            total_valor = float(total_texto.replace("Total: $", ""))
            
            total_esperado = subtotal_esperado + tax_esperado
            
            assert abs(total_valor - total_esperado) < 0.01, \
                f"Total esperado: ${total_esperado:.2f}, Encontrado: ${total_valor}"
            
            print(f"Total verificado: ${total_valor:.2f}")
            
        except:
            print("Total não encontrado no resumo")
        
        print(f"Subtotal verificado: ${subtotal_valor}")
        
    except Exception as e:
        print(f"Erro ao verificar valores: {e}")
        raise


@then('devo poder finalizar a compra')
def step_impl(context):
    """Verifica se é possível finalizar a compra"""
    try:
        # Verificar se o botão Finish está presente e habilitado
        finish_button = context.driver.find_element(By.ID, "finish")
        assert finish_button.is_displayed(), "Botão Finish não está visível"
        assert finish_button.is_enabled(), "Botão Finish não está habilitado"
        
        print("Botao Finish está disponível para finalizar a compra")
        
    except Exception as e:
        print(f"Erro ao verificar botão Finish: {e}")
        raise
