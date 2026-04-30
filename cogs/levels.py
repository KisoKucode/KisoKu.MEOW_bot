import discord
from discord.ext import commands
from discord import app_commands, Embed
import random
import time
from config import GENERAL_CHANNEL

class Levels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_service = bot.user_service
        self.level_service = bot.level_service
        self._cd = commands.CooldownMapping.from_cooldown(1, 60, commands.BucketType.user) # 1 mensaje cada 60s da XP

    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignorar bots y mensajes fuera de servidores
        if message.author.bot or not message.guild:
            return

        # Chequear cooldown (para que no ganen XP por spam)
        bucket = self._cd.get_bucket(message)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            return

        # Dar XP aleatoria (entre 10 y 25)
        xp_gain = random.randint(10, 25)
        user_id = message.author.id
        result = self.level_service.add_experience(user_id, xp_gain)

        if not result.success:
            # Log the error or handle it silently, as it's a background task
            print(f"Error adding experience for user {user_id}: {result.error}")
            return

        data = result.data or {}
        if data.get('leveled_up'):
            channel = discord.utils.get(message.guild.text_channels, name=GENERAL_CHANNEL)
            if not channel:
                channel = message.channel

            embed = Embed(title="¡Subida de Nivel! 🎉", description=f"¡Felicidades {message.author.mention}!", color=discord.Color.gold())
            embed.add_field(name="Nivel Anterior", value=str(data['previous_level']), inline=True)
            embed.add_field(name="Nuevo Nivel", value=str(data['level']), inline=True)
            embed.set_thumbnail(url=message.author.avatar.url if message.author.avatar else None)
            await channel.send(embed=embed)

    @app_commands.command(name="nivel", description="Muestra tu nivel y experiencia actual")
    async def nivel(self, interaction: discord.Interaction):
        result = self.level_service.get_user_level_info(interaction.user.id)
        
        if not result.success:
            await interaction.response.send_message(result.error, ephemeral=True)
            return

        data = result.data or {}
        embed = Embed(title=f"Nivel de {interaction.user.display_name}", color=discord.Color.blue())
        embed.add_field(name="Nivel", value=f"⭐ {data['level']}", inline=True)
        embed.add_field(name="Experiencia", value=f"{data['xp']} / {data['xp_needed']} XP", inline=True)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Levels(bot))