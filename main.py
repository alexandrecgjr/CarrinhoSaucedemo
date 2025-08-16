"""
Script Principal - Automação Sauce Demo
Executa o fluxo completo de login e adição de produtos ao carrinho
"""

import time
from utils.webdriver_config import WebDriverConfig
from pages.login_page import LoginPage
from pages.products_page import ProductsPage


def executar_automacao_sauce_demo():
    """
    Executa a automação completa do Sauce Demo:
    1. Acessa o site
    2. Faz login
    3. Adiciona produtos ao carrinho
    4. Verifica o carrinho
    """
    driver = None
    
    try:
        print("Iniciando automação do Sauce Demo...")
        
        # Configurar o driver
        driver = WebDriverConfig.configurar_chrome_driver()
        WebDriverConfig.configurar_driver_com_espera_implicita(driver)
        
        # URLs e credenciais
        url_site = "https://www.saucedemo.com/"
        usuario = "standard_user"
        senha = "secret_sauce"
        
        # Produtos a serem adicionados ao carrinho
        produtos_para_adicionar = ["backpack", "bike-light"]
        
        # 1. Acessar a página de login
        print("Passo 1: Acessando a página de login...")
        pagina_login = LoginPage(driver)
        pagina_login.acessar_pagina_login(url_site)
        
        # 2. Fazer login
        print("Passo 2: Realizando login...")
        pagina_login.fazer_login(usuario, senha)
        
        # Aguardar um pouco para a página carregar
        time.sleep(2)
        
        # 3. Verificar se o login foi bem-sucedido
        if not pagina_login.verificar_se_login_foi_bem_sucedido():
            mensagem_erro = pagina_login.obter_mensagem_erro()
            print(f"Login falhou: {mensagem_erro}")
            return False
        
        print("Login realizado com sucesso!")
        
        # 4. Navegar para a página de produtos
        print("Passo 3: Navegando para a página de produtos...")
        pagina_produtos = ProductsPage(driver)
        
        # Verificar se está na página de produtos
        if not pagina_produtos.verificar_se_esta_na_pagina_produtos():
            print("Não foi possível acessar a página de produtos")
            return False
        
        print("Página de produtos acessada com sucesso!")
        
        # 5. Adicionar produtos ao carrinho
        print(f"Passo 4: Adicionando {len(produtos_para_adicionar)} produtos ao carrinho...")
        produtos_adicionados = pagina_produtos.adicionar_multiplos_produtos(produtos_para_adicionar)
        
        if produtos_adicionados != len(produtos_para_adicionar):
            print(f"Apenas {produtos_adicionados} de {len(produtos_para_adicionar)} produtos foram adicionados")
        
        # 6. Verificar o carrinho
        print("Passo 5: Verificando o carrinho...")
        quantidade_carrinho = pagina_produtos.obter_quantidade_itens_carrinho()
        
        if quantidade_carrinho == len(produtos_para_adicionar):
            print(f"Sucesso! Carrinho contém {quantidade_carrinho} itens")
            
            # 7. Acessar o carrinho (opcional)
            print("Passo 6: Acessando o carrinho...")
            pagina_produtos.clicar_no_carrinho()
            time.sleep(2)
            
            print("Automação concluída com sucesso!")
            return True
        else:
            print(f"Falha na verificação do carrinho. Esperado: {len(produtos_para_adicionar)}, Encontrado: {quantidade_carrinho}")
            return False
            
    except Exception as e:
        print(f"Erro durante a automação: {e}")
        return False
    
    finally:
        # Fechar o driver
        if driver:
            print("Fechando o navegador...")
            time.sleep(3)  # Aguardar um pouco para visualizar o resultado
            WebDriverConfig.fechar_driver(driver)


def main():
    """Função principal que executa a automação"""
    print("=" * 60)
    print("AUTOMAÇÃO SAUCE DEMO - CARRINHO DE COMPRAS")
    print("=" * 60)
    
    sucesso = executar_automacao_sauce_demo()
    
    print("\n" + "=" * 60)
    if sucesso:
        print("AUTOMAÇÃO CONCLUÍDA COM SUCESSO!")
    else:
        print("AUTOMAÇÃO FALHOU!")
    print("=" * 60)


if __name__ == "__main__":
    main()


