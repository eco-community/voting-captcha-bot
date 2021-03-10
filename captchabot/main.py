from cogs.captha import CaptchaCog
from discord.ext import commands
import json

token = json.load(open('./config.json'))['token']

bot = commands.Bot(command_prefix='.', help_command=None)

bot.add_cog(CaptchaCog(bot))
bot.run(token)
