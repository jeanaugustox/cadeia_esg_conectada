import json
import os
import sys
from datetime import datetime

ARQUIVO_USUARIOS = "data/usuarios.json"


# ===========================
# 🔹 Funções utilitárias
# ===========================

class OperacaoCancelada(Exception):
    """Exceção personalizada para cancelamento de operação."""
    pass


def input_cancelavel(mensagem: str) -> str:
    """Input que permite o usuário digitar 'cancelar' ou 'sair' para interromper a operação."""
    valor = input(mensagem).strip()
    if valor.lower() in ["cancelar", "sair"]:
        raise OperacaoCancelada
    return valor


# ===========================
# 🔹 Funções de arquivo
# ===========================

def carregar_usuarios():
    try:
        if not os.path.exists(ARQUIVO_USUARIOS):
            return []
        with open(ARQUIVO_USUARIOS, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except Exception as e:
        print(f"Erro ao carregar usuários: {e}")
        return []


def salvar_usuarios(usuarios):
    try:
        with open(ARQUIVO_USUARIOS, "w", encoding="utf-8") as arquivo:
            json.dump(usuarios, arquivo, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Erro ao salvar usuários: {e}")
        return False


# ===========================
# 🔹 Funções principais
# ===========================

def cadastrar_usuario():
    print("\n=== CADASTRO DE USUÁRIO ===")

    try:
        usuarios = carregar_usuarios()

        nome = input_cancelavel("Nome de usuário: ")
        if any(u.get("nome") == nome for u in usuarios):
            print("❌ Usuário já existe!")
            return False

        email = input_cancelavel("Email: ").lower()
        senha = input_cancelavel("Senha: ")

        papeis_validos = ["Admin", "Editor", "Leitor"]
        while True:
            papel = input_cancelavel("Papel (Admin / Editor / Leitor): ").title()
            if papel in papeis_validos:
                break
            print("❌ Papel inválido. Opções válidas: Admin, Editor, Leitor.")

        novo_usuario = {
            "id": len(usuarios) + 1,
            "nome": nome,
            "email": email,
            "senha": senha,
            "papel": papel,
            "data_cadastro": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "ativo": True,
        }

        usuarios.append(novo_usuario)
        if salvar_usuarios(usuarios):
            print(f"\n✅ Usuário '{nome}' cadastrado com sucesso!")
            return True
        else:
            print("❌ Erro ao salvar usuário!")
            return False

    except OperacaoCancelada:
        print("\n❌ Operação cancelada pelo usuário.")
        return False


def listar_usuarios():
    usuarios = carregar_usuarios()
    if not usuarios:
        print("\n❌ Nenhum usuário cadastrado.")
        return

    print(f"\nUSUÁRIOS CADASTRADOS ({len(usuarios)} usuários)")
    print("-"*60)

    for u in usuarios:
        usuario_ativo = u.get('ativo', True)
        status = "✅ Ativo" if usuario_ativo else "❌ Inativo"
        print(f"ID: {u['id']}")
        print(f"Nome: {u['nome']}")
        print(f"Papel: {u['papel']}")
        if 'data_cadastro' in u:
            print(f"Data Cadastro: {u['data_cadastro']}")
        print(f"Status: {status}")
        print("-"*60)


def buscar_usuario_por_id(usuario_id: int, incluir_inativos: bool = False):
    usuarios = carregar_usuarios()
    usuario_encontrado = None

    for usuario in usuarios:
        id_confere = usuario.get('id') == usuario_id
        ativo_ok = incluir_inativos or usuario.get('ativo', True)
        if id_confere and ativo_ok:
            usuario_encontrado = usuario
            break

    return usuario_encontrado


def atualizar_usuario():
    try:
        usuario_id = int(input_cancelavel("Digite o ID do usuário que deseja atualizar: "))
        usuario = buscar_usuario_por_id(usuario_id)
        if not usuario:
            print("❌ Usuário não encontrado!")
            return

        print("\nEDITANDO USUÁRIO")
        print("Deixe em branco para manter o valor atual.")

        novo_nome = input_cancelavel(f"Nome ({usuario['nome']}): ")
        if novo_nome:
            usuario['nome'] = novo_nome

        nova_senha = input_cancelavel("Senha: ")
        if nova_senha:
            usuario['senha'] = nova_senha

        novo_papel = input_cancelavel(f"Papel ({usuario['papel']}): ").title()
        if novo_papel:
            if novo_papel not in ["Admin", "Editor", "Leitor"]:
                print("❌ Papel inválido.")
                return
            usuario['papel'] = novo_papel

        usuarios = carregar_usuarios()
        for i in range(len(usuarios)):
            if usuarios[i].get('id') == usuario['id']:
                usuarios[i] = usuario
                break

        if salvar_usuarios(usuarios):
            print("✅ Usuário atualizado com sucesso!")
        else:
            print("❌ Erro ao salvar alterações!")

    except OperacaoCancelada:
        print("\n❌ Operação cancelada pelo usuário.")
        return
    except ValueError:
        print("❌ ID inválido!")
        return


def excluir_usuario():
    try:
        usuario_id = int(input_cancelavel("Digite o ID do usuário que deseja excluir: "))
    except ValueError:
        print("❌ ID inválido!")
        return False
    except OperacaoCancelada:
        print("\n❌ Operação cancelada pelo usuário.")
        return False

    usuario = buscar_usuario_por_id(usuario_id)
    if not usuario:
        print("❌ Usuário não encontrado!")
        return False

    try:
        confirmacao = input_cancelavel(
            f"\n⚠️ Tem certeza que deseja excluir '{usuario['nome']}'? (s/n): "
        ).lower()

        if confirmacao in ['s', 'sim']:
            usuarios = carregar_usuarios()
            for i in range(len(usuarios)):
                if usuarios[i].get('id') == usuario_id:
                    usuarios[i]['ativo'] = False
                    break

            if salvar_usuarios(usuarios):
                print(f"✅ Usuário '{usuario['nome']}' excluído com sucesso!")
                return True
            else:
                print(f"❌ Erro ao excluir usuário '{usuario['nome']}'!")
                return False
        else:
            print(f"❌ Operação cancelada para usuário '{usuario['nome']}'.")
            return False

    except OperacaoCancelada:
        print("\n❌ Operação cancelada pelo usuário.")
        return False


def menu_usuarios():
    while True:
        print("\n" + "="*60)
        print("MÓDULO DE USUÁRIOS")
        print("="*60)
        print("1. Cadastrar Usuário")
        print("2. Listar Usuários")
        print("3. Atualizar Usuário")
        print("4. Excluir Usuário")
        print("5. Voltar ao Menu Principal")
        print("0. Sair do Sistema")
        print("-"*60)

        opcao = input("Escolha uma opção: ").strip()

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
            print("\n👋 Obrigado por usar o Cadeia ESG Conectada!")
            sys.exit(0)
        else:
            print("❌ Opção inválida! Tente novamente.")
            input("\nPressione Enter para continuar...")
