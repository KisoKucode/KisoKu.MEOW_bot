import os
import sys
import asyncio
import discord
from discord import Intents, app_commands
from discord.ext import commands
from dotenv import load_dotenv
import logging
import traceback

# --- Configuración de Logging ---
# Reemplaza los `print` por un sistema de logging más robusto.
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# --- Imports del Proyecto ---
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import BOT_NAME
from DB.database import init_connection_pool, close_connection_pool
from DB.user_dao import UserDAO
from DB.poem_dao import PoemDAO
from DB.panel_dao import PanelDAO

# --- Configuración Inicial ---
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Inicializar la base de datos ANTES de que el bot inicie
init_connection_pool()
UserDAO().create_table()
PoemDAO().create_table()
PanelDAO().create_table()

# --- Configuración del Bot ---
intents = Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='/', intents=intents)

# --- Manejador de Errores Global ---
@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    """
    Manejador de errores global para todos los comandos de barra.
    """
    # Extraer la excepción original de ser necesario
    original_error = getattr(error, 'original', error)
    
    # Loguear el error completo en la consola para depuración
    tb_str = ''.join(traceback.format_exception(type(original_error), original_error, original_error.__traceback__))
    logging.error(f"Error en el comando '{interaction.command.name}':\n{tb_str}")

    # Enviar un mensaje genérico y discreto al usuario
    error_message = "😕 ¡Ups! Ocurrió un error inesperado al procesar tu comando. Ya hemos sido notificados."
    
    # Intentar responder al usuario. Si la interacción ya fue respondida, se edita.
    try:
        if interaction.response.is_done():
            await interaction.followup.send(error_message, ephemeral=True)
        else:
            await interaction.response.send_message(error_message, ephemeral=True)
    except discord.errors.InteractionResponded:
        # Falla el followup si la respuesta original era efímera.
        # Es un caso borde, pero lo manejamos por si acaso.
        await interaction.edit_original_response(content=error_message)
    except Exception as e:
        logging.error(f"No se pudo enviar el mensaje de error al usuario: {e}")


@bot.event
async def on_ready():
    """
    Evento que se ejecuta cuando el bot está conectado y listo.
    """
    logging.info(f"¡{BOT_NAME} está en línea y listo para la acción!")
    logging.info(f"Conectado como {bot.user} (ID: {bot.user.id})")
    
    # Generar enlace de invitación con permisos de Administrador
    invite_url = discord.utils.oauth_url(bot.user.id, permissions=discord.Permissions(administrator=True))
    logging.info(f"🔗 Usa este enlace para invitar al bot con permisos: {invite_url}")

    # Sincronizar comandos de barra (slash commands)
    try:
        synced = await bot.tree.sync()
        logging.info(f"{len(synced)} comandos de barra sincronizados.")
    except Exception as e:
        logging.error(f"Error al sincronizar comandos: {e}")

async def main():
    """
    Función principal para iniciar y cerrar el bot y sus recursos.
    """
    # Cargar cogs ANTES de iniciar el bot
    logging.info("Cargando extensiones (cogs)...")
    extensions = ['cogs.general', 'cogs.utility', 'cogs.casino', 'cogs.levels', 
                  'cogs.shop', 'cogs.romance', 'cogs.status', 'cogs.economy', 'cogs.games']
    for ext in extensions:
        try:
            await bot.load_extension(ext)
        except Exception as e:
            logging.error(f"❌ Error al cargar la extensión '{ext}': {e}")
    logging.info("Extensiones cargadas exitosamente.")

    async with bot:
        await bot.start(TOKEN)

# --- Punto de Entrada ---
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Cierre solicitado por el usuario.")
    finally:
        close_connection_pool()