import discord
import json
from discord.ext import commands
from database_utils import user, club
from utils import filterStringSQL

def init(bot: commands.Bot):
    @bot.tree.command(name="profile")
    async def profile(interaction: discord.Interaction):
        user.checkInTable(interaction.user)
        user_info = user.getInfo(str(interaction.user.id))
        club_info = club.getInfo(user_info["club"])
        
        if (club_info != 'None'):
            club_info = str(club_info.name)
        
        embed_profile = discord.Embed(
            title=f"Профиль {interaction.user.name}"
        )
        embed_profile.add_field(
            name="Уровень",
            value=f"```{user_info['level']}```",
            inline=True
        )
        embed_profile.add_field(
            name="Количество монет",
            value=f"```{user_info['coins']}```",
            inline=True
        )
        embed_profile.add_field(
            name="Клуб",
            value=f"```{filterStringSQL(club_info)}```",
        )
        embed_profile.add_field(
            name="Семейный статус",
            value=f"```{user_info['family']}```",
            inline=True
        )
        embed_profile.add_field(
            name="Инвентарь",
            value=f"```{len(json.loads(user_info['inventory']))}/50```"
        )
        await interaction.response.send_message(embed=embed_profile, ephemeral=True)
