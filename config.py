from dotenv import load_dotenv
import os
import logging

# Cargar variables de entorno antes de leerlas.
load_dotenv()

# --- Carga de Configuración desde Variables de Entorno ---
# Nombre del Bot (String)
BOT_NAME = os.getenv("BOT_NAME", "MEOW")

# Token de Discord
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Canales (Strings)
GENERAL_CHANNEL = os.getenv("GENERAL_CHANNEL", "general")
SUGGESTIONS_CHANNEL = os.getenv("SUGGESTIONS_CHANNEL", "sugerencias")

# --- Configuración de la Base de Datos ---
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "meow_bot_db")
DB_USER = os.getenv("DB_USER", "meow_bot_user")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = int(os.getenv("DB_PORT", "5432") or 5432)

# --- Configuración del Casino (Integer) ---
# Se intenta convertir DAILY_AMOUNT a un entero. Si falla o no está definida,
# se usa 100 como valor por defecto y se registra una advertencia.
try:
    DAILY_AMOUNT = int(os.getenv("DAILY_AMOUNT", 100))
except (ValueError, TypeError):
    logging.warning(
        f"La variable de entorno DAILY_AMOUNT ('{os.getenv('DAILY_AMOUNT')}') no es un número válido. "
        "Se usará el valor por defecto: 100."
    )
    DAILY_AMOUNT = 100

# Validar que DAILY_AMOUNT no sea negativo
if DAILY_AMOUNT < 0:
    logging.warning(
        f"DAILY_AMOUNT ({DAILY_AMOUNT}) es negativo. Se establecerá a 0."
    )
    DAILY_AMOUNT = 0
