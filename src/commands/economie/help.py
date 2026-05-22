from discord import Interaction
import discord

async def register(bot):
    @bot.tree.command(name="help", description="Affiche toutes les commandes du bot.")
    async def help(interaction: Interaction):
        embed = discord.Embed(
            title="📖 Commandes du bot",
            color=discord.Color.blurple()
        )

        embed.add_field(
            name="Économie",
            value=(
                "`/balance` — Voir votre solde\n"
                "`/work` — Gagner des coins (cooldown : 1 semaine)\n"
                "`/shop` — Voir les rôles disponibles à l'achat\n"
                "`/buy [numéro]` — Acheter un rôle (liste déroulante si numéro omis)"
            ),
            inline=False
        )

        embed.add_field(
            name="Administration 🔒",
            value=(
                "`/addmoney <user> <montant>` — Ajouter des coins à un utilisateur\n"
                "`/removemoney <user> <montant>` — Retirer des coins à un utilisateur\n"
                "`/additem <role> <prix> <nom> [description]` — Ajouter un rôle à la boutique\n"
                "`/removeitem <numéro>` — Supprimer un article de la boutique"
            ),
            inline=False
        )

        embed.set_footer(text="Système d'économie")
        await interaction.response.send_message(embed=embed, ephemeral=False)
