import nextcord
import re
import tldextract

from nextcord.ext import commands
from thefuzz import fuzz, process
from urllib.parse import urlparse
from bot import ScamProtectionBot


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot: ScamProtectionBot = bot
        # Open file outside of bot functions to reduce disk calls
        my_file = open("list-all-TLD.txt", "r")  # Use a much thiccer list derived from the origional URL
        content = my_file.read()
        self.scam_links_1 = content.split("\n")

    @commands.Cog.listener("on_ready")
    async def on_ready(self):
        await self.bot.change_presence(activity=nextcord.Game(name="use ->invite to get an invite link! | 🧹 Removing scam bots 🧹 "))
        print("Online")

    @commands.Cog.listener("on_message")
    async def on_message(self, message: nextcord.Message):
        # ignore messages from bots and from dms
        if message.author == self.bot.user.id or message.author.bot or not message.guild:
            return

        # fuzzy search
        if self.bot.is_fuzzy(message.guild.id):
            rx = r"(http|https)\:\/\/([a-zA-Z0-9\.\/\?\:@\-_=#]+)\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*"
            p = re.compile(rx)
            m = re.search(rx, str(message.content))
            if m:
                extracted = tldextract.extract(m.group(0))
                domain = extracted.domain + "." + extracted.suffix
                if domain in self.bot.official_urls or domain in self.bot.config['whitelist']:
                    return
                if domain in self.bot.config['blacklist']:
                    await message.author.ban(delete_message_days=1, reason="Posted scam URL")
                fz = fuzz.ratio(['discord.com'], domain)
                print(fz)
                if fz > 60:
                    await message.delete()
        else:
            message2 = message.content.casefold()
            for y in self.scam_links_1:
                if y == '':
                    break
                scam = y.casefold()

                if any(scam in string for string in message2.split()) and self.bot.is_official_link(message2) or any(f"https://{scam}/" in string for string in message2.split()) and self.bot.is_official_link(message2) or any(f"http://{scam}/" in string for string in message2.split()) and self.bot.is_official_link(message2):
                    if scam in self.bot.official_urls:
                        break
                    try:
                        await message.delete()
                        print("Link found in: discord-scam-links")
                        deleted = True
                        break
                    except:
                        pass


def setup(bot):
    bot.add_cog(Events(bot))
