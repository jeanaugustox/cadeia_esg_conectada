from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils import entrada_segura, log_info


class ChatBotIA:
    def __init__(self):
        # Frases que o modelo IA vai aprender a reconhecer
        self.frases = [
            "como faço login",
            "não consigo entrar no sistema",
            "problema no login",
            "como cadastrar empresa",
            "onde cadastro uma empresa",
            "como registrar uma empresa",
            "como cadastrar usuário",
            "onde adiciono usuário",
            "como criar novo usuário",
            "como gerar certificado",
            "para que serve certificado",
            "como resolver erro",
            "sistema dando erro",
            "como navegar no sistema",
            "me ajude",
            "preciso de ajuda",
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
        mensagem_vec = self.vectorizer.transform([mensagem])
        similaridades = cosine_similarity(mensagem_vec, self.vetores).flatten()

        indice = similaridades.argmax()
        grau = similaridades[indice]

        if grau < 0.20:
            return "Não entendi muito bem. Pode reformular sua pergunta?"

        return self.respostas[indice]

    def ajuda(self):
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


def iniciar_chat():
    bot = ChatBotIA()

    log_info("\n🤖 ChatBot IA - Cadeia ESG Conectada")
    log_info(bot.ajuda())
    log_info("-" * 60)

    while True:
        try:
            msg = entrada_segura("Você: ").lower()

            if msg == "sair":
                log_info("ChatBot: Até logo! 👋")
                break
            elif msg == "voltar":
                log_info("ChatBot: Voltando ao menu principal...")
                return
            elif msg == "ajuda":
                log_info("ChatBot: " + bot.ajuda())
            else:
                log_info("ChatBot: " + bot.responder(msg))
        except KeyboardInterrupt:
            log_info("\nChatBot: Voltando ao menu principal...")
            return


if __name__ == "__main__":
    iniciar_chat()
