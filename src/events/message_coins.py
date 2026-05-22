import discord
from discord import Message
from src.utils.wallet import modify_user_balance
import random

async def register(bot):
    @bot.event
    async def on_message(message: Message):
        if message.author.bot:
            return

        message_length = len(message.content)

        if message_length < 1000:
            gain = random.randint(15, 25)
        else:
            gain = random.randint(30, 50)

        try:
            from src.utils.db import get_db_connection
            db = get_db_connection()
            await modify_user_balance(db, message.author.id, gain, "add")
            db.close()
        except Exception:
            pass

        await bot.process_commands(message)