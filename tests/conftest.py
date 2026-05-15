import os
import sqlite3
import pytest

# DB_PATH must be set before the app module is imported — SQLite resolves the
# path at module load time via os.getenv, so late assignment is silently ignored.
TEST_DB = "test.db"
os.environ["DB_PATH"] = TEST_DB

from fastapi.testclient import TestClient
from main import app, get_gateway, GatewayPagamento


def _seed(db_path: str) -> None:
    conn = sqlite3.connect(db_path)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS produtos "
        "(nome TEXT PRIMARY KEY, preco REAL, estoque INTEGER)"
    )
    conn.execute("INSERT OR REPLACE INTO produtos VALUES ('teclado', 200.0, 10)")
    # mouse com estoque zero: caminho de erro de "sem estoque"
    conn.execute("INSERT OR REPLACE INTO produtos VALUES ('mouse', 100.0, 0)")
    conn.commit()
    conn.close()


@pytest.fixture(scope="function")
def db():
    _seed(TEST_DB)
    yield TEST_DB
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)


@pytest.fixture(scope="function")
def client(db):
    with TestClient(app) as c:
        yield c
