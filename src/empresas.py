import json
import os
import sys
from datetime import datetime

ARQUIVO_EMPRESAS = "data/empresas.json"

# =========================
# Função de entrada segura
# =========================
def entrada_segura(mensagem: str):
    """
    Solicita entrada e permite cancelar a operação a qualquer momento.
    """
    resposta = input(mensagem).strip()
    if resposta.lower() in ["cancelar", "sair", "exit", "stop"]:
        raise KeyboardInterrupt("Operação cancelada pelo usuário.")
    return resposta


def carregar_empresas():
    try:
        with open(ARQUIVO_EMPRESAS, 'r', encoding='utf-8') as arquivo:
            return json.load(arquivo)
    except Exception as e:
        print(f"Erro ao carregar empresas: {e}")
        return []


def salvar_empresas(empresas):
    try:
        with open(ARQUIVO_EMPRESAS, 'w', encoding='utf-8') as arquivo:
            json.dump(empresas, arquivo, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Erro ao salvar empresas: {e}")
        return False


def cadastrar_empresa():
    try:
        print("\n=== CADASTRO DE EMPRESA ===")

        print(f"\nDADOS DA EMPRESA:")

        nome_empresa = entrada_segura("Nome da Empresa: ").title().strip()

        cnpj = entrada_segura("CNPJ (xx.xxx.xxx/xxxx-xx): ").strip()

        empresas = carregar_empresas()
        for empresa in empresas:
            if empresa['cnpj'] == cnpj:
                print("CNPJ já cadastrado!")
                return False

        contato_empresarial = entrada_segura("Contato Empresarial (XX) XXXXX-XXXX: ").strip()
        email_empresarial = entrada_segura("Email Empresarial: ").lower().strip()

        email_confirmacao = entrada_segura("Confirmação de Email: ").lower().strip()
        if email_empresarial != email_confirmacao:
            print("Emails não coincidem!")
            return False

        nome_responsavel = entrada_segura("Nome do Responsável: ").title().strip()
        if not nome_responsavel:
            print("Nome do responsável é obrigatório!")
            return False

        cpf_responsavel = entrada_segura("CPF do Responsável (xxx.xxx.xxx-xx): ").strip()
        outro_contato = entrada_segura("Outro Contato (opcional): ").strip()
        nome_usuario = entrada_segura("Nome de Usuário: ").lower().strip()

        senha = entrada_segura("Senha: ").strip()
        if len(senha) < 6:
            print("Senha deve ter pelo menos 6 caracteres!")
            return False

        print("\nENDEREÇO DA EMPRESA:")
        cep = entrada_segura("CEP (xx.xxx-xxx): ").strip()
        logradouro = entrada_segura("Logradouro: ").title().strip()
        numero = entrada_segura("Número: ").strip()
        complemento = entrada_segura("Complemento: ").title().strip()
        bairro = entrada_segura("Bairro: ").title().strip()
        cidade = entrada_segura("Cidade: ").title().strip()
        estado = entrada_segura("Estado: ").upper().strip()

        observacoes = entrada_segura("Observações: ").title().strip()

        nova_empresa = {
            "id": len(empresas) + 1,
            "nome_empresa": nome_empresa,
            "cnpj": cnpj,
            "contato_empresarial": contato_empresarial,
            "email_empresarial": email_empresarial,
            "nome_responsavel": nome_responsavel,
            "cpf_responsavel": cpf_responsavel,
            "outro_contato": outro_contato,
            "nome_usuario": nome_usuario,
            "senha": senha,
            "endereco": {
                "cep": cep,
                "logradouro": logradouro,
                "numero": numero,
                "complemento": complemento,
                "bairro": bairro,
                "cidade": cidade,
                "estado": estado
            },
            "observacoes": observacoes,
            "data_cadastro": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "ativo": True
        }

        empresas.append(nova_empresa)

        if salvar_empresas(empresas):
            print(f"\n✅ Empresa '{nome_empresa}' cadastrada com sucesso!")
            return True
        else:
            print("❌ Erro ao salvar empresa!")
            return False

    except KeyboardInterrupt as e:
        print(f"\n{e}\nVoltando ao menu principal...")
        return False


def listar_empresas():
    empresas = carregar_empresas()

    if not empresas:
        print("\n❌ Nenhuma empresa cadastrada.")
        return

    print(f"\nEMPRESAS CADASTRADAS ({len(empresas)} empresas)")
    print("-"*60)

    for empresa in empresas:
        empresa_ativa = empresa.get('ativo', True)
        status = "✅ Ativa" if empresa_ativa else "❌ Inativa"
        print(f"ID: {empresa['id']}")
        print(f"Nome: {empresa['nome_empresa']}")
        print(f"CNPJ: {empresa['cnpj']}")
        print(f"Email: {empresa['email_empresarial']}")
        print(f"Responsável: {empresa['nome_responsavel']}")
        print(f"Data Cadastro: {empresa['data_cadastro']}")
        print(f"Status: {status}")
        print("-"*60)


def buscar_empresa_por_id(empresa_id: int):
    empresas = carregar_empresas()
    for empresa in empresas:
        if empresa.get('id') == empresa_id:
            return empresa
    return None


def buscar_empresas_por_nome():
    try:
        search = entrada_segura("Digite o nome da empresa: ").title().strip()
        empresas = carregar_empresas()
        empresas_encontradas = []

        if not empresas:
            print("❌ Nenhuma empresa cadastrada!")
            return

        for empresa in empresas:
            if search in empresa['nome_empresa']:
                empresas_encontradas.append(empresa)

        if empresas_encontradas:
            print(f"EMPRESAS ENCONTRADAS ({len(empresas_encontradas)} empresas)")
            print("-"*60)
            for empresa in empresas_encontradas:
                print(f"ID: {empresa['id']}")
                print(f"Nome: {empresa['nome_empresa']}")
                print(f"CNPJ: {empresa['cnpj']}")
                print(f"Email: {empresa['email_empresarial']}")
                print(f"Responsável: {empresa['nome_responsavel']}")
                print("-"*60)
        else:
            print("❌ Nenhuma empresa encontrada!")
    except KeyboardInterrupt as e:
        print(f"\n{e}\nVoltando ao menu principal...")


def atualizar_empresa():
    try:
        empresa_id = int(entrada_segura("Digite o ID da empresa que deseja atualizar: ").strip())

        empresa = buscar_empresa_por_id(empresa_id)
        if not empresa:
            print("❌ Empresa não encontrada!")
            return

        print(f"\nEDITANDO EMPRESA: {empresa['nome_empresa']}")
        print("Deixe em branco para manter o valor atual.")

        novo_nome = entrada_segura(f"Nome da Empresa [{empresa['nome_empresa']}]: ").strip()
        if novo_nome:
            empresa['nome_empresa'] = novo_nome

        novo_contato = entrada_segura(f"Contato Empresarial [{empresa['contato_empresarial']}]: ").strip()
        if novo_contato:
            empresa['contato_empresarial'] = novo_contato

        novo_email = entrada_segura(f"Email Empresarial [{empresa['email_empresarial']}]: ").strip()
        if novo_email:
            empresa['email_empresarial'] = novo_email

        novo_responsavel = entrada_segura(f"Nome do Responsável [{empresa['nome_responsavel']}]: ").title().strip()
        if novo_responsavel:
            empresa['nome_responsavel'] = novo_responsavel

        novo_usuario = entrada_segura(f"Nome de Usuário [{empresa['nome_usuario']}]: ").lower().strip()
        if novo_usuario:
            empresa['nome_usuario'] = novo_usuario

        print("\nEDITANDO ENDEREÇO")
        novo_logradouro = entrada_segura(f"Logradouro [{empresa['endereco']['logradouro']}]: ").title().strip()
        if novo_logradouro:
            empresa['endereco']['logradouro'] = novo_logradouro

        novo_numero = entrada_segura(f"Número [{empresa['endereco']['numero']}]: ").strip()
        if novo_numero:
            empresa['endereco']['numero'] = novo_numero

        novo_bairro = entrada_segura(f"Bairro [{empresa['endereco']['bairro']}]: ").title().strip()
        if novo_bairro:
            empresa['endereco']['bairro'] = novo_bairro

        nova_cidade = entrada_segura(f"Cidade [{empresa['endereco']['cidade']}]: ").title().strip()
        if nova_cidade:
            empresa['endereco']['cidade'] = nova_cidade

        novo_estado = entrada_segura(f"Estado [{empresa['endereco']['estado']}]: ").upper().strip()
        if novo_estado:
            empresa['endereco']['estado'] = novo_estado

        nova_observacao = entrada_segura(f"Observações [{empresa['observacoes']}]: ").title().strip()
        if nova_observacao:
            empresa['observacoes'] = nova_observacao

        empresas = carregar_empresas()
        for i in range(len(empresas)):
            if empresas[i].get('id') == empresa['id']:
                empresas[i] = empresa
                break

        if salvar_empresas(empresas):
            print("✅ Empresa atualizada com sucesso!")
            return True
        else:
            print("❌ Erro ao salvar alterações!")
            return False

    except KeyboardInterrupt as e:
        print(f"\n{e}\nVoltando ao menu principal...")
        return False


def excluir_empresa():
    try:
        empresa_id = int(entrada_segura("Digite o ID da empresa que deseja excluir: ").strip())

        empresa = buscar_empresa_por_id(empresa_id)

        if not empresa:
            print("❌ Empresa não encontrada!")
            return False

        confirmacao = entrada_segura(
            f"\n⚠️ Tem certeza que deseja excluir '{empresa['nome_empresa']}'? (s/n): "
        ).strip().lower()

        if confirmacao in ['s', 'sim']:
            empresas = carregar_empresas()
            for i in range(len(empresas)):
                if empresas[i].get('id') == empresa_id:
                    empresas[i]['ativo'] = False
                    break

            if salvar_empresas(empresas):
                print(f"✅ Empresa '{empresa['nome_empresa']}' excluída com sucesso!")
                return True
            else:
                print(f"❌ Erro ao excluir empresa '{empresa['nome_empresa']}'!")
                return False
        else:
            print(f"❌ Operação cancelada para empresa '{empresa['nome_empresa']}'.")
            return False
    except KeyboardInterrupt as e:
        print(f"\n{e}\nVoltando ao menu principal...")
        return False


def menu_empresas():
    while True:
        try:
            print("\n" + "="*60)
            print("MÓDULO DE EMPRESAS")
            print("="*60)
            print("1. Cadastrar Empresa")
            print("2. Listar Empresas")
            print("3. Buscar Empresa por Nome")
            print("4. Atualizar Empresa")
            print("5. Excluir Empresa")
            print("6. Voltar ao Menu Principal")
            print("0. Sair do Sistema")
            print("-"*60)

            opcao = entrada_segura("Escolha uma opção: ").strip()

            if opcao == "1":
                cadastrar_empresa()
            elif opcao == "2":
                listar_empresas()
            elif opcao == "3":
                buscar_empresas_por_nome()
            elif opcao == "4":
                atualizar_empresa()
            elif opcao == "5":
                excluir_empresa()
            elif opcao == "6":
                return
            elif opcao == "0":
                print("\n👋 Obrigado por usar o Cadeia ESG Conectada!")
                sys.exit(0)
            else:
                print("❌ Opção inválida! Tente novamente.")
                input("\nPressione Enter para continuar...")

        except KeyboardInterrupt:
            print("\nOperação cancelada. Voltando ao menu principal...")
