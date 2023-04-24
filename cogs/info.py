import discord
from discord import app_commands
from discord.ext import commands
import os

guild_id = int(os.environ.get('GUILD_ID'))
version = os.environ.get('BOT_VERSION')


class Info(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name='info',
                          description='Shows build/version information')
    async def info(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(
            title='Информация о 30avgBot',
            color=discord.Colour.red(),
            description=f'Version: {version}\nDeveloper: 9 avg#5879')
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Info(bot), guilds=[discord.Object(id=guild_id)])
