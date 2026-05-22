import discord

def create_balance_embed(user: discord.User, balance: int, title: str = None) -> discord.Embed:
    
    embed = discord.Embed(
        title=title or f"💰 Solde de {user.name}",
        description=f"Vous avez actuellement **{balance}💵**.",
        color=discord.Color.gold()
    )
    embed.set_footer(text="Système d'économie")
    if user.avatar:
        embed.set_thumbnail(url=user.avatar.url)
    return embed