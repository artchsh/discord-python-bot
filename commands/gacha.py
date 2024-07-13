import discord
import json
from discord.ext import commands
from database_utils import user, club
from utils import filterStringSQL

Choice = discord.app_commands.Choice

def init(bot: commands.Bot):
    @bot.tree.command(name="gacha", description="Гейщит би лайк")
    @discord.app_commands.choices(actions=[
        Choice(name="roll", value=0)
    ])
    async def gacha(interaction: discord.Interaction, actions: Choice[int]):
        user_info = user.getInfo(str(interaction.user.id))
        match actions.to_dict()["name"]:
            case "roll":
                print()
                
        return