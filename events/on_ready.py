from discord.ext import commands

def init(bot: commands.Bot):
    @bot.event
    async def on_ready():
        print("Bot is up and ready!")
        try:
            synced = await bot.tree.sync()
            print(f"Synced {len(synced)} commands")
        except Exception as e:
            print(e)