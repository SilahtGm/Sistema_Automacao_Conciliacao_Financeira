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
        # CHECANDO SE O BANCO JÁ EXISTE
        banco_existe = os.path.exists('database.db')

        # ESTABELECENDO CONEXÃO COM O BANCO
        conexao, cursor = conexao_banco()

        # ABRE E RODA O SCHEMA.SQL
        with open('db/schema.sql', 'r', encoding='utf-8') as f:
            cursor.executescript(f.read())

        # REALIZANDO COMMITS E FECHANDO A CONEXÃO
        conexao.commit()
        conexao.close()
    except FileNotFoundError as e:
        print(f"Erro: Arquivo de script não encontrado! Detalhes: {e}")
    except sqlite3.Error as e:
        print(f"Erro no Banco de Dados (SQLite): {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")


def executar_consulta (query, params=None):
    try:
        # ESTABELECENDO CONEXÃO COM O BANCO DE DADOS
        conexao, cursor = conexao_banco()

        # GUARDANDO EM DADOS O RESULTADO DA QUERY
        # IF CASO TENHA PARÂMETROS, ELSE CASO NÃO TENHA
        if params is not None:
            dados = pd.read_sql_query(query, conexao, params=params)
        else:
            dados = pd.read_sql_query(query, conexao)

        # FECHANDO CONEXÃO COM O BANCO DE DADOS
        conexao.close()
        return dados
    except sqlite3.Error as e:
        print(f"Erro no Banco de Dados (SQLite): {e}")
    except pd.errors.ParserError as e:
        print(f"CSV formato fora do esperado: {e}")
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
        dfnf.to_sql("nota_fiscal", conexao, if_exists="append", index=False, chunksize=1000)
        dflc.to_sql("lancamento_contabel", conexao, if_exists="append", index=False, chunksize=1000)

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
    try:
        # CRIAÇÃO DA QUERY DO SELECT
        query = "SELECT * FROM conciliacao WHERE status = 'DIVERGENCIA' "

        # FAZENDO O SELECT E ARMAZENANDO NA VARIAVEL DADOS
        dados = executar_consulta(query)

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
    except Exception as e:
        print(f"Erro inesperado: {e}")


def mostrar_conformidade():
    try:
        # CRIAÇÃO DA QUERY DO SELECT
        query = "SELECT * FROM conciliacao WHERE status = 'EM CONFORMIDADE' "

        # FAZENDO O SELECT E ARMAZENANDO NA VARIAVEL DADOS
        dados = executar_consulta(query)

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
    except Exception as e:
        print(f"Erro inesperado: {e}")







def pesquisar_por_data (data):
    try:
        # CRIAÇÃO DA QUERY DO SELECT
        query = "SELECT * FROM conciliacao WHERE data_conciliacao = ? "

        # FAZENDO O SELECT E ARMAZENANDO NA VARIAVEL DADOS
        dados = executar_consulta(query, (data,))

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
    except Exception as e:
        print(f"Erro inesperado: {e}")













def pesquisar_a_partir_data (data):
    try:
        # ESTABELECENDO A QUERY DO SELECT
        query = "SELECT * FROM conciliacao WHERE data_conciliacao > ?"

        # FAZENDO O SELECT E ARMAZENANDO NA VARIAVEL DADOS
        dados = executar_consulta(query, (data,))

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
    except Exception as e:
        print(f"Erro inesperado: {e}")


def exibir_nota (id_nf):
    try:
        # CRIANDO QUERY DO SELECT
        query = "SELECT * FROM nota_fiscal WHERE id_nf = ?"

        # FAZENDO O SELECT E ARMAZENANDO NA VARIAVEL DADOS
        dados = executar_consulta(query, (id_nf,))

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
    except Exception as e:
        print(f"Erro inesperado: {e}")

def exibir_lancamento(id_lc):
    try:
        # CRIANDO QUERY DO SELECT
        query = "SELECT * FROM lancamento_contabel WHERE id_lc = ?"

        # FAZENDO O SELECT E ARMAZENANDO NA VARIAVEL DADOS
        dados = executar_consulta(query, (id_lc,))

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
    except Exception as e:
        print(f"Erro inesperado: {e}")

def exibir_conciliacao (id_conciliacao):
    try:
        # CRIANDO QUERY DO SELECT
        query = "SELECT * FROM conciliacao WHERE id_conciliacao = ?"

        # FAZENDO O SELECT E ARMAZENANDO NA VARIAVEL DADOS
        dados = executar_consulta(query, (id_conciliacao,))

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
    except Exception as e:
        print(f"Erro inesperado: {e}")

def listar_notas():
    try:
        # CRIANDO A QUERY SQL
        query = "SELECT * FROM nota_fiscal"

        # FAZENDO O SELECT E ARMAZENANDO NA VARIAVEL DADOS
        dados = executar_consulta(query)

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
                    case "Y": contador = 0
                    case "N": return
                    case _: print("Opção Inválida!")
        print("Todas as notas fiscais foram exibidas.")
    except Exception as e:
        print(f"Erro inesperado: {e}")


def listar_conciliacoes():
    try:
        # CRIANDO A QUERY SQL
        query = "SELECT * FROM conciliacao"

        # FAZENDO O SELECT E ARMAZENANDO NA VARIAVEL DADOS
        dados = executar_consulta(query)

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
    except Exception as e:
        print(f"Erro inesperado: {e}")


def listar_lancamentos():
    try:
        # CRIANDO A QUERY SQL
        query = "SELECT * FROM lancamento_contabel"

        # FAZENDO O SELECT E ARMAZENANDO NA VARIAVEL DADOS
        dados = executar_consulta(query)

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
    except Exception as e:
        print(f"Erro inesperado: {e}")

