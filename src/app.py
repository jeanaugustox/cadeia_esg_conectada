from empresas import menu_empresas
from usuarios import menu_usuarios 
from auth import login, menu_auth 
from certificados import menu_certificados

def menu_principal(usuario):
    
    papel = usuario.get("papel", "Leitor")

    while True:
        print("\n" + "=" * 60)
        print(f"🌐 CADEIA ESG CONECTADA | Usuário: {usuario['nome']} ({papel})")
        print("=" * 60)
        print("1. Gerenciar Empresas")
        
        if papel == "Admin":
            print("2. Gerenciar Usuários")
            
        print("3. Gerenciar Certificados")
        print("4. Autenticação")
        print("0. Sair do Sistema")
        print("-" * 60)

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            menu_empresas()
            input("\nPressione Enter para voltar ao menu principal...")
            
        elif opcao == "2":
            if papel == "Admin":
                menu_usuarios() 
                input("\nPressione Enter para voltar ao menu principal...")
            else:
                print("❌ Acesso negado. Você não tem permissão.")
                input("\nPressione Enter para continuar...")
                
        elif opcao == "3":
            menu_certificados() 
            
        elif opcao == "4":
            novo_usuario = menu_auth(exibir_opcoes_navegacao=True)
            if novo_usuario:
                usuario = novo_usuario
                papel = usuario.get("papel", "Leitor")
            input("\nPressione Enter para voltar ao menu principal...")
            
        elif opcao == "0":
            print("\n👋 Obrigado por usar o Cadeia ESG Conectada!")
            break
        else:
            print("❌ Opção inválida! Tente novamente.")
            input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    usuario_logado = menu_auth()
    
    if usuario_logado:
        menu_principal(usuario_logado)