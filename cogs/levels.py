import discord
from discord.ext import commands
from discord import app_commands, Embed
import random
import time
from DB.user_dao import UserDAO
from config import GENERAL_CHANNEL

class Levels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_dao = UserDAO()
        self._cd = commands.CooldownMapping.from_cooldown(1, 60, commands.BucketType.user) # 1 mensaje cada 60s da XP

    def get_xp_for_level(self, level):
        """Fórmula simple: Nivel * 100 de XP necesaria para el siguiente nivel"""
        return level * 100

    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignorar bots y mensajes fuera de servidores
        if message.author.bot or not message.guild:
            return

        # Chequear cooldown (para que no ganen XP por spam)
        bucket = self._cd.get_bucket(message)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            return # Está en cooldown, no gana XP

        # Obtener datos del usuario
        user_id = message.author.id
        user_data = self.user_dao.find_or_create(user_id)
        
        current_xp = user_data['xp'] or 0
        current_level = user_data['level'] or 1

        # Dar XP aleatoria (entre 10 y 25)
        xp_gain = random.randint(10, 25)
        new_xp = current_xp + xp_gain

        # Verificar subida de nivel
        xp_needed = self.get_xp_for_level(current_level)
        
        if new_xp >= xp_needed:
            new_level = current_level + 1
            new_xp = new_xp - xp_needed # Resetear XP o mantener el remanente (estilo RPG)
            
            self.user_dao.update(user_id, xp=new_xp, level=new_level)
            
            # Anunciar subida de nivel
            channel = discord.utils.get(message.guild.text_channels, name=GENERAL_CHANNEL)
            if not channel:
                channel = message.channel # Si no encuentra el canal general, responde donde escribieron
            
            embed = Embed(title="¡Subida de Nivel! 🎉", description=f"¡Felicidades {message.author.mention}!", color=discord.Color.gold())
            embed.add_field(name="Nivel Anterior", value=str(current_level), inline=True)
            embed.add_field(name="Nuevo Nivel", value=str(new_level), inline=True)
            embed.set_thumbnail(url=message.author.avatar.url if message.author.avatar else None)
            
            await channel.send(embed=embed)
        else:
            # Solo actualizar XP sin subir de nivel
            self.user_dao.update(user_id, xp=new_xp)

    @app_commands.command(name="nivel", description="Muestra tu nivel y experiencia actual")
    async def nivel(self, interaction: discord.Interaction):
        user_data = self.user_dao.find_or_create(interaction.user.id)
        lvl = user_data['level'] or 1
        xp = user_data['xp'] or 0
        xp_needed = self.get_xp_for_level(lvl)

        embed = Embed(title=f"Nivel de {interaction.user.display_name}", color=discord.Color.blue())
        embed.add_field(name="Nivel", value=f"⭐ {lvl}", inline=True)
        embed.add_field(name="Experiencia", value=f"{xp} / {xp_needed} XP", inline=True)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Levels(bot))