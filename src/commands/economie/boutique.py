from discord import Interaction, Embed
import discord
from src.utils.db import get_db_connection

async def register(bot):
    @bot.tree.command(
        name="boutique",
        description="Affiche la boutique des rôles disponibles."
    )
    async def boutique(interaction: Interaction):
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT id, role_id, prix, nom, description FROM boutique_roles")
        items = cursor.fetchall()
        db.close()

        if not items:
            embed = discord.Embed(
                title="🛒 Boutique vide",
                description="La boutique est vide pour le moment.",
                color=discord.Color.orange()
            )
            embed.set_footer(text="Système d'économie")
            await interaction.response.send_message(embed=embed)
            return

        embed = Embed(
            title="🛍️ Boutique des rôles",
            description="Utilise `/buy <numéro>` pour acheter un rôle.",
            color=0x00FFAA
        )

        for item_id, role_id, prix, nom, description in items:
            desc = description if description else "Aucune description."
            embed.add_field(
                name=f"#{item_id} — {nom} — {prix}💰",
                value=f"<@&{role_id}>\n{desc}",
                inline=False
            )

        embed.set_footer(text="Système d'économie")
        await interaction.response.send_message(embed=embed)