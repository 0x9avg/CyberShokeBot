import settings
import discord
from discord.ext import commands
from discord import app_commands
import os

guild_id = int(os.environ.get('GUILD_ID'))
token = os.environ.get('BOT_TOKEN')
aplication_id = os.environ.get('CLIENT_ID')

logger = settings.logging.getLogger("bot")


class Bot(commands.Bot):

    def __init__(self) -> None:
        super().__init__(command_prefix='$',
                         intents=discord.Intents.all(),
                         aplication_id=aplication_id)
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()

        if not self.synced:
            for filename in os.listdir('./cogs'):
                if filename.endswith('.py'):
                    # try:
                    await self.load_extension(f'cogs.{filename[:-3]}')
                    # print(f'Cog {filename[:-3]} loaded')
                    logger.info(f'Cog {filename[:-3]} loaded')

                    # except Exception as ex:
                    #     user = bot.get_user(566652404838170625)
                    #     await user.send(ex)
            await bot.tree.sync()

            self.synced = True
        logger.info(f'Bot has logged in as {self.user}.')


bot = Bot()
bot.run(token=token, root_logger=True)