import discord
from discord import Message
from src.config import GUILD_IDS
from src.utils.rp import get_prefix_cache

# guild_id -> webhook url (cached to avoid refetching every message)
_webhook_cache: dict[int, discord.Webhook] = {}


async def _get_or_create_webhook(channel: discord.TextChannel) -> discord.Webhook:
    if channel.id in _webhook_cache:
        return _webhook_cache[channel.id]

    webhooks = await channel.webhooks()
    for wh in webhooks:
        if wh.name == "MinamixRP":
            _webhook_cache[channel.id] = wh
            return wh

    wh = await channel.create_webhook(name="MinamixRP")
    _webhook_cache[channel.id] = wh
    return wh


async def register(bot):
    @bot.listen("on_message")
    async def on_message_rp(message: Message):
        if message.author.bot:
            return
        if message.guild is None or message.guild.id not in GUILD_IDS:
            return

        content = message.content
        if not content:
            return

        cache = get_prefix_cache(message.guild.id)
        matched_char = None
        matched_prefix = None

        for prefix, char_data in cache.items():
            if content.startswith(prefix):
                char_id, user_id, char_name, image_url = char_data
                # Only the owner can trigger their character
                if message.author.id == user_id:
                    matched_char = (char_name, image_url)
                    matched_prefix = prefix
                    break

        if not matched_char:
            return

        char_name, image_url = matched_char
        spoken_text = content[len(matched_prefix):].strip()
        if not spoken_text:
            return

        try:
            await message.delete()
        except discord.Forbidden:
            pass

        if not isinstance(message.channel, discord.TextChannel):
            return

        try:
            webhook = await _get_or_create_webhook(message.channel)
            await webhook.send(
                content=spoken_text,
                username=char_name,
                avatar_url=image_url,
            )
        except Exception as e:
            print(f"[RP] Erreur webhook : {e}")
