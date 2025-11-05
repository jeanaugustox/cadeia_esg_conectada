from empresas import menu_empresas
from usuarios import menu_usuarios
from auth import login, menu_auth
from chatbot import iniciar_chat  # ← Importa o chatbot

def menu_principal():
    while True:
        print("\n" + "="*60)
        print("CADEIA ESG CONECTADA")
        print("="*60)
        print("1. Gerenciar Empresas")
        print("2. Gerenciar Usuários")
        print("3. Gerenciar Certificados")
        print("4. Autenticação")
        print("5. ChatBot de Ajuda")  # ← Nova opção
        print("0. Sair do Sistema")
        print("-"*60)

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            menu_empresas()
        elif opcao == "2":
            menu_usuarios()
        elif opcao == "3":
            print("Módulo de Certificados")
            input("Pressione Enter para continuar...")
        elif opcao == "4":
            menu_auth(exibir_opcoes_navegacao=True)
        elif opcao == "5":
            iniciar_chat()  # ← Chama o chat bot
        elif opcao == "0":
            print("\n👋 Obrigado por usar o Cadeia ESG Conectada!")
            break
        else:
            print("❌ Opção inválida! Tente novamente.")
            input("Pressione Enter para continuar...")


if __name__ == "__main__":
    if menu_auth():
        menu_principal()
