
### Remark42DiscordRSS

Automatically sends Remark42 comments in a channel based on new entries in the Remark42 RSS feeds.

Remark42DiscordRSS is mostly based on my [Discord RSS](https://github.com/HansiMcKlaus/HansiRSS) project.


## Setup

### Create a Discord Bot

1. Create a new Discord Bot Application at the [Discord Developer Portal](https://discord.com/developers/applications).
2. Fill out the General Information
3. Under OAuth2, select "bot" in the Scopes select and then select "Send Messages" in the Bot Permissions.
4. Use the generated URL at the bottom to invite the Bot to your server.
5. Under Bot, generate a new Token and enable all three Intents under Privileged Gateway Intents.


### Config
1. In `config.py`, fill in your Bot Token and Channel ID and edit the update interval to your liking.
2. Add the Remark42 RSS Feeds.

`url` is the link to the RSS Feed.

`user` is the ID of a user who will be tagged as the author of an article. If no user is to be tagged, then you just leave it empty.


### Requirements

`pip install -r requirements.txt`