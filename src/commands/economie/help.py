from discord import Interaction
from discord.ui import Select
import discord
from src.utils.embed import set_bot_footer
from src.utils.views import ExpiringView

_ECONOMY = (
    "`/balance` — Voir votre solde\n"
    "`/work` — Gagner des coins (cooldown : 1 semaine)\n"
    "`/shop` — Voir les rôles disponibles à l'achat\n"
    "`/buy [numéro]` — Acheter un rôle (liste déroulante si numéro omis)\n"
    "`/leaderboard` — Top 10 des utilisateurs les plus riches"
)

_ADMIN = (
    "`/addmoney <user> <montant>` — Ajouter des coins à un utilisateur\n"
    "`/removemoney <user> <montant>` — Retirer des coins à un utilisateur\n"
    "`/additem <role> <prix> <nom> [description]` — Ajouter un rôle à la boutique\n"
    "`/removeitem <numéro>` — Supprimer un article de la boutique"
)

async def register(bot):
    @bot.tree.command(name="help", description="Affiche les commandes du bot.")
    async def help(interaction: Interaction):
        is_admin = interaction.user.guild_permissions.administrator

        options = [
            discord.SelectOption(label="Économie", value="economy", description="Commandes d'économie", emoji="💰"),
        ]
        if is_admin:
            options.append(
                discord.SelectOption(label="Administration", value="admin", description="Commandes admin", emoji="🔒")
            )

        select = Select(placeholder="Choisir une catégorie...", options=options)

        async def callback(inter: Interaction):
            if select.values[0] == "economy":
                embed = discord.Embed(title="💰 Économie", description=_ECONOMY, color=discord.Color.gold())
            else:
                embed = discord.Embed(title="🔒 Administration", description=_ADMIN, color=discord.Color.red())
            set_bot_footer(embed, inter)
            await inter.response.send_message(embed=embed, ephemeral=True)

        select.callback = callback
        view = ExpiringView()
        view.add_item(select)

        embed = discord.Embed(
            title="📖 Aide",
            description="Sélectionne une catégorie pour voir les commandes disponibles.",
            color=discord.Color.blurple()
        )
        set_bot_footer(embed, interaction)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        view.message = await interaction.original_response()
