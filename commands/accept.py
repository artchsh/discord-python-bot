import discord
from discord.ext import commands
from database_utils import user, invite
from utils import error_embed
from events import club_on_join


def init(bot: commands.Bot):
    @bot.tree.command(name="accept", description="Команда, чтобы принимать приглашения в клубы")
    @discord.app_commands.describe(invite_id="ID приглашения, который был указан в сообщении")
    async def accept(interaction: discord.Interaction, invite_id: str):
        if not invite.isExistsById(invite_id):
            await error_embed(interaction, "Такого приглашение не существует! Или оно не для вас ;)")
            return
        invite_info = invite.getInfo(invite_id)
        user_info = user.getInfo(interaction.user.id)
        if user_info["club"] == "None":
            await error_embed(interaction, "Вы уже состоите в клубе!")
            return
        if invite_info["recepient"] != user_info["user_id"]:
            await error_embed(interaction, "Оп! Это приглашение не для вас!")
            return
        user.update(str(interaction.user.id), "club", invite_info["club"])
        club_on_join.init(invite_info["club"])
        await interaction.response.send_message("Вы успешно приняли приглашение!", ephemeral=True)
