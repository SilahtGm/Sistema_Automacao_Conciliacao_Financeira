import sqlite3
from db.connection import get_connection
import pandas as pd

class ConciliacaoRepository:

    def listar_todas(self):
        try:
            conn, cursor = get_connection()
            data = pd.read_sql_query("SELECT * FROM conciliacao", conn)
            conn.close()
            return data
        except sqlite3.Error as e:
            print(f"Erro no Banco de Dados (SQLite): {e}")
        except pd.errors.ParserError as e:
            print(f"CSV formato fora do esperado: {e}")
        except Exception as e:
            print(f"Erro inesperado: {e}")


    def listar_divergencias(self):
        try:
            conn, cursor = get_connection()
            data = pd.read_sql_query("SELECT * FROM conciliacao WHERE status = 'DIVERGENCIA'", conn)
            conn.close()
            return data
        except sqlite3.Error as e:
            print(f"Erro no Banco de Dados (SQLite): {e}")
        except pd.errors.ParserError as e:
            print(f"CSV formato fora do esperado: {e}")
        except Exception as e:
            print(f"Erro inesperado: {e}")

    def listar_conformidadades(self):
        try:
            conn, cursor = get_connection()
            data = pd.read_sql_query("SELECT * FROM conciliacao WHERE status = 'EM CONFORMIDADE'", conn)
            conn.close()
            return data
        except sqlite3.Error as e:
            print(f"Erro no Banco de Dados (SQLite): {e}")
        except pd.errors.ParserError as e:
            print(f"CSV formato fora do esperado: {e}")
        except Exception as e:
            print(f"Erro inesperado: {e}")

    def listar_conciliacao_por_data(self, data_conciliacao):
        try:
            conn, cursor = get_connection()
            data = pd.read_sql_query("SELECT * FROM conciliacao WHERE data_conciliacao = ? ", conn, params=(data_conciliacao,))
            conn.close()
            return data
        except sqlite3.Error as e:
            print(f"Erro no Banco de Dados (SQLite): {e}")
        except pd.errors.ParserError as e:
            print(f"CSV formato fora do esperado: {e}")
        except Exception as e:
            print(f"Erro inesperado: {e}")

    def listar_conciliacao_pos_data(self, data_conciliacao):
        try:
            conn, cursor = get_connection()
            data = pd.read_sql_query("SELECT * FROM conciliacao WHERE data_conciliacao > ?", conn, params=(data_conciliacao,))
            conn.close()
            return data
        except sqlite3.Error as e:
            print(f"Erro no Banco de Dados (SQLite): {e}")
        except pd.errors.ParserError as e:
            print(f"CSV formato fora do esperado: {e}")
        except Exception as e:
            print(f"Erro inesperado: {e}")

    def buscar_por_id(self, id_conciliacao):
        try:
            conn, cursor = get_connection()
            data = pd.read_sql_query("SELECT * FROM conciliacao WHERE id_conciliacao = ?",conn, params=(id_conciliacao,))
            conn.close()
            return data
        except sqlite3.Error as e:
            print(f"Erro no Banco de Dados (SQLite): {e}")
        except pd.errors.ParserError as e:
            print(f"CSV formato fora do esperado: {e}")
        except Exception as e:
            print(f"Erro inesperado: {e}")


    