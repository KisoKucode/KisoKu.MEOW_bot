import discord
from discord.ext import commands
from discord import app_commands, Embed
import random
from config import BOT_NAME

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_service = bot.user_service
        self.economy_service = bot.economy_service

    @app_commands.command(name="trabajar", description="Realiza un trabajo honesto para ganar monedas.")
    async def trabajar(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        result = self.economy_service.work(user_id)

        if not result.success:
            await interaction.response.send_message(result.error, ephemeral=True)
            return

        data = result.data or {}
        embed = Embed(title="💼 Trabajo Terminado", description=f"{data['job_desc']}\n¡Has ganado **{data['earnings']}** monedas!", color=discord.Color.green())
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="crimen", description="Intenta cometer un crimen. Alto riesgo, alta recompensa.")
    async def crimen(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        result = self.economy_service.crime(user_id)

        if not result.success:
            await interaction.response.send_message(result.error, ephemeral=True)
            return

        data = result.data or {}
        embed = Embed(description=data['message'], color=data.get('color', discord.Color.greyple()))
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="banco", description="Muestra tu saldo en la billetera y en el banco.")
    async def banco(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        user = self.user_service.find_or_create(user_id)
        wallet = user.balance
        bank = user.bank
        net_worth = wallet + bank

        embed = Embed(title=f"🏦 Finanzas de {interaction.user.display_name}", color=discord.Color.gold())
        embed.add_field(name="👛 Billetera", value=f"{wallet}", inline=True)
        embed.add_field(name="💳 Banco", value=f"{bank}", inline=True)
        embed.add_field(name="💰 Valor Neto", value=f"{net_worth}", inline=False)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="depositar", description="Deposita dinero de tu billetera al banco.")
    async def depositar(self, interaction: discord.Interaction, cantidad: int):
        user_id = interaction.user.id
        result = self.economy_service.deposit(user_id, cantidad)

        if not result.success:
            await interaction.response.send_message(result.error, ephemeral=True)
            return
        await interaction.response.send_message(f"✅ Has depositado **{cantidad}** monedas en el banco.")

    @app_commands.command(name="retirar", description="Retira dinero del banco a tu billetera.")
    async def retirar(self, interaction: discord.Interaction, cantidad: int):
        user_id = interaction.user.id
        result = self.economy_service.withdraw(user_id, cantidad)

        if not result.success:
            await interaction.response.send_message(result.error, ephemeral=True)
            return
        await interaction.response.send_message(f"✅ Has retirado **{cantidad}** monedas del banco.")

    @app_commands.command(name="robar", description="Intenta robar la billetera de otro usuario.")
    async def robar(self, interaction: discord.Interaction, victima: discord.Member):
        if victima.id == interaction.user.id:
            await interaction.response.send_message("No puedes robarte a ti mismo.", ephemeral=True)
            return

        if victima.bot:
            await interaction.response.send_message("No puedes robar a los bots (tienen seguridad avanzada).", ephemeral=True)
            return

        result = self.economy_service.rob(interaction.user.id, victima.id)

        if not result.success:
            await interaction.response.send_message(result.error, ephemeral=True)
            return
        await interaction.response.send_message(result.data['message'])

    @app_commands.command(name="donar", description="Transfiere monedas de tu billetera a otro usuario.")
    @app_commands.describe(beneficiario="El usuario que recibirá las monedas", cantidad="La cantidad de monedas a transferir")
    async def donar(self, interaction: discord.Interaction, beneficiario: discord.Member, cantidad: int):
        if beneficiario.id == interaction.user.id:
            await interaction.response.send_message("❌ No puedes donarte monedas a ti mismo.", ephemeral=True)
            return

        if beneficiario.bot:
            await interaction.response.send_message("❌ No puedes donar monedas a los bots.", ephemeral=True)
            return

        result = self.economy_service.donate(interaction.user.id, beneficiario.id, cantidad)

        if not result.success:
            await interaction.response.send_message(result.error, ephemeral=True)
            return
        embed = Embed(title="💸 Transferencia Exitosa", color=discord.Color.blue(), description=result.data['message'])
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Economy(bot))