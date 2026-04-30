import discord
from discord.ext import commands
from discord import app_commands, Embed
import random

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_service = bot.user_service
        self.hangman_service = bot.hangman_service
        self.hangman_games = {}  # {channel_id: game_data}
        self.words = ["python", "discord", "programacion", "servidor", "casino", "aventura", "codigo", "teclado", "monitor", "algoritmo", "desarrollador", "meow"]
        self.stages = [
            "```\n +---+\n     |\n     |\n     |\n     |\n     |\n=========\n```", # 0 attempts
            "```\n +---+\n O   |\n     |\n     |\n     |\n     |\n=========\n```", # 1 attempt (head)
            "```\n +---+\n O   |\n |   |\n     |\n     |\n     |\n=========\n```", # 2 attempts (body)
            "```\n +---+\n O   |\n/|   |\n     |\n     |\n     |\n=========\n```", # 3 attempts (left arm)
            "```\n +---+\n O   |\n/|\\  |\n     |\n     |\n     |\n=========\n```", # 4 attempts (right arm)
            "```\n +---+\n O   |\n/|\\  |\n/    |\n     |\n     |\n=========\n```", # 5 attempts (left leg)
            "```\n +---+\n O   |\n/|\\  |\n/ \\  |\n     |\n     |\n=========\n```"  # 6 attempts (right leg - game over)
        ]
    def get_hangman_embed(self, game):
        word_display = " ".join([c if c in game['guessed'] else "_" for c in game['word']])
        tried = ", ".join(game['tried']) or "Ninguna"
        
        embed = Embed(title="🎮 Mini-Juego: Horcado", color=discord.Color.blue())
        embed.add_field(name="Palabra", value=f"```\n{word_display}\n```", inline=False)
        embed.add_field(name="Letras intentadas", value=f"`{tried}`", inline=True)
        embed.add_field(name="Estado", value=self.stages[game['attempts']], inline=False)
        embed.set_footer(text=f"Vidas restantes: {len(self.stages) - 1 - game['attempts']}")
        return embed

    @app_commands.command(name="mini_horcado", description="Inicia o juega una partida de horcado en modo alternativo.")
    @app_commands.describe(letra="La letra que quieres intentar adivinar")
    async def horcado(self, interaction: discord.Interaction, letra: str = None):
        channel_id = interaction.channel_id
        
        if channel_id not in self.hangman_games:
            word = random.choice(self.words).lower()
            self.hangman_games[channel_id] = {
                'word': word,
                'guessed': [],
                'tried': [],
                'attempts': 0
            }
            await interaction.response.send_message("🏁 ¡Nuevo juego de Horcado iniciado!", embed=self.get_hangman_embed(self.hangman_games[channel_id]))
            return

        game = self.hangman_games[channel_id]
        if not letra:
            await interaction.response.send_message("Ya hay una partida activa. Usa `/horcado letra:<letra>`", embed=self.get_hangman_embed(game), ephemeral=True)
            return

        letra = letra.lower().strip()
        if not letra:
            await interaction.response.send_message("❌ Debes proporcionar una letra.", ephemeral=True)
            return
            
        if len(letra) != 1 or not letra.isalpha():
            await interaction.response.send_message("❌ Introduce una única letra válida.", ephemeral=True)
            return

        if letra in game['tried'] or letra in game['guessed']:
            await interaction.response.send_message(f"⚠️ La letra `{letra}` ya se intentó.", ephemeral=True)
            return

        if letra in game['word']:
            game['guessed'].append(letra)
            if all(c in game['guessed'] for c in game['word']):
                reward = 200
                reward_result = self.hangman_service.reward_for_win(interaction.user.id, reward)
                if not reward_result.success:
                    await interaction.response.send_message(reward_result.error, ephemeral=True)
                    return

                balance = reward_result.data['balance'] if reward_result.data else 'desconocido'
                embed = self.get_hangman_embed(game)
                embed.title = "🎉 ¡Victoria!"
                embed.color = discord.Color.green()
                embed.description = (
                    f"{interaction.user.mention} adivinó la palabra **{game['word'].upper()}**.\n"
                    f"Ganaste: **{reward}** 🪙\nNuevo saldo: `{balance}`"
                )
                
                await interaction.response.send_message(embed=embed)
                del self.hangman_games[channel_id]
                return
        else:
            game['tried'].append(letra)
            game['attempts'] += 1
            if game['attempts'] >= len(self.stages) - 1:
                embed = self.get_hangman_embed(game)
                embed.title = "💀 Game Over"
                embed.color = discord.Color.red()
                embed.description = f"La palabra secreta era: **{game['word'].upper()}**"
                
                await interaction.response.send_message(embed=embed)
                del self.hangman_games[channel_id]
                return

        await interaction.response.send_message(f"Intento: `{letra.upper()}`", embed=self.get_hangman_embed(game))

async def setup(bot):
    await bot.add_cog(Games(bot))