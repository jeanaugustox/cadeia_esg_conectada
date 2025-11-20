# utils.py
import json
import os
from datetime import datetime


def entrada_segura(mensagem: str):
    """
    Solicita entrada e permite cancelar a operação a qualquer momento.
    """
    resposta = input(mensagem).strip()
    if resposta.lower() in ["cancelar", "sair", "exit", "stop"]:
        raise KeyboardInterrupt("Operação cancelada pelo usuário.")
    return resposta


def log_sucesso(mensagem: str):
    """Exibe mensagem de sucesso padronizada."""
    print(f"✅ {mensagem}")


def log_erro(mensagem: str):
    """Exibe mensagem de erro padronizada."""
    print(f"❌ {mensagem}")


def log_info(mensagem: str):
    """Exibe mensagem informativa."""
    print(mensagem)


def log_validacao(mensagem: str):
    """Exibe mensagem de validação/aviso."""
    print(f"❌ {mensagem}")


def carregar_arquivo_json(caminho: str) -> list:
    """
    Carrega dados de um arquivo JSON.
    Retorna lista vazia se arquivo não existir ou houver erro.
    """
    try:
        if not os.path.exists(caminho):
            return []
        with open(caminho, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except Exception as e:
        log_erro(f"Erro ao carregar arquivo {caminho}: {e}")
        return []


def salvar_arquivo_json(caminho: str, dados: list) -> bool:
    """
    Salva dados em um arquivo JSON.
    Retorna True se sucesso, False caso contrário.
    """
    try:
        # Garante que o diretório existe
        diretorio = os.path.dirname(caminho)
        if diretorio and not os.path.exists(diretorio):
            os.makedirs(diretorio, exist_ok=True)

        with open(caminho, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        log_erro(f"Erro ao salvar arquivo {caminho}: {e}")
        return False


def gerar_id(lista: list) -> int:
    """
    Gera próximo ID baseado no tamanho da lista.
    """
    return len(lista) + 1


def formatar_data() -> str:
    """
    Retorna data formatada padronizada.
    """
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")
