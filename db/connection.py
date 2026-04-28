import sqlite3

# FUNÇÃO DE CONECTIVIDADE COM O BANCO DE DADOS
def get_connection ():
    try:
        # ESTABECENDO CONEXAO E CURSOR
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # RETORNANDO UMA TUPLA
        return conn, cursor
    except sqlite3.Error as e:
        print(f"Erro no Banco de Dados (SQLite): {e}")