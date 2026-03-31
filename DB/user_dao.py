from DB.database import get_connection, return_connection
from psycopg2.extras import RealDictCursor
import logging

class UserDAO:
    def create_table(self):
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id BIGINT PRIMARY KEY,
                    balance BIGINT DEFAULT 0,
                    bank BIGINT DEFAULT 0,
                    xp BIGINT DEFAULT 0,
                    level INT DEFAULT 1,
                    last_daily TIMESTAMPTZ,
                    last_work TIMESTAMPTZ,
                    last_crime TIMESTAMPTZ
                );
            """)
            conn.commit()
            cur.close()
        except Exception as e:
            logging.error(f"Error creando tabla users: {e}")
            conn.rollback()
        finally:
            return_connection(conn)

    def find_or_create(self, user_id):
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
            user = cur.fetchone()
            conn.commit()
            cur.close()
            return user
        except Exception as e:
            logging.error(f"Error en find_or_create user {user_id}: {e}")
            return None
        finally:
            return_connection(conn)

    def update(self, user_id, **kwargs):
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

    def get_leaderboard(self, limit=10):
        conn = get_connection()
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute("SELECT user_id, balance FROM users ORDER BY balance DESC LIMIT %s", (limit,))
            rows = cur.fetchall()
            cur.close()
            return rows
        except Exception as e:
            logging.error(f"Error obteniendo leaderboard: {e}")
            return []
        finally:
            return_connection(conn)