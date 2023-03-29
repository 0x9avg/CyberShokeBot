from players import get_info, get_players_count
import discord
from discord.ext import commands, tasks
from table2ascii import table2ascii as t2a, PresetStyle
import os

client = commands.Bot(command_prefix='/')
client.remove_command('help')

token = os.environ.get('BOT_TOKEN')
bot_version = os.environ.get('BOT_VERSION')

servers = [{
    'name': 'Public #8',
    'ip': '79.143.20.74:26215'
}, {
    'name': 'Public #14',
    'ip': '79.143.20.74:26065'
}]


@tasks.loop(minutes=3)
async def RealTimeOnline():
    channel_client = client.get_channel(1090691667230724238)
    online = get_players_count('79.143.20.74:26065')
    new_name = f"Public #14 Online: {online}"
    await channel_client.edit(name=new_name)

    channel_client = client.get_channel(1090691019839914054)
    online = get_players_count('79.143.20.74:26215')
    new_name = f"Public #8 Online: {online}"
    await channel_client.edit(name=new_name)


@client.event
async def on_ready():
    RealTimeOnline.start()

    print(f'{client.user} is alive and listening')


@client.command()
async def help(ctx):
    embed = discord.Embed(title='Commands')
    embed.add_field(name='/info',
                    value='Показывает информацию о боте',
                    inline=False)
    embed.add_field(name='/publics',
                    value='Показывает онлайн на 14 и 8 паблике',
                    inline=False)
    embed.add_field(name='/version',
                    value='Вывести версию бота',
                    inline='False')

    await ctx.send(content=None, embed=embed)


@client.command()
async def info(ctx):
    await ctx.send("Made by 9 avg#5879")


@client.command()
async def version(ctx):
    await ctx.send(f'```Bot version: {bot_version}```')


@client.command()
async def setprefix(ctx, prefix):
    client.command_prefix = prefix
    await ctx.send(f"Prefix changed to ``{prefix}``")


@client.command()
async def publics(ctx):
    for server in servers:
        embed = discord.Embed(title='Server list')
        server_name = server['name']
        server_ip = server['ip']
        server_info = get_info(server_ip)
        body = []
        if server_info[1] == 0:
            await ctx.send(f'```Server {server_name} is empty```')
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
        await ctx.send(content=None, embed=embed)


client.run(token)