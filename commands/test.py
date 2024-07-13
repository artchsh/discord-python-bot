import discord
from discord.ext import commands
from discord import app_commands

def _(bot: commands.Bot):

    embed = discord.Embed(title="Title", description="Description")
    embed.set_author(name="Author name")
    embed.add_field(name="Field 1", value="value")
    embed.set_footer(text="Footer")

    @bot.tree.command(name="test")
    @app_commands.describe(variable="Test variable")
    async def test_command(interaction: discord.Interaction, variable: str):
        await interaction.response.send_message(f"Hey, you wrote {variable}!", ephemeral=True, embed=embed)