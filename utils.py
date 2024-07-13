import discord


async def error_embed(interaction: discord.Interaction, msg: str):
    embed = discord.Embed(title="Ошибка", description=f"{msg}")
    await interaction.response.send_message(embed=embed, ephemeral=True)
    
def filterStringSQL(string: str) -> str:
    # (' '),
    return string.replace("(", "").replace(")","").replace("'","").replace(",","")
