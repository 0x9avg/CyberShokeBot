from players import get_info, get_players_count
import discord
from discord.ui import Select, View
from discord.ext import tasks
from discord import app_commands
from table2ascii import table2ascii as t2a, PresetStyle
import os
from typing import List

online_channel14 = int(os.environ.get('ONLINE_CHANNEL14'))
online_channel8 = int(os.environ.get('ONLINE_CHANNEL8'))

guild_id = int(os.environ.get('GUILD_ID'))
token = os.environ.get('BOT_TOKEN')
bot_version = os.environ.get('BOT_VERSION')

servers = [{
    'name': 'Public #8',
    'ip': '79.143.20.74:26215'
}, {
    'name': 'Public #14',
    'ip': '79.143.20.74:26065'
}]


class aclient(discord.Client):

    def __init__(self) -> None:
        super().__init__(intents=discord.Intents.default())
        self.synced = False
        self.online_monitor = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild=discord.Object(id=guild_id))
            self.synced = True
        if not self.online_monitor:
            RealTimeOnline.start()
            self.online_monitor = True
        print(f'We have logged in as {self.user}.')


client = aclient()
tree = app_commands.CommandTree(client)


@tasks.loop(minutes=3)
async def RealTimeOnline():
    channel_client = client.get_channel(online_channel14)
    online = get_players_count('79.143.20.74:26065') - 1
    new_name = f"Public #14 Online: {online}"
    await channel_client.edit(name=new_name)

    channel_client = client.get_channel(online_channel8)
    online = get_players_count('79.143.20.74:26215') - 1
    new_name = f"Public #8 Online: {online}"
    await channel_client.edit(name=new_name)


@tree.command(name='help',
              description='Shows Help Options for all commands',
              guild=discord.Object(id=guild_id))
async def help(interaction: discord.Integration,
               category: str = None,
               command: str = None):

    info_commands = {
        'help': {
            'description': 'Показывает список команд',
            'full_description':
            'Используется для отображения всех возможных команд. Может использовать как `/help [command]` или `/help [category]`',
            'id': 1091428746134831185
        },
        'info': {
            'description': 'Показывает данные о текущей версии/сборке',
            'full_description':
            'Показывает полный список данных бота (Версия/сборка, автор)',
            'id': 1091459097112608830
        }
    }

    util_commands = {
        'publics': {
            'description': 'Показывает текущий список игроков на серверах',
            'full_description':
            'Выводит полный список игроков на Public #14 и Public #8 \n**`(ПРИМЕЧАНИЕ: В последствии будет меняться и переписываться)`**',
            'id': 1091459097112608829
        }
    }

    commands = {**util_commands, **info_commands}
    if command:
        command = command.replace('/', '')

    embed = discord.Embed(
        title='Доступные команды: ',
        color=discord.Colour.red(),
        description=
        'Вы можете получить детальную справку по каждой команде, выполнив её с указанием названия команды или указав категорию команд. Например: `/info ?` или `/help info`'
    )

    if command and command in commands.keys():
        embed = discord.Embed(title=f'Команда {command}',
                              color=discord.Colour.red())
        embed.add_field(name=commands[command]['description'],
                        value=commands[command]['full_description'],
                        inline=False)
        embed.add_field(name='Использование',
                        value=f'`/{command}`',
                        inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    elif category:
        embed = discord.Embed(title=f'Категория {category}',
                              color=discord.Colour.red())
        if category in ['info', 'Info', 'Information', 'information']:
            for command_iter in info_commands.items():
                embed.add_field(name=f'/{command_iter[0]}',
                                value=command_iter[1]['description'],
                                inline=False)

        elif category in ['Util', 'util', 'Utility', 'utility']:
            for command_iter in util_commands.items():
                embed.add_field(name=f'/{command_iter[0]}',
                                value=command_iter[1]['description'],
                                inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    else:
        value = [
            '<{0}:{1}>'.format(f'/{command[0]}', command[1]['id'])
            for command in info_commands.items()
        ]
        value = ', '.join(value)
        embed.add_field(name='ℹ️ Information commands',
                        value=value,
                        inline=False)
        value = [
            '<{0}:{1}>'.format(f'/{command[0]}', command[1]['id'])
            for command in util_commands.items()
        ]
        value = ', '.join(value)
        embed.add_field(name='⚙️ Utility commands', value=value, inline=False)

        select = Select(options=[
            discord.SelectOption(label='Information',
                                 emoji='ℹ️',
                                 description='Select category Information'),
            discord.SelectOption(label='Utility',
                                 emoji='⚙️',
                                 description='Select category Utility')
        ])

        async def help_category(interaction: discord.Integration):
            embed = discord.Embed(title=f'Категория {select.values[0]}',
                                  color=discord.Colour.red())
            if select.values[0] in [
                    'info', 'Info', 'Information', 'information'
            ]:
                for command_iter in info_commands.items():
                    embed.add_field(name=f'/{command_iter[0]}',
                                    value=command_iter[1]['description'],
                                    inline=False)

            elif select.values[0] in ['Util', 'util', 'Utility', 'utility']:
                for command_iter in util_commands.items():
                    embed.add_field(name=f'/{command_iter[0]}',
                                    value=command_iter[1]['description'],
                                    inline=False)
            await interaction.response.send_message(embed=embed,
                                                    ephemeral=True)

        select.callback = help_category
        view = View()
        view.add_item(select)

        await interaction.response.send_message(embed=embed, view=view)


@help.autocomplete('category')
async def category_autocomplete(
        interaction: discord.Interaction,
        current: str = None) -> List[app_commands.Choice[str]]:
    categories = ['Information', 'Utility']
    return [
        app_commands.Choice(name=category, value=category)
        for category in categories if current.lower() in category.lower()
    ]


@tree.command(name='publics',
              description='Shows online on the servers',
              guild=discord.Object(id=guild_id))
async def publics(interaction: discord.Interaction):
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
        for index, (key, value) in enumerate(server_info[0].items(), start=1):
            body.append([index, key, value])

        output = t2a(header=["Number", "Nick", "Score"],
                     body=body,
                     style=PresetStyle.thin_compact)
        embed.add_field(name=f'{server_name} Online: {server_info[1]}',
                        value=f"```\n{output}\n```",
                        inline=False)
        # print(output)
        await interaction.followup.send(embed=embed)


@tree.command(name='info',
              description='Shows build/version information',
              guild=discord.Object(id=guild_id))
async def info(interaction: discord.Interaction):
    embed = discord.Embed(
        title='Информация о 30avgBot',
        color=discord.Colour.red(),
        description=f'Version: {bot_version}\nDeveloper: 9 avg#5879')


client.run(token=token)