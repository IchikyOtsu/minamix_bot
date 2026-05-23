from discord import Interaction, Embed, app_commands
import discord
from discord.ui import Select, Button
from src.utils.db import get_db_connection
from src.utils.balance import get_user_balance
from src.utils.wallet import modify_user_balance
from src.utils.format import format_amount
from src.utils.embed import set_bot_footer
from src.utils.views import ExpiringView


def _get_items():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT id, role_id, prix, nom FROM boutique_roles ORDER BY id")
    items = cursor.fetchall()
    cursor.close()
    db.close()
    return items


async def _process_purchase(interaction: Interaction, role_id: int, prix: int, nom_role: str):
    db = get_db_connection()
    user_id = interaction.user.id
    current_balance = await get_user_balance(db, user_id)

    if current_balance < prix:
        embed = Embed(
            title="❌ Solde insuffisant",
            description=f"Tu as **{format_amount(current_balance)}💰** mais cet article coûte **{format_amount(prix)}💰**.",
            color=discord.Color.red()
        )
        set_bot_footer(embed, interaction)
        await interaction.response.edit_message(embed=embed, view=None)
        db.close()
        return

    try:
        await modify_user_balance(db, user_id, prix, "remove")
    except Exception:
        embed = Embed(title="❌ Erreur", description="Une erreur est survenue lors du paiement.", color=discord.Color.red())
        set_bot_footer(embed, interaction)
        await interaction.response.edit_message(embed=embed, view=None)
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
            description=f"Tu as acheté <@&{role_id}> pour **{format_amount(prix)}💰**.\nLe rôle t'a été attribué avec succès.",
            color=discord.Color.green()
        )
    else:
        embed = Embed(
            title="✅ Achat réussi !",
            description=f"Tu as acheté <@&{role_id}> pour **{format_amount(prix)}💰**.\n\n⚠️ *Impossible d'attribuer le rôle automatiquement. Contacte un admin.*",
            color=discord.Color.orange()
        )

    set_bot_footer(embed, interaction)
    await interaction.response.edit_message(embed=embed, view=None)
    db.close()


async def _show_confirmation(interaction: Interaction, role_id: int, prix: int, nom_role: str, edit: bool = False):
    embed = Embed(
        title="🛒 Confirmer l'achat ?",
        description=f"Tu t'apprêtes à acheter <@&{role_id}> pour **{format_amount(prix)}💰**.",
        color=discord.Color.blurple()
    )
    set_bot_footer(embed, interaction)

    view = ExpiringView(timeout=30)

    confirm_btn = Button(label="Confirmer", style=discord.ButtonStyle.green, emoji="✅")
    cancel_btn = Button(label="Annuler", style=discord.ButtonStyle.red, emoji="❌")

    async def confirm_callback(inter: Interaction):
        await _process_purchase(inter, role_id, prix, nom_role)

    async def cancel_callback(inter: Interaction):
        cancel_embed = Embed(title="❌ Achat annulé", color=discord.Color.red())
        set_bot_footer(cancel_embed, inter)
        await inter.response.edit_message(embed=cancel_embed, view=None)

    confirm_btn.callback = confirm_callback
    cancel_btn.callback = cancel_callback
    view.add_item(confirm_btn)
    view.add_item(cancel_btn)

    if edit:
        await interaction.response.edit_message(embed=embed, view=view)
    else:
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    view.message = await interaction.original_response()


async def register(bot):
    @bot.tree.command(name="buy", description="Acheter un rôle dans la boutique.")
    @app_commands.describe(numero="Numéro de l'article (laisser vide pour voir la liste)")
    async def buy(interaction: Interaction, numero: int = None):
        items = _get_items()

        if not items:
            await interaction.response.send_message("La boutique est vide.", ephemeral=True)
            return

        if numero is not None:
            if numero < 1 or numero > len(items):
                embed = Embed(
                    title="❌ Numéro invalide",
                    description=f"Il n'y a que **{len(items)}** article(s) dans la boutique.",
                    color=discord.Color.red()
                )
                set_bot_footer(embed, interaction)
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            _, role_id, prix, nom_role = items[numero - 1]
            await _show_confirmation(interaction, role_id, prix, nom_role, edit=False)
            return

        options = [
            discord.SelectOption(
                label=f"#{num} — {nom}",
                value=str(num),
                description=f"{format_amount(prix)}💰"
            )
            for num, (_, role_id, prix, nom) in enumerate(items, start=1)
        ][:25]

        select = Select(placeholder="Choisis un article...", options=options)

        async def callback(inter: Interaction):
            num = int(select.values[0])
            _, role_id, prix, nom_role = items[num - 1]
            await _show_confirmation(inter, role_id, prix, nom_role, edit=True)

        select.callback = callback
        view = ExpiringView()
        view.add_item(select)
        await interaction.response.send_message("Quel article veux-tu acheter ?", view=view, ephemeral=True)
        view.message = await interaction.original_response()
