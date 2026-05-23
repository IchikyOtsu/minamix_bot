from discord import Interaction, Member, app_commands
import discord
from src.utils.shop import get_shop_items
from src.utils.embed import set_bot_footer


async def register(bot):
    @bot.tree.command(
        name="giveitem",
        description="Donner un article de la boutique à un utilisateur (Admin seulement)"
    )
    @app_commands.describe(
        numero="Numéro de l'article affiché dans /shop",
        user="Utilisateur qui reçoit le rôle"
    )
    async def giveitem(interaction: Interaction, numero: int, user: Member):
        if not interaction.user.guild_permissions.administrator:
            embed = discord.Embed(title="❌ Permission refusée", color=discord.Color.red())
            set_bot_footer(embed, interaction)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        items = get_shop_items()

        if numero < 1 or numero > len(items):
            embed = discord.Embed(
                title="❌ Numéro invalide",
                description=f"Il n'y a que **{len(items)}** article(s) dans la boutique.",
                color=discord.Color.red()
            )
            set_bot_footer(embed, interaction)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        _, role_id, _, nom, *__ = items[numero - 1]

        role = interaction.guild.get_role(int(role_id))
        if not role:
            embed = discord.Embed(
                title="❌ Rôle introuvable",
                description=f"Le rôle associé à cet article n'existe plus sur le serveur.",
                color=discord.Color.red()
            )
            set_bot_footer(embed, interaction)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        if role in user.roles:
            embed = discord.Embed(
                title="⚠️ Rôle déjà possédé",
                description=f"{user.mention} a déjà <@&{role_id}>.",
                color=discord.Color.orange()
            )
            set_bot_footer(embed, interaction)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        try:
            await user.add_roles(role)
        except discord.Forbidden:
            embed = discord.Embed(
                title="❌ Permission insuffisante",
                description="Le bot n'a pas la permission d'attribuer ce rôle.",
                color=discord.Color.red()
            )
            set_bot_footer(embed, interaction)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        embed = discord.Embed(
            title="✅ Rôle attribué",
            description=f"{user.mention} a reçu <@&{role_id}> (**#{numero} — {nom}**).",
            color=discord.Color.green()
        )
        set_bot_footer(embed, interaction)
        await interaction.response.send_message(embed=embed, ephemeral=True)
