import logging
from cogs.captha import CaptchaCog
from discord.ext import commands

import config
from utils import use_sentry
from constants import SENTRY_ENV_NAME


bot = commands.Bot(command_prefix=".", help_command=None)

# init sentry SDK
use_sentry(
    bot,
    dsn=config.SENTRY_API_KEY,
    environment=SENTRY_ENV_NAME,
)

# setup logger
logging.basicConfig(filename="eco-voting.log", level=logging.INFO, format="%(asctime)s %(levelname)s:%(message)s")

bot.add_cog(CaptchaCog(bot))
bot.run(config.TOKEN)
