def view_exibir_por_id (dados):
    if dados.empty:
        print("\nNenhuma nota fiscal encontrada.\n")
        return
    else:
        print("\n===== NOTAS FISCAIS ENCONTRADAS =====\n")

        for row in dados.itertuples(index=False):
            print("====================================")
            print(f"Nota Fiscal: {row.id_nf}")
            print(f"Chave de Acesso: {row.chave_acesso}")
            print(f"Fornecedor: {row.fornecedor}")
            print(f"CNPJ: {row.cnpj_fornecedor}")
            print(f"Descrição: {row.descricao}")
            print(f"Valor NF: R$ {row.nf_valor:.2f}")
            print(f"Data de emissão: {row.data_emissao}")
            print(f"Data de vencimento: {row.data_vencimento}")
            print(f"Categoria: {row.categoria}")
            print("====================================\n")


def view_exibir_todos (dados):
    contador = 0

    if dados.empty:
        print("\nNenhuma nota fiscal encontrada.\n")
        return
    else:
        print("\n===== NOTAS FISCAIS ENCONTRADAS =====\n")

    for row in dados.itertuples(index=False):

        print("====================================")
        print(f"Nota Fiscal: {row.id_nf}")
        print(f"Chave de Acesso: {row.chave_acesso}")
        print(f"Fornecedor: {row.fornecedor}")
        print(f"CNPJ: {row.cnpj_fornecedor}")
        print(f"Descrição: {row.descricao}")
        print(f"Valor NF: R$ {row.nf_valor:.2f}")
        print(f"Data de emissão: {row.data_emissao}")
        print(f"Data de vencimento: {row.data_vencimento}")
        print(f"Categoria: {row.categoria}")
        print("====================================\n")
        contador += 1

        if contador == 10:
            print("Deseja vizualizar mais 10 notas fiscais? (Y/N)")
            op = input("Digite a opção desejada: ").upper()

            match op:
                case "Y":
                    contador = 0
                case "N":
                    return
                case _:
                    print("Opção Inválida!")
    print("Todas as notas fiscais foram exibidas.")