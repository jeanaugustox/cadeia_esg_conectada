from empresas import menu_empresas
from usuarios import menu_usuarios
from auth import menu_auth
from chatbot import iniciar_chat
from utils import entrada_segura, log_info, log_validacao


def menu_principal():
    while True:
        try:
            log_info("\n" + "=" * 60)
            log_info("CADEIA ESG CONECTADA")
            log_info("=" * 60)
            log_info("1. Gerenciar Empresas")
            log_info("2. Gerenciar Usuários")
            log_info("3. Gerenciar Certificados")
            log_info("4. Autenticação")
            log_info("5. ChatBot de Ajuda")
            log_info("0. Sair do Sistema")
            log_info("-" * 60)

            opcao = entrada_segura("Escolha uma opção: ")

            if opcao == "1":
                menu_empresas()
            elif opcao == "2":
                menu_usuarios()
            elif opcao == "3":
                log_info("Módulo de Certificados")
                input("Pressione Enter para continuar...")
            elif opcao == "4":
                menu_auth(exibir_opcoes_navegacao=True)
            elif opcao == "5":
                iniciar_chat()
            elif opcao == "0":
                log_info("\n👋 Obrigado por usar o Cadeia ESG Conectada!")
                break
            else:
                log_validacao("Opção inválida! Tente novamente.")
                input("Pressione Enter para continuar...")
        except KeyboardInterrupt:
            log_info("\nOperação cancelada. Voltando ao menu principal...")


if __name__ == "__main__":
    menu_auth()
    menu_principal()
