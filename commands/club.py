import discord
from discord.ext import commands
from discord import app_commands
from utils import error_embed, filterStringSQL
from database_utils import club as club_db, user, invite
from events import club_on_join


def init(bot: commands.Bot):
    @bot.tree.command(name="club")
    @app_commands.choices(action=[
        discord.app_commands.Choice(name="info", value=0),
        discord.app_commands.Choice(name="create", value=1),
        discord.app_commands.Choice(name="invite", value=2),
        discord.app_commands.Choice(name="config", value=3),
        discord.app_commands.Choice(name="remove", value=4),
        discord.app_commands.Choice(name="kick", value=5),
        discord.app_commands.Choice(name="list", value=6),
        discord.app_commands.Choice(name="top", value=7)
    ])
    async def club(interaction: discord.Interaction, action: discord.app_commands.Choice[int]):
        user.checkInTable(interaction.user)
        user_info = user.getInfo(str(interaction.user.id))

        match action.to_dict()["name"]:
            case "info":
                if (user_info["club"] != "None"):
                    club_info = club_db.getInfo(user_info["club"])
                    embed_club = discord.Embed(title=f"Информация о клубе {club_info.name}")
                    embed_club.add_field(
                        name="Уровень",
                        value=f"```{club_info.level}```",
                        inline=True
                    )
                    embed_club.add_field(
                        name="Тег",
                        value=f"```[{club_info.tag}]```",
                        inline=True
                    )
                    embed_club.add_field(
                        name="Описание",
                        value=f"```{club_info.description}```"
                    )
                    await interaction.response.send_message(embed=embed_club, ephemeral=True)
                else:
                    await error_embed(interaction, "Вы не состоите ни в каком клубе")
                return

            case "create":
                class CreateClubModal(discord.ui.Modal, title='Создание клуба'):
                    club_name = discord.ui.TextInput(label='Название клуба')
                    club_description = discord.ui.TextInput(label='Описание клуба', style=discord.TextStyle.long)
                    club_tag = discord.ui.TextInput(label='Краткое название клуба', max_length=4)

                    async def on_submit(self, interaction: discord.Interaction):
                        if not club_db.isExists(club_name=str(self.club_name)):
                            club_info = club_db.create(club_name=str(self.club_name), club_tag=str(self.club_tag),
                                                       club_description=str(self.club_description),
                                                       creator_id=str(interaction.user.id))
                            await interaction.response.send_message(f"Клуб `{self.club_name}` был успешно создан!",
                                                                    ephemeral=True)
                            club_on_join.init(club_info[0])
                            return
                        else:
                            return await error_embed(interaction, "Клуб с таким названием уже существует!")

                await interaction.response.send_modal(CreateClubModal())
                return

            case "invite":
                if (user_info["club"] != "None"):
                    class InviteMemberModal(discord.ui.Modal, title='Пригласить пользователя'):
                        member2inv: discord.User = discord.ui.UserSelect()

                        async def on_submit(self, interaction: discord.Interaction):
                            invite_id = invite.create(str(interaction.user.id), str(self.member2inv.id), user_info["club"])
                            club_info = club_db.getInfo(user_info["club"])
                            invite_embed = discord.Embed(title=f"Приглашение в клуб {club_info.name}")
                            invite_embed.add_field(name="От кого", value=f"```{interaction.user.name}```", inline=True)
                            invite_embed.add_field(name="Уровень", value=f"```{club_info.level}```", inline=True)
                            invite_embed.add_field(name="ID", value=f"```{invite_id}```", inline=True)
                            invite_embed.add_field(name="Описание", value=f"```{club_info.description}```")
                            invite_embed.add_field(name="Как принять?", value=f"```/accept {invite_id}```")
                            await self.member2inv.send(embed=invite_embed)

                    await interaction.response.send_modal(InviteMemberModal())
                else:
                    await error_embed(interaction, "Вы не состоите ни в каком клубе")
                return

        await interaction.response.send_message(f"```json {action.to_dict()}```", ephemeral=True)
