import discord
from discord.ext import commands
from discord import app_commands, Embed
import random
import datetime
from DB.user_dao import UserDAO
from config import BOT_NAME

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_dao = UserDAO()

    def get_cooldown(self, last_time, seconds_needed):
        if not last_time:
            return None
        
        now = datetime.datetime.now(datetime.timezone.utc)
        # Asegurar que last_time tenga zona horaria
        if last_time.tzinfo is None:
             last_time = last_time.replace(tzinfo=datetime.timezone.utc)
             
        diff = now - last_time
        if diff.total_seconds() < seconds_needed:
            return seconds_needed - int(diff.total_seconds())
        return None

    @app_commands.command(name="trabajar", description="Realiza un trabajo honesto para ganar monedas.")
    async def trabajar(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        user_data = self.user_dao.find_or_create(user_id)
        
        # Cooldown de 1 hora (3600 segundos)
        cd = self.get_cooldown(user_data['last_work'], 3600)
        if cd:
            minutes, seconds = divmod(cd, 60)
            await interaction.response.send_message(f"😓 Estás cansado. Puedes volver a trabajar en **{minutes}m {seconds}s**.", ephemeral=True)
            return

        earnings = random.randint(50, 200)
        jobs = [
            f"Ayudaste a {BOT_NAME} a limpiar el servidor.",
            "Programaste una nueva función para el bot.",
            "Vendiste limonada virtual.",
            "Trabajaste de moderador temporal.",
            "Paseaste a los perros del vecindario."
        ]
        job_desc = random.choice(jobs)

        new_balance = user_data['balance'] + earnings
        self.user_dao.update(user_id, balance=new_balance, last_work=datetime.datetime.now(datetime.timezone.utc))

        embed = Embed(title="💼 Trabajo Terminado", description=f"{job_desc}\n¡Has ganado **{earnings}** monedas!", color=discord.Color.green())
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="crimen", description="Intenta cometer un crimen. Alto riesgo, alta recompensa.")
    async def crimen(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        user_data = self.user_dao.find_or_create(user_id)

        # Cooldown de 3 horas
        cd = self.get_cooldown(user_data['last_crime'], 10800)
        if cd:
            hours, remainder = divmod(cd, 3600)
            minutes, _ = divmod(remainder, 60)
            await interaction.response.send_message(f"🚓 La policía te está vigilando. Inténtalo de nuevo en **{hours}h {minutes}m**.", ephemeral=True)
            return

        chance = random.randint(1, 100)
        current_balance = user_data['balance']

        if chance > 60: # 40% de éxito
            earnings = random.randint(300, 800)
            new_balance = current_balance + earnings
            msg = f"😈 ¡Éxito! Robaste un banco virtual y escapaste con **{earnings}** monedas."
            color = discord.Color.dark_red()
        else: # 60% de fallo
            fine = random.randint(100, 300)
            # No dejar saldo negativo, máximo quitar lo que tiene
            fine = min(fine, current_balance)
            new_balance = current_balance - fine
            msg = f"🚔 ¡Te atraparon! Tuviste que pagar una fianza de **{fine}** monedas."
            color = discord.Color.greyple()

        self.user_dao.update(user_id, balance=new_balance, last_crime=datetime.datetime.now(datetime.timezone.utc))
        
        embed = Embed(description=msg, color=color)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="banco", description="Muestra tu saldo en la billetera y en el banco.")
    async def banco(self, interaction: discord.Interaction):
        user_data = self.user_dao.find_or_create(interaction.user.id)
        wallet = user_data['balance']
        bank = user_data.get('bank', 0) or 0
        net_worth = wallet + bank

        embed = Embed(title=f"🏦 Finanzas de {interaction.user.display_name}", color=discord.Color.gold())
        embed.add_field(name="👛 Billetera", value=f"{wallet}", inline=True)
        embed.add_field(name="💳 Banco", value=f"{bank}", inline=True)
        embed.add_field(name="💰 Valor Neto", value=f"{net_worth}", inline=False)
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="depositar", description="Deposita dinero de tu billetera al banco.")
    async def depositar(self, interaction: discord.Interaction, cantidad: int):
        user_id = interaction.user.id
        user_data = self.user_dao.find_or_create(user_id)
        wallet = user_data['balance']
        bank = user_data.get('bank', 0) or 0

        if cantidad <= 0:
            await interaction.response.send_message("La cantidad debe ser positiva.", ephemeral=True)
            return

        if wallet < cantidad:
            await interaction.response.send_message(f"No tienes suficiente dinero en la billetera. Tienes {wallet}.", ephemeral=True)
            return

        new_wallet = wallet - cantidad
        new_bank = bank + cantidad
        
        self.user_dao.update(user_id, balance=new_wallet, bank=new_bank)
        await interaction.response.send_message(f"✅ Has depositado **{cantidad}** monedas en el banco.")

    @app_commands.command(name="retirar", description="Retira dinero del banco a tu billetera.")
    async def retirar(self, interaction: discord.Interaction, cantidad: int):
        user_id = interaction.user.id
        user_data = self.user_dao.find_or_create(user_id)
        wallet = user_data['balance']
        bank = user_data.get('bank', 0) or 0

        if cantidad <= 0:
            await interaction.response.send_message("La cantidad debe ser positiva.", ephemeral=True)
            return

        if bank < cantidad:
            await interaction.response.send_message(f"No tienes suficiente dinero en el banco. Tienes {bank}.", ephemeral=True)
            return

        new_wallet = wallet + cantidad
        new_bank = bank - cantidad
        
        self.user_dao.update(user_id, balance=new_wallet, bank=new_bank)
        await interaction.response.send_message(f"✅ Has retirado **{cantidad}** monedas del banco.")

    @app_commands.command(name="robar", description="Intenta robar la billetera de otro usuario.")
    async def robar(self, interaction: discord.Interaction, victima: discord.Member):
        if victima.id == interaction.user.id:
            await interaction.response.send_message("No puedes robarte a ti mismo.", ephemeral=True)
            return

        if victima.bot:
             await interaction.response.send_message("No puedes robar a los bots (tienen seguridad avanzada).", ephemeral=True)
             return

        ladron_data = self.user_dao.find_or_create(interaction.user.id)
        victima_data = self.user_dao.find_or_create(victima.id)

        # Cooldown para robar (por ejemplo, 2 horas)
        cd = self.get_cooldown(ladron_data['last_crime'], 7200)
        if cd:
             minutes, _ = divmod(cd, 60)
             await interaction.response.send_message(f"Necesitas esperar **{minutes}** minutos antes de cometer otro crimen.", ephemeral=True)
             return

        victima_wallet = victima_data['balance']
        if victima_wallet < 50:
            await interaction.response.send_message(f"{victima.display_name} es demasiado pobre para robarle. ¡Ten piedad!", ephemeral=True)
            return

        success_chance = random.randint(1, 100)
        
        if success_chance > 70: # 30% éxito
            steal_amount = random.randint(10, int(victima_wallet * 0.5)) # Robar hasta el 50%
            
            self.user_dao.update(interaction.user.id, balance=ladron_data['balance'] + steal_amount, last_crime=datetime.datetime.now(datetime.timezone.utc))
            self.user_dao.update(victima.id, balance=victima_wallet - steal_amount)
            
            await interaction.response.send_message(f"🕵️‍♂️ ¡Le has robado **{steal_amount}** monedas a {victima.mention}!")
        else:
            fine = 200
            fine = min(fine, ladron_data['balance'])
            self.user_dao.update(interaction.user.id, balance=ladron_data['balance'] - fine, last_crime=datetime.datetime.now(datetime.timezone.utc))
            
            await interaction.response.send_message(f"🚔 ¡Te atraparon intentando robar a {victima.mention}! Pagaste una multa de **{fine}** monedas.")

async def setup(bot):
    await bot.add_cog(Economy(bot))