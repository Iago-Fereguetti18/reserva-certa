from typing import Optional, List
from .connection_factory import get_connection

class UserRepository:
    """Repository/DAO for users table. Implements basic CRUD."""
    def create(self, id: str, name: str, email: str, is_admin: bool=False, created_at: str=None):
        with get_connection() as conn:
            conn.execute('INSERT INTO users (id,name,email,is_admin,created_at) VALUES (?,?,?,?,?)',
                         (id, name, email, int(is_admin), created_at))
    def get(self, id: str) -> Optional[dict]:
        with get_connection() as conn:
            cur = conn.execute('SELECT * FROM users WHERE id=?', (id,))
            row = cur.fetchone()
            return dict(row) if row else None
    def list_all(self) -> List[dict]:
        with get_connection() as conn:
            cur = conn.execute('SELECT * FROM users')
            return [dict(r) for r in cur.fetchall()]
    def update(self, id: str, **fields):
        keys = ','.join(f"{k}=?" for k in fields.keys())
        vals = list(fields.values()) + [id]
        with get_connection() as conn:
            conn.execute(f'UPDATE users SET {keys} WHERE id=?', vals)
    def delete(self, id: str):
        with get_connection() as conn:
            conn.execute('DELETE FROM users WHERE id=?', (id,))
