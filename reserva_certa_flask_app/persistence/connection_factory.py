# connection_factory.py
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / 'reserva_certa.db'

def get_connection():
    conn = sqlite3.connect(str(DB_PATH), detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON;')
    return conn
