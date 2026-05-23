from discord import Interaction
import discord
from src.utils.db import get_db_connection
from src.utils.embed import set_bot_footer
from src.utils.reactions import EGGS


async def register(bot):
    @bot.tree.command(name="discoveries", description="Voir tes découvertes secrètes.")
    async def discoveries(interaction: Interaction):
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute(
            "SELECT egg_key FROM discoveries WHERE user_id = %s",
            (interaction.user.id,)
        )
        found_keys = {row[0] for row in cursor.fetchall()}
        cursor.close()
        db.close()

        total = len(EGGS)
        count = len(found_keys)

        if count == 0:
            embed = discord.Embed(
                title="🔍 Découvertes",
                description="Tu n'as encore rien trouvé. Il y a des secrets cachés quelque part...",
                color=discord.Color.dark_grey()
            )
            set_bot_footer(embed, interaction)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        lines = []
        for key, name in EGGS.items():
            if key in found_keys:
                lines.append(f"🏆 **{name}**")
                lines.append("")

        lines.append(f"*{count}/{total} trouvé(s)*")
        lines.append("-# Pour plus d'indices va voir L'Hibiscus.")

        embed = discord.Embed(
            title="🔍 Découvertes",
            description="\n".join(lines),
            color=discord.Color.gold()
        )
        set_bot_footer(embed, interaction)
        await interaction.response.send_message(embed=embed, ephemeral=True)
