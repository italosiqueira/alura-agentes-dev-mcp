from pathlib import Path
import sqlite3
from api.banco import bd


BASE_DIR = Path(__file__).resolve().parent
SCHEMA_PATH = Path(f"{BASE_DIR}/schema.sql")
DATA_PATH = Path(f"{BASE_DIR}/data.sql")


def le_script(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Arquivo SQL não encontrado: {path}")
    return path.read_text(encoding="utf-8")


def executa_script(conn: sqlite3.Connection, script: str) -> None:
    conn.executescript(script)
    conn.commit()


def inicializa_base(recria: bool = False) -> None:
    """
    Cria e popula o banco de dados.

    Args:
        recria: se True, apaga o banco atual e recria do zero.
    """
    if recria and bd.DB_PATH.exists():
        bd.DB_PATH.unlink()

    conn = bd.cria_conexao()
    try:
        schema_sql = le_script(SCHEMA_PATH)
        data_sql = le_script(DATA_PATH)

        executa_script(conn, schema_sql)
        executa_script(conn, data_sql)

        print(f"Banco inicializado com sucesso em: {bd.DB_PATH}")
    finally:
        conn.close()


if __name__ == "__main__":
    inicializa_base(recria=True)