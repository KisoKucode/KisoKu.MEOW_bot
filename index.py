# bot.py
import os
from discord import Client, Intents
from discord.ext import commands
from dotenv import load_dotenv

# Leer las variables de entorno
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Permisos del bot
intents = Intents.default()
intents.message_content = True

# Inicialización del bot
bot = commands.Bot(command_prefix='/', intents=intents)

# Comandos
@bot.command()
async def ping(ctx):
    await ctx.send("pong")

bot.run(TOKEN)