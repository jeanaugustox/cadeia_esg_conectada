# utils.py
import json
import os
import re
import hashlib
import binascii
from datetime import datetime

import getpass


def entrada_segura(mensagem: str):
    """
    Solicita entrada e permite cancelar a operação a qualquer momento.
    """
    if "senha" in mensagem.lower():
        resposta = getpass.getpass(mensagem).strip()
    else:
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
    Gera próximo ID baseado no maior ID existente na lista.
    """
    if not lista:
        return 1

    # Busca o maior ID existente na lista
    ids_existentes = [
        item.get("id", 0) for item in lista if isinstance(item, dict) and "id" in item
    ]

    if not ids_existentes:
        return 1

    maior_id = max(ids_existentes)
    return maior_id + 1


def formatar_data() -> str:
    """
    Retorna data formatada padronizada.
    """
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


def validar_formato_data(data: str) -> bool:
    """
    Valida se a data está no formato DD/MM/AAAA.
    """
    # Regex para validar formato DD/MM/AAAA
    padrao = r"^\d{2}/\d{2}/\d{4}$"
    if not re.match(padrao, data):
        return False

    # Tenta converter a data para verificar se é válida
    try:
        datetime.strptime(data, "%d/%m/%Y")
        return True
    except ValueError:
        return False


def validar_senha(senha: str, tamanho_minimo: int = 6) -> tuple[bool, str]:
    """Valida se a senha atende aos requisitos mínimos."""
    if not senha:
        return False, "Senha é obrigatória!"

    if len(senha) < tamanho_minimo:
        return False, f"Senha deve ter pelo menos {tamanho_minimo} caracteres!"

    return True, ""


def validar_email(email: str) -> tuple[bool, str]:
    """Valida formato de email usando regex."""
    if not email:
        return False, "Email é obrigatório!"

    # Regex para validar formato de email
    padrao = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(padrao, email):
        return False, "Formato de email inválido!"

    return True, ""


def gerar_hash(password: str, iterations: int = 200_000) -> str:
    """
    Gera hash de senha usando PBKDF2-HMAC-SHA256 com salt aleatório.
    Formato: pbkdf2_sha256$<iterations>$<salt_hex>$<hash_hex>
    """
    if not isinstance(password, str):
        raise TypeError("password deve ser string")
    salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, iterations)
    return "pbkdf2_sha256${}${}${}".format(
        iterations, binascii.hexlify(
            salt).decode(), binascii.hexlify(dk).decode()
    )


def verifica_senha(password: str, stored: str) -> bool:
    """
    Verifica senha em texto contra hash armazenado (formato acima).
    """
    if not stored or not isinstance(stored, str) or not stored.startswith("pbkdf2_sha256$"):
        return False
    try:
        _, iter_str, salt_hex, hash_hex = stored.split("$", 3)
        iterations = int(iter_str)
        salt = binascii.unhexlify(salt_hex.encode())
        dk = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt, iterations)
        dk_hex = binascii.hexlify(dk).decode()
        # Comparação em string para evitar diferenças de tipo/encoding
        import hmac as _hmac

        return _hmac.compare_digest(dk_hex, hash_hex)
    except Exception:
        return False


def limpa_terminal():
    """Limpa o terminal (Windows e Unix)."""
    os.system("cls" if os.name == "nt" else "clear")
