import discord
from discord.ext import commands
from discord import app_commands, Embed
from DB.user_dao import UserDAO

# --- Configuración de la Tienda ---
# Define aquí los roles y sus precios.
# IMPORTANTE: Los nombres deben coincidir EXACTAMENTE con los roles en tu servidor de Discord.
SHOP_ITEMS = {
    "VIP": 1000,
    "Veterano": 2500,
    "Magnate": 10000,
    "Coleccionista": 5000
}

class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_dao = UserDAO()

    @app_commands.command(name="tienda", description="Muestra los roles disponibles para comprar.")
    async def tienda(self, interaction: discord.Interaction):
        embed = Embed(title="🛒 Tienda de Roles 🛒", description="¡Gasta tus monedas ganadas con esfuerzo!", color=discord.Color.magenta())
        
        for role_name, price in SHOP_ITEMS.items():
            embed.add_field(name=f"✨ {role_name}", value=f"💰 `{price}` monedas", inline=True)
            
        embed.set_footer(text="Usa /comprar <item> para adquirir un rol.")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="comprar", description="Compra un rol de la tienda.")
    @app_commands.choices(item=[
        app_commands.Choice(name=f"{name} ({price} monedas)", value=name)
        for name, price in SHOP_ITEMS.items()
    ])
    async def comprar(self, interaction: discord.Interaction, item: app_commands.Choice[str]):
        role_name = item.value
        price = SHOP_ITEMS.get(role_name)
        
        if not price:
            await interaction.response.send_message("Ese artículo no existe.", ephemeral=True)
            return

        # 1. Verificar saldo
        user_id = interaction.user.id
        user_data = self.user_dao.find_or_create(user_id)
        current_balance = user_data['balance']

        if current_balance < price:
            await interaction.response.send_message(f"🚫 No tienes suficientes monedas. Tienes `{current_balance}`, necesitas `{price}`.", ephemeral=True)
            return

        # 2. Verificar si el rol existe en el servidor
        role = discord.utils.get(interaction.guild.roles, name=role_name)
        if not role:
            await interaction.response.send_message(f"⚠️ El rol **{role_name}** no existe en este servidor. Contacta al administrador.", ephemeral=True)
            return

        # 3. Verificar si ya tiene el rol
        if role in interaction.user.roles:
            await interaction.response.send_message(f"✅ ¡Ya tienes el rol **{role_name}**!", ephemeral=True)
            return

        # 4. Procesar la compra
        try:
            await interaction.user.add_roles(role)
            
            new_balance = current_balance - price
            self.user_dao.update(user_id, balance=new_balance)
            
            await interaction.response.send_message(f"🎉 ¡Compra exitosa! Ahora tienes el rol **{role.mention}**. Tu nuevo saldo es `{new_balance}`.")
            
        except discord.Forbidden:
            await interaction.response.send_message("❌ No tengo permisos para asignar roles. Asegúrate de que mi rol (el del bot) esté por encima del rol que intentas comprar en la lista de roles del servidor.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Ocurrió un error inesperado: {str(e)}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Shop(bot))