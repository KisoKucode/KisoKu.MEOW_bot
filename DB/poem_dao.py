from typing import Optional

from DB.database import get_connection, return_connection
import logging


class PoemDAO:
    def create_table(self) -> None:
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS poems (
                    id SERIAL PRIMARY KEY,
                    content TEXT NOT NULL,
                    author_id BIGINT
                );
            """)
            conn.commit()
            cur.close()
        except Exception as e:
            logging.error(f"Error creando tabla poems: {e}")
        finally:
            return_connection(conn)

    def add_poem(self, content: str, author_id: int) -> None:
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO poems (content, author_id) VALUES (%s, %s)", (content, author_id))
            conn.commit()
            cur.close()
        except Exception as e:
            logging.error(f"Error añadiendo poema: {e}")
        finally:
            return_connection(conn)

    def get_random_poem(self) -> Optional[str]:
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT content FROM poems ORDER BY RANDOM() LIMIT 1")
            row = cur.fetchone()
            cur.close()
            if row:
                return row[0]
            return None
        except Exception as e:
            logging.error(f"Error obteniendo poema: {e}")
            return None
        finally:
            return_connection(conn)