import discord
from discord.ext import commands
from discord import app_commands, Embed
import datetime
import random

# Importar desde config.py
from config import BOT_NAME, GENERAL_CHANNEL, SUGGESTIONS_CHANNEL

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Eventos de bienvenida
    @commands.Cog.listener()
    async def on_member_join(self, member):
        canal = discord.utils.get(member.guild.text_channels, name=GENERAL_CHANNEL)
        if canal:
            server_name = member.guild.name
            await canal.send(
                f"{BOT_NAME} de la un abrazo muy fraternal a {member.mention} y le desea lo mejor y mucha diversion y Bienvenido a {server_name}!"
            )

    # Evento de despedida
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        canal = discord.utils.get(member.guild.text_channels, name=GENERAL_CHANNEL)
        if canal:
            await canal.send(f"{BOT_NAME} llora por {member.name}... ¡Adiós hermano, que no sea un adiós sino un hasta pronto!")

    # Comandos de saludo
    @app_commands.command(name="saludo", description="Saluda al usuario")
    async def saludo(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"¡{BOT_NAME} de la un abrazo muy fraternal a, {interaction.user.mention}! y(le susurra al oido: diviertete mucho en"
        )

    # despedida
    @app_commands.command(name="despedida", description="Despedida personalizada")
    async def despedida(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"¡Hasta luego, {interaction.user.mention}! {BOT_NAME} llora... adios hermano que no sea un adios si no un hasta pronto."
        )

    # Hora
    @app_commands.command(name="hora", description="Muestra la hora actual")
    async def hora(self, interaction: discord.Interaction):
        ahora = datetime.datetime.now()
        await interaction.response.send_message(
            f"{BOT_NAME} dice que la hora actual es: {ahora.strftime('%H:%M:%S')}"
        )

    # chiste
    @app_commands.command(name="chiste", description="Cuenta un chiste")
    async def chiste(self, interaction: discord.Interaction):
        chistes = [
            f"¿Por qué los gatos como {BOT_NAME} no juegan a las cartas? Porque hay demasiados tramposos.",
            "¿Qué hace un pez? ¡Nada!",
            "¿Qué hace un pez? ¡Nada!",
            "¿Cómo se despiden los químicos? Ácido un placer.",
            "¿Por qué los pájaros no usan Facebook? Porque ya tienen Twitter."
        ]
        await interaction.response.send_message(random.choice(chistes))

    # ayuda
    @app_commands.command(name="ayuda", description="Lista de comandos disponibles")
    async def ayuda(self, interaction: discord.Interaction):
        ayuda_texto = (
            "**Comandos Generales**\n"
            "`/saludo` - Te doy un saludo fraternal.\n"
            "`/despedida` - Me despido de ti.\n"
            "`/hora` - Muestro la hora actual.\n"
            "`/chiste` - Te cuento un chiste malo.\n"
            "`/ayuda` - Muestro este mensaje de ayuda.\n"
            "\n"
            "**Comandos de Casino**\n"
            "`/saldo` - Revisa cuántas monedas tienes.\n"
            "`/diario` - Recoge tu recompensa diaria de monedas.\n"
            "`/tragamonedas <apuesta>` - Juega a las tragamonedas.\n"
            "`/moneda <apuesta> <elección>` - Apuesta en un cara o cruz.\n"
            "`/blackjack <apuesta>` - Juega una partida de Blackjack.\n"
            "`/clasificacion` - Muestra a los usuarios más ricos.\n"
            "`/dados_apuesta <apuesta> <elección>` - Apuesta al resultado de dos dados.\n"
            "`/ruleta` - Apuesta en la ruleta (número, color o paridad).\n"
            "`/carrera <apuesta> <corredor>` - Apuesta en una emocionante carrera de animales.\n"
            "`/videopoker <apuesta>` - Juega al Video Poker.\n"
            "\n"
            "**Comandos de Utilidad**\n"
            "`/usuario` - Muestra tu información de Discord.\n"
            "`/server` - Muestra información de este servidor.\n"
            "`/avatar` - Muestra tu foto de perfil.\n"
            "`/miembros` - Muestra el número de miembros.\n"
            "`/sugerencia <texto>` - Envía una sugerencia para el servidor.\n"
        )
        embed = Embed(title=f"Comandos de {BOT_NAME}", description=ayuda_texto, color=discord.Color.blue())
        embed.set_footer(text=f"¡{BOT_NAME} te desea suerte!")
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(General(bot))