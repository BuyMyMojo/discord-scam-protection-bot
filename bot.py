import nextcord
import json
from nextcord.ext import commands


class ScamProtectionBot(commands.Bot):
    official_urls = ['dis.gd', 'discord.co', 'discord.com', 'discord.design', 'discord.dev', 'discord.gg', 'discord.gift', 'discord.gifts', 'discord.media', 'discord.new', 'discord.store', 'discord.tools', 'discordapp.com', 'discordapp.net', 'discordmerch.com', 'discordpartygames.com', 'discord-activities.com', 'discordactivities.com', 'discordsays.com', 'discordstatus.com',
                     'airhorn.solutions', 'airhornbot.com', 'bigbeans.solutions', 'watchanimeattheoffice.com', 'discordapp.io', 'discordcdn.com', 's.team', 'steam-chat.com', 'steamchina.com', 'steamcommunity.com', 'steamcontent.com', 'steamgames.com', 'steampipe.akamaized.net', 'steampowered.com', 'steamstatic.com', 'steamusercontent.com', 'valve.net', 'valvesoftware.com']
    config = {}

    def __init__(self, **attrs):
        super().__init__(**attrs)

        self.config = json.load(open("config.json", "r"))

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
        json.dump(self.config, open('config.json', 'w'))

        return self.config["log_channels"][guild]

    def toggle_fuzzy(self, guild):
        guild = str(guild)  # json doesnt accept integers
        if guild not in self.config["fuzzy"]:
            self.config["fuzzy"][guild] = True
        else:
            self.config["fuzzy"][guild] = not self.config["fuzzy"][guild]
        json.dump(self.config, open('config.json', 'w'))

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
        member = self.get_member(MemberID)
        return member
