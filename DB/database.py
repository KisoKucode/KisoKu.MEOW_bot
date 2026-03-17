import os
import psycopg2
from psycopg2 import pool
import logging

_pool = None

def init_connection_pool():
    """Inicializa el pool de conexiones a la base de datos."""
    global _pool
    try:
        _pool = psycopg2.pool.SimpleConnectionPool(
            1, 20,
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST', 'localhost'),
            port=os.getenv('DB_PORT', '5432'),
            database=os.getenv('DB_NAME')
        )
        logging.info("✅ Conexión a base de datos establecida.")
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(f"❌ Error al conectar a PostgreSQL: {error}")

def get_connection():
    """Obtiene una conexión del pool."""
    global _pool
    if _pool:
        return _pool.getconn()
    else:
        raise Exception("El pool de conexiones no está inicializado.")

def return_connection(conn):
    """Devuelve una conexión al pool."""
    global _pool
    if _pool and conn:
        _pool.putconn(conn)

def close_connection_pool():
    global _pool
    if _pool:
        _pool.closeall()
        logging.info("Pool de conexiones cerrado.")