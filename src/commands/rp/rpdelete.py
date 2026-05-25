import discord
from discord import Interaction, app_commands
from src.utils.db import get_db_connection
from src.utils.embed import set_bot_footer
from src.utils.rp import has_rp_permission, invalidate_cache


async def register(bot):
    @bot.tree.command(name="rpdelete", description="Supprimer un personnage RP par son préfixe")
    @app_commands.describe(prefix="Préfixe du personnage à supprimer")
    async def rpdelete(interaction: Interaction, prefix: str):
        if not has_rp_permission(interaction.user):
            embed = discord.Embed(title="❌ Permission refusée", color=discord.Color.red())
            set_bot_footer(embed, interaction)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute(
            "SELECT id, name, user_id FROM rp_characters WHERE guild_id = %s AND prefix = %s",
            (interaction.guild.id, prefix.strip())
        )
        row = cursor.fetchone()

        if not row:
            cursor.close()
            db.close()
            embed = discord.Embed(
                title="❌ Personnage introuvable",
                description=f"Aucun personnage avec le préfixe `{prefix}` sur ce serveur.",
                color=discord.Color.red()
            )
            set_bot_footer(embed, interaction)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        char_id, char_name, user_id = row
        cursor.execute("DELETE FROM rp_characters WHERE id = %s", (char_id,))
        db.commit()
        cursor.close()
        db.close()
        invalidate_cache(interaction.guild.id)

        owner = interaction.guild.get_member(user_id)
        owner_str = owner.mention if owner else f"ID {user_id}"

        embed = discord.Embed(
            title="✅ Personnage supprimé",
            description=f"**{char_name}** (préfixe `{prefix}`) appartenant à {owner_str} a été supprimé.",
            color=discord.Color.green()
        )
        set_bot_footer(embed, interaction)
        await interaction.response.send_message(embed=embed, ephemeral=True)
