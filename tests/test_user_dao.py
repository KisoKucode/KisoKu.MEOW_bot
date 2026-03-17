import pytest
from DB.database import init_connection_pool, close_connection_pool, get_db_connection, release_db_connection
from DB.user_dao import UserDAO, STARTING_BALANCE

# Marks all tests in this file as asyncio tests for pytest-asyncio
pytestmark = pytest.mark.asyncio

@pytest.fixture(scope="module")
def dao():
    """
    Este es el "fixture" de base de datos para nuestras pruebas.
    - Se ejecuta UNA VEZ por módulo (por sesión de prueba en este caso).
    - Inicializa el pool de conexiones (usando las variables de tests/.env).
    - Crea la instancia del DAO.
    - Crea la tabla 'users'.
    - 'yield' proporciona el objeto DAO a las funciones de prueba.
    - Después de que todas las pruebas en el módulo se completan, el código después
      del yield se ejecuta para limpiar (eliminar la tabla y cerrar conexiones).
    """
    # --- Setup ---
    init_connection_pool()
    user_dao = UserDAO()
    user_dao.create_table()

    yield user_dao

    # --- Teardown ---
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Usamos CASCADE para eliminar dependencias si las hubiera en el futuro
            cursor.execute("DROP TABLE IF EXISTS users CASCADE")
            conn.commit()
    finally:
        release_db_connection(conn)
    
    close_connection_pool()


# --- Pruebas Unitarias para UserDAO ---

def test_find_or_create_creates_user(dao: UserDAO):
    """
    Verifica que un nuevo usuario es creado correctamente si no existe.
    """
    user_id = 1111
    
    # Asegurarse de que el usuario no existe para empezar
    found_user = dao.find_by_id(user_id)
    assert found_user is None

    # Llamar a la función a probar
    created_user = dao.find_or_create(user_id)

    # Verificaciones (Assertions)
    assert created_user is not None
    assert created_user['user_id'] == user_id
    assert created_user['balance'] == STARTING_BALANCE
    assert created_user['last_daily'] is None

def test_find_or_create_finds_existing_user(dao: UserDAO):
    """
    Verifica que un usuario existente es encontrado correctamente.
    """
    user_id = 2222
    
    # Crear un usuario primero
    dao.create(user_id)

    # Llamar a la función a probar
    found_user = dao.find_or_create(user_id)
    
    # Verificaciones
    assert found_user is not None
    assert found_user['user_id'] == user_id
    assert found_user['balance'] == STARTING_BALANCE


def test_update_balance(dao: UserDAO):
    """
    Verifica que el saldo de un usuario se actualiza correctamente.
    """
    user_id = 3333
    new_balance = 9999
    
    # Crear usuario
    user = dao.find_or_create(user_id)
    assert user['balance'] == STARTING_BALANCE

    # Llamar a la función a probar
    dao.update(user_id, balance=new_balance)

    # Obtener el usuario de nuevo para verificar el cambio
    updated_user = dao.find_by_id(user_id)

    # Verificaciones
    assert updated_user['balance'] == new_balance


def test_get_leaderboard(dao: UserDAO):
    """
    Verifica que la clasificación se devuelve en el orden correcto.
    """
    # Crear usuarios con saldos diferentes
    dao.find_or_create(4444) # Saldo inicial 200
    dao.find_or_create(5555) # Saldo inicial 200
    dao.find_or_create(6666) # Saldo inicial 200

    # Actualizar saldos para crear un orden
    dao.update(user_id=4444, balance=50)   # Tercer lugar
    dao.update(user_id=5555, balance=1000) # Primer lugar
    dao.update(user_id=6666, balance=500)  # Segundo lugar

    # Llamar a la función a probar
    leaderboard = dao.get_leaderboard(limit=3)

    # Verificaciones
    assert len(leaderboard) == 3
    assert leaderboard[0]['user_id'] == 5555
    assert leaderboard[0]['balance'] == 1000
    assert leaderboard[1]['user_id'] == 6666
    assert leaderboard[2]['user_id'] == 4444
