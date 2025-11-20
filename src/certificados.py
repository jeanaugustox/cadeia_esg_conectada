import sys
from empresas import carregar_empresas, salvar_empresas
from collections import Counter
from utils import (
    entrada_segura,
    log_sucesso,
    log_erro,
    log_info,
    log_validacao,
)


def registrar_novo_certificado():
    try:
        log_info("\n" + "=" * 60)
        log_info("REGISTRAR NOVO CERTIFICADO")
        log_info("=" * 60)

        empresas = carregar_empresas()

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

            empresa_encontrada = None
            indice_empresa = -1

            for i in range(len(empresas)):
                if empresas[i].get("id") == empresa_id:
                    empresa_encontrada = empresas[i]
                    indice_empresa = i
                    break

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
                entrada_segura("Digite o nome do seu certificado ESG: ").strip().title()
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
            break

        while True:
            emissao = entrada_segura(
                "Digite a data de emissão (ex: DD/MM/AAAA): "
            ).strip()
            if not emissao:
                log_validacao("Data de emissão é obrigatória!")
                continue
            break

        if "certificados" not in empresa_encontrada:
            empresa_encontrada["certificados"] = []

        novo_registro = {
            "certificado_id": len(empresa_encontrada.get("certificados", [])) + 1,
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

    lista_nomes_empresas = []
    for empresa in empresas:
        if not empresa.get("ativo", True):
            continue

        nome_empresa = empresa.get("nome_empresa", "Empresa Desconhecida")

        for cert in empresa.get("certificados", []):
            lista_nomes_empresas.append(nome_empresa)

    if not lista_nomes_empresas:
        log_erro("Nenhum certificado registrado no sistema.")
        return

    ranking = Counter(lista_nomes_empresas)

    log_info(f"{'Pos.':<5} | {'Empresa':<30} | {'Qtd. Certificados':<20}")
    log_info("-" * 60)
    for i, (empresa, contagem) in enumerate(ranking.most_common(), 1):
        log_info(f"{i:<5} | {empresa:<30} | {contagem:<20}")


def menu_certificados():
    while True:
        try:
            log_info("\n" + "=" * 60)
            log_info("MÓDULO DE CERTIFICADOS")
            log_info("=" * 60)
            log_info("1. Registrar Novo Certificado")
            log_info("2. Ver Ranking de Empresas (Total de Certificados)")
            log_info("3. Voltar ao Menu Principal")
            log_info("0. Sair do Sistema")
            log_info("-" * 60)

            opcao = entrada_segura("Escolha uma opção: ").strip()

            if opcao == "1":
                registrar_novo_certificado()
            elif opcao == "2":
                ranking_empresas()
            elif opcao == "3":
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
