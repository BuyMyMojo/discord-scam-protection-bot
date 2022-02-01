import nextcord
from nextcord.ext.commands import *
import os

from bot import ScamProtectionBot

intents = nextcord.Intents.all()

prefix = "->"

bot = ScamProtectionBot(
    command_prefix=prefix,
    description=f'Prefix is {prefix} | Bot for removing scam bots and messages',
    intents=intents,
    allowed_mentions=nextcord.AllowedMentions(everyone=False, roles=False),
    max_messages=100000,
    activity=nextcord.Game(
        name=f"use {prefix}invite to get an invite link! | 🧹 Removing scam bots 🧹 "),
    default_config={
        "fuzzy": {},
        "blacklist": [],
        "whitelist": [],
        "log_channels": {},
        "log_webhook": None,
        "ban": True,
        "modifiers": {
            "@everyone": 1.8, "nitro": 1.6, "steam": 1.3, "discord": 1.1, "airdrop": 2}
    }
)

cogs = ["commands", "events"]

if __name__ == '__main__':
    for cog in cogs:
        cog = "cogs." + cog
        bot.load_extension(cog)
        print('Loaded ' + cog)

bot.run(os.environ.get('scam_cleaner_token'))
