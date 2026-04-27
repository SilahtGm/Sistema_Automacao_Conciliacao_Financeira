import os
import pandas as pd
import sqlite3

def conexao_banco ():
    try:
        conexao = sqlite3.connect('database.db')
        cursor = conexao.cursor()

        return conexao, cursor
    except sqlite3.Error as e:
        print(f"Erro no Banco de Dados (SQLite): {e}")

def inicializar_banco():
    try:
        # Guardando na variavel a checagem de se o banco de dados ja existe
        banco_existe = os.path.exists('database.db')

        # Estabelecendo a conexão com o banco
        conexao, cursor = conexao_banco()

        # 1. Tenta abrir e rodar o Schema, guardado no arquivo schema.sql
        with open('schema.sql', 'r', encoding='utf-8') as f:
            cursor.executescript(f.read())

        # 2. Tenta abrir e rodar os Inserts apenas se o banco for novo, caso
        # contrario, apenas exibira que estará estabelecendo a conexão
        if not banco_existe:
            with open('inserts.sql', 'r', encoding='utf-8') as g:
                cursor.executescript(g.read())
            print(">>> Sucesso: Banco criado e populado pela primeira vez.")
        else:
            print(">>> Conectado: Banco de dados já existente.")

        # Salvando e fechando a conexão
        conexao.commit()
        conexao.close()
        # Excepts trazendo possiveis mensagens de erro
    except FileNotFoundError as e:
        print(f"Erro: Arquivo de script não encontrado! Detalhes: {e}")
    except sqlite3.Error as e:
        print(f"Erro no Banco de Dados (SQLite): {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")





def carregar_arquivo_csv ():

    # CRIANDO VARIAVEIS
    csv_nf = "NotasFiscais.csv"
    csv_lc = "LancamentosContabeis.csv"
    try:
        dfnf = pd.read_csv(csv_nf, encoding= "utf-8", sep=";")
        dflc = pd.read_csv(csv_lc, encoding="utf-8", sep=";")
        return dfnf,dflc
    except FileNotFoundError as e:
        print(f"Erro: Arquivo de script não encontrado! Esperado: {csv_nf} e {csv_lc} .Detalhes: {e}")



def menu_principal ():
    while True:
        print("===========================================================")
        print(" SACF - Sistema de Automação de Conciliação Financeira ")
        print("===========================================================")
        print(" Escolha uma das opções:")
        print("1 - INICIAR")
        print("2 - SAIR")
        opcao = input("Digite a opção desejada: ")
        match opcao:

            case "1":
                menu_secundario()

            case "2":
                break

            case _:
                print("Opção inválida!")


def menu_secundario ():
    while True:
        print("\n===========================================================")
        print("              RELATÓRIOS E CONSULTAS - SACF")
        print("===========================================================")
        print("1 - MOSTRAR TODAS AS DIVERGÊNCIAS")
        print("2 - MOSTRAR REGISTROS EM CONFORMIDADE")
        print("3 - PESQUISAR CONCILIAÇÕES POR DATA ESPECÍFICA")
        print("4 - PESQUISAR CONCILIAÇÕES A PARTIR DE UMA DATA")
        print("5 - EXIBIR NOTA FISCAL ESPECÍFICA")
        print("6 - EXIBIR LANÇAMENTO CONTÁBIL ESPECÍFICO")
        print("7 - EXIBIR CONCILIAÇÃO ESPECÍFICA")
        print("8 - LISTAR TODAS AS NOTAS FISCAIS")
        print("9 - LISTAR TODOS OS LANÇAMENTOS")
        print("10 - LISTAR TODAS AS CONCILIAÇÕES")
        print("0 - VOLTAR AO MENU PRINCIPAL")
        print("===========================================================")

        opcao = input("Digite a opção desejada: ")
        match opcao:

            case "1":
                mostrar_divergencias()

            case "2":
                mostrar_conformidade()

            case "3":
                data = input("Digite a data (YYYY-MM-DD): ")
                pesquisar_por_data(data)

            case "4":
                data = input("Digite a data inicial (YYYY-MM-DD): ")
                pesquisar_a_partir_data(data)

            case "5":
                id_nf = input("Digite o ID da Nota Fiscal: ")
                exibir_nota(id_nf)

            case "6":
                id_lc = input("Digite o ID do Lançamento: ")
                exibir_lancamento(id_lc)

            case "7":
                id_conc = input("Digite o ID da Conciliação: ")
                exibir_conciliacao(id_conc)

            case "8":
                listar_notas()

            case "9":
                listar_lancamentos()

            case "10":
                listar_conciliacoes()

            case "0":
                break

            case _:
                print("Opção inválida!")



# FUNÇÃO RESPONSÁVEL PELO PROCESSAMENTO DO CSV PRO BANCO DE DADOS
def gerar_dados ():
    try:
        # ESTABELECENDO CONEXAO COM O BANCO DE DADOS
        conexao, cursor = conexao_banco()

        # CARREGANDO ARQUIVO E ARMAZENANDO
        dfnf, dflc = carregar_arquivo_csv()

        # FUNÇÃO PANDAS QUE ENCAMINHA OS DADOS DO CSV DIRETAMENTE PRO SQL (INSERT)
        dfnf.to_sql("nome_tabela", conexao, if_exists="append", index=False, chunksize=1000)
        dflc.to_sql("nome_tabela", conexao, if_exists="append", index=False, chunksize=1000)

        # REALIZANDO COMMIT DAS OPERAÇÕES
        conexao.commit()

        conexao.close()

    except sqlite3.Error as e:
        print(f"Erro no Banco de Dados (SQLite): {e}")
    except FileNotFoundError as e:
        print(f"Arquivo não encontrado: {e}")
    except pd.errors.ParserError as e:
        print(f"CSV formato fora do esperado: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")


def mostrar_divergencias ():
    # ESTABELECENDO CONEXÃO COM O BANCO DE DADOS
    conexao, cursor = conexao_banco()

    # CRIAÇÃO DA QUERY DO SELECT
    query = "SELECT * FROM conciliacao WHERE status = 'DIVERGENCIA' "

    # FAZENDO O SELECT E ARMAZENANDO NA VARIAVEL DADOS
    dados = pd.read_sql_query(query, conexao)

    if dados.empty:
        print("\nNenhuma divergência encontrada.\n")
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
    conexao.close()





def mostrar_conformidade():
                # ESTABELECENDO CONEXÃO COM O BANCO DE DADOS
                conexao, cursor = conexao_banco()

                # CRIAÇÃO DA QUERY DO SELECT
                query = "SELECT * FROM conciliacao WHERE status = 'EM CONFORMIDADE' "

                # FAZENDO O SELECT E ARMAZENANDO NA VARIAVEL DADOS
                dados = pd.read_sql_query(query, conexao)

                if dados.empty:
                    print("\nNenhuma divergência encontrada.\n")
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

                conexao.close()



def pesquisar_por_data (data):
    # ESTABELECENDO CONEXÃO COM O BANCO DE DADOS
    conexao, cursor = conexao_banco()

    # CRIAÇÃO DA QUERY DO SELECT
    query = "SELECT * FROM conciliacao WHERE data_conciliacao = ? "

    # FAZENDO O SELECT E ARMAZENANDO NA VARIAVEL DADOS
    dados = pd.read_sql_query(query, conexao, params=(data,))

    if dados.empty:
        print("\nNenhuma divergência encontrada.\n")
    else:
        print("\n===== DIVERGÊNCIAS ENCONTRADAS =====\n")

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

            def mostrar_conformidade():
                # ESTABELECENDO CONEXÃO COM O BANCO DE DADOS
                conexao, cursor = conexao_banco()

                # CRIAÇÃO DA QUERY DO SELECT
                query = "SELECT * FROM conciliacao WHERE status = 'EM CONFORMIDADE' "

                # FAZENDO O SELECT E ARMAZENANDO NA VARIAVEL DADOS
                dados = pd.read_sql_query(query, conexao)

                if dados.empty:
                    print("\nNenhuma divergência encontrada.\n")
                else:
                    print("\n===== DIVERGÊNCIAS ENCONTRADAS =====\n")

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
    conexao.close()