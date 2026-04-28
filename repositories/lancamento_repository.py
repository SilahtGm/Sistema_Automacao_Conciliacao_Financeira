from db.connection import get_connection
import sqlite3
import pandas as pd

class LancamentoContabilRepository:

    def listar_todas(self):
        try:
            conn, cursor = get_connection()
            data = pd.read_sql_query("SELECT * FROM lancamento_contabil", conn)
            conn.close()
            return data
        except sqlite3.Error as e:
            print(f"Erro no Banco de Dados (SQLite): {e}")
        except pd.errors.ParserError as e:
            print(f"CSV formato fora do esperado: {e}")
        except Exception as e:
            print(f"Erro inesperado: {e}")

    def buscar_por_id(self, id_nf):
        try:
            conn, cursor = get_connection()
            data = pd.read_sql_query("SELECT * FROM lancamento_contabil WHERE id_lc = ?",conn, params=(id_nf,))
            conn.close()
            return data
        except sqlite3.Error as e:
            print(f"Erro no Banco de Dados (SQLite): {e}")
        except pd.errors.ParserError as e:
            print(f"CSV formato fora do esperado: {e}")
        except Exception as e:
            print(f"Erro inesperado: {e}")