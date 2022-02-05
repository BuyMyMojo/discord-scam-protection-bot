# discord-scam-protection-bot
Jesus these bots are out of hand

This bot only deletes scam links and nothing else

## Invite the bot to your server!
[Invite link](https://discord.com/api/oauth2/authorize?client_id=935372708089315369&permissions=2147560448&scope=bot)

## What links does this remove?
All the links found in [BuildBot42's repo](https://github.com/BuildBot42/discord-scam-links)

Additionally has a fuzzy search feature to detect any scam link

## Hosting you own instance

1. Install the dependencies
   - `pip install -r requirements.txt`
2. Add your bot token
   - Get your bot's token from https://discord.com/developers, and add it to your environment variables under the name `scam_cleaner_token`
   - Or replace `os.environ.get('scam_cleaner_token')` at the bottom of `main.py` with your bot token in quotes
3. Run the bot
    - `python ./main.py`

## Authors

- [@BuyMyMojo](https://www.github.com/BuyMyMojo)
- [@grialion](https://github.com/grialion)

