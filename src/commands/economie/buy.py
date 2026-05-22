from discord import Interaction, Embed, app_commands
import discord
from discord.ui import Select, View
from src.utils.db import get_db_connection
from src.utils.balance import get_user_balance
from src.utils.wallet import modify_user_balance


async def _process_purchase(interaction: Interaction, item_id: int):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT role_id, prix, nom FROM boutique_roles WHERE id = %s", (item_id,))
    item = cursor.fetchone()

    if not item:
        embed = Embed(title="❌ Article non trouvé", description="Ce numéro n'existe pas dans la boutique.", color=discord.Color.red())
        embed.set_footer(text="Système d'économie")
        await interaction.response.send_message(embed=embed, ephemeral=True)
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
        await interaction.response.send_message(embed=embed, ephemeral=True)
        db.close()
        return

    try:
        await modify_user_balance(db, user_id, prix, "remove")
    except Exception:
        embed = Embed(title="❌ Erreur", description="Une erreur est survenue lors du paiement.", color=discord.Color.red())
        embed.set_footer(text="Système d'économie")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        db.close()
        return

    try:
        role = interaction.guild.get_role(int(role_id))
        role_added = bool(role and not await interaction.user.add_roles(role) or role)
    except Exception:
        role_added = False

    if role_added:
        embed = Embed(
            title="✅ Achat réussi !",
            description=f"Tu as acheté <@&{role_id}> pour **{prix}💰**.\nLe rôle t'a été attribué avec succès.",
            color=discord.Color.green()
        )
    else:
        embed = Embed(
            title="✅ Achat réussi !",
            description=f"Tu as acheté <@&{role_id}> pour **{prix}💰**.\n\n⚠️ *Impossible d'attribuer le rôle automatiquement. Contacte un admin.*",
            color=discord.Color.orange()
        )

    embed.set_footer(text="Système d'économie")
    await interaction.response.send_message(embed=embed)
    db.close()


async def register(bot):
    @bot.tree.command(name="buy", description="Acheter un rôle dans la boutique.")
    @app_commands.describe(numero="Numéro de l'article (laisser vide pour voir la liste)")
    async def buy(interaction: Interaction, numero: int = None):
        if numero is not None:
            await _process_purchase(interaction, numero)
            return

        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT id, nom, prix FROM boutique_roles")
        items = cursor.fetchall()
        db.close()

        if not items:
            await interaction.response.send_message("La boutique est vide.", ephemeral=True)
            return

        options = [
            discord.SelectOption(
                label=f"#{item_id} — {nom}",
                value=str(item_id),
                description=f"{prix}💰"
            )
            for item_id, nom, prix in items[:25]
        ]

        select = Select(placeholder="Choisis un article...", options=options)

        async def callback(inter: Interaction):
            await _process_purchase(inter, int(select.values[0]))

        select.callback = callback
        view = View()
        view.add_item(select)
        await interaction.response.send_message("Quel article veux-tu acheter ?", view=view, ephemeral=True)