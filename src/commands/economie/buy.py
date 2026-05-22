from discord import Interaction, Embed, app_commands
from src.utils.db import get_db_connection
from src.utils.balance import get_user_balance
from src.utils.wallet import modify_user_balance
import discord

async def register(bot):
    @bot.tree.command(
        name="buy",
        description="Acheter un rôle dans la boutique."
    )
    @app_commands.describe(nom="Le nom du rôle à acheter")
    async def buy(interaction: Interaction, nom: str):
        db = get_db_connection()
        cursor = db.cursor()

        cursor.execute(
            "SELECT role_id, prix, nom FROM boutique_roles WHERE LOWER(nom) = LOWER(%s)",
            (nom,)
        )
        item = cursor.fetchone()

        if not item:
            embed = Embed(
                title="❌ Article non trouvé",
                description="Ce rôle n'est pas disponible dans la boutique.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Système d'économie")
            await interaction.response.send_message(embed=embed, ephemeral=False)
            db.close()
            return

        role_id, prix, nom_role = item
        user_id = interaction.user.id

        current_balance = await get_user_balance(db, user_id)

        if current_balance < prix:
            embed = Embed(
                title="❌ Solde insuffisant",
                description=f"Tu as **{current_balance}💰** mais cet article coûte **{prix}💰**.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Système d'économie")
            await interaction.response.send_message(embed=embed, ephemeral=False)
            db.close()
            return

        try:
            await modify_user_balance(db, user_id, prix, "remove")
        except Exception:
            embed = Embed(
                title="❌ Erreur",
                description="Une erreur est survenue lors du paiement.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Système d'économie")
            await interaction.response.send_message(embed=embed, ephemeral=False)
            db.close()
            return

        try:
            role = interaction.guild.get_role(int(role_id))
            if role:
                await interaction.user.add_roles(role)
                role_added = True
            else:
                role_added = False
        except Exception:
            role_added = False

        if role_added:
            embed = Embed(
                title="✅ Achat réussi !",
                description=(
                    f"Tu as acheté **{nom_role}** pour **{prix}💰**.\n"
                    "Le rôle t'a été attribué avec succès."
                ),
                color=discord.Color.green()
            )
        else:
            embed = Embed(
                title="✅ Achat réussi !",
                description=(
                    f"Tu as acheté **{nom_role}** pour **{prix}💰**.\n\n"
                    "⚠️ *Impossible d'attribuer le rôle automatiquement. Contacte un admin.*"
                ),
                color=discord.Color.orange()
            )

        embed.set_footer(text="Système d'économie")
        await interaction.response.send_message(embed=embed, ephemeral=False)
        db.close()