import sqlite3

from db.paths import paths


# FUNÇÃO DE CONECTIVIDADE COM O BANCO DE DADOS
def get_connection ():
    try:
        # OBTENDO PATHS
        db_path, schema_path = paths()

        # ESTABECENDO CONEXAO E CURSOR
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # RETORNANDO UMA TUPLA
        return conn, cursor
    except sqlite3.Error as e:
        print(f"Erro no Banco de Dados (SQLite): {e}")