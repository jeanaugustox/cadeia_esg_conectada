import sys
from empresas import carregar_empresas, salvar_empresas, buscar_empresa_por_id
from utils import (
    entrada_segura,
    log_sucesso,
    log_erro,
    log_info,
    log_validacao,
    validar_formato_data,
    limpa_terminal,
)


def registrar_novo_certificado():
    """
    Registra um novo certificado para uma empresa.
    """
    try:
        log_info("\n" + "=" * 60)
        log_info("REGISTRAR NOVO CERTIFICADO")
        log_info("=" * 60)

        while True:
            try:
                empresa_id = int(
                    entrada_segura(
                        "Digite o ID da empresa que receberá o certificado: "
                    ).strip()
                )
            except ValueError:
                log_validacao("ID inválido!")
                continue

            empresa_encontrada = buscar_empresa_por_id(empresa_id)
            if not empresa_encontrada:
                log_validacao("Empresa não encontrada com este ID.")
                continue

            if not empresa_encontrada.get("ativo", True):
                log_validacao(
                    f"Empresa '{empresa_encontrada.get('nome_empresa')}' "
                    f"está inativa e não pode receber certificados."
                )
                continue

            break

        log_info(
            f"Adicionando certificado para a empresa: "
            f"{empresa_encontrada.get('nome_empresa')}"
        )

        while True:
            certificado = (
                entrada_segura(
                    "Digite o nome do seu certificado ESG: ").strip().title()
            )
            if not certificado:
                log_validacao("Nome do certificado é obrigatório!")
                continue
            break

        while True:
            categoria = (
                entrada_segura("Digite a categoria do seu certificado: ")
                .strip()
                .title()
            )
            if not categoria:
                log_validacao("Categoria é obrigatória!")
                continue
            break

        while True:
            emitido = entrada_segura(
                "Digite onde foi emitido (Fonte oficial): "
            ).strip()
            if not emitido:
                log_validacao("Fonte de emissão é obrigatória!")
                continue
            break

        while True:
            validade = entrada_segura(
                "Digite a data de validade (ex: DD/MM/AAAA): "
            ).strip()
            if not validade:
                log_validacao("Data de validade é obrigatória!")
                continue
            if not validar_formato_data(validade):
                log_validacao(
                    "Formato de data inválido! Use DD/MM/AAAA (ex: 31/12/2024)"
                )
                continue
            break

        while True:
            emissao = entrada_segura(
                "Digite a data de emissão (ex: DD/MM/AAAA): "
            ).strip()
            if not emissao:
                log_validacao("Data de emissão é obrigatória!")
                continue
            if not validar_formato_data(emissao):
                log_validacao(
                    "Formato de data inválido! Use DD/MM/AAAA (ex: 31/12/2024)"
                )
                continue
            break

        empresas = carregar_empresas()

        indice_empresa = -1
        for i in range(len(empresas)):
            if empresas[i].get("id") == empresa_id:
                indice_empresa = i
                break

        if indice_empresa == -1:
            log_erro("Erro ao localizar empresa na lista.")
            return False

        if "certificados" not in empresas[indice_empresa]:
            empresas[indice_empresa]["certificados"] = []

        certificados_existentes = empresas[indice_empresa].get(
            "certificados", [])
        novo_registro = {
            "certificado_id": len(certificados_existentes) + 1,
            "nome_certificado": certificado,
            "categoria": categoria,
            "emitido_por": emitido,
            "data_validade": validade,
            "data_emissao": emissao,
        }

        empresas[indice_empresa]["certificados"].append(novo_registro)

        if salvar_empresas(empresas):
            log_sucesso("Certificado registrado e salvo com sucesso!")
            return True
        else:
            log_erro("Erro ao salvar o certificado.")
            return False

    except KeyboardInterrupt as e:
        log_info(f"\n{e}\nVoltando ao menu principal...")
        return False


def ranking_empresas():
    """
    Calcula e exibe o ranking de empresas com base no número de certificados.
    """
    log_info("\n" + "=" * 60)
    log_info("RANKING TOTAL DE CERTIFICADOS")
    log_info("=" * 60)

    empresas = carregar_empresas()

    if not empresas:
        log_erro("Nenhuma empresa registrada para o ranking.")
        return

    empresas_ativas = [e for e in empresas if e.get("ativo", True)]

    if not empresas_ativas:
        log_erro("Nenhuma empresa encontrada.")
        return

    ranking_dados = []
    for empresa in empresas_ativas:
        nome_empresa = empresa.get("nome_empresa", "Empresa Desconhecida")
        quantidade_certificados = len(empresa.get("certificados", []))
        ranking_dados.append((nome_empresa, quantidade_certificados))

    ranking_dados.sort(key=lambda x: x[1], reverse=True)

    log_info(f"{'Pos.':<5} | {'Empresa':<30} | {'Qtd. Certificados':<20}")
    log_info("-" * 60)
    for i, (empresa, contagem) in enumerate(ranking_dados, 1):
        log_info(f"{i:<5} | {empresa:<30} | {contagem:<20}")


def listar_certificados_publicos():
    """
    Lista certificados públicos de todas as empresas.
    Mostra apenas nome da empresa, nome do certificado, categoria e validade.
    """
    empresas = carregar_empresas()
    empresas_ativas = [e for e in empresas if e.get("ativo", True)]

    if not empresas_ativas:
        log_erro("Nenhuma empresa cadastrada.")
        return

    log_info("\n" + "=" * 60)
    log_info("CERTIFICADOS PÚBLICOS")
    log_info("=" * 60)

    encontrou_algum = False
    for empresa in empresas_ativas:
        certificados = empresa.get("certificados", [])
        if certificados:
            encontrou_algum = True
            log_info(f"\nEmpresa: {empresa['nome_empresa']}")
            for cert in certificados:
                log_info(
                    f"  - {cert.get('nome_certificado', 'N/A')} "
                    f"({cert.get('categoria', 'N/A')}) - "
                    f"Validade: {cert.get('data_validade', 'N/A')}"
                )
            log_info("-" * 60)

    if not encontrou_algum:
        log_erro("Nenhum certificado encontrado.")


def menu_certificados():
    """
    Menu principal do módulo de certificados.
    """

    while True:
        try:
            log_info("\n" + "=" * 60)
            log_info("MÓDULO DE CERTIFICADOS")
            log_info("=" * 60)
            log_info("1. Registrar Novo Certificado")
            log_info("2. Ver Ranking de Empresas (Total de Certificados)")
            log_info("3. Ver Certificados Públicos")
            log_info("4. Voltar ao Menu Principal")
            log_info("0. Sair do Sistema")
            log_info("-" * 60)

            opcao = entrada_segura("Escolha uma opção: ").strip()
            limpa_terminal()

            if opcao == "1":
                registrar_novo_certificado()
            elif opcao == "2":
                ranking_empresas()
            elif opcao == "3":
                listar_certificados_publicos()
            elif opcao == "4":
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
