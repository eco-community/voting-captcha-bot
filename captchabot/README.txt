Before start, open "config.json" in any text editor

Creating a bot
1. Go to https://discord.com/developers/applications and click "New Application"
   Enter the name of the application, this name will not appear anywhere
2. Go to your app and click to "Bot" section and click "Add Bot" button then "Yes, do it!"
3. Click to "Copy" button and replace "bot_token" in the configuration file with token you have copied


Getting channel id
1. Open user settings in discord app and select "Appearance"
2. Scroll to the end and enable "Developer Mode"
3. Then right click on the contest channel and "Copy id"
4. Replace "channel_id" in the configuration file with copied id


Installing python
1. Go to https://python.org/ and download the latest version available and restart the computer
2. Unzip project to folder you like, open this folder in explorer and click on path
   https://prnt.sc/10hzoj0
   Type "cmd" and press Enter
3. Enter this command "pip install pipenv && pipenv update"


To start bot type "pipenv run python main.py" in the cmd.exe

How to use it:
1. Send a post of contest in the channel you specified
2. Right after this post create another one for voting and add reactions to it accordingly
3. When contest is over - delete voting message
