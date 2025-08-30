import sqlite3
import os
from datetime import datetime

DB_FILE = "casino.db"
STARTING_BALANCE = 200

def connect_db():
    """Crea una conexión a la base de datos y la retorna."""
    conn = sqlite3.connect(DB_FILE)
    # Esto permite acceder a las columnas por nombre, como si fuera un diccionario
    conn.row_factory = sqlite3.Row 
    return conn

def setup_database():
    """Crea la tabla de usuarios si no existe."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            balance INTEGER NOT NULL,
            last_daily TEXT
        )
    """)
    conn.commit()
    conn.close()

def get_user(user_id):
    """
    Obtiene los datos de un usuario. Si no existe, lo crea con valores por defecto.
    Devuelve un objeto sqlite3.Row que se puede usar como un diccionario.
    """
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user_data = cursor.fetchone()

    if user_data is None:
        # El usuario no existe, lo creamos
        cursor.execute(
            "INSERT INTO users (user_id, balance, last_daily) VALUES (?, ?, ?)",
            (user_id, STARTING_BALANCE, None)
        )
        conn.commit()
        # Volvemos a buscarlo para retornar los datos recién creados
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        user_data = cursor.fetchone()
    
    conn.close()
    return user_data

def update_user(user_id, balance=None, last_daily=None):
    """
    Actualiza los datos de un usuario.
    """
    conn = connect_db()
    cursor = conn.cursor()

    updates = []
    params = []
    
    if balance is not None:
        updates.append("balance = ?")
        params.append(balance)
    
    if last_daily is not None:
        updates.append("last_daily = ?")
        params.append(last_daily)

    if not updates:
        conn.close()
        return # No hay nada que actualizar

    query = f"UPDATE users SET {', '.join(updates)} WHERE user_id = ?"
    params.append(user_id)
    
    cursor.execute(query, tuple(params))
    conn.commit()
    conn.close()

def get_leaderboard(limit=10):
    """Obtiene los usuarios con los saldos más altos."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT user_id, balance FROM users ORDER BY balance DESC LIMIT ?",
        (limit,)
    )
    leaderboard_data = cursor.fetchall()
    conn.close()
    return leaderboard_data

# Llamamos a setup_database() cuando el módulo se importa por primera vez
# para asegurarnos de que la tabla existe.
setup_database()