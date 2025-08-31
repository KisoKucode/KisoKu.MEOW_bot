import discord
from discord.ext import commands
from discord import app_commands, Embed

# Importar desde config.py
from config import BOT_NAME, SUGGESTIONS_CHANNEL

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # inf server
    @app_commands.command(name="server", description="Información del servidor")
    async def server(self, interaction: discord.Interaction):
        guild = interaction.guild
        await interaction.response.send_message(
            f"¡Hola {BOT_NAME}! Estás en el servidor: {guild.name}"
            f"ID del servidor: {guild.id}"
            f"Total de miembros: {guild.member_count}"
        )

    # id info
    @app_commands.command(name="usuario", description="Muestra tu información")
    async def usuario(self, interaction: discord.Interaction):
        user = interaction.user
        await interaction.response.send_message(
            f"¡Hola {BOT_NAME} {user.mention}! Eres un usuario muy especial para {BOT_NAME}.\n"
            f"Tu nombre de usuario es: {user.name}\nTu ID es: {user.id}"
        )

    # encuesta
    @app_commands.command(name="encuesta", description="Encuesta rápida")
    async def encuesta(self, interaction: discord.Interaction, pregunta: str):
        await interaction.response.send_message(
            f"📊 Encuesta rápida: {pregunta}\nReaccionar con 👍 para sí o 👎 para no."
        )
        mensaje = await interaction.original_response()
        await mensaje.add_reaction("👍")
        await mensaje.add_reaction("👎")

    # Muestra el avatar del usuario que ejecuta el comando
    @app_commands.command(name="avatar", description="Muestra tu avatar")
    async def avatar(self, interaction: discord.Interaction):
        await interaction.response.send_message(interaction.user.avatar.url)

    # Muestra el número total de miembros y cuántos están en línea
    @app_commands.command(name="miembros", description="Muestra el número de miembros y cuántos están en línea")
    async def miembros(self, interaction: discord.Interaction):
        guild = interaction.guild
        online = sum(1 for m in guild.members if m.status == discord.Status.online and not m.bot)
        await interaction.response.send_message(
            f"Total de miembros: {guild.member_count}\nMiembros en línea: {online}"
        )

    # Muestra información sobre un rol específico
    @app_commands.command(name="rolinfo", description="Muestra información sobre un rol")
    async def rolinfo(self, interaction: discord.Interaction, rol: discord.Role):
        await interaction.response.send_message(
            f"Rol: {rol.name}\nID: {rol.id}\nMiembros: {len(rol.members)}"
        )

    @app_commands.command(name="canales", description="Lista todos los canales del servidor")
    async def canales(self, interaction: discord.Interaction):
        canales = [c.name for c in interaction.guild.channels]
        await interaction.response.send_message("Canales:\n" + "\n".join(canales))

    # Envía el enlace de invitación del servidor (puedes personalizar el mensaje)
    @app_commands.command(name="invitar", description="Envía el enlace de invitación del servidor")
    async def invitar(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "Puedes crear una invitación desde Discord o pedirle a un admin que la comparta aquí."
        )

    # Envía un mensaje privado a un usuario
    @app_commands.command(name="mensajeprivado", description="Envía un mensaje privado a un usuario")
    async def mensajeprivado(self, interaction: discord.Interaction, usuario: discord.User, mensaje: str):
        await usuario.send(mensaje)
        await interaction.response.send_message(f"Mensaje enviado a {usuario.mention}")

    # Envía una sugerencia a un canal llamado 'sugerencias'
    @app_commands.command(name="sugerencia", description="Envía una sugerencia")
    async def sugerencia(self, interaction: discord.Interaction, texto: str):
        canal = discord.utils.get(interaction.guild.text_channels, name=SUGGESTIONS_CHANNEL)
        if canal:
            await canal.send(f"Sugerencia de {interaction.user.mention}: {texto}")
            await interaction.response.send_message("¡Sugerencia enviada!")
        else:
            await interaction.response.send_message(f"No existe un canal llamado '{SUGGESTIONS_CHANNEL}'.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Utility(bot))