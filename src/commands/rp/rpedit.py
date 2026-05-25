import discord
from discord import Interaction, app_commands
from src.utils.db import get_db_connection
from src.utils.embed import set_bot_footer
from src.utils.rp import has_rp_permission, invalidate_cache


async def register(bot):
    @bot.tree.command(name="rpedit", description="Modifier un personnage RP par son préfixe actuel")
    @app_commands.describe(
        prefix="Préfixe actuel du personnage",
        name="Nouveau nom (optionnel)",
        new_prefix="Nouveau préfixe (optionnel)",
        image="Nouvelle image (fichier, optionnel)",
    )
    async def rpedit(
        interaction: Interaction,
        prefix: str,
        name: str = None,
        new_prefix: str = None,
        image: discord.Attachment = None,
    ):
        if not has_rp_permission(interaction.user):
            embed = discord.Embed(title="❌ Permission refusée", color=discord.Color.red())
            set_bot_footer(embed, interaction)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        if name is None and new_prefix is None and image is None:
            embed = discord.Embed(
                title="❌ Aucune modification",
                description="Spécifie au moins un champ à modifier.",
                color=discord.Color.red()
            )
            set_bot_footer(embed, interaction)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        if image and (not image.content_type or not image.content_type.startswith("image/")):
            embed = discord.Embed(
                title="❌ Fichier invalide",
                description="Le fichier joint doit être une image.",
                color=discord.Color.red()
            )
            set_bot_footer(embed, interaction)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)

        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute(
            "SELECT id, name FROM rp_characters WHERE guild_id = %s AND prefix = %s",
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
            await interaction.edit_original_response(embed=embed)
            return

        char_id, current_name = row

        stable_url = None
        if image:
            rp_channel = await _get_rp_channel(bot, interaction.guild.id) or interaction.channel
            file = await image.to_file()
            msg = await rp_channel.send(
                content=f"*Mise à jour de **{name or current_name}** :*",
                file=file
            )
            stable_url = msg.attachments[0].url if msg.attachments else image.url

        updates = []
        values = []
        if name:
            updates.append("name = %s")
            values.append(name)
        if new_prefix:
            updates.append("prefix = %s")
            values.append(new_prefix.strip())
        if stable_url:
            updates.append("image_url = %s")
            values.append(stable_url)

        values.append(char_id)
        try:
            cursor.execute(
                f"UPDATE rp_characters SET {', '.join(updates)} WHERE id = %s",
                values
            )
            db.commit()
        except Exception as e:
            cursor.close()
            db.close()
            if "Duplicate" in str(e):
                embed = discord.Embed(
                    title="❌ Préfixe déjà utilisé",
                    description=f"Le préfixe `{new_prefix}` est déjà pris sur ce serveur.",
                    color=discord.Color.red()
                )
            else:
                embed = discord.Embed(title="❌ Erreur", description=str(e), color=discord.Color.red())
            set_bot_footer(embed, interaction)
            await interaction.edit_original_response(embed=embed)
            return

        cursor.close()
        db.close()
        invalidate_cache(interaction.guild.id)

        changes = []
        if name:
            changes.append(f"Nom : **{current_name}** → **{name}**")
        if new_prefix:
            changes.append(f"Préfixe : `{prefix}` → `{new_prefix}`")
        if image:
            changes.append("Image mise à jour")

        embed = discord.Embed(
            title="✅ Personnage modifié",
            description="\n".join(changes),
            color=discord.Color.green()
        )
        set_bot_footer(embed, interaction)
        await interaction.edit_original_response(embed=embed)


async def _get_rp_channel(bot, guild_id: int):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(
        "SELECT value FROM guild_config WHERE guild_id = %s AND config_key = 'rp_channel'",
        (guild_id,)
    )
    row = cursor.fetchone()
    cursor.close()
    db.close()
    if row:
        return bot.get_channel(int(row[0]))
    return None
