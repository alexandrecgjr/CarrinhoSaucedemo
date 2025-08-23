"""
Assertions descritivos para testes de automação
"""

from config.test_config import TestConfig
from utils.test_helpers import TestHelpers


class TestAssertions:
    """Assertions descritivos para validações de teste"""
    
    @staticmethod
    def assert_login_sucesso(driver):
        """
        Valida se o login foi realizado com sucesso
        
        Args:
            driver: Instância do WebDriver
            
        Raises:
            AssertionError: Se o login falhou
        """
        assert TestHelpers.validar_url_contem(driver, "inventory"), (
            f"Login falhou. URL atual: {driver.current_url}. "
            f"URL esperada deveria conter 'inventory'"
        )
    
    @staticmethod
    def assert_quantidade_carrinho_correta(quantidade_esperada, quantidade_real):
        """
        Valida se a quantidade no carrinho está correta
        
        Args:
            quantidade_esperada: Quantidade esperada de itens
            quantidade_real: Quantidade real de itens
            
        Raises:
            AssertionError: Se a quantidade estiver incorreta
        """
        assert quantidade_real == quantidade_esperada, (
            f"Quantidade no carrinho incorreta. "
            f"Esperado: {quantidade_esperada} itens, "
            f"Encontrado: {quantidade_real} itens"
        )
    
    @staticmethod
    def assert_preco_correto(preco_esperado, preco_real, descricao=""):
        """
        Valida se o preço está correto com tolerância
        
        Args:
            preco_esperado: Preço esperado
            preco_real: Preço real encontrado
            descricao: Descrição do preço sendo validado
            
        Raises:
            AssertionError: Se o preço estiver incorreto
        """
        assert TestHelpers.validar_preco_com_tolerancia(preco_esperado, preco_real), (
            f"Preço {descricao} incorreto. "
            f"Esperado: {TestHelpers.formatar_preco(preco_esperado)}, "
            f"Encontrado: {TestHelpers.formatar_preco(preco_real)}"
        )
    
    @staticmethod
    def assert_taxa_imposto_correta(subtotal, taxa_imposto):
        """
        Valida se a taxa de imposto está correta (8%)
        
        Args:
            subtotal: Subtotal dos produtos
            taxa_imposto: Taxa de imposto aplicada
            
        Raises:
            AssertionError: Se a taxa de imposto estiver incorreta
        """
        taxa_esperada = subtotal * TestConfig.TAXA_IMPOSTO_ESPERADA
        assert TestHelpers.validar_preco_com_tolerancia(taxa_esperada, taxa_imposto), (
            f"Taxa de imposto incorreta. "
            f"Esperado: {TestHelpers.formatar_preco(taxa_esperada)} (8% de {TestHelpers.formatar_preco(subtotal)}), "
            f"Encontrado: {TestHelpers.formatar_preco(taxa_imposto)}"
        )
    
    @staticmethod
    def assert_total_final_correto(subtotal, taxa_imposto, total_final):
        """
        Valida se o total final está correto
        
        Args:
            subtotal: Subtotal dos produtos
            taxa_imposto: Taxa de imposto aplicada
            total_final: Total final da compra
            
        Raises:
            AssertionError: Se o total final estiver incorreto
        """
        total_esperado = subtotal + taxa_imposto
        assert TestHelpers.validar_preco_com_tolerancia(total_esperado, total_final), (
            f"Total final incorreto. "
            f"Esperado: {TestHelpers.formatar_preco(total_esperado)} "
            f"({TestHelpers.formatar_preco(subtotal)} + {TestHelpers.formatar_preco(taxa_imposto)}), "
            f"Encontrado: {TestHelpers.formatar_preco(total_final)}"
        )
    
    @staticmethod
    def assert_mensagem_sucesso_presente(mensagem, texto_esperado="thank you"):
        """
        Valida se a mensagem de sucesso está presente
        
        Args:
            mensagem: Mensagem encontrada
            texto_esperado: Texto que deve estar na mensagem
            
        Raises:
            AssertionError: Se a mensagem de sucesso não estiver presente
        """
        assert texto_esperado.lower() in mensagem.lower(), (
            f"Mensagem de sucesso não encontrada. "
            f"Esperado: '{texto_esperado}', "
            f"Encontrado: '{mensagem}'"
        )
    
    @staticmethod
    def assert_produtos_no_carrinho(produtos_esperados, produtos_reais):
        """
        Valida se os produtos esperados estão no carrinho
        
        Args:
            produtos_esperados: Lista de produtos esperados
            produtos_reais: Lista de produtos encontrados
            
        Raises:
            AssertionError: Se os produtos não estiverem corretos
        """
        assert len(produtos_reais) == len(produtos_esperados), (
            f"Quantidade de produtos no carrinho incorreta. "
            f"Esperado: {len(produtos_esperados)} produtos, "
            f"Encontrado: {len(produtos_reais)} produtos"
        )
        
        # Validar se todos os produtos esperados estão presentes
        nomes_esperados = [p['nome'] for p in produtos_esperados]
        nomes_reais = [p['nome'] for p in produtos_reais]
        
        for nome in nomes_esperados:
            assert nome in nomes_reais, (
                f"Produto '{nome}' não encontrado no carrinho. "
                f"Produtos no carrinho: {nomes_reais}"
            )
    
    @staticmethod
    def assert_elemento_visivel(driver, locator, descricao=""):
        """
        Valida se um elemento está visível
        
        Args:
            driver: Instância do WebDriver
            locator: Localizador do elemento
            descricao: Descrição do elemento
            
        Raises:
            AssertionError: Se o elemento não estiver visível
        """
        try:
            TestHelpers.aguardar_elemento_visivel(driver, locator)
        except Exception as e:
            raise AssertionError(
                f"Elemento {descricao} não está visível. "
                f"Locator: {locator}, "
                f"Erro: {str(e)}"
            )
    
    @staticmethod
    def assert_url_correta(driver, url_esperada):
        """
        Valida se a URL atual está correta
        
        Args:
            driver: Instância do WebDriver
            url_esperada: URL esperada
            
        Raises:
            AssertionError: Se a URL estiver incorreta
        """
        url_atual = driver.current_url
        assert url_atual == url_esperada, (
            f"URL incorreta. "
            f"Esperado: {url_esperada}, "
            f"Encontrado: {url_atual}"
        )
    
    @staticmethod
    def assert_texto_presente(elemento, texto_esperado, descricao=""):
        """
        Valida se um texto está presente em um elemento
        
        Args:
            elemento: Elemento WebElement
            texto_esperado: Texto esperado
            descricao: Descrição do elemento
            
        Raises:
            AssertionError: Se o texto não estiver presente
        """
        texto_real = elemento.text
        assert texto_esperado.lower() in texto_real.lower(), (
            f"Texto não encontrado no elemento {descricao}. "
            f"Esperado: '{texto_esperado}', "
            f"Encontrado: '{texto_real}'"
        )
