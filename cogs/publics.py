import discord
from discord import app_commands
from table2ascii import table2ascii as t2a, PresetStyle
from discord.ext import commands
from utils.players import get_info
from utils.paginator import PaginationView

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
        embeds = []

        for server in servers:
            embed = discord.Embed(title='Server list')
            server_name = server['name']
            server_ip = server['ip']
            server_info = get_info(server_ip)
            body = []
            if server_info[1] == 0:
                output = f'Server empty'
            else:
                for index, (key, value) in enumerate(server_info[0].items(),
                                                     start=1):
                    body.append([index, key, value])

                output = t2a(header=["#", "Nick", "Score"],
                             body=body,
                             style=PresetStyle.thick_compact)
            embed.add_field(name=f'{server_name} Online: {server_info[1]}',
                            value=f"```\n{output}\n```",
                            inline=False)
            embeds.append(embed)

        view = PaginationView(embeds, author=interaction.user.id)
        await interaction.response.send_message(embed=view.initial,
                                                view=view,
                                                ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Publics(bot))
