import discord
from discord import app_commands
from table2ascii import table2ascii as t2a, PresetStyle
from discord.ext import commands
import os
from utils.players import *

guild_id = int(os.environ.get('GUILD_ID'))

servers = [{
    'name': 'Public #8',
    'ip': '79.143.20.74:26215'
}, {
    'name': 'Public #14',
    'ip': '79.143.20.74:26065'
}]


class Publics(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name='publics',
                          description='Shows online on the servers')
    async def publics(self, interaction: discord.Interaction):
        await interaction.response.defer()
        for server in servers:
            embed = discord.Embed(title='Server list')
            server_name = server['name']
            server_ip = server['ip']
            server_info = get_info(server_ip)
            body = []
            if server_info[1] == 0:
                await interaction.followup.send(
                    f'```Server {server_name} is empty```')
                continue
            for index, (key, value) in enumerate(server_info[0].items(),
                                                 start=1):
                body.append([index, key, value])

            output = t2a(header=["Number", "Nick", "Score"],
                         body=body,
                         style=PresetStyle.thin_compact)
            embed.add_field(name=f'{server_name} Online: {server_info[1]}',
                            value=f"```\n{output}\n```",
                            inline=False)
            await interaction.followup.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Publics(bot), guilds=[discord.Object(id=guild_id)])
