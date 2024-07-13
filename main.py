import discord
from discord.ext import commands
from events import on_ready
from commands import profile, club, accept
from config import TOKEN
from database_utils import user, club as club_db, invite

intents = discord.Intents.default()

bot = commands.Bot(
    command_prefix="!", 
    intents=intents
)


user.checkTable()
invite.checkTable()
club_db.checkTable()

# Events
on_ready.init(bot)

# Commands
profile.init(bot)
club.init(bot)
accept.init(bot)

bot.run(TOKEN)
