#!/usr/bin/env python3
"""
Script para executar testes BDD com Behave
Gera relatórios HTML e Allure com screenshots
"""

import os
import sys
import subprocess
import time
from datetime import datetime


def criar_diretorios():
    """Cria os diretórios necessários para relatórios"""
    diretorios = ["reports", "screenshots", "reports/allure-results", "reports/allure-report", "logs"]
    for diretorio in diretorios:
        if not os.path.exists(diretorio):
            os.makedirs(diretorio)
            print(f"📁 Diretório criado: {diretorio}")


def executar_testes_behave():
    """Executa os testes usando behave"""
    print("=" * 60)
    print("🚀 INICIANDO EXECUÇÃO DOS TESTES BDD")
    print("=" * 60)
    
    # Comando para executar os testes
    comando = [
        "behave",
        "features/",
        "--verbose",
        "--format=pretty",
        "--outfile=reports/behave_report.txt",
        "--tags=~@skip"
    ]
    
    print(f"📋 Comando: {' '.join(comando)}")
    print("-" * 60)
    
    try:
        # Executar os testes
        resultado = subprocess.run(comando, capture_output=True, text=True)
        
        # Exibir saída
        if resultado.stdout:
            print("📤 Saída dos testes:")
            print(resultado.stdout)
        
        if resultado.stderr:
            print("⚠️  Avisos/Erros:")
            print(resultado.stderr)
        
        print(f"📊 Código de retorno: {resultado.returncode}")
        
        return resultado.returncode == 0
        
    except Exception as e:
        print(f"❌ Erro ao executar testes: {e}")
        return False


def gerar_relatorio_allure():
    """Gera relatório Allure a partir dos resultados"""
    print("\n" + "=" * 60)
    print("📊 GERANDO RELATÓRIO ALLURE")
    print("=" * 60)
    
    # Verificar se o Allure está instalado
    try:
        resultado = subprocess.run(["allure", "--version"], capture_output=True, text=True)
        if resultado.returncode == 0:
            print(f"✅ Allure encontrado: {resultado.stdout.strip()}")
        else:
            print("⚠️  Allure não encontrado. Instalando...")
            subprocess.run(["npm", "install", "-g", "allure-commandline"], check=True)
    except:
        print("⚠️  Allure não encontrado. Tentando instalar...")
        try:
            subprocess.run(["npm", "install", "-g", "allure-commandline"], check=True)
        except:
            print("❌ Não foi possível instalar o Allure automaticamente.")
            print("💡 Instale manualmente: npm install -g allure-commandline")
            return False
    
    # Gerar relatório Allure
    comando_allure = [
        "allure", "generate",
        "reports/allure-results",
        "-o", "reports/allure-report",
        "--clean"
    ]
    
    print(f"📋 Comando Allure: {' '.join(comando_allure)}")
    
    try:
        resultado = subprocess.run(comando_allure, capture_output=True, text=True)
        
        if resultado.stdout:
            print("📤 Saída do Allure:")
            print(resultado.stdout)
        
        if resultado.stderr:
            print("⚠️  Avisos do Allure:")
            print(resultado.stderr)
        
        if resultado.returncode == 0:
            print("✅ Relatório Allure gerado com sucesso!")
            return True
        else:
            print(f"❌ Erro ao gerar relatório Allure: {resultado.returncode}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao executar Allure: {e}")
        return False


def abrir_relatorio_allure():
    """Abre o relatório Allure no navegador"""
    print("\n" + "=" * 60)
    print("🌐 ABRINDO RELATÓRIO ALLURE")
    print("=" * 60)
    
    comando_abrir = [
        "allure", "open",
        "reports/allure-report"
    ]
    
    print(f"📋 Comando: {' '.join(comando_abrir)}")
    
    try:
        # Executar em background
        subprocess.Popen(comando_abrir)
        print("✅ Relatório Allure aberto no navegador!")
        print("💡 O relatório será fechado automaticamente quando você fechar o terminal.")
        
    except Exception as e:
        print(f"❌ Erro ao abrir relatório: {e}")
        print("💡 Abra manualmente: allure open reports/allure-report")


def mostrar_resumo():
    """Mostra resumo dos arquivos gerados"""
    print("\n" + "=" * 60)
    print("📋 RESUMO DOS ARQUIVOS GERADOS")
    print("=" * 60)
    
    arquivos_relatorio = [
        "reports/behave_report.txt",
        "reports/behave_report.json",
        "reports/allure-report/index.html"
    ]
    
    for arquivo in arquivos_relatorio:
        if os.path.exists(arquivo):
            tamanho = os.path.getsize(arquivo)
            print(f"✅ {arquivo} ({tamanho} bytes)")
        else:
            print(f"❌ {arquivo} (não encontrado)")
    
    # Contar screenshots
    if os.path.exists("screenshots"):
        screenshots = [f for f in os.listdir("screenshots") if f.endswith('.png')]
        print(f"📸 Screenshots capturados: {len(screenshots)}")
    
    # Contar resultados Allure
    if os.path.exists("reports/allure-results"):
        resultados = [f for f in os.listdir("reports/allure-results") if f.endswith('.json')]
        print(f"📊 Resultados Allure: {len(resultados)}")


def main():
    """Função principal"""
    print("🛒 AUTOMAÇÃO BDD - SAUCE DEMO")
    print("=" * 60)
    
    # Criar diretórios
    criar_diretorios()
    
    # Executar testes
    sucesso = executar_testes_behave()
    
    if sucesso:
        print("\n✅ Todos os testes BDD executados com sucesso!")
    else:
        print("\n⚠️  Alguns testes falharam, mas continuando...")
    
    # Gerar relatório Allure
    allure_sucesso = gerar_relatorio_allure()
    
    # Mostrar resumo
    mostrar_resumo()
    
    # Perguntar se quer abrir o relatório
    if allure_sucesso:
        resposta = input("\n🌐 Deseja abrir o relatório Allure no navegador? (s/n): ").lower()
        if resposta in ['s', 'sim', 'y', 'yes']:
            abrir_relatorio_allure()
    
    print("\n" + "=" * 60)
    print("🎉 EXECUÇÃO BDD CONCLUÍDA!")
    print("=" * 60)
    print("📁 Relatórios disponíveis em:")
    print("   - Behave: reports/behave_report.txt")
    print("   - JSON: reports/behave_report.json")
    print("   - Allure: reports/allure-report/index.html")
    print("   - Screenshots: screenshots/")
    print("=" * 60)


if __name__ == "__main__":
    main()
