from typing import Any, List, Optional

from DB.database import get_connection, return_connection
from psycopg2.extras import RealDictCursor
from models.user import User
import logging

STARTING_BALANCE = 200

class UserDAO:
    def create_table(self) -> None:
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(f"""
                CREATE TABLE IF NOT EXISTS users (
                    user_id BIGINT PRIMARY KEY,
                    balance BIGINT DEFAULT {STARTING_BALANCE},
                    bank BIGINT DEFAULT 0,
                    xp BIGINT DEFAULT 0,
                    level INT DEFAULT 1,
                    last_daily TIMESTAMPTZ,
                    last_work TIMESTAMPTZ,
                    last_crime TIMESTAMPTZ
                );
            """)
            cur.execute(f"ALTER TABLE users ALTER COLUMN balance SET DEFAULT {STARTING_BALANCE}")
            conn.commit()
            cur.close()
        except Exception as e:
            logging.error(f"Error creando tabla users: {e}")
            conn.rollback()
        finally:
            return_connection(conn)

    def create(self, user_id: int) -> Optional[User]:
        conn = get_connection()
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute(
                """
                INSERT INTO users (user_id, balance)
                VALUES (%s, %s)
                ON CONFLICT (user_id) DO NOTHING
                RETURNING *;
                """,
                (user_id, STARTING_BALANCE)
            )
            record = cur.fetchone()
            conn.commit()
            cur.close()
            if record is None:
                return self.find_by_id(user_id)
            return User.from_record(record)
        except Exception as e:
            logging.error(f"Error creando usuario {user_id}: {e}")
            conn.rollback()
            return None
        finally:
            return_connection(conn)

    def find_or_create(self, user_id: int) -> Optional[User]:
        conn = get_connection()
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            # Usamos INSERT ... ON CONFLICT para hacer todo en una sola consulta
            cur.execute("""
                INSERT INTO users (user_id) 
                VALUES (%s) 
                ON CONFLICT (user_id) DO UPDATE SET user_id = EXCLUDED.user_id 
                RETURNING *;
            """, (user_id,))
            record = cur.fetchone()
            conn.commit()
            cur.close()
            return User.from_record(record) if record else None
        except Exception as e:
            logging.error(f"Error en find_or_create user {user_id}: {e}")
            return None
        finally:
            return_connection(conn)

    def find_by_id(self, user_id: int) -> Optional[User]:
        conn = get_connection()
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
            record = cur.fetchone()
            cur.close()
            return User.from_record(record) if record else None
        except Exception as e:
            logging.error(f"Error buscando usuario {user_id}: {e}")
            return None
        finally:
            return_connection(conn)

    def update(self, user_id: int, **kwargs: Any) -> None:
        conn = get_connection()
        try:
            cur = conn.cursor()
            set_clause = ", ".join([f"{k} = %s" for k in kwargs.keys()])
            values = list(kwargs.values()) + [user_id]
            
            cur.execute(f"UPDATE users SET {set_clause} WHERE user_id = %s", values)
            conn.commit()
            cur.close()
        except Exception as e:
            logging.error(f"Error actualizando usuario {user_id}: {e}")
            conn.rollback()
        finally:
            return_connection(conn)

    def get_leaderboard(self, limit: int = 10) -> List[User]:
        conn = get_connection()
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute("SELECT user_id, balance FROM users ORDER BY balance DESC LIMIT %s", (limit,))
            rows = cur.fetchall()
            cur.close()
            return [User.from_record(row) for row in rows]
        except Exception as e:
            logging.error(f"Error obteniendo leaderboard: {e}")
            return []
        finally:
            return_connection(conn)