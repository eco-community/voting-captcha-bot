import sys
import logging

from discord.ext import commands

import config
from utils import use_sentry
from cogs.captha import CaptchaCog
from constants import SENTRY_ENV_NAME


if __name__ == "__main__":
    bot = commands.Bot(command_prefix="!voting_bot", help_command=None)

    # init sentry SDK
    use_sentry(
        bot,
        dsn=config.SENTRY_API_KEY,
        environment=SENTRY_ENV_NAME,
    )

    # setup logger
    file_handler = logging.FileHandler(filename="eco-voting.log")
    stdout_handler = logging.StreamHandler(sys.stdout)

    logging.basicConfig(
        level=logging.getLevelName(config.LOG_LEVEL),
        format="%(asctime)s %(levelname)s:%(message)s",
        handlers=[file_handler if config.LOG_TO_FILE else stdout_handler],
    )

    bot.add_cog(CaptchaCog(bot))
    bot.run(config.TOKEN)
