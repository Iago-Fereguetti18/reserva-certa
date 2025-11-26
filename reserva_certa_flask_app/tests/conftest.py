import sqlite3
from pathlib import Path
import pytest

from persistence import connection_factory


@pytest.fixture(scope='session')
def test_db(tmp_path_factory):
    """Create a temporary sqlite DB initialized with project's SQL scripts and
    point persistence.connection_factory.DB_PATH to it.
    """
    # tests/ -> project root is parents[1]
    root = Path(__file__).resolve().parents[1]
    sql_dir = root / 'sql'
    db_path = tmp_path_factory.mktemp('data') / 'test_reserva.db'
    # Point the connection factory to the test DB path
    connection_factory.DB_PATH = db_path

    # initialize schema and seed data
    conn = sqlite3.connect(str(db_path))
    with open(sql_dir / 'create_tables.sql', 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    with open(sql_dir / 'insert_data.sql', 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()

    yield db_path


@pytest.fixture
def client(test_db):
    """Import the Flask app after the DB has been initialized and return a test client."""
    # import here so that repositories pick up the patched DB_PATH
    import importlib
    app_mod = importlib.import_module('app')
    app = app_mod.app
    app.testing = True
    with app.test_client() as c:
        yield c
