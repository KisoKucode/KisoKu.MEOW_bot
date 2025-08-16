import os
import discord
from discord import Intents
from discord.ext import commands
from dotenv import load_dotenv
import datetime
import random

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)


# Eventos de bienvenida 
@bot.event
async def on_member_join(member):
    canal = discord.utils.get(member.guild.text_channels, name='general')
    if canal:
        server_name = member.guild.name
        await canal.send(
            f"MEOW de la un abrazo muy fraternal a {member.mention} y le desea lo mejor y mucha diversion y Bienvenido a {server_name}!"
        )

# Evento de despedida
@bot.event
async def on_member_remove(member):
    canal = discord.utils.get(member.guild.text_channels, name='general')
    if canal:
        await canal.send(f"MEOW llora por {member.name}... ¡Adiós hermano, que no sea un adiós sino un hasta pronto!")



# Comandos de saludo
@bot.tree.command(name="saludo", description="Saluda al usuario")
async def saludo(interaction: discord.Interaction):
    await interaction.response.send_message(
        f"¡MEOW de la un abrazo muy fraternal a, {interaction.user.mention}! y(le susurra al oido: diviertete mucho en"
    )
#despedia
@bot.tree.command(name="despedida", description="Despedida personalizada") 
async def despedida(interaction: discord.Interaction):
    await interaction.response.send_message(
        f"¡Hasta luegoMEOW llora , {interaction.user.mention}! adios hermano que no sea un adios si no un asta pronto."
    )
# Hora
@bot.tree.command(name="hora", description="Muestra la hora actual")
async def hora(interaction: discord.Interaction):
    ahora = datetime.datetime.now()
    await interaction.response.send_message(
        f"MEOW La hora actual es: {ahora.strftime('%H:%M:%S')}"
    )
# chiste
@bot.tree.command(name="chiste", description="Cuenta un chiste")
async def chiste(interaction: discord.Interaction):
    chistes = [
        "¿Por qué los gatos no juegan a las cartas? Porque hay demasiados tramposos.",
        "¿Qué hace un pez? ¡Nada!",
        "¿Cómo se despiden los químicos? Ácido un placer.",
        "¿Por qué los pájaros no usan Facebook? Porque ya tienen Twitter."
    ]
    await interaction.response.send_message(random.choice(chistes))
# ayuda
@bot.tree.command(name="ayuda", description="Lista de comandos disponibles")
async def ayuda(interaction: discord.Interaction):
    ayuda_texto = (
        "Comandos disponibles:\n"
        "/saludo - Saluda al usuario\n"
        "/despedida - Se despide del usuario\n"
        "/hora - Muestra la hora actual\n"
        "/chiste - Cuenta un chiste\n"
        "/usuario - Muestra tu información\n"
        "/dado - Lanza un dado\n"
        "/server - Información del servidor\n"
        "/repetir <mensaje> - Repite tu mensaje\n"
        "/encuesta <pregunta> - Encuesta rápida\n"
    )
    await interaction.response.send_message(ayuda_texto)
# inf server
@bot.tree.command(name="server", description="Información del servidor")
async def server(interaction: discord.Interaction):
    guild = interaction.guild
    await interaction.response.send_message(
        f"¡Hola MEOW! Estás en el servidor: {guild.name}\n"
        f"ID del servidor: {guild.id}\n"
        f"Total de miembros: {guild.member_count}"
    )
# id info
@bot.tree.command(name="usuario", description="Muestra tu información")
async def usuario(interaction: discord.Interaction):
    user = interaction.user
    await interaction.response.send_message(
        f"¡Hola MEOW {user.mention}! Eres un usuario muy especial MEOW.\n"
        f"Tu nombre de usuario es: {user.name}\nTu ID es: {user.id}"
    )
# encuesta
@bot.tree.command(name="encuesta", description="Encuesta rápida")
async def encuesta(interaction: discord.Interaction, pregunta: str):
    mensaje = await interaction.response.send_message(
        f"📊 Encuesta rápida: {pregunta}\nReaccionar con 👍 para sí o 👎 para no."
    )
  
# primer mini juego
@bot.tree.command(name="dado", description="Lanza un dado")
async def dado(interaction: discord.Interaction):
    resultado = random.randint(1, 6)
    await interaction.response.send_message(f"🎲 El dado cayó en: {resultado}")
#repetir mensaje
@bot.tree.command(name="repetir", description="Repite tu mensaje")
async def repetir(interaction: discord.Interaction, mensaje: str):
    await interaction.response.send_message(mensaje)
#evento de inicio en cmd (el placer en forma pura)
# python index.py
@bot.event
async def on_ready():  
    await bot.tree.sync()
    print(f"Bot conectado como {bot.user}")
    print("Slash commands sincronizados.")

bot.run(TOKEN)