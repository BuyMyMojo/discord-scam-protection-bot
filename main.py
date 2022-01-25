import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import *
import requests
import random
import os

intents = nextcord.Intents.all()

bot = commands.Bot(command_prefix='->', description='Prefix is -> | Removing scam links one message at a time', intents=intents, allowed_mentions=nextcord.AllowedMentions(everyone=False, roles=False), max_messages=100000)

bot.official_urls = ['dis.gd', 'discord.co', 'discord.com', 'discord.design', 'discord.dev', 'discord.gg', 'discord.gift', 'discord.gifts', 'discord.media', 'discord.new', 'discord.store', 'discord.tools', 'discordapp.com', 'discordapp.net', 'discordmerch.com', 'discordpartygames.com', 'discord-activities.com', 'discordactivities.com', 'discordsays.com', 'discordstatus.com', 'airhorn.solutions', 'airhornbot.com', 'bigbeans.solutions', 'watchanimeattheoffice.com', 'discordapp.io', 'discordcdn.com', 's.team', 'steam-chat.com', 'steamchina.com', 'steamcommunity.com', 'steamcontent.com', 'steamgames.com', 'steampipe.akamaized.net', 'steampowered.com', 'steamstatic.com', 'steamusercontent.com', 'valve.net', 'valvesoftware.com']

def get_member(GuildID: int, MemberID: int):
    guild = bot.get_guild(GuildID)
    member = guild.get_member(MemberID)
    return member


@bot.event
async def on_ready():
    await bot.change_presence(activity=nextcord.Game(name="use ->invite to get an invite link! | 🧹 Removing scam bots 🧹 "))
    print("Online")


@bot.event
async def on_message(message):
    message2 = message.content.casefold()
    deleted = False

    # ignore messages from bots
    if message.author == bot.user.id:
        return
    if message.author.bot:
        return

    my_file = open("list-all-TLD.txt", "r")  # Use a much thiccer list derived from the origional URL
    content = my_file.read()

    scam_links_1 = content.split("\n")
    for y in scam_links_1:
        if y.casefold() in message2 and y != '' and y not in bot.official_urls:
            try:
                await message.delete()
                print("Link found in: discord-scam-links")
                deleted = True
                break
            except:
                pass

    if deleted is True:
        pass
    else:
        await bot.process_commands(message)


@bot.command(aliases=['invitelink', 'link'])
async def invite(ctx):
    """Send a DM to user with invite link"""
    member = get_member(ctx.message.guild.id, ctx.message.author.id)
    channel = await member.create_dm()
    embed = nextcord.Embed(title="Invite me!",
                          url="https://discord.com/api/oauth2/authorize?client_id=935372708089315369&permissions=2147560448&scope=bot",
                          description="So you want to invite me to a server to keep it clean? here is the invite link you need!",
                          color=random.randint(0, 0xFFFFFF))
    embed.add_field(name="Invite link:",
                    value="https://discord.com/api/oauth2/authorize?client_id=935372708089315369&permissions=2147560448&scope=bot",
                    inline=False)
    await channel.send(embed=embed)
    await ctx.message.delete()


@bot.command(aliases=['about'])
async def info(ctx):
    """Send a DM to user with info about the bot"""
    member = get_member(ctx.message.guild.id, ctx.message.author.id)
    channel = await member.create_dm()
    embed = nextcord.Embed(title="About me", description="So what do you wanna know?", color=random.randint(0, 0xFFFFFF))
    embed.add_field(name="Who made the bot?", value="The bot was made by BuyMyMojo#0308 on discord", inline=False)
    embed.add_field(name="Can I host my own copy?",
                    value="Yes! go grab the code from https://github.com/BuyMyMojo/discord-scam-protection-bot",
                    inline=True)
    embed.add_field(name="What links does this remove?",
                    value="All the links found in BuildBot42's repo https://github.com/BuildBot42/discord-scam-links",
                    inline=True)
    embed.add_field(name="Where do I submit links the bot missed?",
                    value="email them to me at hello@buymymojo.net in case discord flags you as a spam user in the future",
                    inline=True)
    await channel.send(embed=embed)
    await ctx.message.delete()

bot.run(os.environ.get('scam_cleaner_token'))
