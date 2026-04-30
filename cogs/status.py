import discord
from discord.ext import commands, tasks
from discord import app_commands, Embed
import datetime
import time
from config import BOT_NAME
import logging

class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.panel_service = bot.panel_service
        self.panel_message = None # Aquí guardaremos el mensaje para editarlo luego
        self.start_time = time.time()
        self.status_loop.start() # Iniciar el bucle de actualización

    def cog_unload(self):
        self.status_loop.cancel()

    def get_uptime(self):
        """Calcula cuánto tiempo lleva encendido el bot."""
        current_time = time.time()
        difference = int(current_time - self.start_time)
        return str(datetime.timedelta(seconds=difference))

    def get_system_art(self):
        """Devuelve un dibujo ASCII del estado."""
        return """
     |\\__/,|   (`\\
   _.|o o  |_   ) )
--(((---(((--------
  [ SYSTEM ONLINE ]
        """

    def build_embed(self):
        """Construye el Embed con los datos actuales."""
        # Calcular estadísticas
        ping = round(self.bot.latency * 1000)
        guilds = len(self.bot.guilds)
        users = sum(g.member_count for g in self.bot.guilds)
        uptime = self.get_uptime()
        
        embed = Embed(title=f"🖥️ Panel de Control - {BOT_NAME}", color=discord.Color.teal())
        embed.description = "```diff\n+ Estado: OPERATIVO\n+ Sistema: ESTABLE\n```"
        
        # Filas de datos
        embed.add_field(name="📶 Latencia", value=f"**{ping}** ms", inline=True)
        embed.add_field(name="⏱️ Actividad", value=f"**{uptime}**", inline=True)
        embed.add_field(name="🛡️ Servidores", value=f"**{guilds}**", inline=True)
        embed.add_field(name="👥 Usuarios Totales", value=f"**{users}**", inline=True)
        
        # Sección visual (El dibujo)
        embed.add_field(name="Monitor", value=f"```\n{self.get_system_art()}\n```", inline=False)
        
        embed.set_footer(text=f"Última actualización: {datetime.datetime.now().strftime('%H:%M:%S')}")
        
        if self.bot.user.avatar:
            embed.set_thumbnail(url=self.bot.user.avatar.url)
            
        return embed

    @tasks.loop(seconds=30)
    async def status_loop(self):
        """Tarea que se ejecuta cada 30 segundos para actualizar el panel."""
        if self.panel_message:
            try:
                embed = self.build_embed()
                await self.panel_message.edit(embed=embed)
            except (discord.NotFound, discord.Forbidden):
                # Si borran el mensaje, dejamos de intentar actualizarlo
                logging.warning("El mensaje del panel no fue encontrado. Limpiando la referencia.")
                self.panel_message = None
                self.panel_service.clear_panel()

    @status_loop.before_loop
    async def before_status_loop(self):
        await self.bot.wait_until_ready()
        # Intentar cargar el panel persistente desde la DB
        panel_data = self.panel_service.get_panel()
        if panel_data:
            try:
                guild = self.bot.get_guild(panel_data['guild_id'])
                if not guild:
                    raise discord.NotFound("Servidor no encontrado")
                
                channel = guild.get_channel(panel_data['channel_id'])
                if not channel:
                    raise discord.NotFound("Canal no encontrado")

                message = await channel.fetch_message(panel_data['message_id'])
                self.panel_message = message
                logging.info(f"Panel de estado persistente encontrado y cargado (Mensaje: {message.id})")
            except (discord.NotFound, discord.Forbidden) as e:
                logging.warning(f"No se pudo cargar el panel de estado persistente: {e}. Limpiando de la DB.")
                self.panel_service.clear_panel()

    @app_commands.command(name="panel_estado", description="Crea un panel de estado que se actualiza en tiempo real.")
    async def panel_estado(self, interaction: discord.Interaction):
        # Verificar permisos (Opcional: solo administradores)
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ Necesitas permisos de administrador para crear el panel.", ephemeral=True)
            return

        if self.panel_message:
            await interaction.response.send_message("⚠️ Ya existe un panel de estado activo. Para crear uno nuevo, primero borra el mensaje del panel anterior.", ephemeral=True)
            return

        embed = self.build_embed()
        await interaction.response.send_message(embed=embed)
        self.panel_message = await interaction.original_response()
        # Guardar la información del nuevo panel en la base de datos
        self.panel_service.save_panel(
            guild_id=interaction.guild.id,
            channel_id=interaction.channel.id,
            message_id=self.panel_message.id
        )

async def setup(bot):
    await bot.add_cog(Status(bot))