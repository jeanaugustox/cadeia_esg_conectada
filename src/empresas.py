import sys
from usuarios import listar_usuarios_empresa
from utils import (
    entrada_segura,
    carregar_arquivo_json,
    salvar_arquivo_json,
    log_sucesso,
    log_erro,
    log_info,
    log_validacao,
    gerar_id,
    formatar_data,
    validar_senha,
    validar_email,
)

ARQUIVO_EMPRESAS = "data/empresas.json"


def carregar_empresas():
    """Carrega empresas do arquivo JSON."""
    return carregar_arquivo_json(ARQUIVO_EMPRESAS)


def salvar_empresas(empresas):
    """Salva empresas no arquivo JSON."""
    return salvar_arquivo_json(ARQUIVO_EMPRESAS, empresas)


def cadastrar_empresa():
    """
    Cadastra uma nova empresa.
    """
    try:
        log_info("\n" + "=" * 60)
        log_info("CADASTRO DE EMPRESA")
        log_info("=" * 60)
        log_info("\nDADOS DA EMPRESA:")

        empresas = carregar_empresas()

        while True:
            nome_empresa = entrada_segura("Nome da Empresa: ").title().strip()
            if not nome_empresa:
                log_validacao("Nome da empresa é obrigatório!")
                continue
            break

        while True:
            cnpj = entrada_segura("CNPJ (xx.xxx.xxx/xxxx-xx): ").strip()
            if not cnpj:
                log_validacao("CNPJ é obrigatório!")
                continue
            if any(empresa.get("cnpj") == cnpj for empresa in empresas):
                log_validacao("CNPJ já cadastrado!")
                continue
            break

        contato_empresarial = entrada_segura(
            "Contato Empresarial (XX) XXXXX-XXXX: "
        ).strip()

        while True:
            email_empresarial = entrada_segura("Email Empresarial: ").lower().strip()
            valido, mensagem = validar_email(email_empresarial)
            if not valido:
                log_validacao(mensagem)
                continue
            break

        while True:
            email_confirmacao = entrada_segura("Confirmação de Email: ").lower().strip()
            valido, mensagem = validar_email(email_confirmacao)
            if not valido:
                log_validacao(mensagem)
                continue
            if email_empresarial != email_confirmacao:
                log_validacao("Emails não coincidem!")
                continue
            break

        while True:
            nome_responsavel = entrada_segura("Nome do Responsável: ").title().strip()
            if not nome_responsavel:
                log_validacao("Nome do responsável é obrigatório!")
                continue
            break

        cpf_responsavel = entrada_segura(
            "CPF do Responsável (xxx.xxx.xxx-xx): "
        ).strip()
        outro_contato = entrada_segura("Outro Contato (opcional): ").strip()
        nome_usuario = entrada_segura("Nome de Usuário: ").lower().strip()

        while True:
            senha = entrada_segura("Senha: ").strip()
            valida, mensagem = validar_senha(senha)
            if not valida:
                log_validacao(mensagem)
                continue
            break

        log_info("\nENDEREÇO DA EMPRESA:")
        cep = entrada_segura("CEP (xx.xxx-xxx): ").strip()
        logradouro = entrada_segura("Logradouro: ").title().strip()
        numero = entrada_segura("Número: ").strip()
        complemento = entrada_segura("Complemento: ").title().strip()
        bairro = entrada_segura("Bairro: ").title().strip()
        cidade = entrada_segura("Cidade: ").title().strip()
        estado = entrada_segura("Estado: ").upper().strip()

        observacoes = entrada_segura("Observações: ").title().strip()

        nova_empresa = {
            "id": gerar_id(empresas),
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
                "estado": estado,
            },
            "observacoes": observacoes,
            "data_cadastro": formatar_data(),
            "ativo": True,
        }

        empresas.append(nova_empresa)

        if salvar_empresas(empresas):
            log_sucesso(f"Empresa '{nome_empresa}' cadastrada com sucesso!")
            return True
        else:
            log_erro("Erro ao salvar empresa!")
            return False

    except KeyboardInterrupt as e:
        log_info(f"\n{e}\nVoltando ao menu principal...")
        return False


def listar_empresas():
    """
    Lista todas as empresas cadastradas.
    """
    empresas = carregar_empresas()

    if not empresas:
        log_erro("Nenhuma empresa cadastrada.")
        return

    log_info(f"\nEMPRESAS CADASTRADAS ({len(empresas)} empresas)")
    log_info("-" * 60)

    for empresa in empresas:
        empresa_ativa = empresa.get("ativo", True)
        status = "✅ Ativa" if empresa_ativa else "❌ Inativa"
        log_info(f"ID: {empresa['id']}")
        log_info(f"Nome: {empresa['nome_empresa']}")
        log_info(f"CNPJ: {empresa['cnpj']}")
        log_info(f"Email: {empresa['email_empresarial']}")
        log_info(f"Responsável: {empresa['nome_responsavel']}")
        log_info(f"Data Cadastro: {empresa['data_cadastro']}")
        log_info(f"Status: {status}")
        log_info("-" * 60)


def buscar_empresa_por_id(empresa_id: int):
    empresas = carregar_empresas()
    for empresa in empresas:
        if empresa.get("id") == empresa_id:
            return empresa
    return None


def buscar_empresas_por_nome():
    """
    Busca empresas por nome.
    """
    try:
        search = entrada_segura("Digite o nome da empresa: ").title().strip()
        empresas = carregar_empresas()
        empresas_encontradas = []

        if not empresas:
            log_erro("Nenhuma empresa cadastrada!")
            return

        for empresa in empresas:
            if search.lower() in empresa["nome_empresa"].lower():
                empresas_encontradas.append(empresa)

        if empresas_encontradas:
            log_info(f"EMPRESAS ENCONTRADAS ({len(empresas_encontradas)} empresas)")
            log_info("-" * 60)
            for empresa in empresas_encontradas:
                log_info(f"ID: {empresa['id']}")
                log_info(f"Nome: {empresa['nome_empresa']}")
                log_info(f"CNPJ: {empresa['cnpj']}")
                log_info(f"Email: {empresa['email_empresarial']}")
                log_info(f"Responsável: {empresa['nome_responsavel']}")
                log_info("-" * 60)
        else:
            log_erro("Nenhuma empresa encontrada!")
    except KeyboardInterrupt as e:
        log_info(f"\n{e}\nVoltando ao menu principal...")


def atualizar_empresa():
    """
    Atualiza dados de uma empresa existente.
    """
    try:
        empresa_id = int(
            entrada_segura("Digite o ID da empresa que deseja atualizar: ").strip()
        )

        empresa = buscar_empresa_por_id(empresa_id)
        if not empresa:
            log_erro("Empresa não encontrada!")
            return False

        log_info(f"\nEDITANDO EMPRESA: {empresa['nome_empresa']}")
        log_info("Deixe em branco para manter o valor atual.")

        novo_nome = entrada_segura(
            f"Nome da Empresa [{empresa['nome_empresa']}]: "
        ).strip()
        if novo_nome:
            empresa["nome_empresa"] = novo_nome
        else:
            log_info(f"Nome mantido como '{empresa['nome_empresa']}'.")

        novo_contato = entrada_segura(
            f"Contato Empresarial [{empresa['contato_empresarial']}]: "
        ).strip()
        if novo_contato:
            empresa["contato_empresarial"] = novo_contato
        else:
            log_info(f"Contato mantido como '{empresa['contato_empresarial']}'.")

        novo_email = entrada_segura(
            f"Email Empresarial [{empresa['email_empresarial']}]: "
        ).strip()
        if novo_email:
            empresa["email_empresarial"] = novo_email
        else:
            log_info(f"Email mantido como '{empresa['email_empresarial']}'.")

        novo_responsavel = (
            entrada_segura(f"Nome do Responsável [{empresa['nome_responsavel']}]: ")
            .title()
            .strip()
        )
        if novo_responsavel:
            empresa["nome_responsavel"] = novo_responsavel
        else:
            log_info(f"Responsável mantido como '{empresa['nome_responsavel']}'.")

        novo_usuario = (
            entrada_segura(f"Nome de Usuário [{empresa['nome_usuario']}]: ")
            .lower()
            .strip()
        )
        if novo_usuario:
            empresa["nome_usuario"] = novo_usuario
        else:
            log_info(f"Usuário mantido como '{empresa['nome_usuario']}'.")

        log_info("\nEDITANDO ENDEREÇO")
        novo_logradouro = (
            entrada_segura(f"Logradouro [{empresa['endereco']['logradouro']}]: ")
            .title()
            .strip()
        )
        if novo_logradouro:
            empresa["endereco"]["logradouro"] = novo_logradouro
        else:
            log_info(
                f"Logradouro mantido como " f"'{empresa['endereco']['logradouro']}'."
            )

        novo_numero = entrada_segura(
            f"Número [{empresa['endereco']['numero']}]: "
        ).strip()
        if novo_numero:
            empresa["endereco"]["numero"] = novo_numero
        else:
            log_info(f"Número mantido como '{empresa['endereco']['numero']}'.")

        novo_bairro = (
            entrada_segura(f"Bairro [{empresa['endereco']['bairro']}]: ")
            .title()
            .strip()
        )
        if novo_bairro:
            empresa["endereco"]["bairro"] = novo_bairro
        else:
            log_info(f"Bairro mantido como '{empresa['endereco']['bairro']}'.")

        nova_cidade = (
            entrada_segura(f"Cidade [{empresa['endereco']['cidade']}]: ")
            .title()
            .strip()
        )
        if nova_cidade:
            empresa["endereco"]["cidade"] = nova_cidade
        else:
            log_info(f"Cidade mantida como '{empresa['endereco']['cidade']}'.")

        novo_estado = (
            entrada_segura(f"Estado [{empresa['endereco']['estado']}]: ")
            .upper()
            .strip()
        )
        if novo_estado:
            empresa["endereco"]["estado"] = novo_estado
        else:
            log_info(f"Estado mantido como '{empresa['endereco']['estado']}'.")

        nova_observacao = (
            entrada_segura(f"Observações [{empresa['observacoes']}]: ").title().strip()
        )
        if nova_observacao:
            empresa["observacoes"] = nova_observacao
        else:
            log_info(f"Observações mantidas como '{empresa['observacoes']}'.")

        empresas = carregar_empresas()
        for i in range(len(empresas)):
            if empresas[i].get("id") == empresa["id"]:
                empresas[i] = empresa
                break

        if salvar_empresas(empresas):
            log_sucesso("Empresa atualizada com sucesso!")
            return True
        else:
            log_erro("Erro ao salvar alterações!")
            return False

    except KeyboardInterrupt as e:
        log_info(f"\n{e}\nVoltando ao menu principal...")
        return False
    except ValueError:
        log_validacao("ID inválido!")
        return False


def excluir_empresa():
    """
    Exclui (desativa) uma empresa.
    """
    try:
        empresa_id = int(
            entrada_segura("Digite o ID da empresa que deseja excluir: ").strip()
        )

        empresa = buscar_empresa_por_id(empresa_id)

        if not empresa:
            log_erro("Empresa não encontrada!")
            return False

        nome_empresa = empresa["nome_empresa"]
        confirmacao = (
            entrada_segura(
                f"\n⚠️ Tem certeza que deseja excluir '{nome_empresa}'? (s/n): "
            )
            .strip()
            .lower()
        )

        if confirmacao in ["s", "sim"]:
            empresas = carregar_empresas()
            for i in range(len(empresas)):
                if empresas[i].get("id") == empresa_id:
                    empresas[i]["ativo"] = False
                    break

            if salvar_empresas(empresas):
                log_sucesso(f"Empresa '{nome_empresa}' excluída com sucesso!")
                return True
            else:
                log_erro(f"Erro ao excluir empresa '{nome_empresa}'!")
                return False
        else:
            log_validacao(f"Operação cancelada para empresa '{nome_empresa}'.")
            return False
    except KeyboardInterrupt as e:
        log_info(f"\n{e}\nVoltando ao menu principal...")
        return False


def listar_usuarios_da_empresa():
    """
    Lista usuários de uma empresa específica.
    """
    try:
        empresa_id = int(
            entrada_segura("Digite o ID da empresa para listar seus usuários: ").strip()
        )

        empresa = buscar_empresa_por_id(empresa_id)
        if not empresa:
            log_erro("Empresa não encontrada!")
            return

        log_info(f"\nUSUÁRIOS DA EMPRESA: {empresa['nome_empresa']}")
        log_info("=" * 60)
        listar_usuarios_empresa(empresa_id)

    except KeyboardInterrupt as e:
        log_info(f"\n{e}\nVoltando ao menu principal...")
    except ValueError:
        log_validacao("ID inválido!")


def menu_empresas():
    """
    Menu principal do módulo de empresas.
    """
    while True:
        try:
            log_info("\n" + "=" * 60)
            log_info("MÓDULO DE EMPRESAS")
            log_info("=" * 60)
            log_info("1. Cadastrar Empresa")
            log_info("2. Listar Empresas")
            log_info("3. Buscar Empresa por Nome")
            log_info("4. Atualizar Empresa")
            log_info("5. Excluir Empresa")
            log_info("6. Listar Usuários da Empresa")
            log_info("7. Voltar ao Menu Principal")
            log_info("0. Sair do Sistema")
            log_info("-" * 60)

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
                listar_usuarios_da_empresa()
            elif opcao == "7":
                return
            elif opcao == "0":
                log_info("\n👋 Obrigado por usar o Cadeia ESG Conectada!")
                sys.exit(0)
            else:
                log_validacao("Opção inválida! Tente novamente.")
                input("\nPressione Enter para continuar...")

        except KeyboardInterrupt:
            log_info("\nOperação cancelada. Voltando ao menu principal...")
            return
