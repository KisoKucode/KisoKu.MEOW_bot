import discord
from discord.ext import commands, tasks
from discord import app_commands, Embed
import random
from config import GENERAL_CHANNEL, BOT_NAME
# Arte ASCII de flores y paisajes
ARTE_ASCII = [
    """
         , . . ,
      . . , . . .
    . . . . . . . .
      ` . . . . `
         ` | `
     _  \\|/  _
    (_)(@)(_)
     / | \\
    """,
    """
       _(_)_        _(_)_       _(_)_
      (_)@(_)      (_)@(_)     (_)@(_)
        (_)\\        /(_)         /(_)
           |/      \\|           |\\
          \\|/      \\|/          \\|/
    \\|///\\|///\\|///\\|///
    """,
    """
         {@} * {@}
      * {@} * {@} *
    {@} * {@} * {@}
     \\ \\ \\ | / / /
      \\ \\ \\|/ / /
       \\ \\ | / /
        \\ \\|/ /
         \\|//
    ^^^^^^^^^^^^^^^
    """,
    """
           .
         .';
     .-'` . '
   ,`.-\'-.`\\ 
  ; /     '-'
  | \\       
  \\  \'-.__   _
   '-.__  `' _`
        `''-`
    """
]

class Romance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.poem_service = bot.poem_service
        # Iniciar el bucle automático al cargar el Cog
        self.romance_loop.start()

    def cog_unload(self):
        # Detener el bucle si se descarga el Cog
        self.romance_loop.cancel()

    def get_poem_content(self):
        """Elige entre un poema de la DB o uno de la lista predefinida."""
        return self.poem_service.get_poem()

    # Se ejecuta cada 60 minutos (puedes cambiar 'minutes=60' por lo que quieras)
    @tasks.loop(minutes=60)
    async def romance_loop(self):
        # Iterar sobre todos los servidores (guilds) donde está el bot
        for guild in self.bot.guilds:
            canal = discord.utils.get(guild.text_channels, name=GENERAL_CHANNEL)
            if canal:
                poema = self.get_poem_content()
                arte = random.choice(ARTE_ASCII)
                
                embed = Embed(title="🌹 Un momento de poesía...", description=f"_{poema}_", color=discord.Color.from_rgb(255, 182, 193)) # Light Pink
                embed.add_field(name="Paisaje", value=f"```\n{arte}\n```", inline=False)
                embed.set_footer(text=f"Con cariño, {BOT_NAME}")
                
                try:
                    await canal.send(embed=embed)
                except Exception:
                    pass # Si no puede enviar mensaje, lo ignora

    @romance_loop.before_loop
    async def before_romance_loop(self):
        # Esperar a que el bot esté completamente listo antes de empezar el bucle
        await self.bot.wait_until_ready()

    @app_commands.command(name="poema", description="Dedica un poema y un dibujo romántico.")
    async def poema_comando(self, interaction: discord.Interaction):
        poema = self.get_poem_content()
        arte = random.choice(ARTE_ASCII)
        
        embed = Embed(title="💖 Poema para ti", description=f"_{poema}_", color=discord.Color.red())
        embed.add_field(name="Para alegrar tu día:", value=f"```\n{arte}\n```", inline=False)
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="agregar_poema", description="Agrega tu propio poema a la base de datos.")
    async def agregar_poema(self, interaction: discord.Interaction, poema: str):
        if len(poema) < 10:
             await interaction.response.send_message("El poema es muy corto. ¡Inspírate un poco más!", ephemeral=True)
             return
        
        self.poem_service.add_poem(poema, interaction.user.id)
        await interaction.response.send_message("¡Qué hermoso! Tu poema ha sido guardado en mi corazón (y en la base de datos). 💖")

async def setup(bot):
    await bot.add_cog(Romance(bot))
