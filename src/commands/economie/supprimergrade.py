from discord import Interaction, app_commands
import discord
from src.utils.db import get_db_connection
from src.utils.embed import set_bot_footer

async def register(bot):
    @bot.tree.command(
        name="removeitem",
        description="Supprimer un article de la boutique (Admin seulement)"
    )
    @app_commands.describe(numero="Numéro de l'article affiché dans /boutique")
    async def supprimergrade(interaction: Interaction, numero: int):
        if not interaction.user.guild_permissions.administrator:
            embed = discord.Embed(
                title="❌ Permission refusée",
                description="Vous n'avez pas la permission d'utiliser cette commande.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        db = get_db_connection()
        cursor = db.cursor()

        cursor.execute("SELECT id, role_id, nom FROM boutique_roles ORDER BY id")
        items = cursor.fetchall()

        if numero < 1 or numero > len(items):
            embed = discord.Embed(
                title="❌ Numéro invalide",
                description=f"Il n'y a que **{len(items)}** article(s) dans la boutique.",
                color=discord.Color.red()
            )
            set_bot_footer(embed, interaction)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            db.close()
            return

        actual_id, role_id, role_name = items[numero - 1]
        cursor.execute("DELETE FROM boutique_roles WHERE id = %s", (actual_id,))
        db.commit()
        cursor.close()
        db.close()

        embed = discord.Embed(
            title="✅ Article supprimé",
            description=f"L'article **#{numero} — {role_name}** (<@&{role_id}>) a été supprimé de la boutique.",
            color=discord.Color.green()
        )
        set_bot_footer(embed, interaction)
        await interaction.response.send_message(embed=embed, ephemeral=True)
