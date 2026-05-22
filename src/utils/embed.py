import discord
from src.utils.format import format_amount


def set_bot_footer(embed: discord.Embed, interaction: discord.Interaction) -> None:
    bot_user = interaction.client.user
    embed.set_footer(
        text=f"{bot_user.name} • {bot_user.id}",
        icon_url=bot_user.avatar.url if bot_user.avatar else None
    )


def create_balance_embed(user: discord.User, balance: int, interaction: discord.Interaction, title: str = None) -> discord.Embed:
    embed = discord.Embed(
        title=title or f"💰 Solde de {user.name}",
        description=f"Vous avez actuellement **{balance:,}💵**.",
        color=discord.Color.gold()
    )
    if user.avatar:
        embed.set_thumbnail(url=user.avatar.url)
    set_bot_footer(embed, interaction)
    return embed