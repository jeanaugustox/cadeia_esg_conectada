import json
import os
import sys
from datetime import datetime

ARQUIVO_USUARIOS = "data/usuarios.json"

# ================ CARREGAR USUÁRIOS ================ #

def carregar_usuarios():
    try:
        if not os.path.exists(ARQUIVO_USUARIOS):
            return []
        with open(ARQUIVO_USUARIOS, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except Exception as e:
        print(f"Erro ao carregar usuários: {e}")
        return []

# ================ SALVAR USUÁRIOS ================ #

def salvar_usuarios(usuarios):
    try:
        with open(ARQUIVO_USUARIOS, "w", encoding="utf-8") as arquivo:
            json.dump(usuarios, arquivo, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Erro ao salvar usuários: {e}")
        return False

# ================ CADASTRAR USUÁRIOS ================ # 

def cadastrar_usuario():
    print("\n" + "=" * 60)
    print("CADASTRO DE USUÁRIO")
    print("=" * 60)

    usuarios = carregar_usuarios()

    # Nome
    while True:
        nome = input("Nome de usuário: ").strip()
        if not nome:
            print("Digite um nome de usuário para prosseguir.")
            continue
        if any(u.get("nome") == nome for u in usuarios):
            print("❌ Usuário já existe!")
            return False
        break

    # Email
    while True:
        email = input("Email: ").lower().strip()
        if not email:
            print("Digite o seu email para prosseguir.")
            continue
        break

    # Senha
    while True:
        senha = input("Senha: ").strip()
        if not senha:
            print("Digite uma senha para prosseguir.")
            continue
        if len(senha) < 6:
            print("Digite uma senha com 6 ou mais caracteres.")
            continue
        break
    
    # Papel
    papeis_validos = ["Admin", "Editor", "Leitor"]
    while True:
        papel = input("Papel (Admin / Editor / Leitor): ").title().strip()
        if not papel:
            print("Digite o papel para prosseguir. Papéis: Admin, Editor, Leitor.")
            continue
        if papel in papeis_validos:
            break
        print("❌ Opção inválida. Tente novamente. Papéis: Admin, Editor, Leitor.")

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

# ================ LISTAR USUÁRIOS ================ #

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

# ================ BUSCAR USUÁRIOS ================ #

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

# ================ ATUALIZAR USUÁRIOS ================ #

def atualizar_usuario():
    try:
        usuario_id = int(
            input("Digite o ID do usuário que deseja atualizar: ").strip())
    except ValueError:
        print("❌ ID inválido!")
        return

    usuario = buscar_usuario_por_id(usuario_id)
    if not usuario:
        print("❌ Usuário não encontrado!")
        return

    print("\n" + "=" * 60)
    print("ATUALIZAR USUÁRIO")
    print("=" * 60)
    print("Deixe em branco para manter o valor atual.")
    print(f"\nUsuário selecionado: {usuario['nome']} ({usuario['papel']})")
    print("-" * 60)

    nome_atual = usuario['nome']
    papel_atual = usuario['papel']
    senha_atual = usuario['senha']
    alguma_alteracao = False

    # Nome
    novo_nome = input("Novo nome: ").strip()
    if novo_nome:
        if novo_nome == nome_atual:
            print(f"Nome mantido como '{nome_atual}' (mesmo valor informado).")
        else:
            usuario['nome'] = novo_nome
            alguma_alteracao = True
            print(f"Nome atualizado de '{nome_atual}' para '{novo_nome}'.")
    else:
        print(f"Nome mantido como '{nome_atual}' (campo deixado em branco).")

    # Senha
    while True:
        nova_senha = input("Nova senha: ").strip()
        if not nova_senha:
            print("Senha mantida (campo deixado em branco).")
            break
        if nova_senha == senha_atual:
            print("Senha mantida (mesmo valor informado).")
            break
        if len(nova_senha) < 6:
            print("Digite uma senha com 6 ou mais caracteres.")
            continue
        usuario['senha'] = nova_senha
        alguma_alteracao = True
        print("Senha atualizada com sucesso.")
        break

    # Papel
    papeis_validos = ["Admin", "Editor", "Leitor"]
    while True:
        novo_papel = input("Escolha o papel (Admin, Editor, Leitor): ").title().strip()
        if not novo_papel:
            print(f"Papel mantido como '{papel_atual}' (campo deixado em branco).")
            break
        if novo_papel == papel_atual:
            print(f"Papel mantido como '{papel_atual}' (mesmo valor informado).")
            break
        if novo_papel in papeis_validos:
            usuario['papel'] = novo_papel
            alguma_alteracao = True
            print(f"Papel atualizado de '{papel_atual}' para '{novo_papel}'.")
            break
        else:
            print("❌ Opção inválida. Tente novamente. Papéis: Admin, Editor, Leitor.")

    if not alguma_alteracao:
        print("\nNenhuma alteração realizada. As informações atuais foram mantidas.")
        return

    usuarios = carregar_usuarios()
    for i in range(len(usuarios)):
        if usuarios[i].get('id') == usuario['id']:
            usuarios[i] = usuario
            break

    if salvar_usuarios(usuarios):
        print("✅ Usuário atualizado com sucesso!")
    else:
        print("❌ Erro ao salvar alterações!")

# ================ EXCLUIR USUÁRIOS ================ #
    
def excluir_usuario():
    try:
        usuario_id = int(
            input("Digite o ID do usuário que deseja excluir: ").strip())
    except ValueError:
        print("❌ ID inválido!")
        return False

    usuario = buscar_usuario_por_id(usuario_id)

    if not usuario:
        print("❌ Usuário não encontrado!")
        return False

    confirmacao = input(
        f"\n⚠️ Tem certeza que deseja excluir '{usuario['nome']}'? (s/n): ").strip().lower()

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

# ================ MENU DE USUÁRIOS ================ #

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
