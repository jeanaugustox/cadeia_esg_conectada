from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import sys
from utils import entrada_segura, log_info, log_validacao, limpa_terminal


class ChatBotIA:
    """ChatBot simples baseado em TF-IDF para perguntas frequentes do sistema."""

    def __init__(self):
        # Frases que o modelo IA vai aprender a reconhecer
        self.frases = [
            "Como faço login?",
            "Não consigo entrar no sistema",
            "Problema no login",
            "Como cadastrar empresa?",
            "Onde cadastro uma empresa?",
            "Como registrar uma empresa?",
            "Como cadastrar usuário?",
            "Onde adiciono usuário?",
            "Como criar novo usuário?",
            "Como gerar certificado?",
            "Para que serve certificado?",
            "Como resolver erro?",
            "Sistema dando erro?",
            "Como navegar no sistema?",
            "Me ajude?",
            "Preciso de ajuda?",
        ]

        # Respostas alinhadas EXATAMENTE com as frases acima
        self.respostas = [
            "Para fazer login, vá até a tela inicial e insira usuário e senha.",
            "Verifique se seu usuário está ativo e a senha correta.",
            "Se houver problema no login, tente redefinir sua senha ou contate o administrador.",
            "No menu principal, acesse 'Gerenciar Empresas' para cadastrar.",
            "Use a opção 'Gerenciar Empresas' no menu principal.",
            "Você pode registrar uma empresa no módulo de Empresas.",
            "Usuários são cadastrados no menu 'Gerenciar Usuários'.",
            "Entre em 'Gerenciar Usuários' para adicionar novos usuários.",
            "Somente administradores podem criar novos usuários.",
            "Certificados são gerados no módulo 'Certificados'.",
            "Certificados servem para validar empresas dentro do sistema ESG.",
            "Verifique se preencheu tudo corretamente e tente novamente.",
            "Reinicie o sistema e confira as informações inseridas.",
            "Use o menu principal para acessar empresas, usuários e certificados.",
            "Claro! Como posso te ajudar exatamente?",
            "Estou aqui para ajudar. Pode explicar melhor sua dúvida?",
        ]

        self.vectorizer = TfidfVectorizer()
        self.vetores = self.vectorizer.fit_transform(self.frases)

    def responder(self, mensagem: str) -> str:
        """Retorna a melhor resposta com base em similaridade (TF-IDF + cosseno)."""
        mensagem_vec = self.vectorizer.transform([mensagem])
        similaridades = cosine_similarity(mensagem_vec, self.vetores).flatten()

        indice = similaridades.argmax()
        grau = similaridades[indice]

        if grau < 0.20:
            return "Não entendi muito bem. Pode reformular sua pergunta?"

        return self.respostas[indice]

    def ajuda(self):
        """Retorna texto com tópicos e comandos suportados pelo ChatBot."""
        return (
            "Eu posso te ajudar com:\n"
            "- Login e autenticação\n"
            "- Cadastro de empresas\n"
            "- Cadastro de usuários\n"
            "- Certificados\n"
            "- Erros comuns\n\n"
            "Comandos:\n"
            "- 'ajuda'\n"
            "- 'voltar'\n"
            "- 'sair'"
        )


def executar_conversa(bot: ChatBotIA):
    """Executa o modo de conversa com o ChatBot no terminal.

    Instruções:
    - Digite sua pergunta livremente
    - Use 'ajuda' para ver os tópicos e comandos
    - Digite 'voltar' ou pressione Ctrl+C para retornar ao menu do ChatBot
    """
    log_info("\n" + "=" * 60)
    log_info("CONVERSA COM O CHATBOT")
    log_info("=" * 60)
    log_info("Digite sua pergunta (ou 'voltar' para retornar).")
    log_info("-" * 60)

    while True:
        try:
            msg = entrada_segura("Você: ").strip().lower()

            if msg == "voltar":
                log_info("Voltando ao menu do ChatBot...")
                return
            elif msg == "ajuda":
                log_info(bot.ajuda())
                continue

            log_info("ChatBot: " + bot.responder(msg))
        except KeyboardInterrupt:
            log_info("\nOperação cancelada. Voltando ao menu do ChatBot...")
            return


def iniciar_chat():
    """Menu principal do módulo de ChatBot (formato padronizado do CLI)."""
    while True:
        try:
            log_info("\n" + "=" * 60)
            log_info("MÓDULO DE CHATBOT")
            log_info("=" * 60)
            log_info("1. Iniciar conversa")
            log_info("2. Ver comandos de ajuda")
            log_info("3. Voltar ao Menu Principal")
            log_info("0. Sair do Sistema")
            log_info("-" * 60)

            opcao = entrada_segura("Escolha uma opção: ").strip()
            limpa_terminal()

            if opcao == "1":
                bot = ChatBotIA()
                executar_conversa(bot)
            elif opcao == "2":
                bot = ChatBotIA()
                log_info(bot.ajuda())
            elif opcao == "3":
                return
            elif opcao == "0":
                log_info("\n👋 Obrigado por usar o Cadeia ESG Conectada!")
                sys.exit(0)
            else:
                log_validacao("Opção inválida! Tente novamente.")
                input("\nPressione Enter para continuar...")
        except KeyboardInterrupt:
            log_info("\nOperação cancelada. Voltando ao menu principal...")
            return


if __name__ == "__main__":
    iniciar_chat()
