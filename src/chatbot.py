class ChatBot:
    def __init__(self):
        self.respostas = {
            "login": "Para fazer login, vá até a tela inicial e insira seu usuário e senha. Se não tiver conta, peça a um administrador para criar.",
            "cadastro": "O cadastro de empresas e usuários pode ser feito pelos administradores no menu principal.",
            "certificado": "O módulo de certificado serve para gerar e gerenciar certificados das empresas cadastradas.",
            "empresa": "No menu de empresas, você pode cadastrar novas, editar ou consultar informações já registradas.",
            "usuário": "Usuários são gerenciados pelo administrador, que pode definir permissões e acesso.",
            "erro": "Se estiver enfrentando erros, tente reiniciar o sistema e verificar se o login está correto. Caso continue, contate o suporte."
        }

    def responder(self, mensagem: str) -> str:
        msg = mensagem.lower()
        for chave, resposta in self.respostas.items():
            if chave in msg:
                return resposta
        return "Desculpe, não entendi. Você pode reformular a pergunta ou digitar 'ajuda' para ver as opções."

    def ajuda(self):
        return (
            "Eu posso te ajudar com:\n"
            "- Login e autenticação\n"
            "- Cadastro de empresas\n"
            "- Usuários e permissões\n"
            "- Certificados\n"
            "- Problemas e erros comuns"
        )


def iniciar_chat():
    chatbot = ChatBot()
    print("\n🤖 ChatBot de Ajuda - Cadeia ESG Conectada")
    print("Digite 'sair' para encerrar o chat.\n")

    while True:
        msg = input("Você: ").strip().lower()
        if msg == "sair":
            print("ChatBot: Até logo! 👋")
            break
        elif msg == "ajuda":
            print("ChatBot:", chatbot.ajuda())
        else:
            print("ChatBot:", chatbot.responder(msg))


if __name__ == "__main__":
    iniciar_chat()
