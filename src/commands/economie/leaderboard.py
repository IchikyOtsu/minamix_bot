from discord import Interaction, Embed
import discord
from src.utils.db import get_db_connection
from src.utils.format import format_amount
from src.utils.embed import set_bot_footer


async def _resolve_name(bot, guild: discord.Guild, user_id: int) -> str:
    member = guild.get_member(user_id)
    if member:
        return f"@{member.display_name}"
    try:
        user = await bot.fetch_user(user_id)
        return f"@{user.name}"
    except Exception:
        return f"Utilisateur inconnu"


async def register(bot):
    @bot.tree.command(name="leaderboard", description="Top 10 des utilisateurs les plus riches.")
    async def leaderboard(interaction: Interaction):
        await interaction.response.defer()

        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute(
            "SELECT user_id, balance FROM wallets ORDER BY balance DESC LIMIT 10"
        )
        rows = cursor.fetchall()
        cursor.close()
        db.close()

        if not rows:
            await interaction.followup.send("Aucun utilisateur enregistré.", ephemeral=True)
            return

        medals = {1: "🥇", 2: "🥈", 3: "🥉"}
        lines = []
        for rank, (user_id, balance) in enumerate(rows, start=1):
            prefix = medals.get(rank, f"`#{rank}`")
            name = await _resolve_name(bot, interaction.guild, user_id)
            lines.append(f"{prefix} {name} — **{format_amount(balance)}💰**")

        embed = Embed(
            title="🏆 Leaderboard",
            description="\n".join(lines),
            color=discord.Color.gold()
        )
        set_bot_footer(embed, interaction)
        await interaction.followup.send(embed=embed)
