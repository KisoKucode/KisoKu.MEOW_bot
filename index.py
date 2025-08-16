# bot.py
import os
from discord import Client, Intents
from discord.ext import commands
from dotenv import load_dotenv
import datetime   
import random
# Iniciar el bot
# python index.py
# Leer las variables de entorno
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Permisos del bot
intents = Intents.default()
intents.message_content = True

# Inicialización del bot
bot = commands.Bot(command_prefix='/', intents=intents)

# Comandos
# saludo

@bot.command()
async def saludo(ctx):
    await ctx.send(f"¡MEOW de la un abrazo muy fraternal a, {ctx.author.mention}! MEOW de la un abrazo muy fraternal y Bienvenido al servidor.")
    


# despedida
@bot.command()
async def despedida(ctx):
    await ctx.send(f"¡Hasta luegoMEOW llora , {ctx.author.mention}! adios hermano que no sea un adios si no un asta pronto.")


# hora
@bot.command()
async def hora(ctx):
    ahora = datetime.datetime.now()
    await ctx.send(f"MEOW La hora actual es: {ahora.strftime('%H:%M:%S')}")

# chistes
@bot.command()
async def chiste(ctx):
    chistes = [
        "¿Por qué los gatos no juegan a las cartas? Porque hay demasiados tramposos.",
        "¿Qué hace un pez? ¡Nada!",
        "¿Cómo se despiden los químicos? Ácido un placer.",
        "¿Por qué los pájaros no usan Facebook? Porque ya tienen Twitter."
    ]
    await ctx.send(random.choice(chistes))
# Comando para mostrar la lista de comandos
@bot.command()
async def comandos(ctx):
    comandos = [
        "/ping - Responde con pong",
        "/saludo - Saluda al usuario",
        "/despedida - Se despide del usuario",
        "/hora - Muestra la hora actual",
        "/chiste - Cuenta un chiste"
    ]
    await ctx.send("Lista de comandos:\n" + "\n".join(comandos))

 # usuario
@bot.command()
async def usuario(ctx):
    user = ctx.author
    await ctx.send(
        f"¡Hola MEOW {user.mention}! Eres un usuario muy especial MEOW.\n"
        f"Tu nombre de usuario es: {user.name}\nTu ID es: {user.id}"
    )



    
# Evento que se ejecuta cuando el bot está listo
@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")
    print("Lista de comandos disponibles:")
    for command in bot.commands:
        print(f" - {command.name}") 
        
        
        

bot.run(TOKEN)