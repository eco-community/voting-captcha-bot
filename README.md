# EcoVotingCaptchaBot

Bot which is able to protect voting contest from spammer abuse

**For more on this bot and all the rest of the Eco Community bots, check out [this post](https://echo.mirror.xyz/GlFuqSbTZOLDl0LA7eDa0Yibhqq6IHNUC48nd3WJZQw).**

# Creating a bot token
1. Go to https://discord.com/developers/applications and click "New Application"
   Enter the name of the application, this name will not appear anywhere
2. Go to your app and click to "Bot" section and click "Add Bot" button then "Yes, do it!"
3. Click to "Copy" button and replace "bot_token" in the configuration file with token you have copied
4. Create oauth2 link with at least `273472` permissions


# Getting channel id
1. Open user settings in discord app and select "Appearance"
2. Scroll to the end and enable "Developer Mode"
3. Then right click on the contest channel and "Copy id"
4. Replace "channel_id" in the configuration file with copied id


# Installation
1. Install requirements from `requirements.txt` for `Python 3`
2. Copy and update settings in `config.example.py`
3. Start bot via `python bot.py`


# How to use:
1. Create a new post in the voting channel with #votehere tag
2. When the contest is over remove #votehere tag
