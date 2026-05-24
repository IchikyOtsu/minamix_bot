import discord
from discord import Interaction
from datetime import datetime
from src.utils.db import get_db_connection
from src.utils.embed import set_bot_footer


class _AfkModal(discord.ui.Modal, title="Définir mon statut absent"):
    reason = discord.ui.TextInput(
        label="Raison (reste vague si tu veux)",
        placeholder="Santé · Famille · Voyage · Travail · Repos · Études · Ne vous regarde pas",
        required=True,
        max_length=100,
    )
    end_time = discord.ui.TextInput(
        label="Fin de l'absence (optionnel)",
        placeholder="JJ/MM/AAAA HH:MM — laisser vide = indéfini",
        required=False,
        max_length=16,
    )

    async def on_submit(self, interaction: Interaction):
        reason = self.reason.value.strip()
        end_time = None

        raw_end = self.end_time.value.strip()
        if raw_end:
            try:
                end_time = datetime.strptime(raw_end, "%d/%m/%Y %H:%M")
            except ValueError:
                embed = discord.Embed(
                    title="❌ Format de date invalide",
                    description="Utilise le format `JJ/MM/AAAA HH:MM` (ex: `25/12/2025 18:00`).",
                    color=discord.Color.red()
                )
                set_bot_footer(embed, interaction)
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

        member = interaction.user
        original_nick = member.nick or member.name

        new_nick = f"Absent · {member.display_name}"
        if len(new_nick) > 32:
            new_nick = new_nick[:32]

        try:
            await member.edit(nick=new_nick)
        except discord.Forbidden:
            pass

        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO afk_users (user_id, guild_id, original_nick, reason, end_time) "
            "VALUES (%s, %s, %s, %s, %s) "
            "ON DUPLICATE KEY UPDATE reason = %s, original_nick = %s, end_time = %s, start_time = NOW()",
            (member.id, interaction.guild.id, original_nick, reason, end_time,
             reason, original_nick, end_time)
        )
        db.commit()
        cursor.close()
        db.close()

        end_str = f"<t:{int(end_time.timestamp())}:f>" if end_time else "indéfinie"
        embed = discord.Embed(
            title="💤 Statut absent activé",
            description=f"Ton absence a été enregistrée.\nFin : {end_str}",
            color=discord.Color.greyple()
        )
        set_bot_footer(embed, interaction)
        await interaction.response.send_message(embed=embed, ephemeral=True)


async def register(bot):
    @bot.tree.command(name="afk", description="Définir ton statut absent.")
    async def afk(interaction: Interaction):
        await interaction.response.send_modal(_AfkModal())
