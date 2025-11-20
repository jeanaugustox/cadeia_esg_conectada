import sys
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
)

ARQUIVO_USUARIOS = "data/usuarios.json"

# ================ CARREGAR USUÁRIOS ================ #


def carregar_usuarios():
    """Carrega usuários do arquivo JSON."""
    return carregar_arquivo_json(ARQUIVO_USUARIOS)


# ================ SALVAR USUÁRIOS ================ #


def salvar_usuarios(usuarios):
    """Salva usuários no arquivo JSON."""
    return salvar_arquivo_json(ARQUIVO_USUARIOS, usuarios)


# ================ CADASTRAR USUÁRIOS ================ #


def cadastrar_usuario():
    try:
        log_info("\n" + "=" * 60)
        log_info("CADASTRO DE USUÁRIO")
        log_info("=" * 60)

        usuarios = carregar_usuarios()

        while True:
            nome = entrada_segura("Nome de usuário: ").strip()
            if not nome:
                log_validacao("Nome de usuário é obrigatório!")
                continue
            if any(u.get("nome") == nome for u in usuarios):
                log_validacao("Usuário já existe!")
                continue
            break

        while True:
            email = entrada_segura("Email: ").lower().strip()
            if not email:
                log_validacao("Email é obrigatório!")
                continue
            break

        while True:
            senha = entrada_segura("Senha: ").strip()
            if not senha:
                log_validacao("Senha é obrigatória!")
                continue
            if len(senha) < 6:
                log_validacao("Senha deve ter pelo menos 6 caracteres!")
                continue
            break

        papeis_validos = ["Admin", "Editor", "Leitor"]
        while True:
            papel = entrada_segura("Papel (Admin / Editor / Leitor): ").title().strip()
            if not papel:
                log_validacao("Papel é obrigatório!")
                continue
            if papel not in papeis_validos:
                log_validacao("Papel inválido. Opções válidas: Admin, Editor, Leitor.")
                continue
            break

        novo_usuario = {
            "id": gerar_id(usuarios),
            "nome": nome,
            "email": email,
            "senha": senha,
            "papel": papel,
            "data_cadastro": formatar_data(),
            "ativo": True,
        }

        usuarios.append(novo_usuario)
        if salvar_usuarios(usuarios):
            log_sucesso(f"Usuário '{nome}' cadastrado com sucesso!")
            return True
        else:
            log_erro("Erro ao salvar usuário!")
            return False

    except KeyboardInterrupt as e:
        log_info(f"\n{e}\nVoltando ao menu principal...")
        return False


# ================ LISTAR USUÁRIOS ================ #


def listar_usuarios():
    usuarios = carregar_usuarios()
    if not usuarios:
        log_erro("Nenhum usuário cadastrado.")
        return

    log_info(f"\nUSUÁRIOS CADASTRADOS ({len(usuarios)} usuários)")
    log_info("-" * 60)

    for u in usuarios:
        usuario_ativo = u.get("ativo", True)
        status = "✅ Ativo" if usuario_ativo else "❌ Inativo"
        log_info(f"ID: {u['id']}")
        log_info(f"Nome: {u['nome']}")
        log_info(f"Papel: {u['papel']}")
        if "data_cadastro" in u:
            log_info(f"Data Cadastro: {u['data_cadastro']}")
        log_info(f"Status: {status}")
        log_info("-" * 60)


# ================ BUSCAR USUÁRIOS ================ #


def buscar_usuario_por_id(usuario_id: int, incluir_inativos: bool = False):
    usuarios = carregar_usuarios()
    usuario_encontrado = None

    for usuario in usuarios:
        id_confere = usuario.get("id") == usuario_id
        ativo_ok = incluir_inativos or usuario.get("ativo", True)
        if id_confere and ativo_ok:
            usuario_encontrado = usuario
            break

    return usuario_encontrado


# ================ ATUALIZAR USUÁRIOS ================ #


def atualizar_usuario():
    try:
        usuario_id = int(
            entrada_segura("Digite o ID do usuário que deseja atualizar: ").strip()
        )

        usuario = buscar_usuario_por_id(usuario_id)
        if not usuario:
            log_erro("Usuário não encontrado!")
            return False

        log_info(f"\nEDITANDO USUÁRIO: {usuario['nome']}")
        log_info("Deixe em branco para manter o valor atual.")

        novo_nome = entrada_segura(f"Nome [{usuario['nome']}]: ").strip()
        if novo_nome:
            usuario["nome"] = novo_nome
        else:
            log_info(f"Nome mantido como '{usuario['nome']}'.")

        novo_email = entrada_segura(f"Email [{usuario['email']}]: ").lower().strip()
        if novo_email:
            usuario["email"] = novo_email
        else:
            log_info(f"Email mantido como '{usuario['email']}'.")

        nova_senha = entrada_segura("Senha (deixe em branco para manter): ").strip()
        if nova_senha:
            if len(nova_senha) < 6:
                log_validacao("Senha deve ter pelo menos 6 caracteres!")
                return False
            usuario["senha"] = nova_senha
        else:
            log_info("Senha mantida (campo deixado em branco).")

        papeis_validos = ["Admin", "Editor", "Leitor"]
        novo_papel = entrada_segura(f"Papel [{usuario['papel']}]: ").title().strip()
        if novo_papel:
            if novo_papel not in papeis_validos:
                log_validacao("Papel inválido. Opções válidas: Admin, Editor, Leitor.")
                return False
            usuario["papel"] = novo_papel
        else:
            log_info(f"Papel mantido como '{usuario['papel']}'.")

        usuarios = carregar_usuarios()
        for i in range(len(usuarios)):
            if usuarios[i].get("id") == usuario["id"]:
                usuarios[i] = usuario
                break

        if salvar_usuarios(usuarios):
            log_sucesso("Usuário atualizado com sucesso!")
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


# ================ EXCLUIR USUÁRIOS ================ #


def excluir_usuario():
    try:
        usuario_id = int(
            entrada_segura("Digite o ID do usuário que deseja excluir: ").strip()
        )

        usuario = buscar_usuario_por_id(usuario_id)
        if not usuario:
            log_erro("Usuário não encontrado!")
            return False

        nome_usuario = usuario["nome"]
        confirmacao = (
            entrada_segura(
                f"\n⚠️ Tem certeza que deseja excluir " f"'{nome_usuario}'? (s/n): "
            )
            .strip()
            .lower()
        )

        if confirmacao in ["s", "sim"]:
            usuarios = carregar_usuarios()
            for i in range(len(usuarios)):
                if usuarios[i].get("id") == usuario_id:
                    usuarios[i]["ativo"] = False
                    break

            if salvar_usuarios(usuarios):
                log_sucesso(f"Usuário '{nome_usuario}' excluído com sucesso!")
                return True
            else:
                log_erro(f"Erro ao excluir usuário '{nome_usuario}'!")
                return False
        else:
            log_validacao(f"Operação cancelada para usuário '{nome_usuario}'.")
            return False

    except KeyboardInterrupt as e:
        log_info(f"\n{e}\nVoltando ao menu principal...")
        return False
    except ValueError:
        log_validacao("ID inválido!")
        return False


# ================ MENU DE USUÁRIOS ================ #


def menu_usuarios():
    while True:
        try:
            log_info("\n" + "=" * 60)
            log_info("MÓDULO DE USUÁRIOS")
            log_info("=" * 60)
            log_info("1. Cadastrar Usuário")
            log_info("2. Listar Usuários")
            log_info("3. Atualizar Usuário")
            log_info("4. Excluir Usuário")
            log_info("5. Voltar ao Menu Principal")
            log_info("0. Sair do Sistema")
            log_info("-" * 60)

            opcao = entrada_segura("Escolha uma opção: ").strip()

            if opcao == "1":
                cadastrar_usuario()
            elif opcao == "2":
                listar_usuarios()
            elif opcao == "3":
                atualizar_usuario()
            elif opcao == "4":
                excluir_usuario()
            elif opcao == "5":
                return
            elif opcao == "0":
                log_info("\n👋 Obrigado por usar o Cadeia ESG Conectada!")
                sys.exit(0)
            else:
                log_validacao("Opção inválida! Tente novamente.")
                input("\nPressione Enter para continuar...")

        except KeyboardInterrupt:
            log_info("\nOperação cancelada. Voltando ao menu principal...")
