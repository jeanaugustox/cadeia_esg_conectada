from datetime import datetime
from empresas import carregar_empresas, salvar_empresas
from collections import Counter 

def registrar_novo_certificado():
    
    print("\n--- Registrar Novo Certificado ---")
    
    try:
        empresa_id = int(
            input("Digite o ID da empresa que receberá o certificado: ").strip())
    except ValueError:
        print("❌ ID inválido!")
        return

    empresas = carregar_empresas()
    empresa_encontrada = None
    indice_empresa = -1 

    for i in range(len(empresas)):
        if empresas[i].get('id') == empresa_id:
            empresa_encontrada = empresas[i]
            indice_empresa = i
            break

    if not empresa_encontrada:
        print("❌ Empresa não encontrada com este ID.")
        return

    if not empresa_encontrada.get('ativo', True):
        print(f"❌ Empresa '{empresa_encontrada.get('nome_empresa')}' está inativa e não pode receber certificados.")
        return

    print(f"Adicionando certificado para a empresa: {empresa_encontrada.get('nome_empresa')}")
    
    certificado = input("Digite o nome do seu certificado ESG: ").strip().title()
    categoria = input("Digite a categoria do seu certificado: ").strip().title()
    emitido = input("Digite onde foi emitido (Fonte oficial): ").strip()
    validade = input("Digite a data de validade (ex: DD/MM/AAAA): ").strip()
    emissao = input("Digite a data de emissão (ex: DD/MM/AAAA): ").strip()

    if "certificados" not in empresa_encontrada:
        empresa_encontrada["certificados"] = []

    novo_registro = {
        "certificado_id": len(empresa_encontrada.get("certificados", [])) + 1,
        "nome_certificado": certificado,
        "categoria": categoria,
        "emitido_por": emitido,
        "data_validade": validade,
        "data_emissao": emissao,
    }

    empresas[indice_empresa]["certificados"].append(novo_registro)

    if salvar_empresas(empresas):
        print("✅ Certificado registrado e salvo com sucesso!")
    else:
        print("❌ Erro ao salvar o certificado.")


def ranking_empresas():
    
    print("\n" + "=" * 10 + " Ranking Total de Certificados " + "=" * 10)

    empresas = carregar_empresas()

    if not empresas:
        print("Nenhuma empresa registrada para o ranking.")
        return

    lista_nomes_empresas = []
    for empresa in empresas:
        if not empresa.get('ativo', True):
            continue
            
        nome_empresa = empresa.get("nome_empresa", "Empresa Desconhecida")
        
        for cert in empresa.get("certificados", []):
              lista_nomes_empresas.append(nome_empresa)

    if not lista_nomes_empresas:
        print("Nenhum certificado registrado no sistema.")
        return

    ranking = Counter(lista_nomes_empresas)
    
    print(f"{'Pos.':<5} | {'Empresa':<30} | {'Qtd. Certificados':<20}")
    print("-" * 57)
    for i, (empresa, contagem) in enumerate(ranking.most_common(), 1):
        print(f"{i:<5} | {empresa:<30} | {contagem:<20}")


def validar_certificados_automaticamente():
    print("\n" + "=" * 60)
    print("🔍 VALIDAÇÃO AUTOMÁTICA DE CERTIFICADOS (Vencimento)")
    print("=" * 60)

    empresas = carregar_empresas()
    hoje = datetime.now()
    encontrou_algum = False

    if not empresas:
        print("Nenhuma empresa para validar.")
        return

    print(f"{'Empresa':<20} | {'Certificado':<20} | {'Validade':<12} | {'STATUS':<10}")
    print("-" * 70)

    for empresa in empresas:
        if not empresa.get('ativo', True):
            continue

        certificados = empresa.get('certificados', [])
        if not certificados:
            continue

        for cert in certificados:
            encontrou_algum = True
            data_str = cert.get('data_validade')
            nome_cert = cert.get('nome_certificado')
            nome_emp = empresa.get('nome_empresa')

            try:
                data_validade = datetime.strptime(data_str, "%d/%m/%Y")
                
                if data_validade >= hoje:
                    status = "✅ VÁLIDO"
                else:
                    status = "❌ VENCIDO"
            except ValueError:
                status = "⚠️ DATA INVÁLIDA"

            print(f"{nome_emp[:20]:<20} | {nome_cert[:20]:<20} | {data_str:<12} | {status:<10}")

    if not encontrou_algum:
        print("\nNenhum certificado encontrado para validar.")
    else:
        print("-" * 70)
        print(f"Data da verificação automática: {hoje.strftime('%d/%m/%Y')}")


def menu_certificados():
    
    while True:
        print("\n" + "=" * 60)
        print("📋 Módulo de Certificados")
        print("=" * 60)
        print("1. Registrar Novo Certificado")
        print("2. Ver Ranking de Empresas (Total de Certificados)")
        print("3. Validar Certificados (Automático)") 
        print("4. Voltar ao Menu Principal")
        print("-" * 60)

        escolha = input("Escolha uma opção (1-4): ").strip()

        if escolha == "1":
            registrar_novo_certificado()
            input("\nPressione Enter para continuar...")
        elif escolha == "2":
            ranking_empresas()
            input("\nPressione Enter para continuar...")
        elif escolha == "3":
            validar_certificados_automaticamente()
            input("\nPressione Enter para continuar...")
        elif escolha == "4":
            print("Retornando ao menu principal...")
            break
        else:
            print("❌ Opção inválida. Por favor, escolha de 1 a 4.")
            input("\nPressione Enter para continuar...")