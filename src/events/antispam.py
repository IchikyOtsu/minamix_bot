import discord
from discord import Message
from src.utils.db import get_db_connection
from src.utils.embed import set_bot_footer
from src.config import GUILD_IDS


async def register(bot):
    @bot.listen("on_message")
    async def on_message_antispam(message: Message):
        if message.author.bot:
            return
        if message.guild is None or message.guild.id not in GUILD_IDS:
            return

        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute(
            "SELECT 1 FROM antispam_channels WHERE guild_id = %s AND channel_id = %s",
            (message.guild.id, message.channel.id)
        )
        is_antispam = cursor.fetchone() is not None

        if not is_antispam:
            cursor.close()
            db.close()
            return

        try:
            await message.delete()
        except Exception:
            pass

        try:
            await message.guild.ban(
                message.author,
                reason="Message posté dans un channel anti-spam",
                delete_message_days=0
            )
        except Exception:
            pass

        cursor.execute(
            "SELECT value FROM guild_config WHERE guild_id = %s AND config_key = 'logs_channel'",
            (message.guild.id,)
        )
        logs_result = cursor.fetchone()
        cursor.close()
        db.close()

        if not logs_result:
            return

        logs_channel = message.guild.get_channel(int(logs_result[0]))
        if not logs_channel:
            return

        embed = discord.Embed(
            title="🔨 Ban automatique — Anti-spam",
            color=discord.Color.red()
        )
        embed.add_field(name="Utilisateur", value=f"{message.author} (`{message.author.id}`)", inline=False)
        embed.add_field(name="Channel", value=f"<#{message.channel.id}>", inline=False)
        embed.add_field(name="Message", value=message.content[:500] if message.content else "*vide*", inline=False)
        embed.timestamp = message.created_at

        await logs_channel.send(embed=embed)
