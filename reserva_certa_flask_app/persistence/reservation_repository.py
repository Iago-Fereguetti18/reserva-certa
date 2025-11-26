from typing import Optional, List
from .connection_factory import get_connection

class ReservationRepository:
    def create(self, id: str, user_id: str, space_id: str, start: str, end: str, status: str, notes: str, created_at: str):
        with get_connection() as conn:
            conn.execute('INSERT INTO reservations (id,user_id,space_id,start,end,status,notes,created_at) VALUES (?,?,?,?,?,?,?,?)',
                         (id,user_id,space_id,start,end,status,notes,created_at))
    def get(self, id: str) -> Optional[dict]:
        with get_connection() as conn:
            cur = conn.execute('SELECT * FROM reservations WHERE id=?', (id,))
            row = cur.fetchone()
            return dict(row) if row else None
    def list_all(self) -> List[dict]:
        with get_connection() as conn:
            cur = conn.execute('SELECT * FROM reservations')
            return [dict(r) for r in cur.fetchall()]
    def list_by_space(self, space_id: str) -> List[dict]:
        with get_connection() as conn:
            cur = conn.execute('SELECT * FROM reservations WHERE space_id=?', (space_id,))
            return [dict(r) for r in cur.fetchall()]
    def list_by_user(self, user_id: str) -> List[dict]:
        with get_connection() as conn:
            cur = conn.execute('SELECT * FROM reservations WHERE user_id=?', (user_id,))
            return [dict(r) for r in cur.fetchall()]
    def update(self, id: str, **fields):
        keys = ','.join(f"{k}=?" for k in fields.keys())
        vals = list(fields.values()) + [id]
        with get_connection() as conn:
            conn.execute(f'UPDATE reservations SET {keys} WHERE id=?', vals)
    def delete(self, id: str):
        with get_connection() as conn:
            conn.execute('DELETE FROM reservations WHERE id=?', (id,))
