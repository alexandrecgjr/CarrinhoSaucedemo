"""
Página de Checkout do Sauce Demo
Contém métodos para preencher dados, validar resumo e finalizar compra
"""

import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CheckoutPage:
    """Classe que representa o fluxo de checkout"""

    # Step One
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")

    # Step Two - Resumo
    SUBTOTAL_LABEL = (By.CLASS_NAME, "summary_subtotal_label")
    TAX_LABEL = (By.CLASS_NAME, "summary_tax_label")
    TOTAL_LABEL = (By.CLASS_NAME, "summary_total_label")
    FINISH_BUTTON = (By.ID, "finish")

    # Complete
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def preencher_informacoes_pessoais(self, primeiro_nome: str, sobrenome: str, cep: str):
        self.wait.until(EC.element_to_be_clickable(self.FIRST_NAME)).send_keys(primeiro_nome)
        self.wait.until(EC.element_to_be_clickable(self.LAST_NAME)).send_keys(sobrenome)
        self.wait.until(EC.element_to_be_clickable(self.POSTAL_CODE)).send_keys(cep)

    def continuar_para_resumo(self):
        self.wait.until(EC.element_to_be_clickable(self.CONTINUE_BUTTON)).click()

    @staticmethod
    def _extrair_valor(label_texto: str) -> float:
        # Extrai o primeiro número com casas decimais do texto
        numeros = re.findall(r"\d+\.\d+|\d+", label_texto)
        if not numeros:
            return 0.0
        # Considera o último token como valor (ex.: 'Item total: $39.98')
        return float(numeros[-1])

    def obter_resumo_valores(self):
        subtotal_texto = self.wait.until(EC.presence_of_element_located(self.SUBTOTAL_LABEL)).text
        tax_texto = self.wait.until(EC.presence_of_element_located(self.TAX_LABEL)).text
        total_texto = self.wait.until(EC.presence_of_element_located(self.TOTAL_LABEL)).text
        return {
            "subtotal": round(self._extrair_valor(subtotal_texto), 2),
            "taxa": round(self._extrair_valor(tax_texto), 2),
            "total": round(self._extrair_valor(total_texto), 2),
        }

    def finalizar_compra(self):
        self.wait.until(EC.element_to_be_clickable(self.FINISH_BUTTON)).click()

    def verificar_compra_concluida(self) -> bool:
        try:
            cabecalho = self.wait.until(EC.presence_of_element_located(self.COMPLETE_HEADER))
            return "Thank you" in cabecalho.text or "Obrigado" in cabecalho.text
        except:
            return False
    
    def preencher_informacoes(self, primeiro_nome: str, sobrenome: str, cep: str):
        """Alias para preencher_informacoes_pessoais"""
        self.preencher_informacoes_pessoais(primeiro_nome, sobrenome, cep)
    
    def continuar_checkout(self):
        """Alias para continuar_para_resumo"""
        self.continuar_para_resumo()
    
    def obter_subtotal(self):
        """Obtém o subtotal do checkout"""
        valores = self.obter_resumo_valores()
        return valores["subtotal"]
    
    def obter_taxa_imposto(self):
        """Obtém a taxa de imposto do checkout"""
        valores = self.obter_resumo_valores()
        return valores["taxa"]
    
    def obter_total_final(self):
        """Obtém o total final do checkout"""
        valores = self.obter_resumo_valores()
        return valores["total"]
    
    def obter_mensagem_sucesso(self):
        """Obtém a mensagem de sucesso após finalizar a compra"""
        try:
            cabecalho = self.wait.until(EC.presence_of_element_located(self.COMPLETE_HEADER))
            return cabecalho.text
        except:
            return ""
