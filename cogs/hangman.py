import discord
from discord.ext import commands
from discord import app_commands, Embed
import random

class Hangman(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_service = bot.user_service
        self.hangman_service = bot.hangman_service
        self.games = {}  # Diccionario para rastrear juegos por canal: {channel_id: game_data}
        self.words = ["python", "discord", "programacion", "servidor", "casino", "aventura", "codigo", "teclado", "monitor", "algoritmo", "desarrollador", "meow"]
        self.stages = [
            """
               +---+
               |   |
                   |
                   |
                   |
                   |
            =========
            """,
            """
               +---+
               |   |
               O   |
                   |
                   |
                   |
            =========
            """,
            """
               +---+
               |   |
               O   |
               |   |
                   |
                   |
            =========
            """,
            """
               +---+
               |   |
               O   |
              /|   |
                   |
                   |
            =========
            """,
            """
               +---+
               |   |
               O   |
              /|\\  |
                   |
                   |
            =========
            """,
            """
               +---+
               |   |
               O   |
              /|\\  |
              /    |
                   |
            =========
            """,
            """
               +---+
               |   |
               O   |
              /|\\  |
              / \\  |
                   |
            =========
            """
        ]

    def get_embed(self, game):
        word_display = " ".join([c if c in game['guessed'] else "_" for c in game['word']])
        tried = ", ".join(game['tried']) or "Ninguna"
        
        embed = Embed(title="🎮 Juego del Horcado", color=discord.Color.blue())
        embed.add_field(name="Palabra", value=f"```\n{word_display}\n```", inline=False)
        embed.add_field(name="Estado", value=f"```\n{self.stages[game['attempts']]}\n```", inline=True)
        embed.add_field(name="Letras intentadas", value=tried, inline=True)
        embed.set_footer(text=f"Vidas restantes: {len(self.stages) - 1 - game['attempts']}")
        return embed

    @app_commands.command(name="horcado", description="Inicia una partida de horcado o adivina una letra.")
    @app_commands.describe(letra="La letra que quieres intentar adivinar")
    async def horcado(self, interaction: discord.Interaction, letra: str = None):
        channel_id = interaction.channel_id
        
        # Iniciar juego si no existe uno en el canal
        if channel_id not in self.games:
            word = random.choice(self.words).lower()
            self.games[channel_id] = {
                'word': word,
                'guessed': [],
                'tried': [],
                'attempts': 0
            }
            await interaction.response.send_message("🏁 ¡Nuevo juego iniciado!", embed=self.get_embed(self.games[channel_id]))
            return

        game = self.games[channel_id]
        if not letra:
            await interaction.response.send_message("Ya hay una partida en curso.", embed=self.get_embed(game), ephemeral=True)
            return

        letra = letra.lower()[0]
        if letra in game['tried'] or letra in game['guessed']:
            await interaction.response.send_message(f"La letra `{letra}` ya ha sido intentada.", ephemeral=True)
            return

        if letra in game['word']:
            game['guessed'].append(letra)
            if all(c in game['guessed'] for c in game['word']):
                reward = 50
                reward_result = self.hangman_service.reward_for_win(interaction.user.id, reward)
                if not reward_result.success:
                    await interaction.response.send_message(reward_result.error, ephemeral=True)
                    return

                balance = reward_result.data['balance'] if reward_result.data else 'desconocido'
                await interaction.response.send_message(
                    f"🎉 ¡Felicidades {interaction.user.mention}! Adivinaste la palabra: **{game['word']}**. Has ganado `{reward}` monedas. Nuevo saldo: `{balance}`"
                )
                del self.games[channel_id]
                return
        else:
            game['tried'].append(letra)
            game['attempts'] += 1
            if game['attempts'] >= len(self.stages) - 1:
                await interaction.response.send_message(f"💀 ¡Game Over! La palabra era **{game['word']}**.")
                del self.games[channel_id]
                return

        await interaction.response.send_message(f"Intentaste con la letra `{letra}`", embed=self.get_embed(game))

async def setup(bot):
    await bot.add_cog(Hangman(bot))