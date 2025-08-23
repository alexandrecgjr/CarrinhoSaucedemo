"""
Sistema de logging estruturado para testes de automação
"""

import logging
import os
from datetime import datetime
from config.test_config import TestConfig


class TestLogger:
    """Sistema de logging para testes"""
    
    def __init__(self, nome_teste):
        """
        Inicializa o logger para um teste específico
        
        Args:
            nome_teste: Nome do teste para identificar os logs
        """
        self.nome_teste = nome_teste
        self.logger = logging.getLogger(nome_teste)
        self.logger.setLevel(logging.INFO)
        
        # Evitar duplicação de handlers
        if not self.logger.handlers:
            self._configurar_handlers()
    
    def _configurar_handlers(self):
        """Configura os handlers para console e arquivo"""
        # Criar diretório de logs se não existir
        if not os.path.exists(TestConfig.LOGS_DIR):
            os.makedirs(TestConfig.LOGS_DIR)
        
        # Handler para arquivo
        log_file = os.path.join(TestConfig.LOGS_DIR, f"{self.nome_teste}.log")
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        
        # Handler para console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Adicionar handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def info(self, mensagem):
        """Log de informação"""
        self.logger.info(f"ℹ️  {mensagem}")
    
    def error(self, mensagem):
        """Log de erro"""
        self.logger.error(f"❌ {mensagem}")
    
    def warning(self, mensagem):
        """Log de aviso"""
        self.logger.warning(f"⚠️  {mensagem}")
    
    def success(self, mensagem):
        """Log de sucesso"""
        self.logger.info(f"✅ {mensagem}")
    
    def screenshot(self, descricao):
        """Log de screenshot"""
        self.logger.info(f"📸 Screenshot: {descricao}")
    
    def step(self, descricao):
        """Log de etapa do teste"""
        self.logger.info(f"🔄 Etapa: {descricao}")
    
    def data(self, titulo, dados):
        """Log de dados estruturados"""
        self.logger.info(f"📊 {titulo}: {dados}")
    
    def performance(self, operacao, tempo):
        """Log de performance"""
        self.logger.info(f"⏱️  {operacao}: {tempo:.2f}s")
