def view_divergencias (dados):
    if dados.empty:
        print("\nNenhuma divergência encontrada.\n")
        return
    else:
        print("\n===== DIVERGÊNCIAS ENCONTRADAS =====\n")

        # TRANSFORMANDOS OS DADOS OBTIDOS EM TUPLAS
        for row in dados.itertuples(index=False):
            print("====================================")
            print(f"Nota Fiscal: {row.id_nf}")
            print(f"Valor NF: R$ {row.valor_nota_fiscal:.2f}")
            print(f"Valor Lançamento: R$ {row.valor_lancamento:.2f}")
            print(f"Status: {row.status}")
            print(f"Descrição: {row.descricao}")
            print("====================================\n")

def view_conformidades (dados):
    if dados.empty:
        print("\nNenhuma conformidade encontrada.\n")
        return
    else:
        print("\n===== CONFORMIDADES ENCONTRADAS =====\n")

        # TRANSFORMANDOS OS DADOS OBTIDOS EM TUPLAS
        for row in dados.itertuples(index=False):
            print("====================================")
            print(f"Nota Fiscal: {row.id_nf}")
            print(f"Fornecedor: {row.fornecedor}")
            print(f"Valor NF: R$ {row.valor_nota_fiscal:.2f}")
            print(f"Valor Lançamento: R$ {row.valor_lancamento:.2f}")
            print(f"Status: {row.status}")
            print(f"Descrição: {row.descricao}")
            print("====================================\n")


def view_pesquisa_por_data (dados):
    if dados.empty:
        print("\nNenhuma conciliação encontrada.\n")
        return
    else:
        print("\n===== CONCILIAÇÕES ENCONTRADAS (POR DATA) =====\n")

        # TRANSFORMANDOS OS DADOS OBTIDOS EM TUPLAS
        for row in dados.itertuples(index=False):
            print("====================================")
            print(f"Nota Fiscal: {row.id_nf}")
            print(f"Data da conciliação: {row.data_conciliacao}")
            print(f"Valor NF: R$ {row.valor_nota_fiscal:.2f}")
            print(f"Valor Lançamento: R$ {row.valor_lancamento:.2f}")
            print(f"Status: {row.status}")
            print(f"Descrição: {row.descricao}")
            print("====================================\n")


def view_pesquisa_a_partir_data (dados):
    if dados.empty:
        print("\nNenhuma conciliação encontrada.\n")
        return
    else:
        print("\n===== CONCILIAÇÕES ENCONTRADAS (A PARTIR DE UMA DATA) =====\n")

        # TRANSFORMANDOS OS DADOS OBTIDOS EM TUPLAS
        for row in dados.itertuples(index=False):
            print("====================================")
            print(f"Nota Fiscal: {row.id_nf}")
            print(f"Data: {row.data_conciliacao}")
            print(f"Valor NF: R$ {row.valor_nota_fiscal:.2f}")
            print(f"Valor Lançamento: R$ {row.valor_lancamento:.2f}")
            print(f"Status: {row.status}")
            print(f"Descrição: {row.descricao}")
            print("====================================\n")

def view_conciliacao_por_id (dados):
    if dados.empty:
        print("\nNenhuma conciliação encontrada.\n")
        return
    else:
        print("\n===== CONCILIAÇÕES ENCONTRADAS =====\n")

        for row in dados.itertuples(index=False):
            print("====================================")
            print(f"ID Conciliação: {row.id_conciliacao}")
            print(f"Lançamento Contábil: {row.id_lc}")
            print(f"Nota Fiscal: {row.id_nf}")
            print(f"Data da Conciliação: {row.data_conciliacao}")
            print(f"Valor Nota Fiscal: R$ {row.valor_nota_fiscal:.2f}")
            print(f"Valor Lançamento: R$ {row.valor_lancamento:.2f}")
            print(f"Status: {row.status}")
            print(f"Descrição: {row.descricao}")
            print("====================================\n")


def view_listar_conciliacoes (dados):
    contador = 0

    if dados.empty:
        print("\nNenhuma conciliação encontrada.\n")
        return
    else:
        print("\n===== CONCILIAÇÕES ENCONTRADAS =====\n")

    for row in dados.itertuples(index=False):

        print("====================================")
        print(f"ID Conciliação: {row.id_conciliacao}")
        print(f"Lançamento Contábil: {row.id_lc}")
        print(f"Nota Fiscal: {row.id_nf}")
        print(f"Descrição: {row.descricao}")
        print(f"Valor Nota Fiscal: R$ {row.valor_nota_fiscal:.2f}")
        print(f"Valor Lançamento: R$ {row.valor_lancamento:.2f}")
        print(f"Status: {row.status}")
        print(f"Data da Conciliação: {row.data_conciliacao}")
        print("====================================\n")

        contador += 1

        if contador == 10:
            print("Deseja visualizar mais 10 conciliações? (Y/N)")
            op = input("Digite a opção desejada: ").upper()

            match op:
                case "Y":
                    contador = 0
                case "N":
                    return
                case _:
                    print("Opção Inválida!")

    print("Todas as conciliações foram exibidas.")