import os
from db.connection_db import get_connection
import sqlite3

from db.paths_db import paths


# FUNÇÃO DE CRIAÇÃO/INICIALIZAÇÃO DO BANCO DE DADOS
def inicializar_banco():
    try:
        # OBTENDO PATHS
        db_path, schema_path = paths()

        # SE O BANCO JÁ EXISTIR, FINALIZA A FUNÇÃO
        if os.path.exists(db_path):
            return
        else:
            # ESTABELECENDO CONEXÃO COM O BANCO
            conn, cursor = get_connection()

            # ABRE E RODA O SCHEMA.SQL
            with open(schema_path, 'r', encoding='utf-8') as f:
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