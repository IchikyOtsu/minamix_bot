from discord import Interaction, Embed
from discord import app_commands
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

        cursor.execute("SELECT role_id, prix, nom, description FROM boutique_roles")
        items = cursor.fetchall()

        if not items:
            embed = discord.Embed(
                title="🛒 Boutique vide",
                description="La boutique est vide pour le moment.",
                color=discord.Color.orange()
            )
            embed.set_footer(text="Système d'économie")
            
            # Message visible par tout le monde
            await interaction.response.send_message(embed=embed, ephemeral=False)
            db.close()
            return

        embed = Embed(
            title="🛍️ Boutique des rôles",
            description="Voici les rôles que tu peux acheter !",
            color=0x00FFAA
        )

        for role_id, prix, nom, description in items:
            desc = description if description else "Aucune description."
            embed.add_field(
                name=f"🎭 {nom} — {prix}💰",
                value=f"**ID du rôle :** `{role_id}`\n{desc}",
                inline=False
            )

        await interaction.response.send_message(embed=embed, ephemeral=False)
        db.close()