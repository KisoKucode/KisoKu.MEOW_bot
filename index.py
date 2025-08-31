import os
import discord
from discord import Intents
from discord.ext import commands
from dotenv import load_dotenv

# Import from config.py
from config import BOT_NAME

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f"¡{BOT_NAME} está en línea y listo para la acción!")
    print(f"Conectado como {bot.user}")
    
    # Load cogs
    await bot.load_extension('cogs.general')
    await bot.load_extension('cogs.utility')
    await bot.load_extension('cogs.casino')
    
    # Sync slash commands
    await bot.tree.sync()
    print("Slash commands sincronizados.")

bot.run(TOKEN)
