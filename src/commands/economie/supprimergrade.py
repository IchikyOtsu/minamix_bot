from discord import Interaction
from discord import app_commands
import discord
from src.utils.db import get_db_connection

async def register(bot):
    @bot.tree.command(
        name="supprimergrade",
        description="Supprimer un grade de la boutique (Admin seulement)"
    )
    @app_commands.describe(
        role_id="ID du rôle à supprimer de la boutique",
        nom="Nom du rôle pour confirmation (optionnel)"
    )
    async def supprimergrade(interaction: Interaction, role_id: str, nom: str = None):
        if not interaction.user.guild_permissions.administrator:
            embed = discord.Embed(
                title="❌ Permission refusée",
                description="Vous n'avez pas la permission d'utiliser cette commande.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        if not role_id.isdigit():
            embed = discord.Embed(
                title="❌ ID invalide",
                description="L'ID du rôle doit être un nombre valide.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        db = get_db_connection()
        cursor = db.cursor()

        cursor.execute("SELECT nom FROM boutique_roles WHERE role_id = %s", (int(role_id),))
        result = cursor.fetchone()
        
        if not result:
            embed = discord.Embed(
                title="❌ Rôle non trouvé",
                description=f"Aucun rôle avec l'ID `{role_id}` n'existe dans la boutique.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            db.close()
            return

        role_name = result[0]
        
        if nom and nom.lower() != role_name.lower():
            embed = discord.Embed(
                title="⚠️ Nom incorrect",
                description=f"Le nom `{nom}` ne correspond pas au rôle trouvé (`{role_name}`).",
                color=discord.Color.orange()
            )
            embed.add_field(
                name="Rôle trouvé :",
                value=f"ID: `{role_id}`\nNom: `{role_name}`",
                inline=False
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            db.close()
            return

        cursor.execute("DELETE FROM boutique_roles WHERE role_id = %s", (int(role_id),))
        db.commit()

        embed = discord.Embed(
            title="✅ Grade supprimé",
            description=f"Le rôle **{role_name}** (ID: `{role_id}`) a été supprimé de la boutique.",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        db.close()
