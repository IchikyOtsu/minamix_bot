import discord

def create_balance_embed(user, balance):
    embed = discord.Embed(
        title="💰 Solde mis à jour",
        description=f"Vous avez maintenant **{balance}** pièces.",
        color=discord.Color.gold()
    )
    embed.set_thumbnail(url=user.display_avatar.url)
    return embed

def create_basic_embed(title, description, color=discord.Color.blue()):
    embed = discord.Embed(
        title=title,
        description=description,
        color=color
    )
    return embed