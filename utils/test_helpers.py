"""
Utilitários para facilitar a escrita de testes de automação
"""

import time
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.test_config import TestConfig


class TestHelpers:
    """Utilitários para facilitar a escrita de testes"""
    
    @staticmethod
    def aguardar_carregamento_pagina(driver, timeout=None):
        """
        Aguarda até a página carregar completamente
        
        Args:
            driver: Instância do WebDriver
            timeout: Timeout em segundos (usa DEFAULT_TIMEOUT se não especificado)
        """
        if timeout is None:
            timeout = TestConfig.DEFAULT_TIMEOUT
            
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
    
    @staticmethod
    def gerar_nome_arquivo_timestamp(prefixo, extensao="png"):
        """
        Gera nome de arquivo com timestamp
        
        Args:
            prefixo: Prefixo do nome do arquivo
            extensao: Extensão do arquivo (padrão: png)
            
        Returns:
            str: Nome do arquivo com timestamp
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{prefixo}_{timestamp}.{extensao}"
    
    @staticmethod
    def validar_preco_com_tolerancia(preco_esperado, preco_real, tolerancia=None):
        """
        Valida preço com tolerância para diferenças de arredondamento
        
        Args:
            preco_esperado: Preço esperado
            preco_real: Preço real encontrado
            tolerancia: Tolerância aceitável (usa TOLERANCIA_PRECO se não especificado)
            
        Returns:
            bool: True se o preço está dentro da tolerância
        """
        if tolerancia is None:
            tolerancia = TestConfig.TOLERANCIA_PRECO
            
        return abs(preco_esperado - preco_real) < tolerancia
    
    @staticmethod
    def medir_tempo_execucao(func):
        """
        Decorator para medir o tempo de execução de uma função
        
        Args:
            func: Função a ser executada
            
        Returns:
            tuple: (resultado, tempo_execucao)
        """
        def wrapper(*args, **kwargs):
            inicio = time.time()
            resultado = func(*args, **kwargs)
            fim = time.time()
            tempo_execucao = fim - inicio
            return resultado, tempo_execucao
        return wrapper
    
    @staticmethod
    def aguardar_elemento_visivel(driver, locator, timeout=None):
        """
        Aguarda até um elemento ficar visível
        
        Args:
            driver: Instância do WebDriver
            locator: Localizador do elemento
            timeout: Timeout em segundos
            
        Returns:
            WebElement: Elemento encontrado
        """
        if timeout is None:
            timeout = TestConfig.DEFAULT_TIMEOUT
            
        return WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
    
    @staticmethod
    def aguardar_elemento_clicavel(driver, locator, timeout=None):
        """
        Aguarda até um elemento ficar clicável
        
        Args:
            driver: Instância do WebDriver
            locator: Localizador do elemento
            timeout: Timeout em segundos
            
        Returns:
            WebElement: Elemento encontrado
        """
        if timeout is None:
            timeout = TestConfig.DEFAULT_TIMEOUT
            
        return WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
    
    @staticmethod
    def extrair_numero_de_texto(texto):
        """
        Extrai número de um texto (remove símbolos de moeda, etc.)
        
        Args:
            texto: Texto contendo número
            
        Returns:
            float: Número extraído
        """
        import re
        # Remove símbolos de moeda e espaços, mantém apenas números e ponto
        numero_texto = re.sub(r'[^\d.]', '', texto)
        return float(numero_texto) if numero_texto else 0.0
    
    @staticmethod
    def formatar_preco(preco):
        """
        Formata preço para exibição
        
        Args:
            preco: Preço em float
            
        Returns:
            str: Preço formatado
        """
        return f"R$ {preco:.2f}"
    
    @staticmethod
    def validar_url_contem(driver, texto_esperado):
        """
        Valida se a URL atual contém o texto esperado
        
        Args:
            driver: Instância do WebDriver
            texto_esperado: Texto que deve estar na URL
            
        Returns:
            bool: True se a URL contém o texto
        """
        return texto_esperado in driver.current_url
    
    @staticmethod
    def aguardar_pequena_pausa():
        """Aguarda uma pequena pausa para estabilização"""
        time.sleep(TestConfig.SHORT_TIMEOUT)
    
    @staticmethod
    def aguardar_pausa_padrao():
        """Aguarda uma pausa padrão"""
        time.sleep(TestConfig.DEFAULT_TIMEOUT)
