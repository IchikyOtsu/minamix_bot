from discord import Interaction, Role, Embed
from discord import app_commands
import discord
from src.utils.db import get_db_connection

async def register(bot):

    @bot.tree.command(
        name="additem",
        description="Ajouter un rôle à la boutique (Admin seulement)"
    )
    @app_commands.describe(
        role="Le rôle Discord à ajouter dans la boutique",
        prix="Prix en coins",
        nom="Nom affiché dans la boutique",
        description="Description du rôle (optionnel)"
    )
    async def addgrade(
        interaction: Interaction,
        role: Role,
        prix: int,
        nom: str,
        description: str = None
    ):
        if not interaction.user.guild_permissions.administrator:
            embed = discord.Embed(
                title="❌ Permission refusée",
                description="Vous n'avez pas la permission d'utiliser cette commande.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        if prix <= 0:
            embed = discord.Embed(
                title="💢 Prix invalide",
                description="Le prix doit être supérieur à 0.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        db = get_db_connection()
        cursor = db.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO boutique_roles (role_id, prix, nom, description)
                VALUES (%s, %s, %s, %s)
                """,
                (role.id, prix, nom, description)
            )
            db.commit()

            embed = discord.Embed(
                title="✅ Grade ajouté",
                description=f"**{role.name}** a été ajouté à la boutique pour **{prix}💰**",
                color=discord.Color.green()
            )
            embed.set_footer(text="Système d'économie")
            await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as e:
            embed = discord.Embed(
                title="❌ Erreur SQL",
                description=f"Une erreur s'est produite : {e}",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

        finally:
            cursor.close()
            db.close()
