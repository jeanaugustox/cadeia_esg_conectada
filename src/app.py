from empresas import menu_empresas
from usuarios import menu_usuarios 
from auth import login, menu_auth 
from certificados import menu_certificados

def menu_principal():
    while True:
        print("\n" + "=" * 60)
        print("🌐 CADEIA ESG CONECTADA")
        print("=" * 60)
        print("1. Gerenciar Empresas")
        print("2. Gerenciar Usuários")
        print("3. Gerenciar Certificados")
        print("4. Autenticação")
        print("0. Sair do Sistema")
        print("-" * 60)

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            menu_empresas()
            input("\nPressione Enter para voltar ao menu principal...")
        elif opcao == "2":
            menu_usuarios() 
            input("\nPressione Enter para voltar ao menu principal...")
        elif opcao == "3":
            menu_certificados() 
        elif opcao == "4":
            menu_auth(exibir_opcoes_navegacao=True)
            input("\nPressione Enter para voltar ao menu principal...")
        elif opcao == "0":
            print("\n👋 Obrigado por usar o Cadeia ESG Conectada!")
            break
        else:
            print("❌ Opção inválida! Tente novamente.")
            input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    menu_auth()
    menu_principal()