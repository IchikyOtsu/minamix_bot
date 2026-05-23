from discord import Interaction, Embed
import discord
from src.utils.shop import get_shop_items
from src.utils.format import format_amount
from src.utils.embed import set_bot_footer


async def register(bot):
    @bot.tree.command(
        name="shop",
        description="Affiche la boutique des rôles disponibles."
    )
    async def boutique(interaction: Interaction):
        items = get_shop_items()

        if not items:
            embed = discord.Embed(
                title="🛒 Boutique vide",
                description="La boutique est vide pour le moment.",
                color=discord.Color.orange()
            )
            set_bot_footer(embed, interaction)
            await interaction.response.send_message(embed=embed)
            return

        standard = [(num, r, p, n) for num, (_, r, p, n, _d, ex) in enumerate(items, start=1) if not ex]
        exclusifs = [(num, r, p, n) for num, (_, r, p, n, _d, ex) in enumerate(items, start=1) if ex]

        lines = []
        for num, role_id, prix, nom in standard:
            lines.append(f"》 **#{num}** — {format_amount(prix)}💰 : <@&{role_id}>")

        if exclusifs:
            lines.append("")
            lines.append("★―――――――――| Rôles exclusifs |―――――――――★")
            lines.append("")
            for num, role_id, prix, nom in exclusifs:
                lines.append(f"》 **#{num}** — {format_amount(prix)}💰 : <@&{role_id}>")

        embed = Embed(
            title="🛍️ Boutique",
            description="\n".join(lines) + "\n\n*Utilise `/buy <numéro>` pour acheter.*",
            color=0x2B2D31
        )
        set_bot_footer(embed, interaction)
        await interaction.response.send_message(embed=embed)
