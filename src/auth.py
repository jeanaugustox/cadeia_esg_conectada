import sys
from usuarios import (
    carregar_usuarios,
    salvar_usuarios,
    cadastrar_usuario_publico,
)
from utils import (
    entrada_segura,
    log_sucesso,
    log_erro,
    log_info,
    log_validacao,
    validar_senha,
)


def esqueci_senha():
    try:
        log_info("\n" + "=" * 60)
        log_info("RECUPERAÇÃO DE SENHA")
        log_info("=" * 60)

        nome = entrada_segura("Nome de usuário: ")
        email = entrada_segura("Email cadastrado: ").lower()

        usuarios = carregar_usuarios()
        usuario_encontrado = None

        for usuario in usuarios:
            nome_ok = usuario.get("nome") == nome
            email_ok = usuario.get("email", "").lower() == email

            if nome_ok and email_ok:
                usuario_encontrado = usuario
                break

        if not usuario_encontrado:
            log_erro("Usuário ou email inválidos.")
            return False

        while True:
            nova_senha = entrada_segura("Nova senha (mín. 6 caracteres): ")
            valida, mensagem = validar_senha(nova_senha)
            if not valida:
                log_validacao(mensagem)
                continue
            break
    except KeyboardInterrupt as e:
        log_info(f"\n{e}\nVoltando ao menu principal...")
        return False

    # Atualiza a senha no array e salva
    for i in range(len(usuarios)):
        if usuarios[i].get("id") == usuario_encontrado.get("id"):
            usuarios[i]["senha"] = nova_senha
            break

    if salvar_usuarios(usuarios):
        log_sucesso("Senha atualizada com sucesso! Faça login com a nova senha.")
        return True
    else:
        log_erro("Erro ao atualizar senha!")
        return False


def login():
    log_info("\n" + "=" * 60)
    log_info("TELA DE LOGIN")
    log_info("=" * 60)

    while True:
        try:
            nome = entrada_segura("Nome de usuário: ")
            senha = entrada_segura("Senha: ")

            usuarios = carregar_usuarios()
            usuario_valido = None

            for usuario in usuarios:
                nome_ok = usuario.get("nome") == nome
                senha_ok = usuario.get("senha") == senha
                ativo_ok = usuario.get("ativo", True)

                if nome_ok and senha_ok and ativo_ok:
                    usuario_valido = usuario
                    break

            if usuario_valido:
                log_sucesso(f"Bem-vindo(a), {usuario_valido.get('nome')}!")
                return usuario_valido

            log_erro("Credenciais inválidas ou usuário inativo.")
            log_info("-" * 60)
            log_info("1. Tentar novamente")
            log_info("2. Esqueci a senha")
            log_info("0. Sair do Sistema")
            log_info("-" * 60)

            opcao = entrada_segura("Escolha uma opção: ")

            if opcao == "1":
                continue
            elif opcao == "2":
                esqueci_senha()
                continue
            elif opcao == "0":
                log_info("\n👋 Obrigado por usar o Cadeia ESG Conectada!")
                sys.exit(0)
            else:
                log_validacao("Opção inválida! Tente novamente.")
                input("\nPressione Enter para continuar...")
        except KeyboardInterrupt as e:
            log_info(f"\n{e}\nVoltando ao menu principal...")
            return None


def menu_auth(exibir_opcoes_navegacao: bool = False):
    while True:
        try:
            log_info("\n" + "=" * 60)
            log_info("MÓDULO DE AUTENTICAÇÃO")
            log_info("=" * 60)
            log_info("1. Fazer Login")
            log_info("2. Cadastrar Usuário")
            log_info("3. Esqueci a Senha")
            if exibir_opcoes_navegacao:
                log_info("4. Voltar ao Menu Principal")
                log_info("0. Sair do Sistema")
            else:
                log_info("0. Sair do Sistema")
            log_info("-" * 60)

            opcao = entrada_segura("Escolha uma opção: ")

            if opcao == "1":
                usuario_logado = login()
                if usuario_logado:
                    return usuario_logado
            elif opcao == "2":
                cadastrar_usuario_publico()
            elif opcao == "3":
                esqueci_senha()
            elif exibir_opcoes_navegacao and opcao == "4":
                return None
            elif opcao == "0":
                log_info("\n👋 Obrigado por usar o Cadeia ESG Conectada!")
                sys.exit(0)
            else:
                log_validacao("Opção inválida! Tente novamente.")
                input("\nPressione Enter para continuar...")
        except KeyboardInterrupt:
            log_info("\nOperação cancelada. Voltando ao menu principal...")
            return None
