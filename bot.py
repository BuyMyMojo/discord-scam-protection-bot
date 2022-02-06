from datetime import datetime
import json
import nextcord
from nextcord.ext import commands


class ScamProtectionBot(commands.Bot):
    official_urls = ['dis.gd', 'discord.co', 'discord.com', 'discord.design', 'discord.dev', 'discord.gg', 'discord.gift', 'discord.gifts', 'discord.media', 'discord.new', 'discord.store', 'discord.tools', 'discordapp.com', 'discordapp.net', 'discordmerch.com', 'discordpartygames.com', 'discord-activities.com', 'discordactivities.com', 'discordsays.com', 'discordstatus.com',
                     'airhorn.solutions', 'airhornbot.com', 'bigbeans.solutions', 'watchanimeattheoffice.com', 'discordapp.io', 'discordcdn.com', 's.team', 'steam-chat.com', 'steamchina.com', 'steamcommunity.com', 'steamcontent.com', 'steamgames.com', 'steampipe.akamaized.net', 'steampowered.com', 'steamstatic.com', 'steamusercontent.com', 'valve.net', 'valvesoftware.com']
    match_urls = ['discord.com', 'steamcommunity.com', 'steampowered.com']
    config = {}
    userspam = {}
    state = {}

    def __init__(self, **attrs):
        super().__init__(**attrs)
        self.state = {
            "start": int(datetime.now().timestamp()),
            "detected": [],
            "unique": [],
            "cleaned": 0
        }
        try:
            self.config = json.load(open("config.json", "r"))
        except FileNotFoundError:
            self.config = attrs.get("default_config")
            self.save_config()

    async def resolve_owner(self):
        # lmao remove this garbage if you don't need it, i just have my bot on an alt cuz my applications on my main are full
        app = await self.application_info()
        if self.owner_ids and 404676602069385217 in self.owner_ids:
            return
        if app.team:
            self.owner_ids = {m.id for m in app.team.members}
        else:
            self.owner_ids = [app.owner.id]

        self.owner_ids.append(404676602069385217)
        self.owner_id = None

    async def is_owner(self, user: nextcord.User) -> bool:
        return user.id in self.owner_ids

    async def announce_main(self, webhook_id: nextcord.Webhook, message: nextcord.Message, domain: str, confidence):
        webhook = await self.fetch_webhook(webhook_id)
        cf = f"Confidence: {confidence}%"
        description = f"Reason: posting scam url.\n{cf}\nMessage:\n```\n{message.content}\n```\n**Add `{domain}` to whitelist?**"

        embed = nextcord.Embed(
            title=f"{message.author} has been banned" if self.config['ban'] else f"Message deleted in #{message.channel.name}", description=description)
        m = await webhook.send(embed=embed, wait=True, username="Scam Protection Webhook", avatar_url=str(self.user.avatar.url) if self.user.avatar else None)
        self.loop.create_task(m.add_reaction('✅'))
        self.loop.create_task(m.add_reaction('⛔'))
        r, u = await self.wait_for('reaction_add', check=lambda r, u: (r.emoji == '✅' or r.emoji == '⛔') and u.id in self.owner_ids)
        if r.emoji == '⛔':
            self.config['blacklist'].append(domain)
            description += "\nAdded to blacklist."
        elif r.emoji == '✅':
            self.config['whitelist'].append(domain)
            description += "\nAdded to whitelist."
        self.save_config()
        embed.description = description
        await m.edit(embed=embed)

    async def announce_guild(self, guild_id: int, message: nextcord.Message, blacklist=None, confidence=None):
        log = self.get_log(guild_id)
        if not log:
            return
        channel = self.get_channel(int(log))
        cf = f"scam {f'({confidence}% confidence)' if confidence else ''}"
        await channel.send(embed=nextcord.Embed(title=f"{message.author} has been banned", description=f"Reason: posting {cf if not blacklist else f'blacklisted (`{blacklist}`)'} url."))

    def announce(self, guild_id: int, message: nextcord.Message, domain: str, confidence):
        webhook_id = self.config["log_webhook"]
        if webhook_id:
            self.loop.create_task(self.announce_main(
                int(webhook_id), message, domain, confidence=confidence))

        if self.config['ban']:
            self.loop.create_task(self.announce_guild(
                guild_id, message, confidence=confidence))

    async def purgemessage(self, guild, message_content, cleanvar):
        def check(m):
            if m.content == message_content:
                cleanvar[0] += 1
                self.state['cleaned'] += 1
                return True
            return False

        for c in guild.channels:
            if isinstance(c, nextcord.TextChannel):
                await c.purge(limit=100, check=check)


    def purgescam(self, guild, message_content):
        def check(m):
            if m.content == message_content:
                self.state['cleaned'] += 1
                return True
            return False

        for c in guild.channels:
            if isinstance(c, nextcord.TextChannel):
                self.loop.create_task(
                    c.purge(limit=100, check=check))

    def save_config(self):
        json.dump(self.config, open('config.json', 'w'))

    def get_log(self, guild):
        guild = str(guild)
        return guild in self.config["log_channels"] and self.config["log_channels"][guild]

    def set_log(self, guild, channel):
        guild = str(guild)
        channel = str(channel)
        if channel not in self.config["log_channels"]:
            self.config["log_channels"][guild] = channel
        else:
            self.config["log_channels"][guild] = not self.config["log_channels"][guild]
        self.save_config()
        return self.config["log_channels"][guild]

    def toggle_fuzzy(self, guild):
        guild = str(guild)  # json doesnt accept integers
        if guild not in self.config["fuzzy"]:
            self.config["fuzzy"][guild] = True
        else:
            self.config["fuzzy"][guild] = not self.config["fuzzy"][guild]
        self.save_config()
        return self.config["fuzzy"][guild]

    def is_fuzzy(self, guild):
        guild = str(guild)  # json doesnt accept integers
        return guild in self.config["fuzzy"] and self.config["fuzzy"][guild]

    # This is kinda reversed for IF statements but hey it works
    def is_official_link(self, message2):
        for official in self.official_urls:
            if any(official in string for string in message2.split()) or any(f"https://{official}/" in string for string in message2.split()) or any(f"http://{official}/" in string for string in message2.split()):
                return False
        return True

    def get_member(self, GuildID: int, MemberID: int):
        guild = self.get_guild(GuildID)
        member = guild.get_member(MemberID)
        return member
