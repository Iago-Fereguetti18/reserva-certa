# Demo script to initialize DB, run SQL scripts, and exercise repositories
import sqlite3, os
from pathlib import Path
from persistence.connection_factory import get_connection
from persistence.user_repository import UserRepository
from persistence.space_repository import SpaceRepository
from persistence.reservation_repository import ReservationRepository

BASE = Path(__file__).resolve().parents[1]
DB = BASE / 'reserva_certa.db'
SQL_DIR = BASE / 'sql'

def init_db():
    if DB.exists():
        DB.unlink()
    conn = sqlite3.connect(DB)
    with open(SQL_DIR / 'create_tables.sql', 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    with open(SQL_DIR / 'insert_data.sql', 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.close()

def main():
    init_db()
    urepo = UserRepository()
    srepo = SpaceRepository()
    rrepo = ReservationRepository()

    print('Users:', urepo.list_all())
    print('Spaces:', srepo.list_all())
    print('Reservations:', rrepo.list_all())

    # CRUD example: add, update, delete
    urepo.create('u3','Joao','joao@example.com',0,'2025-09-11T14:00:00Z')
    print('After add u3:', urepo.get('u3'))
    urepo.update('u3', name='João Silva', email='joao.silva@example.com')
    print('After update u3:', urepo.get('u3'))
    urepo.delete('u3')
    print('After delete u3:', urepo.get('u3'))

if __name__ == '__main__':
    main()
