"""
Página de Produtos do Sauce Demo
Contém os elementos e métodos para interagir com a página de produtos
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random


class ProductsPage:
    """Classe que representa a página de produtos do Sauce Demo"""
    
    # Locators (localizadores dos elementos)
    TITULO_PAGINA_PRODUTOS = (By.CLASS_NAME, "title")
    LISTA_ELEMENTOS_PRODUTOS = (By.CLASS_NAME, "inventory_item")
    BOTAO_CARRINHO = (By.CLASS_NAME, "shopping_cart_link")
    BOTAO_ADICIONAR_PRODUTO_TEMPLATE = "add-to-cart-sauce-labs-{}"
    BOTAO_REMOVER_PRODUTO_TEMPLATE = "remove-sauce-labs-{}"
    CONTADOR_ITENS_CARRINHO = (By.CLASS_NAME, "shopping_cart_badge")
    
    def __init__(self, driver):
        """
        Inicializa a página de produtos
        
        Args:
            driver: Instância do WebDriver
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def verificar_se_esta_na_pagina_produtos(self):
        """
        Verifica se está na página de produtos
        
        Returns:
            bool: True se está na página de produtos, False caso contrário
        """
        try:
            titulo = self.wait.until(
                EC.presence_of_element_located(self.TITULO_PAGINA_PRODUTOS)
            )
            return "Products" in titulo.text
        except:
            return False
    
    def obter_elementos_produtos(self):
        """
        Obtém os elementos WebElement dos produtos disponíveis
        
        Returns:
            list: Lista de elementos WebElement dos produtos
        """
        elementos = self.wait.until(
            EC.presence_of_all_elements_located(self.LISTA_ELEMENTOS_PRODUTOS)
        )
        print(f"Encontrados {len(elementos)} produtos na página")
        return elementos
    
    def obter_dados_produtos(self):
        """
        Obtém os dados estruturados dos produtos disponíveis
        
        Returns:
            list: Lista de dicionários com dados dos produtos
        """
        elementos = self.obter_elementos_produtos()
        dados_produtos = []
        
        for elemento in elementos:
            try:
                nome = elemento.find_element(By.CLASS_NAME, "inventory_item_name").text.strip()
                preco_texto = elemento.find_element(By.CLASS_NAME, "inventory_item_price").text.strip()
                preco = float(preco_texto.replace("$", "").replace(",", ""))
                
                dados_produtos.append({
                    "nome": nome,
                    "preco": preco,
                    "elemento": elemento
                })
            except Exception as e:
                print(f"Erro ao obter dados do produto: {e}")
        
        return dados_produtos

    def adicionar_produtos_aleatorios(self, quantidade: int = 2):
        """
        Adiciona 'quantidade' produtos aleatórios ao carrinho e retorna seus nomes e preços.

        Args:
            quantidade: Quantidade de produtos a adicionar (padrão: 2)

        Returns: 
            list[dict]: Lista de produtos adicionados com nome e preço
        """
        elementos = self.obter_elementos_produtos()
        random.shuffle(elementos)
        selecionados = []

        for elemento in elementos:
            if len(selecionados) >= quantidade:
                break
            try:
                nome = elemento.find_element(By.CLASS_NAME, "inventory_item_name").text.strip()
                preco_texto = elemento.find_element(By.CLASS_NAME, "inventory_item_price").text.strip().replace("$", "").replace(",", "")
                preco = float(preco_texto)
                # Botão dentro do elemento
                botao = elemento.find_element(By.TAG_NAME, "button")
                if "Add to cart" in botao.text or "Add" in botao.text or botao.get_attribute("data-test").startswith("add-to-cart"):
                    botao.click()
                    selecionados.append({"nome": nome, "preco": preco})
                    print(f"Produto aleatório adicionado: {nome} - ${preco}")
            except Exception as e:
                print(f"Falha ao adicionar item aleatório: {e}")

        print(f"Total aleatórios adicionados: {len(selecionados)}")
        return selecionados
    
    def adicionar_produto_ao_carrinho(self, nome_produto):
        """
        Adiciona um produto específico ao carrinho
        
        Args:
            nome_produto: Nome do produto (ex: "backpack", "bike-light")
        """
        try:
            # Primeiro, tentar pelo ID do botão (mais rápido)
            id_botao = self.BOTAO_ADICIONAR_PRODUTO_TEMPLATE.format(nome_produto)
            locator_botao = (By.ID, id_botao)
            
            botao_adicionar = self.wait.until(
                EC.element_to_be_clickable(locator_botao)
            )
            botao_adicionar.click()
            print(f"Produto '{nome_produto}' adicionado ao carrinho")
            return True
        except Exception as e:
            print(f"Erro ao adicionar produto '{nome_produto}' pelo ID: {e}")
            
            # Se falhar, tentar encontrar pelo nome do produto (mais robusto)
            try:
                dados_produtos = self.obter_dados_produtos()
                for produto in dados_produtos:
                    if nome_produto.lower() in produto['nome'].lower():
                        # Encontrar o botão dentro do elemento do produto
                        botao = produto['elemento'].find_element(By.TAG_NAME, "button")
                        if "Add to cart" in botao.text or "Add" in botao.text:
                            botao.click()
                            print(f"Produto '{produto['nome']}' adicionado ao carrinho (por nome)")
                            return True
            except Exception as e2:
                print(f"Erro ao adicionar produto '{nome_produto}' por nome: {e2}")
            
            return False
    
    def remover_produto_do_carrinho(self, nome_produto):
        """
        Remove um produto específico do carrinho
        
        Args:
            nome_produto: Nome do produto (ex: "backpack", "bike-light")
        """
        # Construir o ID do botão baseado no nome do produto
        id_botao = self.BOTAO_REMOVER_CARRINHO.format(nome_produto)
        locator_botao = (By.ID, id_botao)
        
        try:
            botao_remover = self.wait.until(
                EC.element_to_be_clickable(locator_botao)
            )
            botao_remover.click()
            print(f"Produto '{nome_produto}' removido do carrinho")
            return True
        except Exception as e:
            print(f"Erro ao remover produto '{nome_produto}': {e}")
            return False
    
    def obter_quantidade_itens_carrinho(self):
        """
        Obtém a quantidade de itens no carrinho
        
        Returns:
            int: Quantidade de itens no carrinho (0 se vazio)
        """
        try:
            contador = self.driver.find_element(*self.CONTADOR_ITENS_CARRINHO)
            quantidade = int(contador.text)
            print(f"Quantidade de itens no carrinho: {quantidade}")
            return quantidade
        except:
            print("Carrinho está vazio")
            return 0
    
    def clicar_no_carrinho(self):
        """Clica no ícone do carrinho para acessá-lo"""
        botao_carrinho = self.wait.until(
            EC.element_to_be_clickable(self.BOTAO_CARRINHO)
        )
        botao_carrinho.click()
        print("Carrinho acessado")
    
    def ir_para_carrinho(self):
        """Alias para clicar_no_carrinho"""
        self.clicar_no_carrinho()
    
    def adicionar_multiplos_produtos(self, lista_produtos):
        """
        Adiciona múltiplos produtos ao carrinho
        
        Args:
            lista_produtos: Lista com os nomes dos produtos a serem adicionados
        
        Returns:
            int: Quantidade de produtos adicionados com sucesso
        """
        produtos_adicionados = 0
        
        for produto in lista_produtos:
            if self.adicionar_produto_ao_carrinho(produto):
                produtos_adicionados += 1
        
        print(f"Total de produtos adicionados: {produtos_adicionados}")
        return produtos_adicionados
    
    def verificar_produtos_no_carrinho(self, produtos_esperados):
        """
        Verifica se os produtos esperados estão no carrinho
        
        Args:
            produtos_esperados: Lista de produtos que devem estar no carrinho
        
        Returns:
            bool: True se todos os produtos estão no carrinho, False caso contrário
        """
        quantidade_atual = self.obter_quantidade_itens_carrinho()
        quantidade_esperada = len(produtos_esperados)
        
        if quantidade_atual == quantidade_esperada:
            print(f"Carrinho contém {quantidade_atual} itens conforme esperado")
            return True
        else:
            print(f"Carrinho contém {quantidade_atual} itens, esperado {quantidade_esperada}")
            return False
    
    def adicionar_todos_produtos(self):
        """
        Adiciona todos os produtos disponíveis ao carrinho
        
        Returns:
            list: Lista de produtos adicionados com seus nomes e preços
        """
        elementos = self.obter_elementos_produtos()
        selecionados = []

        for elemento in elementos:
            try:
                nome = elemento.find_element(By.CLASS_NAME, "inventory_item_name").text.strip()
                preco_texto = elemento.find_element(By.CLASS_NAME, "inventory_item_price").text.strip().replace("$", "").replace(",", "")
                preco = float(preco_texto)
                
                # Botão dentro do elemento
                botao = elemento.find_element(By.TAG_NAME, "button")
                if "Add to cart" in botao.text or "Add" in botao.text or botao.get_attribute("data-test").startswith("add-to-cart"):
                    botao.click()
                    selecionados.append({"nome": nome, "preco": preco})
                    print(f"Produto adicionado: {nome} - ${preco}")
            except Exception as e:
                print(f"Falha ao adicionar item: {e}")

        print(f"Total de produtos adicionados: {len(selecionados)}")
        return selecionados
