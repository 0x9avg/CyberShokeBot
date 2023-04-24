import discord
from discord.ui import Select, View
from discord import app_commands
from discord.ext import commands
from discord.app_commands import Choice
import os

guild_id = int(os.environ.get('GUILD_ID'))


class Help(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name='help',
                          description='Shows Help Options for all commands')
    @app_commands.describe(category='Help by category',
                           command='Help on command')
    @app_commands.choices(category=[
        Choice(name='Information', value='Information'),
        Choice(name='Utility', value='Utility')
    ])
    async def help(self,
                   interaction: discord.Integration,
                   category: str = None,
                   command: str = None) -> None:

        info_commands = {
            'help': {
                'description': 'Показывает список команд',
                'full_description':
                'Используется для отображения всех возможных команд. Может использовать как `/help [command]` или `/help [category]`',
                'id': 1091652953926029382
            },
            'info': {
                'description': 'Показывает данные о текущей версии/сборке',
                'full_description':
                'Показывает полный список данных бота (Версия/сборка, автор)',
                'id': 1091652953926029384
            }
        }

        util_commands = {
            'publics': {
                'description': 'Показывает текущий список игроков на серверах',
                'full_description':
                'Выводит полный список игроков на Public #14 и Public #8 \n**`(ПРИМЕЧАНИЕ: В последствии будет меняться и переписываться)`**',
                'id': 1091652953926029383
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
            await interaction.response.send_message(embed=embed,
                                                    ephemeral=True)

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
            await interaction.response.send_message(embed=embed,
                                                    ephemeral=True)

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
            embed.add_field(name='⚙️ Utility commands',
                            value=value,
                            inline=False)

            select = Select(options=[
                discord.SelectOption(
                    label='Information',
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

                elif select.values[0] in [
                        'Util', 'util', 'Utility', 'utility'
                ]:
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


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Help(bot), guilds=[discord.Object(id=guild_id)])
