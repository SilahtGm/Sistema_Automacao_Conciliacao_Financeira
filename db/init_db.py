import os
from db.connection import get_connection
import sqlite3

# FUNÇÃO DE CRIAÇÃO/INICIALIZAÇÃO DO BANCO DE DADOS
def inicializar_banco():
    try:

        # VERIFICANDO SE O BANCO JÁ EXISTE
        bd = os.path.exists("./db/database.db")

        if bd:
            return

        # ESTABELECENDO CONEXÃO COM O BANCO
        conn, cursor = get_connection()

        # ABRE E RODA O SCHEMA.SQL
        with open('./db/schema.sql', 'r', encoding='utf-8') as f:
            cursor.executescript(f.read())

        # REALIZANDO COMMITS E FECHANDO A CONEXÃO
        conn.commit()
        conn.close()

    except FileNotFoundError as e:
        print(f"Erro: Arquivo de script não encontrado! Detalhes: {e}")
    except sqlite3.Error as e:
        print(f"Erro no Banco de Dados (SQLite): {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")