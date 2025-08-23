"""
Carregador de dados de teste
"""

import json
import os
import random
from typing import List, Dict, Any


class TestDataLoader:
    """Classe para carregar dados de teste do arquivo JSON"""
    
    def __init__(self, arquivo_dados="data/users.json"):
        self.arquivo_dados = arquivo_dados
        self.dados = self._carregar_dados()
    
    def _carregar_dados(self) -> Dict[str, Any]:
        """
        Carrega os dados do arquivo JSON
        
        Returns:
            Dict: Dados carregados do arquivo
        """
        try:
            if not os.path.exists(self.arquivo_dados):
                raise FileNotFoundError(f"Arquivo de dados não encontrado: {self.arquivo_dados}")
            
            with open(self.arquivo_dados, 'r', encoding='utf-8') as f:
                return json.load(f)
                
        except Exception as e:
            print(f"Erro ao carregar dados de teste: {e}")
            return {"usuarios": [], "dados_checkout": []}
    
    def obter_usuarios(self) -> List[Dict[str, str]]:
        """
        Retorna a lista de usuários
        
        Returns:
            List[Dict]: Lista de usuários
        """
        return self.dados.get("usuarios", [])
    
    def obter_usuarios_por_tipo(self, tipo: str) -> List[Dict[str, str]]:
        """
        Retorna usuários filtrados por tipo
        
        Args:
            tipo (str): Tipo de usuário (valido, bloqueado, performance, etc.)
            
        Returns:
            List[Dict]: Lista de usuários do tipo especificado
        """
        usuarios = self.obter_usuarios()
        return [usuario for usuario in usuarios if usuario.get("tipo") == tipo]
    
    def obter_usuario_aleatorio(self) -> Dict[str, str]:
        """
        Retorna um usuário aleatório
        
        Returns:
            Dict: Usuário aleatório
        """
        usuarios = self.obter_usuarios()
        if not usuarios:
            raise ValueError("Nenhum usuário encontrado nos dados de teste")
        return random.choice(usuarios)
    
    def obter_usuario_por_tipo_aleatorio(self, tipo: str) -> Dict[str, str]:
        """
        Retorna um usuário aleatório do tipo especificado
        
        Args:
            tipo (str): Tipo de usuário
            
        Returns:
            Dict: Usuário aleatório do tipo especificado
        """
        usuarios_tipo = self.obter_usuarios_por_tipo(tipo)
        if not usuarios_tipo:
            raise ValueError(f"Nenhum usuário do tipo '{tipo}' encontrado")
        return random.choice(usuarios_tipo)
    
    def obter_usuario_por_tipo(self, tipo: str) -> Dict[str, str]:
        """
        Retorna o primeiro usuário do tipo especificado
        
        Args:
            tipo (str): Tipo de usuário
            
        Returns:
            Dict: Primeiro usuário do tipo especificado
        """
        usuarios_tipo = self.obter_usuarios_por_tipo(tipo)
        if not usuarios_tipo:
            raise ValueError(f"Nenhum usuário do tipo '{tipo}' encontrado")
        return usuarios_tipo[0]
    
    def obter_dados_checkout(self) -> List[Dict[str, str]]:
        """
        Retorna a lista de dados de checkout
        
        Returns:
            List[Dict]: Lista de dados de checkout
        """
        return self.dados.get("dados_checkout", [])
    
    def obter_dados_checkout_aleatorio(self) -> Dict[str, str]:
        """
        Retorna dados de checkout aleatórios
        
        Returns:
            Dict: Dados de checkout aleatórios
        """
        dados_checkout = self.obter_dados_checkout()
        if not dados_checkout:
            # Dados padrão caso não existam no arquivo
            return {
                "first_name": "Teste",
                "last_name": "Automacao",
                "zip_code": "12345-678"
            }
        return random.choice(dados_checkout)
    
    def obter_usuarios_validos(self) -> List[Dict[str, str]]:
        """
        Retorna apenas usuários válidos (que podem fazer login)
        
        Returns:
            List[Dict]: Lista de usuários válidos
        """
        usuarios_validos = []
        for usuario in self.obter_usuarios():
            tipo = usuario.get("tipo", "")
            if tipo in ["valido", "performance", "problema", "erro", "visual"]:
                usuarios_validos.append(usuario)
        return usuarios_validos
    
    def obter_usuarios_invalidos(self) -> List[Dict[str, str]]:
        """
        Retorna apenas usuários inválidos (que não podem fazer login)
        
        Returns:
            List[Dict]: Lista de usuários inválidos
        """
        return self.obter_usuarios_por_tipo("bloqueado")
    
    def validar_dados(self) -> bool:
        """
        Valida se os dados estão no formato correto
        
        Returns:
            bool: True se os dados são válidos, False caso contrário
        """
        try:
            if not self.dados:
                return False
            
            if "usuarios" not in self.dados:
                return False
            
            for usuario in self.dados["usuarios"]:
                campos_obrigatorios = ["username", "password", "tipo"]
                for campo in campos_obrigatorios:
                    if campo not in usuario:
                        return False
            
            return True
            
        except Exception:
            return False
    
    def obter_estatisticas(self) -> Dict[str, int]:
        """
        Retorna estatísticas dos dados carregados
        
        Returns:
            Dict: Estatísticas dos dados
        """
        usuarios = self.obter_usuarios()
        dados_checkout = self.obter_dados_checkout()
        
        tipos_usuarios = {}
        for usuario in usuarios:
            tipo = usuario.get("tipo", "desconhecido")
            tipos_usuarios[tipo] = tipos_usuarios.get(tipo, 0) + 1
        
        return {
            "total_usuarios": len(usuarios),
            "total_dados_checkout": len(dados_checkout),
            "tipos_usuarios": tipos_usuarios
        }
