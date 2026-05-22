from discord import Interaction, app_commands
import discord
from src.utils.db import get_db_connection

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

        cursor.execute("SELECT role_id, nom FROM boutique_roles WHERE id = %s", (numero,))
        result = cursor.fetchone()

        if not result:
            embed = discord.Embed(
                title="❌ Article non trouvé",
                description=f"Aucun article avec le numéro `#{numero}` n'existe dans la boutique.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            db.close()
            return

        role_id, role_name = result
        cursor.execute("DELETE FROM boutique_roles WHERE id = %s", (numero,))
        db.commit()

        embed = discord.Embed(
            title="✅ Grade supprimé",
            description=f"L'article **#{numero} — {role_name}** (<@&{role_id}>) a été supprimé de la boutique.",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        db.close()
