import nextcord
import random
from nextcord.ext import commands

from bot import ScamProtectionBot


class Commands(commands.Cog):

    def __init__(self, bot):
        self.bot: ScamProtectionBot = bot

    @commands.command(name="log", aliases=["log_channel"])
    @commands.has_guild_permissions(administrator=True)
    async def _log(self, ctx: commands.Context, channel: commands.TextChannelConverter=None):
        await ctx.send(f"Log channel has been set to <#{self.bot.set_log(ctx.guild.id, ctx.channel.id if not channel else channel.id)}> in this guild.")

    @commands.command(name="fuzzy", aliases=["togglefuzzy"])
    @commands.has_guild_permissions(administrator=True)
    async def _fuzzy(self, ctx: commands.Context):
        await ctx.send(f"Fuzzy search has been set to `{self.bot.toggle_fuzzy(ctx.guild.id)}` in this guild.")

    @commands.command(aliases=['invitelink', 'link'])
    async def invite(self, ctx):
        """Send a DM to user with invite link"""
        member = self.bot.get_member(
            ctx.message.guild.id, ctx.message.author.id)
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

    @commands.command(aliases=['about'])
    async def info(self, ctx):
        """Send a DM to user with info about the bot"""
        member = self.bot.get_member(
            ctx.message.guild.id, ctx.message.author.id)
        channel = await member.create_dm()
        embed = nextcord.Embed(
            title="About me", description="So what do you wanna know?", color=random.randint(0, 0xFFFFFF))
        embed.add_field(name="Who made the bot?",
                        value="The bot was made by BuyMyMojo#0308 on discord", inline=False)
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


def setup(bot):
    bot.add_cog(Commands(bot))
