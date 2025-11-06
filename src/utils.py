# utils.py
def entrada_segura(mensagem: str):
    """
    Solicita entrada e permite cancelar a operação a qualquer momento.
    """
    resposta = input(mensagem)
    if resposta.lower() in ["cancelar", "sair", "exit", "stop"]:
        raise KeyboardInterrupt("Operação cancelada pelo usuário.")
    return resposta
