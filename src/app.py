from empresas import menu_empresas
from usuarios import menu_usuarios
from certificados import menu_certificados
from auth import menu_auth
from chatbot import iniciar_chat
from utils import entrada_segura, log_info, log_validacao, limpa_terminal


def menu_principal():
    """Menu principal do sistema."""
    limpa_terminal()

    while True:
        try:
            log_info("\n" + "=" * 60)
            log_info(f"CADEIA ESG CONECTADA")
            log_info("=" * 60)
            log_info("1. Gerenciar Empresas")
            log_info("2. Gerenciar Usuários")
            log_info("3. Gerenciar Certificados")
            log_info("4. Autenticação")
            log_info("5. ChatBot de Ajuda")
            log_info("0. Sair do Sistema")
            log_info("-" * 60)

            opcao = entrada_segura("Escolha uma opção: ").strip()
            limpa_terminal()

            if opcao == "1":
                menu_empresas()
            elif opcao == "2":
                menu_usuarios()
            elif opcao == "3":
                menu_certificados()
            elif opcao == "4":
                novo_usuario = menu_auth(exibir_opcoes_navegacao=True)
                if novo_usuario:
                    usuario = novo_usuario
            elif opcao == "5":
                iniciar_chat()
            elif opcao == "0":
                log_info("\n👋 Obrigado por usar o Cadeia ESG Conectada!")
                break
            else:
                log_validacao("Opção inválida! Tente novamente.")
                input("\nPressione Enter para continuar...")
        except KeyboardInterrupt:
            log_info("\nOperação cancelada. Voltando ao menu principal...")
            return


if __name__ == "__main__":
    usuario_logado = menu_auth()

    if usuario_logado:
        menu_principal()
    else:
        log_info("\n👋 Obrigado por usar o Cadeia ESG Conectada!")
