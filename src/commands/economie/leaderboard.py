from discord import Interaction, Embed
import discord
from src.utils.db import get_db_connection


async def register(bot):
    @bot.tree.command(name="leaderboard", description="Top 10 des utilisateurs les plus riches.")
    async def leaderboard(interaction: Interaction):
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute(
            "SELECT user_id, balance FROM wallets ORDER BY balance DESC LIMIT 10"
        )
        rows = cursor.fetchall()
        db.close()

        if not rows:
            await interaction.response.send_message("Aucun utilisateur enregistré.", ephemeral=True)
            return

        medals = {1: "🥇", 2: "🥈", 3: "🥉"}
        lines = []
        for rank, (user_id, balance) in enumerate(rows, start=1):
            prefix = medals.get(rank, f"`#{rank}`")
            lines.append(f"{prefix} <@{user_id}> — **{balance}💰**")

        embed = Embed(
            title="🏆 Leaderboard",
            description="\n".join(lines),
            color=discord.Color.gold()
        )
        embed.set_footer(text="Système d'économie")
        await interaction.response.send_message(embed=embed)
