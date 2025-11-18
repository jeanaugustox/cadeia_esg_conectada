import sys
from usuarios import carregar_usuarios, salvar_usuarios, cadastrar_usuario


def esqueci_senha():
    print("\n" + "="*60)
    print("RECUPERAÇÃO DE SENHA")
    print("="*60)

    nome = input("Nome de usuário: ").strip()
    email = input("Email cadastrado: ").lower().strip()

    usuarios = carregar_usuarios()
    usuario_encontrado = None

    for usuario in usuarios:
        nome_ok = usuario.get('nome') == nome
        email_ok = usuario.get('email', '').lower() == email

        if nome_ok and email_ok:
            usuario_encontrado = usuario
            break

    if not usuario_encontrado:
        print("❌ Usuário ou email inválidos.")
        return False

    while True:
        nova_senha = input("Nova senha (mín. 6 caracteres): ").strip()
        if len(nova_senha) < 6:
            print("❌ Senha muito curta. Tente novamente.")
            continue
        break

    # Atualiza a senha no array e salva
    for i in range(len(usuarios)):
        if usuarios[i].get('id') == usuario_encontrado.get('id'):
            usuarios[i]['senha'] = nova_senha
            break

    if salvar_usuarios(usuarios):
        print("✅ Senha atualizada com sucesso! Faça login com a nova senha.")
        return True
    else:
        print("❌ Erro ao atualizar senha!")
        return False


def login():
    while True:
        print("\n" + "="*60)
        print("TELA DE LOGIN")
        print("="*60)

        nome = input("Nome de usuário: ").strip()
        senha = input("Senha: ").strip()

        usuarios = carregar_usuarios()
        usuario_valido = None

        for usuario in usuarios:
            if (
                usuario.get('nome') == nome
                and usuario.get('senha') == senha
            ):
                usuario_valido = usuario
                break

        if usuario_valido:
            print(f"\n✅ Bem-vindo(a), {usuario_valido.get('nome')}!")
            return True

        print("❌ Credenciais inválidas ou usuário inativo.")
        print("-"*60)
        print("1. Tentar novamente")
        print("2. Esqueci a senha")
        print("0. Sair do Sistema")
        print("-"*60)

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            continue
        elif opcao == "2":
            esqueci_senha()
            # Após recuperação, volta para tentar login novamente
            continue
        elif opcao == "0":
            print("\n👋 Obrigado por usar o Cadeia ESG Conectada!")
            sys.exit(0)
        else:
            print("❌ Opção inválida! Tente novamente.")
            input("\nPressione Enter para continuar...")


def menu_auth(exibir_opcoes_navegacao: bool = False):
    while True:
        print("\n" + "="*60)
        print("MÓDULO DE AUTENTICAÇÃO")
        print("="*60)
        print("1. Fazer Login")
        print("2. Cadastrar Usuário")
        print("3. Esqueci a Senha")
        if exibir_opcoes_navegacao:
            print("6. Voltar ao Menu Principal")
            print("0. Sair do Sistema")
        print("-"*60)

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            if login():
                return True
        elif opcao == "2":
            cadastrar_usuario()
        elif opcao == "3":
            esqueci_senha()
        elif exibir_opcoes_navegacao and opcao == "6":
            return False
        elif exibir_opcoes_navegacao and opcao == "0":
            print("\n👋 Obrigado por usar o Cadeia ESG Conectada!")
            sys.exit(0)
        else:
            print("❌ Opção inválida! Tente novamente.")
            input("\nPressione Enter para continuar...")
