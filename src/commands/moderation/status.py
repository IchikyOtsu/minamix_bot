import time
import discord
from discord import Interaction
from src.utils.embed import set_bot_footer

_start_time = time.time()


async def register(bot):
    @bot.tree.command(name="status", description="Afficher le statut et les infos du bot.")
    async def status(interaction: Interaction):
        await interaction.response.defer()

        latency = round(bot.latency * 1000)
        uptime_seconds = int(time.time() - _start_time)
        hours, remainder = divmod(uptime_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        uptime_str = f"{hours}h {minutes}m {seconds}s"

        total_members = sum(g.member_count for g in bot.guilds)

        embed = discord.Embed(
            title=f"📡 Statut — {bot.user.name}",
            color=discord.Color.green() if latency < 200 else discord.Color.orange()
        )
        embed.add_field(name="Ping", value=f"`{latency} ms`", inline=True)
        embed.add_field(name="Uptime", value=f"`{uptime_str}`", inline=True)
        embed.add_field(name="Serveurs", value=f"`{len(bot.guilds)}`", inline=True)
        embed.add_field(name="Membres", value=f"`{total_members}`", inline=True)
        embed.add_field(name="Version discord.py", value=f"`{discord.__version__}`", inline=True)

        if bot.user.avatar:
            embed.set_thumbnail(url=bot.user.avatar.url)

        set_bot_footer(embed, interaction)
        await interaction.followup.send(embed=embed)
