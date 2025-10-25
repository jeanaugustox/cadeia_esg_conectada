#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exemplo de uso do sistema Cadeia ESG Conectada
Este arquivo demonstra como usar as funções do CRUD de empresas
"""

from src.empresas import *


def exemplo_cadastro_empresa():
    """Exemplo de como cadastrar uma empresa programaticamente"""
    print("=== EXEMPLO: Cadastrando empresa programaticamente ===")

    # Dados de exemplo
    empresa_exemplo = {
        "id": 1,
        "nome_empresa": "Tech Verde Ltda",
        "cnpj": "12.345.678/0001-90",
        "contato_empresarial": "(11) 99999-9999",
        "email_empresarial": "contato@techverde.com.br",
        "nome_responsavel": "João Silva",
        "cpf_responsavel": "123.456.789-00",
        "outro_contato": "(11) 88888-8888",
        "nome_usuario": "joao.silva",
        "senha": "senha123",
        "endereco": {
            "cep": "01234-567",
            "logradouro": "Rua das Flores, 123",
            "numero": "123",
            "complemento": "Sala 45",
            "bairro": "Centro",
            "cidade": "São Paulo",
            "estado": "SP"
        },
        "observacoes": "Empresa focada em soluções sustentáveis",
        "data_cadastro": "15/12/2024 10:30:00",
        "ativo": True
    }

    # Carrega empresas existentes
    empresas = carregar_empresas()

    # Adiciona a empresa de exemplo
    empresas.append(empresa_exemplo)

    # Salva no arquivo
    if salvar_empresas(empresas):
        print("✅ Empresa de exemplo cadastrada com sucesso!")
    else:
        print("❌ Erro ao cadastrar empresa de exemplo!")


def exemplo_listar_empresas():
    """Exemplo de como listar empresas"""
    print("\n=== EXEMPLO: Listando empresas ===")
    listar_empresas()


def exemplo_buscar_empresa():
    """Exemplo de como buscar uma empresa"""
    print("\n=== EXEMPLO: Buscando empresa ===")
    # Simula busca por CNPJ
    cnpj_busca = "12.345.678/0001-90"
    empresas = carregar_empresas()

    for empresa in empresas:
        if empresa['cnpj'] == cnpj_busca:
            print(f"🔍 EMPRESA ENCONTRADA:")
            print(f"Nome: {empresa['nome_empresa']}")
            print(f"CNPJ: {empresa['cnpj']}")
            print(f"Email: {empresa['email_empresarial']}")
            break
    else:
        print("❌ Empresa não encontrada!")


def main():
    """Função principal do exemplo"""
    print("🌐 EXEMPLO DE USO - CADEIA ESG CONECTADA")
    print("="*50)

    # Executa exemplos
    exemplo_cadastro_empresa()
    exemplo_listar_empresas()
    exemplo_buscar_empresa()

    print("\n✅ Exemplos executados com sucesso!")
    print("\nPara usar o sistema interativo, execute:")
    print("python src/app.py")


if __name__ == "__main__":
    main()
