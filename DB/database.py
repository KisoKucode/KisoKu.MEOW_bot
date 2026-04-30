import logging
from psycopg2 import pool
import psycopg2
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

_pool = None

def init_connection_pool():
    """Inicializa el pool de conexiones a la base de datos."""
    global _pool
    if _pool:
        return

    if not all([DB_USER, DB_PASSWORD, DB_NAME]):
        raise RuntimeError("Faltan variables de entorno de base de datos. Revisa DB_USER, DB_PASSWORD y DB_NAME.")

    try:
        _pool = pool.SimpleConnectionPool(
            1, 20,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME
        )
        logging.info("✅ Conexión a base de datos establecida.")
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(f"❌ Error al conectar a PostgreSQL: {error}")
        raise

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

# Alias compatibles con pruebas y nomenclatura más explícita
def get_db_connection():
    return get_connection()

# Alias compatibles con pruebas y nomenclatura más explícita
def release_db_connection(conn):
    return return_connection(conn)

def close_connection_pool():
    global _pool
    if _pool:
        _pool.closeall()
        logging.info("Pool de conexiones cerrado.")