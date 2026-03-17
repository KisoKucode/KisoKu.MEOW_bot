import discord
from discord.ext import commands
from discord import app_commands, Embed
import datetime
import random

# Importar desde config.py
from config import BOT_NAME, GENERAL_CHANNEL

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
                f"¡{BOT_NAME} le da un abrazo muy fraternal a {member.mention}! Le desea lo mejor, mucha diversión y le da la bienvenida a {server_name}."
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
            f"¡{BOT_NAME} le da un abrazo muy fraternal a {interaction.user.mention}! (y le susurra al oído: ¡diviértete mucho!)"
        )

    # despedida
    @app_commands.command(name="despedida", description="Despedida personalizada")
    async def despedida(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"¡Hasta luego, {interaction.user.mention}! {BOT_NAME} llora... adiós hermano, que no sea un adiós sino un hasta pronto."
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
        embed = Embed(title=f"📜 Comandos de {BOT_NAME}",
                      description=f"¡Hola! Soy {BOT_NAME}, tu asistente. Aquí tienes una lista de lo que puedo hacer.\n"
                                  "Usa los comandos con `/` para interactuar conmigo.",
                      color=discord.Color.blue())

        cog_emojis = {
            "General": "🎉", "Utility": "🔧", "Economy": "💰", "Casino": "🎰",
            "Levels": "⭐", "Shop": "🛍️", "Romance": "💖", "Status": "🖥️",
        }

        # Definir el orden de prioridad para mostrar los Cogs
        priority_order = ["General", "Utility", "Economy", "Casino", "Levels", "Shop", "Romance", "Status"]
        
        # Obtener los Cogs cargados y ordenarlos según la prioridad
        loaded_cogs = list(self.bot.cogs.items())
        loaded_cogs.sort(key=lambda item: priority_order.index(item[0]) if item[0] in priority_order else 999)

        for cog_name, cog in loaded_cogs:
            commands_list = []
            # Usamos get_app_commands() que es el método oficial para obtener los comandos de un Cog
            for command in cog.get_app_commands():
                if command.name == "ayuda":
                    continue

                if isinstance(command, app_commands.Group):
                    for sub in command.commands:
                        commands_list.append(f"`/{command.name} {sub.name}`")
                else:
                    commands_list.append(f"`/{command.name}`")
            
            if commands_list:
                commands_list.sort()
                emoji = cog_emojis.get(cog_name, "⚙️")
                embed.add_field(name=f"{emoji} {cog_name}", value=", ".join(commands_list), inline=False)

        embed.set_footer(text="Desarrollado con ❤️. ¡Diviértete!")
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(General(bot))