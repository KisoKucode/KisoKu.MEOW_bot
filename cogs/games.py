import discord
from discord.ext import commands
from discord import app_commands, Embed
import random
from DB.user_dao import UserDAO

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot1e
        self.user_dao = UserDAO()
        self.hangman_games = {}  # {channel_id: game_data}
        self.words = ["python", "discord", "programacion", "servidor", "casino", "aventura", "codigo", "teclado", "monitor", "algoritmo", "desarrollador", "meow"]
        self.stages = [
            "```\n +---+\n     |\n     |\n     |\n     |\n     |\n=========\n```",
            "```\n +---+\n O   |\n     |\n     |\n     |\n     |\n=========\n```",
            "```\n +---+\n O   |\n |   |\n     |\n     |\n     |\n=========\n```",
            "```\n +---+\n O   |\n/|   |\n     |\n     |\n     |\n=========\n```",
            "```\n +---+\n O   |\n/|\\  |\n     |\n     |\n     |\n=========\n```",
            "```\n +---+\n O   |\n/|\\  |\n/    |\n     |\n     |\n=========\n```",
            "```\n +---+\n O   |\n/|\\  |\n/ \\  |\n     |\n     |\n=========\n```"
            r"```+---+"+"\n"+r"    |"+"\n"+r"    |"+"\n"+r"    |"+"\n"+r"    |"+"\n"+r"========="+r"```",
            r"```+---+"+"\n"+r"O   |"+"\n"+r"    |"+"\n"+r"    |"+"\n"+r"    |"+"\n"+r"========="+r"```",
            r"```+---+"+"\n"+r"O   |"+"\n"+r"|   |"+"\n"+r"    |"+"\n"+r"    |"+"\n"+r"========="+r"```",
            r"```+---+"+"\n"+r"O   |"+"\n"+r"/|  |"+"\n"+r"    |"+"\n"+r"    |"+"\n"+r"========="+r"```",
            r"```+---+"+"\n"+r"O   |"+"\n"+r"/|\ |"+"\n"+r"    |"+"\n"+r"    |"+"\n"+r"========="+r"```",
            r"```+---+"+"\n"+r"O   |"+"\n"+r"/|\ |"+"\n"+r"/   |"+"\n"+r"    |"+"\n"+r"========="+r"```",
            r"```+---+"+"\n"+r"O   |"+"\n"+r"/|\ |"+"\n"+r"/ \ |"+"\n"+r"    |"+"\n"+r"========="+r"```"
        ]

    def get_hangman_embed(self, game):
        word_display = " ".join([c if c in game['guessed'] else "_" for c in game['word']])
        tried = ", ".join(game['tried']) or "Ninguna"
        
        embed = Embed(title="🎮 Mini-Juego: Horcado", color=discord.Color.blue())
        embed.add_field(name="Palabra", value=f"**`{word_display}`**", inline=False)
        embed.add_field(name="Palabra", value=f"```\n{word_display}\n```", inline=False)
        embed.add_field(name="Estado", value=self.stages[game['attempts']], inline=True)
        embed.add_field(name="Letras intentadas", value=f"{tried}", inline=True)
        embed.add_field(name="Letras intentadas", value=f"`{tried}`", inline=True)
        embed.set_footer(text=f"Vidas restantes: {len(self.stages) - 1 - game['attempts']}")
        return embed

    @app_commands.command(name="horcado", description="Inicia o juega una partida de horcado en este canal.")
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
                user_data = self.user_dao.find_or_create(interaction.user.id)
                reward = 150
                self.user_dao.update(interaction.user.id, balance=user_data['balance'] + reward)
                reward = 200
                new_balance = user_data['balance'] + reward
                self.user_dao.update(interaction.user.id, balance=new_balance)
                
                embed = self.get_hangman_embed(game)
                embed.title = "🎉 ¡Victoria!"
                embed.color = discord.Color.green()
                embed.description = f"{interaction.user.mention} adivinó la palabra y ganó **{reward}** monedas."
                embed.description = f"{interaction.user.mention} adivinó la palabra **{game['word'].upper()}**.\nGanaste: **{reward}** 🪙\nNuevo saldo: `{new_balance}`"
                
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