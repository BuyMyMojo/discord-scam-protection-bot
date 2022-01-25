import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import *
import requests
import random
import os

intents = nextcord.Intents.all()

bot = commands.Bot(command_prefix='->', description='Prefix is -> | Removing scam links one message at a time', intents=intents, allowed_mentions=nextcord.AllowedMentions(everyone=False, roles=False), max_messages=100000)

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

    if message.author == bot.user:
        return
    if message.author.bot:
        return

    # this is my personal fork of the list until the main fork takes my changes
    url = 'https://raw.githubusercontent.com/BuyMyMojo/discord-scam-links/steam-free-nutro_ru_com/list.txt'
    discord_scam_list = requests.get(url).text
    scam_links_1 = discord_scam_list.split("\n")
    scam_links_2 = discord_scam_list.split("\r\n")
    for y in scam_links_1:
        if y in message2 and y != '':
            try:
                await message.delete()
                print("Link found in: discord-scam-links")
                deleted = True
                break
            except:
                pass
    if deleted is not True:
        for y in scam_links_2:
            if y in message2 and y != '':
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


@bot.command()
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

bot.run(os.environ.get('scam_cleaner_token'))
