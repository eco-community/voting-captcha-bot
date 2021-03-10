from discord.ext import commands
from operator import itemgetter
from random import shuffle, randint
from PIL import Image, ImageDraw, ImageFont
from string import ascii_lowercase, ascii_uppercase, digits
from datetime import datetime, timedelta
import asyncio
import discord
import json
import io


class CaptchaCog(commands.Cog, name='captcha'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        config = json.load(open("config.json"))
        self.messages = {}
        self.channels = config["channels"]
        self.letters = list(ascii_uppercase + ascii_lowercase + digits)
        del self.letters[self.letters.index("I")]
        del self.letters[self.letters.index("l")]
        self.waiting = []

    def get_captcha(self):
        letters = self.letters.copy()
        shuffle(letters)
        key = "".join(letters[:7])
        image = Image.new("RGBA", (400, 100), (255, 255, 255, 0))
        draw = ImageDraw.Draw(image)
        x, y = image.width, image.height
        draw.text((200 / 2, 50 / 2), key, (255, 255, 255, 255), ImageFont.truetype("arial", 50))

        rx, ry = lambda: randint(0, x), lambda: randint(0, y)
        for i in range(15):
            f, s = (rx(), ry()), (rx(), ry())
            color = (randint(0, 255), randint(0, 255), randint(0, 255), 255)
            draw.line((f, s), fill=color, width=3)

        buffer = io.BytesIO()
        image.save(buffer, "png")
        buffer.seek(0)
        return buffer, key

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.Member):
        if isinstance(user, discord.User) or reaction.message.guild is None: return
        if reaction.message.id in self.messages.keys():
            captcha, key = self.get_captcha()
            file = discord.File(captcha, filename='captcha.png')
            await user.send("Enter the letters on the image to confirm vote, you have 5 minutes to answer.", file=file)

            try:
                answer = await self.bot.wait_for("message", check=lambda m: m.guild is None and m.author == user, timeout=600, )
                if answer.content == key:
                    await user.send("Success!")
                else:
                    await user.send("You have failed the captcha, try again.")
                    await reaction.remove(user)
            except asyncio.TimeoutError:
                await user.send("You have failed the captcha, try again.")
                return

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.channel.id in self.channels and message.channel.id not in map(itemgetter(0), self.waiting):
            self.waiting.append((message.channel.id, message.id))
        elif message.channel.id in self.channels:
            for channel, id in self.waiting:
                if channel == message.channel.id:
                    self.messages[message.id] = id
                    break

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        if message.id in self.messages.keys():
            for k, v in self.messages.copy().items():
                if k == message.id:
                    del self.messages[k]
                    break
