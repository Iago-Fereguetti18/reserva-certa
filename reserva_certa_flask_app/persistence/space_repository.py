from typing import Optional, List
from .connection_factory import get_connection

class SpaceRepository:
    def create(self, id: str, name: str, capacity: int, equipments: str, price_per_hour: float, description: str=None):
        with get_connection() as conn:
            conn.execute('INSERT INTO spaces (id,name,capacity,equipments,price_per_hour,description) VALUES (?,?,?,?,?,?)',
                         (id, name, capacity, equipments, price_per_hour, description))
    def get(self, id: str) -> Optional[dict]:
        with get_connection() as conn:
            cur = conn.execute('SELECT * FROM spaces WHERE id=?', (id,))
            row = cur.fetchone()
            return dict(row) if row else None
    def list_all(self) -> List[dict]:
        with get_connection() as conn:
            cur = conn.execute('SELECT * FROM spaces')
            return [dict(r) for r in cur.fetchall()]
    def update(self, id: str, **fields):
        keys = ','.join(f"{k}=?" for k in fields.keys())
        vals = list(fields.values()) + [id]
        with get_connection() as conn:
            conn.execute(f'UPDATE spaces SET {keys} WHERE id=?', vals)
    def delete(self, id: str):
        with get_connection() as conn:
            conn.execute('DELETE FROM spaces WHERE id=?', (id,))
