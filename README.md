# discord-scam-protection-bot
Jesus these bots are out of hand

This bot only deletes scam links and nothing else

## Invite the bot to your server!
[Invite link](https://discord.com/api/oauth2/authorize?client_id=935372708089315369&permissions=2147560448&scope=bot)

## What links does this remove?
All the links found in [BuildBot42's repo](https://github.com/BuildBot42/discord-scam-links)

## How to host your own:

1. install `nextcord` with pip
   - `pip install nextcord`
2. Add your bot token
   1. add it as `scam_cleaner_token` in your env variabled
   2. replace `os.environ.get('scam_cleaner_token')` at the bottom of `main.py` with your bot token in quotes
3. Run bot
    - `python ./main.py`
