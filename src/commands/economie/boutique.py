from discord import Interaction, Embed
import discord
from src.utils.db import get_db_connection
from src.utils.format import format_amount
from src.utils.embed import set_bot_footer

async def register(bot):
    @bot.tree.command(
        name="shop",
        description="Affiche la boutique des rôles disponibles."
    )
    async def boutique(interaction: Interaction):
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT role_id, prix, nom, description FROM boutique_roles ORDER BY id")
        items = cursor.fetchall()
        db.close()

        if not items:
            embed = discord.Embed(
                title="🛒 Boutique vide",
                description="La boutique est vide pour le moment.",
                color=discord.Color.orange()
            )
            set_bot_footer(embed, interaction)
            await interaction.response.send_message(embed=embed)
            return

        embed = Embed(
            title="🛍️ Boutique des rôles",
            description="Utilise `/buy <numéro>` pour acheter.",
            color=0x00FFAA
        )

        for num, (role_id, prix, nom, description) in enumerate(items, start=1):
            desc = description if description else "Aucune description."
            embed.add_field(
                name=f"#{num} — {nom} — {format_amount(prix)}💰",
                value=f"<@&{role_id}>\n{desc}",
                inline=False
            )

        set_bot_footer(embed, interaction)
        await interaction.response.send_message(embed=embed)