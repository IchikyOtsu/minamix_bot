from discord import Interaction
import discord
from src.utils.embed import set_bot_footer
from src.config import GUILD_IDS


async def register(bot):
    @bot.tree.command(name="servers", description="Afficher les serveurs autorisés (Admin seulement)")
    async def servers(interaction: Interaction):
        if not interaction.user.guild_permissions.administrator:
            embed = discord.Embed(title="❌ Permission refusée", color=discord.Color.red())
            set_bot_footer(embed, interaction)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        lines = []
        for guild_id in GUILD_IDS:
            guild = bot.get_guild(guild_id)
            if guild:
                lines.append(f"✅ **{guild.name}** (`{guild_id}`)")
            else:
                lines.append(f"⚠️ Serveur inconnu (`{guild_id}`)")

        embed = discord.Embed(
            title="🔒 Serveurs autorisés",
            description="\n".join(lines),
            color=discord.Color.blurple()
        )
        set_bot_footer(embed, interaction)
        await interaction.response.send_message(embed=embed, ephemeral=True)
