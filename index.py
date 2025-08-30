import os
import discord
from discord import Intents, Embed, app_commands, ui
from discord.ext import commands
from dotenv import load_dotenv
import datetime
import random
import asyncio
import database as db # ¡Aquí importamos nuestro módulo de base de datos!

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# --- Constantes de Configuración ---
BOT_NAME = "MEOW"
GENERAL_CHANNEL = "general"
SUGGESTIONS_CHANNEL = "sugerencias"

# --- Configuración de Economía ---
DAILY_AMOUNT = 100


intents = Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)


# Eventos de bienvenida 
@bot.event
async def on_member_join(member):
    canal = discord.utils.get(member.guild.text_channels, name=GENERAL_CHANNEL)
    if canal:
        server_name = member.guild.name
        await canal.send(
            f"{BOT_NAME} de la un abrazo muy fraternal a {member.mention} y le desea lo mejor y mucha diversion y Bienvenido a {server_name}!"
        )

# Evento de despedida
@bot.event
async def on_member_remove(member):
    canal = discord.utils.get(member.guild.text_channels, name=GENERAL_CHANNEL)
    if canal:
        await canal.send(f"{BOT_NAME} llora por {member.name}... ¡Adiós hermano, que no sea un adiós sino un hasta pronto!")



# Comandos de saludo
@bot.tree.command(name="saludo", description="Saluda al usuario")
async def saludo(interaction: discord.Interaction):
    await interaction.response.send_message(
        f"¡{BOT_NAME} de la un abrazo muy fraternal a, {interaction.user.mention}! y(le susurra al oido: diviertete mucho en"
    )
#despedia
@bot.tree.command(name="despedida", description="Despedida personalizada") 
async def despedida(interaction: discord.Interaction):
    await interaction.response.send_message(
        f"¡Hasta luego, {interaction.user.mention}! {BOT_NAME} llora... adios hermano que no sea un adios si no un hasta pronto."
    )
# Hora
@bot.tree.command(name="hora", description="Muestra la hora actual")
async def hora(interaction: discord.Interaction):
    ahora = datetime.datetime.now()
    await interaction.response.send_message(  
        f"{BOT_NAME} dice que la hora actual es: {ahora.strftime('%H:%M:%S')}"
    )
# chiste
@bot.tree.command(name="chiste", description="Cuenta un chiste")
async def chiste(interaction: discord.Interaction):
    chistes = [
        f"¿Por qué los gatos como {BOT_NAME} no juegan a las cartas? Porque hay demasiados tramposos.",
        "¿Qué hace un pez? ¡Nada!",
        "¿Cómo se despiden los químicos? Ácido un placer.",
        "¿Por qué los pájaros no usan Facebook? Porque ya tienen Twitter."
    ]
    await interaction.response.send_message(random.choice(chistes))
# ayuda
@bot.tree.command(name="ayuda", description="Lista de comandos disponibles")
async def ayuda(interaction: discord.Interaction):
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

# inf server
@bot.tree.command(name="server", description="Información del servidor")
async def server(interaction: discord.Interaction):
    guild = interaction.guild
    await interaction.response.send_message(
        f"¡Hola {BOT_NAME}! Estás en el servidor: {guild.name}\n"
        f"ID del servidor: {guild.id}\n"
        f"Total de miembros: {guild.member_count}"
    )
# id info
@bot.tree.command(name="usuario", description="Muestra tu información")
async def usuario(interaction: discord.Interaction):
    user = interaction.user
    await interaction.response.send_message(
        f"¡Hola {BOT_NAME} {user.mention}! Eres un usuario muy especial para {BOT_NAME}.\n"
        f"Tu nombre de usuario es: {user.name}\nTu ID es: {user.id}"
    )
# encuesta
@bot.tree.command(name="encuesta", description="Encuesta rápida")
async def encuesta(interaction: discord.Interaction, pregunta: str):
    await interaction.response.send_message(
        f"📊 Encuesta rápida: {pregunta}\nReaccionar con 👍 para sí o 👎 para no."
    )
    mensaje = await interaction.original_response()
    await mensaje.add_reaction("👍")
    await mensaje.add_reaction("👎")

# Muestra el avatar del usuario que ejecuta el comando
@bot.tree.command(name="avatar", description="Muestra tu avatar")
async def avatar(interaction: discord.Interaction):
    await interaction.response.send_message(interaction.user.avatar.url)

# Muestra el número total de miembros y cuántos están en línea
@bot.tree.command(name="miembros", description="Muestra el número de miembros y cuántos están en línea")
async def miembros(interaction: discord.Interaction):
    guild = interaction.guild
    online = sum(1 for m in guild.members if m.status == discord.Status.online and not m.bot)
    await interaction.response.send_message(
        f"Total de miembros: {guild.member_count}\nMiembros en línea: {online}"
    )

# Muestra información sobre un rol específico
@bot.tree.command(name="rolinfo", description="Muestra información sobre un rol")
async def rolinfo(interaction: discord.Interaction, rol: discord.Role):
    await interaction.response.send_message(
        f"Rol: {rol.name}\nID: {rol.id}\nMiembros: {len(rol.members)}"
    )

@bot.tree.command(name="canales", description="Lista todos los canales del servidor")
async def canales(interaction: discord.Interaction):
    canales = [c.name for c in interaction.guild.channels]
    await interaction.response.send_message("Canales:\n" + "\n".join(canales))

# Envía el enlace de invitación del servidor (puedes personalizar el mensaje)
@bot.tree.command(name="invitar", description="Envía el enlace de invitación del servidor")
async def invitar(interaction: discord.Interaction):
    await interaction.response.send_message(
        "Puedes crear una invitación desde Discord o pedirle a un admin que la comparta aquí."
    )

# Envía un mensaje privado a un usuario
@bot.tree.command(name="mensajeprivado", description="Envía un mensaje privado a un usuario")
async def mensajeprivado(interaction: discord.Interaction, usuario: discord.User, mensaje: str):
    await usuario.send(mensaje)
    await interaction.response.send_message(f"Mensaje enviado a {usuario.mention}")

# Envía una sugerencia a un canal llamado 'sugerencias'
@bot.tree.command(name="sugerencia", description="Envía una sugerencia")
async def sugerencia(interaction: discord.Interaction, texto: str):
    canal = discord.utils.get(interaction.guild.text_channels, name=SUGGESTIONS_CHANNEL)
    if canal:
        await canal.send(f"Sugerencia de {interaction.user.mention}: {texto}")
        await interaction.response.send_message("¡Sugerencia enviada!")
    else:
        await interaction.response.send_message(f"No existe un canal llamado '{SUGGESTIONS_CHANNEL}'.", ephemeral=True)  

# --- Comandos de Casino ---

async def validate_bet(interaction: discord.Interaction, apuesta: int):
    """Valida la apuesta de un usuario y retorna su saldo si es válida, o None si no lo es."""
    user_id = interaction.user.id
    user_data = db.get_user(user_id)
    balance = user_data["balance"]

    if apuesta <= 0:
        await interaction.response.send_message("La apuesta debe ser mayor que cero.", ephemeral=True)
        return None, None

    if balance < apuesta:
        await interaction.response.send_message(f"No tienes suficientes monedas. Tu saldo es de {balance}.", ephemeral=True)
        return None, None
    
    return balance, user_id

@bot.tree.command(name="saldo", description="Revisa tu saldo de monedas.")
async def saldo(interaction: discord.Interaction):
    user_data = db.get_user(interaction.user.id)
    balance = user_data["balance"]
    await interaction.response.send_message(f"🪙 {interaction.user.mention}, tu saldo actual es de **{balance}** monedas.")

@bot.tree.command(name="diario", description="Recoge tu recompensa diaria de monedas.")
async def diario(interaction: discord.Interaction):
    user_id = interaction.user.id
    user_data = db.get_user(user_id)
    now = datetime.datetime.now()

    if user_data["last_daily"]:
        last_claim = datetime.datetime.fromisoformat(user_data["last_daily"])
        time_since_claim = now - last_claim
        if time_since_claim.total_seconds() < 86400:
            remaining_time = datetime.timedelta(seconds=86400) - time_since_claim
            hours, remainder = divmod(int(remaining_time.total_seconds()), 3600)
            minutes, _ = divmod(remainder, 60)
            await interaction.response.send_message(f"¡Hey! Ya recogiste tu premio diario. Vuelve en **{hours}h {minutes}m**.", ephemeral=True)
            return

    new_balance = user_data["balance"] + DAILY_AMOUNT
    db.update_user(user_id, balance=new_balance, last_daily=now.isoformat())

    await interaction.response.send_message(f"🎉 ¡Has recibido **{DAILY_AMOUNT}** monedas! Tu nuevo saldo es **{new_balance}**.")

@bot.tree.command(name="tragamonedas", description="Juega a las tragamonedas y prueba tu suerte.")
async def tragamonedas(interaction: discord.Interaction, apuesta: int):
    balance, user_id = await validate_bet(interaction, apuesta)
    if balance is None:
        return

    embed = Embed(title="🎰 Tragamonedas 🎰", description="¡Girando los rodillos...!", color=discord.Color.gold())
    embed.set_image(url="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbjltNXE1MzNtZXV3Mmx2NTk3cHF2dzczY2xrdjhmMzU2OXBzMWh1ZCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/CF2RZkG4nq6hG/giphy.gif")
    await interaction.response.send_message(embed=embed)

    await asyncio.sleep(3)

    emojis = ["🍒", "🍊", "🍋", "🍇", "🔔", "💎"]
    reels = [random.choice(emojis) for _ in range(3)]
    result_text = f"**[ {reels[0]} | {reels[1]} | {reels[2]} ]**"

    current_balance = balance - apuesta
    winnings = 0

    if reels[0] == reels[1] == reels[2]:
        if reels[0] == "💎":
            winnings = apuesta * 10
        else:
            winnings = apuesta * 5
    elif reels[0] == reels[1] or reels[1] == reels[2]:
        winnings = apuesta * 2

    final_embed = Embed(title="🎰 Tragamonedas 🎰", color=discord.Color.gold())
    final_embed.add_field(name="Resultado", value=result_text, inline=False)

    if winnings > 0:
        current_balance += winnings
        final_embed.description = f"¡Felicidades, {interaction.user.mention}! ¡Has ganado **{winnings}** monedas!"
        final_embed.color = discord.Color.green()
    else:
        final_embed.description = f"Mejor suerte para la próxima, {interaction.user.mention}. Has perdido tu apuesta."
        final_embed.color = discord.Color.red()

    db.update_user(user_id, balance=current_balance)
    final_embed.set_footer(text=f"Apostaste: {apuesta} | Tu nuevo saldo: {current_balance}")

    await interaction.edit_original_response(embed=final_embed)

@bot.tree.command(name="moneda", description="Apuesta en un clásico cara o cruz.")
@app_commands.choices(eleccion=[
    app_commands.Choice(name="Cara", value="cara"),
    app_commands.Choice(name="Cruz", value="cruz"),
])
async def moneda(interaction: discord.Interaction, apuesta: int, eleccion: app_commands.Choice[str]):
    balance, user_id = await validate_bet(interaction, apuesta)
    if balance is None:
        return

    embed = Embed(title="🪙 Cara o Cruz 🪙", description="¡Lanzando la moneda al aire!", color=discord.Color.blue())
    embed.set_image(url="https://media.tenor.com/images/c3b990b0b9b33d2195a547ee7a3ccc3a/tenor.gif")
    await interaction.response.send_message(embed=embed)

    await asyncio.sleep(3)

    opciones = ["cara", "cruz"]
    resultado = random.choice(opciones)
    
    final_embed = Embed(title="🪙 Cara o Cruz 🪙")
    final_embed.add_field(name="Tu elección", value=eleccion.name, inline=True)
    final_embed.add_field(name="Resultado", value=resultado.capitalize(), inline=True)

    if eleccion.value == resultado:
        new_balance = balance + apuesta
        final_embed.description = f"¡Felicidades! Ha salido **{resultado}**. ¡Has ganado **{apuesta}** monedas!"
        final_embed.color = discord.Color.green()
    else:
        new_balance = balance - apuesta
        final_embed.description = f"¡Oh no! Ha salido **{resultado}**. Has perdido tu apuesta."
        final_embed.color = discord.Color.red()

    db.update_user(user_id, balance=new_balance)
    final_embed.set_footer(text=f"Tu nuevo saldo es: {new_balance}")
    await interaction.edit_original_response(embed=final_embed)

@bot.tree.command(name="clasificacion", description="Muestra a los 10 usuarios más ricos del casino.")
async def clasificacion(interaction: discord.Interaction):
    leaderboard_data = db.get_leaderboard(10)
    
    embed = Embed(title="🏆 Clasificación del Casino 🏆", color=discord.Color.gold())
    
    if not leaderboard_data:
        embed.description = "Aún no hay nadie en la clasificación. ¡Sé el primero!"
        await interaction.response.send_message(embed=embed)
        return

    description = ""
    for i, row in enumerate(leaderboard_data):
        user_id = row['user_id']
        balance = row['balance']
        user = interaction.guild.get_member(user_id)
        user_name = user.display_name if user else f"Usuario ({user_id})"
        
        medals = {0: "🥇", 1: "🥈", 2: "🥉"}
        medal = medals.get(i, f"**{i+1}.**")
        description += f"{medal} {user_name} - `{balance}` monedas\n"
        
    embed.description = description
    await interaction.response.send_message(embed=embed)

# --- Lógica de Blackjack ---
suits = ['♠️', '♥️', '♦️', '♣️']
ranks = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}

def create_deck():
    deck = [{'rank': rank, 'suit': suit} for rank in ranks for suit in suits]
    random.shuffle(deck)
    return deck

def hand_value(hand):
    value = sum(ranks[card['rank']] for card in hand)
    num_aces = sum(1 for card in hand if card['rank'] == 'A')
    while value > 21 and num_aces:
        value -= 10
        num_aces -= 1
    return value

def hand_to_string(hand):
    return ' '.join([f"`{card['rank']}{card['suit']}`" for card in hand])

class BlackjackView(ui.View):
    def __init__(self, *, interaction: discord.Interaction, apuesta: int):
        super().__init__(timeout=180.0)
        self.interaction = interaction
        self.apuesta = apuesta
        self.deck = create_deck()
        self.player_hand = [self.deck.pop(), self.deck.pop()]
        selfdealer_hand = [self.deck.pop(), self.deck.pop()]

    async def end_game(self, embed: Embed):
        for item in self.children:
            item.disabled = True
        await self.interaction.edit_original_response(embed=embed, view=self)
        self.stop()

    async def check_winner(self, player_value, dealer_value):
        user_id = self.interaction.user.id
        balance = db.get_user(user_id)['balance']
        
        embed = self.build_embed(game_over=True)

        if player_value > 21:
            new_balance = balance - self.apuesta
            embed.description = f"¡Te pasaste de 21! Pierdes **{self.apuesta}** monedas."
            embed.color = discord.Color.red()
        elif dealer_value > 21 or player_value > dealer_value:
            new_balance = balance + self.apuesta
            embed.description = f"¡Ganaste! Recibes **{self.apuesta}** monedas."
            embed.color = discord.Color.green()
        elif player_value < dealer_value:
            new_balance = balance - self.apuesta
            embed.description = f"El crupier gana. Pierdes **{selfapuesta}** monedas."
            embed.color = discord.Color.red()
        else:
            new_balance = balance
            embed.description = "¡Empate! Recuperas tu apuesta."
            embed.color = discord.Color.light_grey()

        db.update_user(user_id, balance=new_balance)
        embed.set_footer(text=f"Apuesta: {self.apuesta} | Nuevo saldo: {new_balance}")
        await self.end_game(embed)

    def build_embed(self, game_over=False):
        player_value = hand_value(self.player_hand)
        dealer_value = hand_value(self.dealer_hand)
        
        embed = Embed(title="🃏 Blackjack 🃏", color=discord.Color.dark_blue())
        embed.add_field(name=f"Tu mano ({player_value})", value=hand_to_string(self.player_hand), inline=False)
        
        if game_over:
            embed.add_field(name=f"Mano del crupier ({dealer_value})", value=hand_to_string(self.dealer_hand), inline=False)
        else:
            embed.add_field(name=f"Mano del crupier ({ranks[self.dealer_hand[0]['rank']]})", value=f"{hand_to_string([self.dealer_hand[0]])} `?`", inline=False)
        
        return embed

    @ui.button(label="Pedir Carta", style=discord.ButtonStyle.primary, emoji="➕")
    async def hit(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.defer()
        self.player_hand.append(self.deck.pop())
        player_value = hand_value(self.player_hand)
        
        if player_value >= 21:
            await self.stand(interaction, button)
        else:
            embed = self.build_embed()
            await self.interaction.edit_original_response(embed=embed, view=self)

    @ui.button(label="Plantarse", style=discord.ButtonStyle.success, emoji="✋")
    async def stand(self, interaction: discord.Interaction, button: ui.Button):
        if interaction.type == discord.InteractionType.component:
            await interaction.response.defer()

        player_value = hand_value(self.player_hand)
        if player_value > 21:
            await self.check_winner(player_value, 0)
            return

        while hand_value(self.dealer_hand) < 17:
            self.dealer_hand.append(self.deck.pop())
        
        dealer_value = hand_value(self.dealer_hand)
        await self.check_winner(player_value, dealer_value)

@bot.tree.command(name="blackjack", description="Juega una partida de Blackjack.")
async def blackjack(interaction: discord.Interaction, apuesta: int):
    balance, user_id = await validate_bet(interaction, apuesta)
    if balance is None:
        return

    embed = Embed(title="🃏 Blackjack 🃏", description="Barajando las cartas...", color=discord.Color.dark_blue())
    embed.set_image(url="https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExaWt2N2RyeWpxcTVhczJiN2Q3dTF4aXR2Mnd1amh2NzJ0bHp3ZG5zNSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/THIyYnHlVLdXFWqNzG/giphy.gif")
    await interaction.response.send_message(embed=embed)

    await asyncio.sleep(3)

    view = BlackjackView(interaction=interaction, apuesta=apuesta)
    
    player_value = hand_value(view.player_hand)
    if player_value == 21:
        winnings = int(apuesta * 1.5)
        new_balance = balance + winnings
        db.update_user(user_id, balance=new_balance)
        
        embed = view.build_embed(game_over=True)
        embed.description = f"¡BLACKJACK! ¡Ganaste **{winnings}** monedas!"
        embed.color = discord.Color.gold()
        embed.set_footer(text=f"Apuesta: {apuesta} | Nuevo saldo: {new_balance}")
        await interaction.edit_original_response(embed=embed)
        return

    embed = view.build_embed()
    await interaction.edit_original_response(embed=embed, view=view)
   

# --- Lógica de Video Poker ---
poker_ranks = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
VIDEO_POKER_PAYOUTS = {
    "Royal Flush": 800,
    "Straight Flush": 50,
    "Four of a Kind": 25,
    "Full House": 9,
    "Flush": 6,
    "Straight": 4,
    "Three of a Kind": 3,
    "Two Pair": 2,
    "Jacks or Better": 1,
}

def create_poker_deck():
    deck = [{'rank': rank, 'suit': suit} for rank in poker_ranks for suit in suits]
    random.shuffle(deck)
    return deck

def get_hand_rank(hand):
    if not hand: return "Nothing"
    
    poker_ranks_in_hand = sorted([poker_ranks[card['rank']] for card in hand])
    suits_in_hand = [card['suit'] for card in hand]
    
    is_flush = len(set(suits_in_hand)) == 1
    
    # Straight check
    is_straight = (len(set(poker_ranks_in_hand)) == 5 and (poker_ranks_in_hand[4] - poker_ranks_in_hand[0] == 4))
    # Ace-low straight (A, 2, 3, 4, 5) -> ranks are [2, 3, 4, 5, 14]
    if not is_straight and poker_ranks_in_hand == [2, 3, 4, 5, 14]:
        is_straight = True

    if is_straight and is_flush:
        if poker_ranks_in_hand == [10, 11, 12, 13, 14]:
             return "Royal Flush"
        return "Straight Flush"

    rank_counts = {r: poker_ranks_in_hand.count(r) for r in set(poker_ranks_in_hand)}
    counts = sorted(rank_counts.values(), reverse=True)

    if counts[0] == 4:
        return "Four of a Kind"
    if counts == [3, 2]:
        return "Full House"
    if is_flush:
        return "Flush"
    if is_straight:
        return "Straight"
    if counts[0] == 3:
        return "Three of a Kind"
    if counts == [2, 2, 1]:
        return "Two Pair"
    if counts[0] == 2:
        # Using poker_ranks, J=11, Q=12, K=13, A=14
        pair_rank_value = [r for r, c in rank_counts.items() if c == 2][0]
        if pair_rank_value >= 11:
            return "Jacks or Better"
            
    return "Nothing"

class CardButton(ui.Button):
    def __init__(self, index: int, card: dict):
        super().__init__(style=discord.ButtonStyle.secondary, label=f"{card['rank']}{card['suit']}")
        self.index = index

    async def callback(self, interaction: discord.Interaction):
        self.view.held[self.index] = not self.view.held[self.index]
        self.style = discord.ButtonStyle.success if self.view.held[self.index] else discord.ButtonStyle.secondary
        await interaction.response.edit_message(view=self.view)

class DrawButton(ui.Button):
    def __init__(self):
        super().__init__(label="Repartir", style=discord.ButtonStyle.primary, row=1)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        
        for item in self.view.children:
            item.disabled = True
        
        for i in range(5):
            if not self.view.held[i]:
                self.view.hand[i] = self.view.deck.pop()

        final_hand = self.view.hand
        hand_rank_name = get_hand_rank(final_hand)
        winnings = 0
        if hand_rank_name in VIDEO_POKER_PAYOUTS:
            winnings = self.view.apuesta * VIDEO_POKER_PAYOUTS[hand_rank_name]

        user_id = self.view.interaction.user.id
        user_data = db.get_user(user_id)
        new_balance = user_data['balance'] - self.view.apuesta + winnings

        db.update_user(user_id, balance=new_balance)

        embed = Embed(title="🃏 Video Poker 🃏", color=discord.Color.purple())
        embed.add_field(name="Tu Mano Final", value=hand_to_string(final_hand), inline=False)

        if winnings > 0:
            embed.description = f"¡Felicidades! Tienes **{hand_rank_name}**. ¡Has ganado **{winnings}** monedas!"
            embed.color = discord.Color.green()
        else:
            embed.description = f"No has conseguido una mano ganadora. ¡Mejor suerte la próxima vez!"
            embed.color = discord.Color.red()
        
        embed.set_footer(text=f"Apostaste: {self.view.apuesta} | Nuevo saldo: {new_balance}")

        await self.view.interaction.edit_original_response(embed=embed, view=self.view)
        self.view.stop()

class VideoPokerView(ui.View):
    def __init__(self, *, interaction: discord.Interaction, apuesta: int, deck: list, hand: list):
        super().__init__(timeout=180.0)
        self.interaction = interaction
        self.apuesta = apuesta
        self.deck = deck
        self.hand = hand
        self.held = [False] * 5

        for i in range(5):
            self.add_item(CardButton(i, hand[i]))
        
        self.add_item(DrawButton())

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        await self.interaction.edit_original_response(content="Tiempo de espera agotado.", view=self)

@bot.tree.command(name="videopoker", description="Juega una partida de Video Poker (Jacks or Better).")
async def videopoker(interaction: discord.Interaction, apuesta: int):
    balance, user_id = await validate_bet(interaction, apuesta)
    if balance is None:
        return

    deck = create_poker_deck()
    hand = [deck.pop() for _ in range(5)]

    view = VideoPokerView(interaction=interaction, apuesta=apuesta, deck=deck, hand=hand)
    
    embed = Embed(title="🃏 Video Poker 🃏", description="Elige las cartas que quieres conservar y pulsa 'Repartir'.", color=discord.Color.purple())
    embed.add_field(name="Tu Mano", value=hand_to_string(hand), inline=False)
    
    payout_table = "\n".join([f"**{name}**: {payout}x" for name, payout in VIDEO_POKER_PAYOUTS.items()])
    embed.add_field(name="Tabla de Pagos", value=payout_table, inline=False)
    embed.set_footer(text=f"Apostaste: {apuesta} | Saldo actual: {balance}")

    await interaction.response.send_message(embed=embed, view=view)

@bot.tree.command(name="dados_apuesta", description="Apuesta si la suma de dos dados será alta, baja o 7.")
@app_commands.choices(eleccion=[
    app_commands.Choice(name="Bajo (2-6)", value="bajo"),
    app_commands.Choice(name="Siete (7)", value="siete"),
    app_commands.Choice(name="Alto (8-12)", value="alto"),
])
async def dados_apuesta(interaction: discord.Interaction, apuesta: int, eleccion: app_commands.Choice[str]):
    balance, user_id = await validate_bet(interaction, apuesta)
    if balance is None:
        return

    embed = Embed(title="🎲 Apuesta de Dados 🎲", description="Lanzando los dados...", color=discord.Color.red())
    embed.set_image(url="https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExcDVybHRuZHVzcHFkdHltcHUwYzd1OGh5cm8zMGU2a3I2NWRkbGNwcCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/tJFkuce3fKf4Aw6jRH/giphy.gif")
    await interaction.response.send_message(embed=embed)

    await asyncio.sleep(3)

    dado1 = random.randint(1, 6)
    dado2 = random.randint(1, 6)
    suma = dado1 + dado2

    resultado_real = ""
    if suma < 7:
        resultado_real = "bajo"
    elif suma == 7:
        resultado_real = "siete"
    else:
        resultado_real = "alto"

    final_embed = Embed(title="🎲 Apuesta de Dados 🎲")
    final_embed.add_field(name="Resultado", value=f"Lanzaste un `{dado1}` y un `{dado2}`. ¡La suma es **{suma}**!", inline=False)
    final_embed.add_field(name="Tu elección", value=eleccion.name, inline=True)

    if eleccion.value == resultado_real:
        if eleccion.value == "siete":
            winnings = apuesta * 4
            new_balance = balance + winnings
            final_embed.description = f"¡Increíble! Acertaste al 7. ¡Has ganado **{winnings}** monedas!"
        else:
            winnings = apuesta
            new_balance = balance + winnings
            final_embed.description = f"¡Felicidades! Acertaste. ¡Has ganado **{winnings}** monedas!"
        final_embed.color = discord.Color.green()
    else:
        new_balance = balance - apuesta
        final_embed.description = f"¡Oh no! No acertaste. Has perdido tu apuesta."
        final_embed.color = discord.Color.red()

    db.update_user(user_id, balance=new_balance)
    final_embed.set_footer(text=f"Tu nuevo saldo es: {new_balance}")
    await interaction.edit_original_response(embed=final_embed)

# --- Lógica de Ruleta ---
ROULETTE_NUMBERS = {
    0: '🟢',
    1: '🔴', 2: '⚫', 3: '🔴', 4: '⚫', 5: '🔴', 6: '⚫', 7: '🔴', 8: '⚫', 9: '🔴', 10: '⚫',
    11: '⚫', 12: '🔴', 13: '⚫', 14: '🔴', 15: '⚫', 16: '🔴', 17: '⚫', 18: '🔴', 19: '🔴',
    20: '⚫', 21: '🔴', 22: '⚫', 23: '🔴', 24: '⚫', 25: '🔴', 26: '⚫', 27: '🔴', 28: '⚫',
    29: '⚫', 30: '🔴', 31: '⚫', 32: '🔴', 33: '⚫', 34: '🔴', 35: '⚫', 36: '🔴'
}

ruleta_group = app_commands.Group(name="ruleta", description="Juega a la ruleta del casino.")

async def play_roulette(interaction: discord.Interaction, apuesta: int, did_win_check: callable, prize_multiplier: int, bet_type: str):
    balance, user_id = await validate_bet(interaction, apuesta)
    if balance is None:
        return

    embed = Embed(title="🎡 Ruleta 🎡", description="¡La ruleta está girando!", color=discord.Color.dark_purple())
    embed.set_image(url="https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExMjFkMmQ4YmlmNjFmMWl3bWNkenQ3Mmp4NWd4dDJrb3h3bnhjcWduZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/lDiDLlWv12JAzn6X25/giphy.gif")
    await interaction.response.send_message(embed=embed)

    await asyncio.sleep(4)

    winning_number = random.randint(0, 36)
    winning_color_emoji = ROULETTE_NUMBERS[winning_number]
    
    final_embed = Embed(title="🎡 Ruleta 🎡", description=f"La bola ha caído en... **{winning_number} {winning_color_emoji}**!")

    if did_win_check(winning_number):
        winnings = apuesta * prize_multiplier
        new_balance = balance + winnings
        final_embed.description += f"\n¡Felicidades! Tu apuesta a **{bet_type}** ha ganado. Recibes **{winnings}** monedas."
        final_embed.color = discord.Color.green()
    else:
        new_balance = balance - apuesta
        final_embed.description += f"\n¡Mala suerte! Tu apuesta a **{bet_type}** no ha salido."
        final_embed.color = discord.Color.red()

    db.update_user(user_id, balance=new_balance)
    final_embed.set_footer(text=f"Tu nuevo saldo: {new_balance}")
    await interaction.edit_original_response(embed=final_embed)

@ruleta_group.command(name="numero", description="Apuesta a un número específico (Premio: 35x).")
@app_commands.describe(numero="El número al que quieres apostar (0-36).")
async def ruleta_numero(interaction: discord.Interaction, apuesta: int, numero: app_commands.Range[int, 0, 36]):
    await play_roulette(
        interaction, apuesta,
        did_win_check=lambda res: res == numero,
        prize_multiplier=35,
        bet_type=f"Número {numero}"
    )

@ruleta_group.command(name="color", description="Apuesta a un color (Premio: 1x).")
@app_commands.choices(color=[
    app_commands.Choice(name="Rojo 🔴", value="rojo"),
    app_commands.Choice(name="Negro ⚫", value="negro"),
])
async def ruleta_color(interaction: discord.Interaction, apuesta: int, color: app_commands.Choice[str]):
    color_emoji = '🔴' if color.value == "rojo" else '⚫'
    await play_roulette(
        interaction, apuesta,
        did_win_check=lambda res: res != 0 and ROULETTE_NUMBERS[res] == color_emoji,
        prize_multiplier=1,
        bet_type=color.name
    )

@ruleta_group.command(name="paridad", description="Apuesta a par o impar (Premio: 1x).")
@app_commands.choices(paridad=[
    app_commands.Choice(name="Par", value="par"),
    app_commands.Choice(name="Impar", value="impar"),
])
async def ruleta_paridad(interaction: discord.Interaction, apuesta: int, paridad: app_commands.Choice[str]):
    await play_roulette(
        interaction, apuesta,
        did_win_check=lambda res: res != 0 and (res % 2 == 0 if paridad.value == "par" else res % 2 != 0),
        prize_multiplier=1,
        bet_type=paridad.name
    )

bot.tree.add_command(ruleta_group)

# --- Lógica de Carrera ---
@bot.tree.command(name="carrera", description="Apuesta en una emocionante carrera de animales.")
@app_commands.describe(corredor="Elige el número del corredor por el que quieres apostar.")
async def carrera(interaction: discord.Interaction, apuesta: int, corredor: app_commands.Range[int, 1, 5]):
    balance, user_id = await validate_bet(interaction, apuesta)
    if balance is None:
        return

    racers = ["🐎", "🦓", "🦄", "🦌", "🐫"]
    track_len = 20
    positions = [0] * len(racers)
    
    await interaction.response.send_message("Preparando la carrera...")

    def build_track_string():
        track_str = "🏁\n"
        for i, racer_pos in enumerate(positions):
            progress = '─' * racer_pos
            remaining = '─' * (track_len - racer_pos)
            track_str += f"`{i+1}` {progress}{racers[i]}{remaining}ゴール\n"
        return track_str

    while max(positions) < track_len:
        await interaction.edit_original_response(content=f"**¡La carrera ha comenzado!**\n{build_track_string()}")
        await asyncio.sleep(2)
        for i in range(len(racers)):
            positions[i] += random.randint(1, 3)

    winner_index = positions.index(max(positions))
    
    embed = Embed(title="🏁 ¡Carrera Terminada! 🏁", description=f"**¡El ganador es el corredor número {winner_index + 1}: {racers[winner_index]}!**\n\n{build_track_string()}", color=discord.Color.blue())
    embed.set_image(url="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbjltNXE1MzNtZXV3Mmx2NTk3cHF2dzczY2xrdjhmMzU2OXBzMWh1ZCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/5Wi5Ccpvv0dJQ4BE3p/giphy.gif")

    if (corredor - 1) == winner_index:
        winnings = apuesta * (len(racers) - 1)
        new_balance = balance + winnings
        embed.description += f"\n\n¡Felicidades! ¡Has ganado **{winnings}** monedas!"
        embed.color = discord.Color.green()
    else:
        new_balance = balance - apuesta
        embed.description += f"\n\n¡Mala suerte! No has acertado el ganador."
        embed.color = discord.Color.red()

    db.update_user(user_id, balance=new_balance)
    embed.set_footer(text=f"Tu nuevo saldo: {new_balance}")
    await interaction.edit_original_response(content=None, embed=embed)

#repetir mensaje
@bot.tree.command(name="repetir", description="Repite tu mensaje")
async def repetir(interaction: discord.Interaction, mensaje: str):
    await interaction.response.send_message(mensaje)
#evento de inicio en cmd (el placer en forma pura)
# python index.py



@bot.event
async def on_ready():  
    await bot.tree.sync()
    print(f"¡{BOT_NAME} está en línea y listo para la acción!")
    print(f"Conectado como {bot.user}")
    print("Slash commands sincronizados.")

bot.run(TOKEN)