import os
import logging

# --- Carga de Configuración desde Variables de Entorno ---
# Lee las variables del entorno, proporcionando valores por defecto
# para asegurar que el bot pueda funcionar incluso si no están definidas.

# Nombre del Bot (String)
BOT_NAME = os.getenv("BOT_NAME", "MEOW")

# Canales (Strings)
GENERAL_CHANNEL = os.getenv("GENERAL_CHANNEL", "general")
SUGGESTIONS_CHANNEL = os.getenv("SUGGESTIONS_CHANNEL", "sugerencias")

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
