from datetime import datetime
from discord import TextChannel
import nextcord
import re
import tldextract

from nextcord.ext import commands
from thefuzz import fuzz
from bot import ScamProtectionBot


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot: ScamProtectionBot = bot
        # Open file outside of bot functions to reduce disk calls
        # Use a much thiccer list derived from the origional URL
        my_file = open("list-all-TLD.txt", "r")
        content = my_file.read()
        self.scam_links_1 = content.split("\n")

    @commands.Cog.listener("on_ready")
    async def on_ready(self):
        print("Online")
        self.bot.loop.create_task(self.bot.resolve_owner())

    @commands.Cog.listener("on_message")
    async def on_message(self, message: nextcord.Message):
        # ignore messages from bots and from dms
        if message.author == self.bot.user.id or message.author.bot or not message.guild:
            return

        # fuzzy search
        if self.bot.is_fuzzy(message.guild.id):
            auid = message.author.id
            links = []
            scam = 0
            highest_risk = 0

            rx = r"(http|https)\:\/\/([a-zA-Z0-9\.\/\?\:@\-_=#]+)\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*"
            if not re.search(rx, message.content):
                # no match found
                return
            for m in re.finditer(rx, str(message.content)):
                extracted = tldextract.extract(m.group(0))
                domain = extracted.domain + "." + extracted.suffix
                if domain in self.bot.official_urls or domain in self.bot.config['whitelist']:
                    continue
                if domain in self.bot.config['blacklist']:
                    self.bot.loop.create_task(message.delete())
                    self.bot.state['cleaned'] += 1
                    self.bot.state['detected'].append(domain)
                    if domain not in self.bot.state['unique']:
                        self.bot.state['unique'].append(domain)
                    if self.bot.config['ban']:
                        self.bot.loop.create_task(message.author.ban(delete_message_days=1, reason="Posted blacklisted URL"))
                        self.bot.loop.create_task(self.bot.announce_guild(
                            message.guild.id, message, domain))
                    return
                links.append(m.group(0))

                for match_url in self.bot.match_urls:
                    fz = fuzz.ratio(match_url, domain)
                    if highest_risk < fz:
                        highest_risk = fz

                    if fz > 60:
                        break

            if highest_risk == 0:
                return
            scam += highest_risk / 2
            for modifier in self.bot.config['modifiers']:
                if modifier in message.content:
                    scam *= self.bot.config['modifiers'][modifier]

            if scam >= 100:
                scam = 99.99

            # fancyness
            scam = (int(scam*100) / 100.0)

            if scam > 80:
                # try to detect the scam link from the first appearence

                self.bot.state['detected'].append(domain)
                if domain not in self.bot.state['unique']:
                    self.bot.state['unique'].append(domain)

                if self.bot.config['ban']:
                    self.bot.loop.create_task(message.author.ban(
                        delete_message_days=1, reason="Posted scam URL"))
                    self.bot.loop.create_task(message.reply(
                        content=f"User banned for posting scam URL."))

                self.bot.purgescam(message.guild, message.content)
                self.bot.announce(message.guild.id, message, domain, scam)
                return

            if scam < 30:
                # probably false detection, ignore spam for now
                return

            print("scam%: " + str(scam))

            # handle spam
            now = datetime.now().timestamp()
            if message.guild.id not in self.bot.userspam:
                self.bot.userspam[message.guild.id] = {}
            userspam = self.bot.userspam[message.guild.id]
            if auid not in userspam:
                userspam[auid] = {}

            userspam[auid][now] = {
                "links": links, "risk": scam
            }
            [userspam[auid].pop(exp)
             for exp in userspam[auid].copy() if exp < (now - 60)]

            # get overall risk
            total_risk = 0
            for timestamp in userspam[auid]:
                if timestamp == now:
                    continue
                msg = userspam[auid][timestamp]
                risk = msg['risk']
                total_risk += risk * \
                    (2 if ','.join(msg['links']) == ','.join(links) else 1)

            if total_risk >= 100:
                self.bot.state['detected'].append(domain)
                if domain not in self.bot.state['unique']:
                    self.bot.state['unique'].append(domain)

                if self.bot.config['ban']:
                    self.bot.loop.create_task(message.author.ban(
                        delete_message_days=1, reason="Posted scam URL"))
                    self.bot.loop.create_task(message.reply(
                        content=f"User banned for posting scam URL."))

                self.bot.purgescam(message.guild, message.content)
                self.bot.announce(message.guild.id, message, domain, scam)
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

    @commands.Cog.listener("on_command_error")
    async def _error(self, ctx, error: commands.CommandError):
        # fancy error handling
        if ctx.command:
            await ctx.send(embed=nextcord.Embed(title=f"{ctx.command.name} - Error", description=f"```py\n{error}\n```", color=nextcord.Colour.red()))
        elif ctx.message:
            if isinstance(error, commands.CommandNotFound):
                return
            await ctx.send(embed=nextcord.Embed(title="Error", description=f"```py\n{error}\n```", color=nextcord.Colour.red()))
        else:
            raise error


def setup(bot):
    bot.add_cog(Events(bot))
