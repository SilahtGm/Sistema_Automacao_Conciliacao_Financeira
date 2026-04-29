import sqlite3
import pandas as pd
from db.connection import get_connection

def carregar_arquivo_csv ():

    # CRIANDO VARIAVEIS
    csv_nf = "NotasFiscais.csv"
    csv_lc = "LancamentosContabeis.csv"
    try:
        nf = pd.read_csv(csv_nf, encoding= "utf-8", sep=";")
        lc = pd.read_csv(csv_lc, encoding="utf-8", sep=";")
        return nf,lc
    except FileNotFoundError as e:
        print(f"Erro: Arquivo de script não encontrado! Esperado: {csv_nf} e {csv_lc} .Detalhes: {e}")


# FUNÇÃO RESPONSÁVEL PELO PROCESSAMENTO DO CSV PRO BANCO DE DADOS
def gerar_dados ():
    try:
        # ESTABELECENDO CONEXAO COM O BANCO DE DADOS
        conn, cursor = get_connection()

        # CARREGANDO ARQUIVO E ARMAZENANDO
        nf, lc = carregar_arquivo_csv()

        # COLUNAS NECESSÁRIAS PARA INSERT NO BANCO DE DADOS
        required_nf_columns = [
            "id_nf",
            "chave_acesso",
            "fornecedor",
            "cnpj_fornecedor",
            "descricao",
            "nf_valor",
            "data_emissao",
            "data_vencimento",
            "categoria"
        ]
        # Validação Nota Fiscal
        for column in required_nf_columns:
            if column not in nf.columns:
                raise ValueError(f"Coluna obrigatória ausente: {column}")

        # COLUNAS NECESSÁRIAS PARA INSERT NO BANCO DE DADOS
        required_lc_columns = [
            "id_lc",
            "id_nf",
            "fornecedor",
            "cnpj_fornecedor",
            "descricao",
            "lc_valor",
            "data_lancamento",
            "conta_debito",
            "conta_credito"
        ]
        # Validação Lançamento Contábil
        for column in required_lc_columns:
            if column not in lc.columns:
                raise ValueError(f"Coluna obrigatória ausente: {column}")

        # FUNÇÃO PANDAS QUE ENCAMINHA OS DADOS DO CSV DIRETAMENTE PRO SQL (INSERT)
        nf.to_sql("nota_fiscal", conn, if_exists="append", index=False, chunksize=1000)
        lc.to_sql("lancamento_contabel", conn, if_exists="append", index=False, chunksize=1000)

        # REALIZANDO COMMIT DAS OPERAÇÕES
        conn.commit()
        conn.close()

    except sqlite3.Error as e:
        print(f"Erro no Banco de Dados (SQLite): {e}")
    except FileNotFoundError as e:
        print(f"Arquivo não encontrado: {e}")
    except pd.errors.ParserError as e:
        print(f"CSV formato fora do esperado: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")