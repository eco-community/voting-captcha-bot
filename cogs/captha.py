import io
import asyncio
import logging
import platform
from typing import Set
from random import shuffle, randint
from string import ascii_lowercase, ascii_uppercase, digits

import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont

import config


class CaptchaCog(commands.Cog, name="captcha"):  # type: ignore[call-arg]
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.channels = config.VOTING_CHANNELS
        self.letters = list(ascii_uppercase + ascii_lowercase + digits)
        del self.letters[self.letters.index("I")]
        del self.letters[self.letters.index("l")]
        self.messages: Set[int] = set()
        # TODO: remove this, temporary hack to keep state during bot restart
        self.messages.add(822302708412186654)

    def get_captcha(self):
        letters = self.letters.copy()
        shuffle(letters)
        key = "".join(letters[:7])
        image = Image.new("RGBA", (400, 100), (255, 255, 255, 0))
        draw = ImageDraw.Draw(image)
        x, y = image.width, image.height
        platform_running = platform.system()
        if platform_running in ["Windows", "Linux"]:
            font_path = "arial"
        else:
            font_path = "/Library/Fonts/Arial.ttf"
        draw.text((200 / 2, 50 / 2), key, (255, 255, 255, 255), ImageFont.truetype(font_path, 50))

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
    async def on_raw_message_edit(self, payload: discord.RawMessageUpdateEvent):
        if payload.channel_id in self.channels:
            if payload.message_id in self.messages and config.VOTING_TAG not in payload.data["content"]:
                # voting tag was removed from message, we should stop voting process on it
                self.messages.remove(payload.message_id)
                logging.debug(f"Message id:{payload.message_id} was removed from voting")
            elif payload.message_id not in self.messages and config.VOTING_TAG in payload.data["content"]:
                logging.debug(f"Message id:{payload.message_id} was added to voting")
                # voting tag was applied to message, we should start voting process on it
                self.messages.add(payload.message_id)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.message_id in self.messages:
            channel = self.bot.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            user = self.bot.get_user(payload.user_id)
            if not user:
                user = await self.bot.fetch_user(payload.user_id)
            captcha, key = self.get_captcha()
            file = discord.File(captcha, filename="captcha.png")
            try:
                await user.send(
                    "Enter the letters on the image to confirm vote, you have 5 minutes to answer.", file=file
                )

                try:
                    answer = await self.bot.wait_for(
                        "message",
                        check=lambda m: m.guild is None and m.author == user,
                        timeout=600,
                    )
                    if answer.content.lower() == key.lower():
                        await user.send("Success! Your vote was recorded")
                    else:
                        # remove reaction if user failed captcha
                        await message.remove_reaction(payload.emoji, user)
                        await user.send("You have failed the captcha, your vote was removed")

                except asyncio.TimeoutError:
                    # remove reaction if user ignores bot
                    await message.remove_reaction(payload.emoji, user)
                    await user.send("You have failed to answer captcha in 5 minutes, your vote was removed")

            except discord.errors.Forbidden:
                # remove reaction from users that forbid private messages
                await message.remove_reaction(payload.emoji, user)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.channel.id in self.channels and config.VOTING_TAG in message.content:
            self.messages.add(message.id)

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        if message.id in self.messages:
            self.messages.remove(message.id)
