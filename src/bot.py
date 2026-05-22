import os
import sys
import asyncio
from dotenv import load_dotenv
import pymysql
import discord
from discord.ext import commands

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.fonction.load_sql import load_sql_files
from src.fonction.load_commands import load_commands
from src.fonction.load_events import load_events

def run_bot():
    asyncio.run(_main_async())

async def _main_async():
    load_dotenv()

    db = pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT", 3306)),
        charset="utf8mb4",
        autocommit=True
    )

    load_sql_files(db)

    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise RuntimeError("DISCORD_TOKEN manquant dans le .env")

    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        print(f"Bot connecté : {bot.user}")
        try:
            synced = await bot.tree.sync()
            print(f"Slash commands synchronisées : {len(synced)}")
        except Exception as e:
            print("Erreur sync:", e)

    await load_events(bot)
    await load_commands(bot)

    try:
        await bot.start(token)
    except KeyboardInterrupt:
        await bot.close()

if __name__ == "__main__":
    run_bot()