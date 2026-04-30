import asyncio
import logging
import traceback
import discord
from discord import Intents, app_commands
from discord.ext import commands
from dotenv import load_dotenv

from config import BOT_NAME, DISCORD_TOKEN
from DB.database import init_connection_pool, close_connection_pool
from DB.user_dao import UserDAO
from DB.poem_dao import PoemDAO
from DB.panel_dao import PanelDAO
from services.user_service import UserService
from services.economy_service import EconomyService
from services.level_service import LevelService
from services.poem_service import PoemService
from services.panel_service import PanelService
from services.casino_service import CasinoService
from services.shop_service import ShopService
from services.hangman_service import HangmanService

load_dotenv()

COG_EXTENSIONS = [
    'cogs.general',
    'cogs.utility',
    'cogs.casino',
    'cogs.levels',
    'cogs.shop',
    'cogs.romance',
    'cogs.status',
    'cogs.economy',
    'cogs.hangman'
]


def validate_config():
    if not DISCORD_TOKEN:
        logging.error('La variable de entorno DISCORD_TOKEN no está definida. Revisa tu archivo .env.')
        raise SystemExit('DISCORD_TOKEN no definido')


def create_bot():
    intents = Intents.default()
    intents.message_content = True
    intents.members = True

    bot = commands.Bot(command_prefix='/', intents=intents)
    register_event_handlers(bot)
    return bot


def register_event_handlers(bot):
    @bot.tree.error
    async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
        original_error = getattr(error, 'original', error)
        tb_str = ''.join(traceback.format_exception(type(original_error), original_error, original_error.__traceback__))
        logging.error(f"Error en el comando '{interaction.command.name}':\n{tb_str}")

        error_message = '😕 ¡Ups! Ocurrió un error inesperado al procesar tu comando. Ya hemos sido notificados.'
        try:
            if interaction.response.is_done():
                await interaction.followup.send(error_message, ephemeral=True)
            else:
                await interaction.response.send_message(error_message, ephemeral=True)
        except discord.errors.InteractionResponded:
            await interaction.edit_original_response(content=error_message)
        except Exception as e:
            logging.error(f'No se pudo enviar el mensaje de error al usuario: {e}')

    @bot.event
    async def on_ready():
        logging.info(f'¡{BOT_NAME} está en línea y listo para la acción!')
        print(f"\n✨ >>> ✅ {BOT_NAME} está funcionando y corriendo perfecto. <<< ✨\n")
        logging.info(f'Conectado como {bot.user} (ID: {bot.user.id})')

        invite_url = discord.utils.oauth_url(bot.user.id, permissions=discord.Permissions(administrator=True))
        logging.info(f'🔗 Usa este enlace para invitar el bot con permisos: {invite_url}')

        try:
            synced = await bot.tree.sync()
            logging.info(f'{len(synced)} comandos de barra sincronizados.')
        except Exception as e:
            logging.error(f'Error al sincronizar comandos: {e}')


def initialize_services(bot):
    init_connection_pool()

    user_dao = UserDAO()
    poem_dao = PoemDAO()
    panel_dao = PanelDAO()

    user_dao.create_table()
    poem_dao.create_table()
    panel_dao.create_table()

    bot.user_service = UserService(user_dao)
    bot.economy_service = EconomyService(bot.user_service)
    bot.level_service = LevelService(bot.user_service)
    bot.casino_service = CasinoService(bot.user_service)
    bot.shop_service = ShopService(bot.user_service)
    bot.hangman_service = HangmanService(bot.user_service)
    bot.poem_service = PoemService(poem_dao)
    bot.panel_service = PanelService(panel_dao)


async def load_extensions(bot):
    for ext in COG_EXTENSIONS:
        try:
            await bot.load_extension(ext)
        except Exception as e:
            logging.error(f"❌ Error al cargar la extensión '{ext}': {e}")


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logging.info('Inicializando configuración y servicios...')
    validate_config()
    bot = create_bot()
    initialize_services(bot)

    logging.info('Cargando extensiones (cogs)...')
    await load_extensions(bot)
    logging.info('Extensiones cargadas exitosamente.')

    try:
        async with bot:
            await bot.start(DISCORD_TOKEN, reconnect=False)
    except discord.LoginFailure as err:
        logging.error('Fallo de autenticación en Discord: revisa DISCORD_TOKEN en .env.')
        logging.error(err)
    except discord.HTTPException as err:
        logging.error('Error HTTP al conectar con Discord. Puede ser token inválido o un problema de red.')
        logging.error(err)
    except Exception:
        logging.error('Error inesperado al iniciar el bot:')
        logging.error(traceback.format_exc())
    finally:
        close_connection_pool()


def run():
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info('Cierre solicitado por el usuario.')
