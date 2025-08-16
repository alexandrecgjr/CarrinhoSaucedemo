"""
Testes Automatizados - Sauce Demo
Testes usando pytest para validar a automação
"""

import pytest
import time
from utils.webdriver_config import WebDriverConfig
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


class TestSauceDemo:
    """Classe de testes para o Sauce Demo"""
    
    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        """
        Fixture para configurar e limpar o ambiente de teste
        """
        # Setup - executado antes de cada teste
        self.driver = WebDriverConfig.configurar_chrome_driver()
        WebDriverConfig.configurar_driver_com_espera_implicita(self.driver)
        
        # Dados de teste
        self.url_site = "https://www.saucedemo.com/"
        self.usuario = "standard_user"
        self.senha = "secret_sauce"
        self.produtos_teste = ["backpack", "bike-light"]
        
        yield  # Executa o teste
        
        # Teardown - executado após cada teste
        if self.driver:
            time.sleep(2)  # Aguardar para visualizar o resultado
            WebDriverConfig.fechar_driver(self.driver)
    
    def test_login_sucesso(self):
        """Testa se o login é realizado com sucesso"""
        # Arrange
        pagina_login = LoginPage(self.driver)
        pagina_login.acessar_pagina_login(self.url_site)
        
        # Act
        pagina_login.fazer_login(self.usuario, self.senha)
        time.sleep(2)
        
        # Assert
        assert pagina_login.verificar_se_login_foi_bem_sucedido(), "Login falhou"
    
    def test_acesso_pagina_produtos(self):
        """Testa se consegue acessar a página de produtos após login"""
        # Arrange
        pagina_login = LoginPage(self.driver)
        pagina_produtos = ProductsPage(self.driver)
        
        # Act
        pagina_login.acessar_pagina_login(self.url_site)
        pagina_login.fazer_login(self.usuario, self.senha)
        time.sleep(2)
        
        # Assert
        assert pagina_produtos.verificar_se_esta_na_pagina_produtos(), "Não conseguiu acessar a página de produtos"
    
    def test_adicionar_produtos_ao_carrinho(self):
        """Testa se consegue adicionar produtos ao carrinho"""
        # Arrange
        pagina_login = LoginPage(self.driver)
        pagina_produtos = ProductsPage(self.driver)
        
        # Act
        pagina_login.acessar_pagina_login(self.url_site)
        pagina_login.fazer_login(self.usuario, self.senha)
        time.sleep(2)
        
        produtos_adicionados = pagina_produtos.adicionar_multiplos_produtos(self.produtos_teste)
        
        # Assert
        assert produtos_adicionados == len(self.produtos_teste), f"Esperado {len(self.produtos_teste)} produtos, adicionado {produtos_adicionados}"
    
    def test_verificar_quantidade_carrinho(self):
        """Testa se a quantidade de itens no carrinho está correta"""
        # Arrange
        pagina_login = LoginPage(self.driver)
        pagina_produtos = ProductsPage(self.driver)
        
        # Act
        pagina_login.acessar_pagina_login(self.url_site)
        pagina_login.fazer_login(self.usuario, self.senha)
        time.sleep(2)
        
        pagina_produtos.adicionar_multiplos_produtos(self.produtos_teste)
        quantidade_carrinho = pagina_produtos.obter_quantidade_itens_carrinho()
        
        # Assert
        assert quantidade_carrinho == len(self.produtos_teste), f"Carrinho deve ter {len(self.produtos_teste)} itens, mas tem {quantidade_carrinho}"
    
    def test_fluxo_completo(self):
        """Testa o fluxo completo: login + adicionar produtos + verificar carrinho"""
        # Arrange
        pagina_login = LoginPage(self.driver)
        pagina_produtos = ProductsPage(self.driver)
        
        # Act - Login
        pagina_login.acessar_pagina_login(self.url_site)
        pagina_login.fazer_login(self.usuario, self.senha)
        time.sleep(2)
        
        # Assert - Verificar login
        assert pagina_login.verificar_se_login_foi_bem_sucedido(), "Login falhou"
        
        # Act - Adicionar produtos
        produtos_adicionados = pagina_produtos.adicionar_multiplos_produtos(self.produtos_teste)
        
        # Assert - Verificar produtos adicionados
        assert produtos_adicionados == len(self.produtos_teste), f"Falha ao adicionar produtos"
        
        # Act - Verificar carrinho
        quantidade_carrinho = pagina_produtos.obter_quantidade_itens_carrinho()
        
        # Assert - Verificar quantidade no carrinho
        assert quantidade_carrinho == len(self.produtos_teste), f"Quantidade incorreta no carrinho"
        
        # Act - Acessar carrinho
        pagina_produtos.clicar_no_carrinho()
        time.sleep(2)
        
        # Assert - Verificar se conseguiu acessar o carrinho
        assert "cart" in self.driver.current_url.lower(), "Não conseguiu acessar o carrinho"

    def test_fluxo_compra_completo_aleatorio(self):
        """
        Fluxo completo de compra:
        - Login
        - Seleciona 2 produtos aleatórios
        - Valida subtotal, imposto 8% e total
        - Conclui o checkout
        """
        pagina_login = LoginPage(self.driver)
        produtos_page = ProductsPage(self.driver)
        
        # Login
        pagina_login.acessar_pagina_login(self.url_site)
        pagina_login.fazer_login(self.usuario, self.senha)
        time.sleep(2)
        assert produtos_page.verificar_se_esta_na_pagina_produtos()
        
        # Selecionar 2 produtos aleatórios e adicionar ao carrinho
        selecionados = produtos_page.adicionar_produtos_aleatorios(2)
        assert len(selecionados) == 2, "Não foi possível adicionar 2 produtos aleatórios"
        subtotal_esperado = round(sum(p["preco"] for p in selecionados), 2)
        
        # Ir para o carrinho e conferir itens
        produtos_page.clicar_no_carrinho()
        cart_page = CartPage(self.driver)
        itens_carrinho = cart_page.obter_itens_carrinho()
        assert len(itens_carrinho) == 2, "Carrinho não possui 2 itens"
        subtotal_carrinho = round(sum(i["preco"] for i in itens_carrinho), 2)
        assert subtotal_carrinho == subtotal_esperado, f"Subtotal do carrinho ({subtotal_carrinho}) difere do esperado ({subtotal_esperado})"
        
        # Checkout - Step One
        cart_page.clicar_checkout()
        checkout_page = CheckoutPage(self.driver)
        checkout_page.preencher_informacoes_pessoais("Alex", "Tester", "12345")
        checkout_page.continuar_para_resumo()
        
        # Resumo de pagamento
        resumo = checkout_page.obter_resumo_valores()
        imposto_esperado = round(subtotal_esperado * 0.08, 2)
        total_esperado = round(subtotal_esperado + imposto_esperado, 2)
        
        assert resumo["subtotal"] == subtotal_esperado, f"Subtotal incorreto: {resumo['subtotal']} != {subtotal_esperado}"
        assert resumo["taxa"] == imposto_esperado, f"Imposto incorreto: {resumo['taxa']} != {imposto_esperado}"
        assert resumo["total"] == total_esperado, f"Total incorreto: {resumo['total']} != {total_esperado}"
        
        # Finalizar compra
        checkout_page.finalizar_compra()
        assert checkout_page.verificar_compra_concluida(), "Compra não foi concluída com sucesso"


if __name__ == "__main__":
    # Executar os testes
    pytest.main([__file__, "-v", "--tb=short"])


