import os
import discord
from discord import Message


async def handle(message: Message) -> None:
    content = message.content.strip()
    low = content.lower()

    if low == "gg":
        await message.add_reaction("🏆")
    if low == "ok":
        await message.add_reaction("👍")
    if len(content) == 1:
        await message.add_reaction("🤏")
    if low == "un anneau":
        asset = os.path.join(os.path.dirname(__file__), "..", "assets", "one_bot.jpg")
        if os.path.exists(asset):
            await message.reply(file=discord.File(asset))
