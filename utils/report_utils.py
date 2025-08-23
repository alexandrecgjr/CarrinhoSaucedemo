"""
Utilitários para relatórios e captura de evidências
"""

import os
import json
import time
import allure
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException


class ReportUtils:
    """Classe utilitária para geração de relatórios e captura de evidências"""
    
    def __init__(self, driver):
        self.driver = driver
        self.screenshots_dir = "screenshots"
        self.reports_dir = "reports"
        self._criar_diretorios()
    
    def _criar_diretorios(self):
        """Cria os diretórios necessários para screenshots e relatórios"""
        for diretorio in [self.screenshots_dir, self.reports_dir]:
            if not os.path.exists(diretorio):
                os.makedirs(diretorio)
    
    def capturar_screenshot(self, nome_arquivo=None):
        """
        Captura screenshot da tela atual
        
        Args:
            nome_arquivo: Nome do arquivo para salvar (opcional)
        
        Returns:
            str: Caminho do arquivo salvo
        """
        if nome_arquivo is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"screenshot_{timestamp}.png"
        
        caminho_completo = os.path.join(self.screenshots_dir, nome_arquivo)
        
        try:
            self.driver.save_screenshot(caminho_completo)
            print(f"📸 Screenshot capturado: {caminho_completo}")
            
            # Anexar screenshot ao relatório Allure
            with allure.step(f"Capturando screenshot: {nome_arquivo}"):
                allure.attach.file(
                    caminho_completo,
                    name=nome_arquivo,
                    attachment_type=allure.attachment_type.PNG
                )
            
            return caminho_completo
        except Exception as e:
            print(f"❌ Erro ao capturar screenshot: {e}")
            return None
    
    def capturar_screenshot_em_caso_de_falha(self, nome_teste):
        """
        Captura screenshot quando um teste falha
        
        Args:
            nome_teste: Nome do teste que falhou
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"falha_{nome_teste}_{timestamp}.png"
        
        caminho = self.capturar_screenshot(nome_arquivo)
        
        if caminho:
            # Adicionar ao relatório Allure como evidência de falha
            with allure.step("Screenshot da falha"):
                allure.attach.file(
                    caminho,
                    name=f"Falha - {nome_teste}",
                    attachment_type=allure.attachment_type.PNG
                )
    
    def capturar_screenshot_etapa(self, etapa, nome_teste=None):
        """
        Captura screenshot de uma etapa específica do teste
        
        Args:
            etapa: Descrição da etapa
            nome_teste: Nome do teste (opcional)
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if nome_teste:
            nome_arquivo = f"{nome_teste}_{etapa}_{timestamp}.png"
        else:
            nome_arquivo = f"{etapa}_{timestamp}.png"
        
        caminho = self.capturar_screenshot(nome_arquivo)
        
        # Adicionar ao relatório Allure com descrição da etapa
        with allure.step(f"Screenshot - {etapa}"):
            allure.attach.file(
                caminho,
                name=f"{etapa} - {nome_arquivo}",
                attachment_type=allure.attachment_type.PNG
            )
        
        return caminho
    
    def gerar_relatorio_json(self, dados_teste, resultado):
        """
        Gera relatório JSON com dados do teste
        
        Args:
            dados_teste: Dados do teste executado
            resultado: Resultado do teste (pass/fail)
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"relatorio_{timestamp}.json"
        caminho = os.path.join(self.reports_dir, nome_arquivo)
        
        relatorio = {
            "timestamp": datetime.now().isoformat(),
            "teste": dados_teste,
            "resultado": resultado,
            "screenshots": self._obter_screenshots_recentes()
        }
        
        try:
            with open(caminho, 'w', encoding='utf-8') as f:
                json.dump(relatorio, f, indent=2, ensure_ascii=False)
            
            print(f"📄 Relatório JSON gerado: {caminho}")
            
            # Anexar relatório ao Allure
            with allure.step("Relatório JSON gerado"):
                allure.attach.file(
                    caminho,
                    name="Relatório JSON",
                    attachment_type=allure.attachment_type.JSON
                )
            
            return caminho
        except Exception as e:
            print(f"❌ Erro ao gerar relatório JSON: {e}")
            return None
    
    def _obter_screenshots_recentes(self):
        """Obtém lista de screenshots recentes"""
        screenshots = []
        if os.path.exists(self.screenshots_dir):
            arquivos = os.listdir(self.screenshots_dir)
            arquivos_png = [f for f in arquivos if f.endswith('.png')]
            # Pegar os 5 mais recentes
            arquivos_png.sort(key=lambda x: os.path.getmtime(os.path.join(self.screenshots_dir, x)), reverse=True)
            screenshots = arquivos_png[:5]
        return screenshots
    
    def adicionar_evidencia_allure(self, titulo, conteudo, tipo="text"):
        """
        Adiciona evidência ao relatório Allure
        
        Args:
            titulo: Título da evidência
            conteudo: Conteúdo da evidência
            tipo: Tipo de conteúdo (text, html, json, etc.)
        """
        with allure.step(titulo):
            if tipo == "text":
                allure.attach(conteudo, name=titulo, attachment_type=allure.attachment_type.TEXT)
            elif tipo == "html":
                allure.attach(conteudo, name=titulo, attachment_type=allure.attachment_type.HTML)
            elif tipo == "json":
                allure.attach(conteudo, name=titulo, attachment_type=allure.attachment_type.JSON)
    
    def capturar_pagina_completa(self, nome_arquivo=None):
        """
        Captura screenshot da página completa (scroll)
        
        Args:
            nome_arquivo: Nome do arquivo para salvar (opcional)
        
        Returns:
            str: Caminho do arquivo salvo
        """
        if nome_arquivo is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"pagina_completa_{timestamp}.png"
        
        try:
            # Obter altura total da página
            altura_total = self.driver.execute_script("return document.body.scrollHeight")
            largura = self.driver.execute_script("return document.body.scrollWidth")
            
            # Definir tamanho da janela
            self.driver.set_window_size(largura, altura_total)
            
            # Capturar screenshot
            caminho = self.capturar_screenshot(nome_arquivo)
            
            # Anexar ao Allure como página completa
            with allure.step("Screenshot da página completa"):
                allure.attach.file(
                    caminho,
                    name=f"Página Completa - {nome_arquivo}",
                    attachment_type=allure.attachment_type.PNG
                )
            
            return caminho
        except Exception as e:
            print(f"❌ Erro ao capturar página completa: {e}")
            return None
