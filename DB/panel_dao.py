from typing import Optional

from DB.database import get_connection, return_connection
from psycopg2.extras import RealDictCursor
from models.panel import Panel
import logging


class PanelDAO:
    def create_table(self) -> None:
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS panel_status (
                    id INT PRIMARY KEY DEFAULT 1,
                    guild_id BIGINT,
                    channel_id BIGINT,
                    message_id BIGINT,
                    CONSTRAINT one_row_only CHECK (id = 1)
                );
            """)
            conn.commit()
            cur.close()
        except Exception as e:
            logging.error(f"Error creando tabla panel_status: {e}")
        finally:
            return_connection(conn)

    def save_panel(self, guild_id: int, channel_id: int, message_id: int) -> None:
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO panel_status (id, guild_id, channel_id, message_id)
                VALUES (1, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE 
                SET guild_id = EXCLUDED.guild_id, 
                    channel_id = EXCLUDED.channel_id, 
                    message_id = EXCLUDED.message_id;
            """, (guild_id, channel_id, message_id))
            conn.commit()
            cur.close()
        except Exception as e:
            logging.error(f"Error guardando panel: {e}")
        finally:
            return_connection(conn)

    def get_panel(self) -> Optional[Panel]:
        conn = get_connection()
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute("SELECT * FROM panel_status WHERE id = 1")
            record = cur.fetchone()
            cur.close()
            return Panel.from_record(record)
        finally:
            return_connection(conn)

    def clear_panel(self) -> None:
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM panel_status WHERE id = 1")
            conn.commit()
        finally:
            return_connection(conn)