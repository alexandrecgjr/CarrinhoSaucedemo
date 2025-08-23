#!/usr/bin/env python3
"""
Exemplo de execução de testes específicos
Este arquivo demonstra como executar diferentes tipos de testes
"""

import pytest
import sys
import os

# Adicionar o diretório atual ao path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.test_data_loader import TestDataLoader


def exemplo_testes_login():
    """Exemplo: Executar apenas testes de login"""
    print("🔐 Executando testes de login...")
    
    comando = [
        "pytest",
        "test_fluxo_completo_compra.py::TestFluxoCompletoCompra::test_login_usuarios_validos",
        "-v",
        "--html=reports/login_report.html",
        "--self-contained-html"
    ]
    
    print(f"Comando: {' '.join(comando)}")
    return comando


def exemplo_testes_fluxo_completo():
    """Exemplo: Executar apenas fluxo completo de compra"""
    print("🛒 Executando fluxo completo de compra...")
    
    comando = [
        "pytest",
        "test_fluxo_completo_compra.py::TestFluxoCompletoCompra::test_fluxo_completo_compra",
        "-v",
        "--html=reports/fluxo_completo_report.html",
        "--self-contained-html"
    ]
    
    print(f"Comando: {' '.join(comando)}")
    return comando


def exemplo_testes_performance():
    """Exemplo: Executar apenas testes de performance"""
    print("⚡ Executando testes de performance...")
    
    comando = [
        "pytest",
        "test_fluxo_completo_compra.py::TestFluxoCompletoCompra::test_performance_glitch_user",
        "-v",
        "--html=reports/performance_report.html",
        "--self-contained-html"
    ]
    
    print(f"Comando: {' '.join(comando)}")
    return comando


def exemplo_testes_por_marker():
    """Exemplo: Executar testes por marcador"""
    print("🏷️ Executando testes por marcador...")
    
    comando = [
        "pytest",
        "test_fluxo_completo_compra.py",
        "-m", "smoke",  # Apenas testes marcados como 'smoke'
        "-v",
        "--html=reports/smoke_report.html",
        "--self-contained-html"
    ]
    
    print(f"Comando: {' '.join(comando)}")
    return comando


def exemplo_testes_paralelos():
    """Exemplo: Executar testes em paralelo"""
    print("🔄 Executando testes em paralelo...")
    
    comando = [
        "pytest",
        "test_fluxo_completo_compra.py",
        "-n", "2",  # 2 processos paralelos
        "-v",
        "--html=reports/parallel_report.html",
        "--self-contained-html"
    ]
    
    print(f"Comando: {' '.join(comando)}")
    return comando


def exemplo_com_retry():
    """Exemplo: Executar testes com retry em caso de falha"""
    print("🔄 Executando testes com retry...")
    
    comando = [
        "pytest",
        "test_fluxo_completo_compra.py",
        "--reruns", "2",  # Tentar 2 vezes em caso de falha
        "--reruns-delay", "1",  # Esperar 1 segundo entre tentativas
        "-v",
        "--html=reports/retry_report.html",
        "--self-contained-html"
    ]
    
    print(f"Comando: {' '.join(comando)}")
    return comando


def mostrar_dados_teste():
    """Mostra os dados de teste disponíveis"""
    print("📊 Dados de teste disponíveis:")
    print("=" * 50)
    
    try:
        loader = TestDataLoader()
        estatisticas = loader.obter_estatisticas()
        
        print(f"Total de usuários: {estatisticas['total_usuarios']}")
        print(f"Total de dados de checkout: {estatisticas['total_dados_checkout']}")
        print("\nTipos de usuários:")
        for tipo, quantidade in estatisticas['tipos_usuarios'].items():
            print(f"  - {tipo}: {quantidade}")
        
        print("\nUsuários disponíveis:")
        usuarios = loader.obter_usuarios()
        for usuario in usuarios:
            print(f"  - {usuario['username']} ({usuario['tipo']})")
        
        print("\nDados de checkout:")
        dados_checkout = loader.obter_dados_checkout()
        for dados in dados_checkout:
            print(f"  - {dados['first_name']} {dados['last_name']} - {dados['zip_code']}")
            
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")


def main():
    """Função principal com menu de opções"""
    print("🚀 EXEMPLOS DE EXECUÇÃO DE TESTES")
    print("=" * 50)
    
    while True:
        print("\nEscolha uma opção:")
        print("1. Mostrar dados de teste")
        print("2. Testes de login")
        print("3. Fluxo completo de compra")
        print("4. Testes de performance")
        print("5. Testes por marcador")
        print("6. Testes em paralelo")
        print("7. Testes com retry")
        print("8. Executar todos os testes")
        print("0. Sair")
        
        opcao = input("\nDigite sua opção: ").strip()
        
        if opcao == "0":
            print("👋 Saindo...")
            break
        elif opcao == "1":
            mostrar_dados_teste()
        elif opcao == "2":
            exemplo_testes_login()
        elif opcao == "3":
            exemplo_testes_fluxo_completo()
        elif opcao == "4":
            exemplo_testes_performance()
        elif opcao == "5":
            exemplo_testes_por_marker()
        elif opcao == "6":
            exemplo_testes_paralelos()
        elif opcao == "7":
            exemplo_com_retry()
        elif opcao == "8":
            print("🎯 Executando todos os testes...")
            print("Comando: python run_tests.py")
        else:
            print("❌ Opção inválida!")
        
        input("\nPressione Enter para continuar...")


if __name__ == "__main__":
    main()


