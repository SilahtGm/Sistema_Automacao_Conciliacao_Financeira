import os


def paths():
    # ---- VARIÁAVEIS DE CAMINHO ----
    # ARMAZENANDO O CAMINHO DO DIRETÓRIO ATUAL DESTE ARQUIVO
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # OS.PATH.JOIN JUNTA CAMINHOS EM UMA STRING
    # ARMAZENANDO O CAMINHO JUNTO COM O DATABASE.DB: "C:/Users/Thalis/Projeto/db/database.db"
    db_path = os.path.join(BASE_DIR, "database.db")
    # ARMAZENANDO O CAMINHO JUNTO COM O SCHEMA.SQL
    schema_path = os.path.join(BASE_DIR, "schema.sql")
    return db_path, schema_path