import os
import sqlite3
import pandas as pd
from db.connection_db import get_connection

def carregar_arquivo_csv():

    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        # VOLTA UMA PASTA (sai de services)
        ROOT_DIR = os.path.dirname(BASE_DIR)

        caminho_nf = os.path.join(ROOT_DIR, "data", "NotasFiscais.csv")
        caminho_lc = os.path.join(ROOT_DIR, "data", "LancamentosContabeis.csv")

        nf = pd.read_csv(caminho_nf, encoding="utf-8", sep=",")
        lc = pd.read_csv(caminho_lc, encoding="utf-8", sep=",")

        return nf, lc

    except FileNotFoundError as e:
        print(f"Erro: Arquivo não encontrado. Detalhes: {e}")
        return None, None


# FUNÇÃO RESPONSÁVEL PELO PROCESSAMENTO DO CSV PRO BANCO DE DADOS
def gerar_dados ():
    try:
        # ESTABELECENDO CONEXAO COM O BANCO DE DADOS
        conn, cursor = get_connection()

        # CARREGANDO ARQUIVO E ARMAZENANDO
        nf, lc = carregar_arquivo_csv()
        if nf is None or lc is None:
            return

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


        # TRANSFORMANDO EM UMA LISTA
        nf_data = list(nf.itertuples(index=False, name=None))

        cursor.executemany("""
            INSERT INTO nota_fiscal (
                id_nf,
                chave_acesso,
                fornecedor,
                cnpj_fornecedor,
                descricao,
                nf_valor,
                data_emissao,
                data_vencimento,
                categoria
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, nf_data)

        lc_data = list(lc.itertuples(index=False, name=None))

        cursor.executemany("""
            INSERT INTO lancamento_contabil (
                id_lc,
                id_nf,
                fornecedor,
                cnpj_fornecedor,
                descricao,
                lc_valor,
                data_lancamento,
                conta_debito,
                conta_credito
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, lc_data)


        # SALVANDO E FECHANDO a CONEXÃO COM O BANCO
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