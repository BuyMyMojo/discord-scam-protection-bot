import nextcord
from nextcord.ext.commands import *
import os

from bot import ScamProtectionBot

intents = nextcord.Intents.all()

bot = ScamProtectionBot(
    command_prefix='->',
    description='Prefix is -> | Removing scam links one message at a time',
    intents=intents,
    allowed_mentions=nextcord.AllowedMentions(everyone=False, roles=False),
    max_messages=100000,
    activity=nextcord.Game(name="use ->invite to get an invite link! | 🧹 Removing scam bots 🧹 "))

cogs = ["commands", "events"]

if __name__ == '__main__':
    for cog in cogs:
        cog = "cogs." + cog
        bot.load_extension(cog)
        print('Loaded ' + cog)

bot.run(os.environ.get('scam_cleaner_token'))
