from empresas import menu_empresas


def menu_principal():
    while True:
        print("\n" + "="*60)
        print("CADEIA ESG CONECTADA")
        print("="*60)
        print("1. Gerenciar Empresas")
        print("2. Gerenciar Usuários")
        print("3. Gerenciar Certificados")
        print("4. Autenticação")
        print("0. Sair do Sistema")
        print("-"*60)

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            menu_empresas()
        elif opcao == "2":
            print("Módulo de Usuários")
            input("Pressione Enter para continuar...")
        elif opcao == "3":
            print("Módulo de Certificados")
            input("Pressione Enter para continuar...")
        elif opcao == "4":
            print("Módulo de Autenticação")
            input("Pressione Enter para continuar...")
        elif opcao == "0":
            print("\n👋 Obrigado por usar o Cadeia ESG Conectada!")
            break
        else:
            print("❌ Opção inválida! Tente novamente.")

        input("\nPressione Enter para continuar...")


if __name__ == "__main__":
    menu_principal()
