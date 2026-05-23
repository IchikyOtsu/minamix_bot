import time
import random
import discord
from discord import Message
from src.utils.wallet import modify_user_balance
from src.config import GUILD_IDS

_last_gain: dict[int, float] = {}
COOLDOWN = 60


async def register(bot):
    @bot.event
    async def on_message(message: Message):
        if message.author.bot:
            return

        if message.guild is None or message.guild.id not in GUILD_IDS:
            return

        if bot.user in message.mentions:
            await message.reply("Tu veux quoi toi ?")
            return

        now = time.time()
        if now - _last_gain.get(message.author.id, 0) < COOLDOWN:
            await bot.process_commands(message)
            return
        _last_gain[message.author.id] = now

        gain = random.randint(30, 50) if len(message.content) >= 1000 else random.randint(15, 25)

        try:
            from src.utils.db import get_db_connection
            db = get_db_connection()
            await modify_user_balance(db, message.author.id, gain, "add")
            db.close()
        except Exception:
            pass

        await bot.process_commands(message)