import time
import discord
from discord import Message
from src.utils.db import get_db_connection
from src.utils.views import ExpiringView
from src.config import GUILD_IDS

# user_id → timestamp of last "are you back?" prompt (1h cooldown)
_reminded: dict[int, float] = {}
REMIND_COOLDOWN = 3600


async def remove_afk(member: discord.Member, guild: discord.Guild) -> None:
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(
        "SELECT original_nick FROM afk_users WHERE user_id = %s AND guild_id = %s",
        (member.id, guild.id)
    )
    row = cursor.fetchone()
    if row:
        original_nick = row[0]
        cursor.execute(
            "DELETE FROM afk_users WHERE user_id = %s AND guild_id = %s",
            (member.id, guild.id)
        )
        db.commit()
        try:
            await member.edit(nick=original_nick if original_nick != member.name else None)
        except discord.Forbidden:
            pass
    cursor.close()
    db.close()
    _reminded.pop(member.id, None)


async def register(bot):
    @bot.listen("on_message")
    async def on_message_afk(message: Message):
        if message.author.bot:
            return
        if message.guild is None or message.guild.id not in GUILD_IDS:
            return

        db = get_db_connection()
        cursor = db.cursor()

        # Check if the author is AFK
        cursor.execute(
            "SELECT reason FROM afk_users WHERE user_id = %s AND guild_id = %s",
            (message.author.id, message.guild.id)
        )
        author_afk = cursor.fetchone()

        if author_afk:
            now = time.time()
            last = _reminded.get(message.author.id, 0)
            if now - last >= REMIND_COOLDOWN:
                _reminded[message.author.id] = now

                view = ExpiringView(timeout=60)
                yes_btn = discord.ui.Button(label="Oui, je suis de retour", style=discord.ButtonStyle.green, emoji="👋")
                no_btn = discord.ui.Button(label="Non, je suis encore absent", style=discord.ButtonStyle.grey, emoji="💤")

                async def yes_callback(inter: discord.Interaction):
                    await remove_afk(inter.user, inter.guild)
                    await inter.response.edit_message(
                        content="👋 Bienvenue de retour ! Ton statut absent a été annulé.",
                        view=None
                    )

                async def no_callback(inter: discord.Interaction):
                    _reminded[inter.user.id] = time.time()
                    await inter.response.edit_message(
                        content="💤 Ok, ton statut absent est maintenu.",
                        view=None
                    )

                yes_btn.callback = yes_callback
                no_btn.callback = no_callback
                view.add_item(yes_btn)
                view.add_item(no_btn)

                sent = await message.channel.send(
                    f"{message.author.mention} Tu as l'air de revenir — veux-tu annuler ton statut absent ?",
                    view=view
                )
                view.message = sent

            cursor.close()
            db.close()
            return

        # Check if any mentioned user is AFK
        if not message.mentions:
            cursor.close()
            db.close()
            return

        afk_users = []
        for mentioned in message.mentions:
            if mentioned.bot:
                continue
            cursor.execute(
                "SELECT reason FROM afk_users WHERE user_id = %s AND guild_id = %s",
                (mentioned.id, message.guild.id)
            )
            row = cursor.fetchone()
            if row:
                afk_users.append((mentioned, row[0]))

        cursor.close()
        db.close()

        if afk_users:
            lines = [f"• {m.display_name} — *{r}*" for m, r in afk_users]
            await message.reply(
                f"{'Cette personne est absente' if len(afk_users) == 1 else 'Ces personnes sont absentes'} "
                f"et ne peut pas te répondre pour le moment. Merci de ne pas les mentionner inutilement.\n"
                + "\n".join(lines),
                mention_author=False
            )
