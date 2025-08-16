"""
Página do Carrinho do Sauce Demo
Responsável por listar itens e seguir para o checkout
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CartPage:
    """Classe que representa a página do carrinho"""

    CART_ITEM = (By.CLASS_NAME, "cart_item")
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICE = (By.CLASS_NAME, "inventory_item_price")
    CHECKOUT_BUTTON = (By.ID, "checkout")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def obter_itens_carrinho(self):
        """
        Retorna a lista de itens presentes no carrinho
        Returns: list[dict] -> [{"nome": str, "preco": float}]
        """
        itens = self.wait.until(EC.presence_of_all_elements_located(self.CART_ITEM))
        resultado = []
        for item in itens:
            nome = item.find_element(*self.ITEM_NAME).text.strip()
            preco_texto = item.find_element(*self.ITEM_PRICE).text.strip().replace("$", "").replace(",", "")
            try:
                preco = float(preco_texto)
            except:
                preco = 0.0
            resultado.append({"nome": nome, "preco": preco})
        return resultado

    def clicar_checkout(self):
        botao = self.wait.until(EC.element_to_be_clickable(self.CHECKOUT_BUTTON))
        botao.click()
        return True
