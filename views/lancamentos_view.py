def view_exibir_lancamento (dados):
    if dados.empty:
        print("\nNenhum lançamento encontrada.\n")
        return
    else:
        print("\n===== LANÇAMENTOS ENCONTRADOS =====\n")

        for row in dados.itertuples(index=False):
            print("====================================")
            print(f"ID Lançamento: {row.id_lc}")
            print(f"Nota Fiscal vinculada: {row.id_nf}")
            print(f"Fornecedor: {row.fornecedor}")
            print(f"CNPJ: {row.cnpj_fornecedor}")
            print(f"Descrição: {row.descricao}")
            print(f"Valor do Lançamento: R$ {row.lc_valor:.2f}")
            print(f"Data do Lançamento: {row.data_lancamento}")
            print(f"Conta Débito: {row.conta_debito}")
            print(f"Conta Crédito: {row.conta_credito}")
            print("====================================\n")

def view_listar_lancamento (dados):
    contador = 0

    if dados.empty:
        print("\nNenhum lançamento contábil encontrado.\n")
        return
    else:
        print("\n===== LANÇAMENTOS CONTÁBEIS ENCONTRADOS =====\n")

    for row in dados.itertuples(index=False):

        print("====================================")
        print(f"ID Lançamento: {row.id_lc}")
        print(f"Nota Fiscal vinculada: {row.id_nf}")
        print(f"Fornecedor: {row.fornecedor}")
        print(f"CNPJ: {row.cnpj_fornecedor}")
        print(f"Descrição: {row.descricao}")
        print(f"Valor: R$ {row.lc_valor:.2f}")
        print(f"Data do Lançamento: {row.data_lancamento}")
        print(f"Conta Débito: {row.conta_debito}")
        print(f"Conta Crédito: {row.conta_credito}")
        print("====================================\n")

        contador += 1

        if contador == 10:
            print("Deseja visualizar mais 10 lançamentos? (Y/N)")
            op = input("Digite a opção desejada: ").upper()

            match op:
                case "Y":
                    contador = 0
                case "N":
                    return
                case _:
                    print("Opção Inválida!")

    print("Todos os lançamentos foram exibidos.")