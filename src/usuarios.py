# Arquivo para CRUD de usuários 
import json
import os

ARQ_USUARIOS = "data/usuarios.json"

def carregar_usuarios():
    if not os.path.exists(ARQ_USUARIOS):
        return []
    with open(ARQ_USUARIOS, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_usuarios(usuarios):
    with open(ARQ_USUARIOS, "w", encoding="utf-8") as f:
        json.dump(usuarios, f, indent=4, ensure_ascii=False)

# CREATE
def cadastrar_usuario():
    usuarios = carregar_usuarios()
    nome = input("Nome de usuário: ").strip()
    if any(u["nome"] == nome for u in usuarios):
        print(" Usuário já existe.")
        return
    senha = input("Senha: ").strip()
    papel = input("Papel (Admin / Editor / Leitor): ").title().strip()
    if papel not in ["Admin", "Editor", "Leitor"]:
        print(" Papel inválido.")
        return
    usuarios.append({"id": len(usuarios)+1, "nome": nome, "senha": senha, "papel": papel})
    salvar_usuarios(usuarios)
    print(f" Usuário '{nome}' cadastrado com sucesso como {papel}.")

# READ
def listar_usuarios():
    usuarios = carregar_usuarios()
    if not usuarios:
        print("Nenhum usuário cadastrado.")
        return
    print("\n=== Usuários Cadastrados ===")
    for u in usuarios:
        print(f"[{u['id']}] {u['nome']} ({u['papel']})")

# UPDATE
def editar_usuario():
    usuarios = carregar_usuarios()
    listar_usuarios()
    try:
        uid = int(input("ID do usuário que deseja editar: "))
    except ValueError:
        print("ID inválido.")
        return
    usuario = next((u for u in usuarios if u["id"] == uid), None)
    if not usuario:
        print("Usuário não encontrado.")
        return

    print("Deixe em branco para manter o valor atual.")
    novo_nome = input(f"Novo nome ({usuario['nome']}): ").strip() or usuario["nome"]
    nova_senha = input("Nova senha: ").strip() or usuario["senha"]
    novo_papel = input(f"Novo papel ({usuario['papel']}): ").title().strip() or usuario["papel"]

    usuario["nome"] = novo_nome
    usuario["senha"] = nova_senha
    usuario["papel"] = novo_papel

    salvar_usuarios(usuarios)
    print(f"Usuário '{usuario['nome']}' atualizado com sucesso.")

# DELETE
def excluir_usuario():
    usuarios = carregar_usuarios()
    listar_usuarios()
    try:
        uid = int(input("ID do usuário a excluir: "))
    except ValueError:
        print("ID inválido.")
        return
    usuarios = [u for u in usuarios if u["id"] != uid]
    salvar_usuarios(usuarios)
    print(" Usuário removido com sucesso.")
