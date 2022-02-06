from datetime import datetime
from re import M
import nextcord
from nextcord.ext import commands

from bot import ScamProtectionBot


class Commands(commands.Cog):

    def __init__(self, bot):
        self.bot: ScamProtectionBot = bot

    @commands.command(name="purge", aliases=["purgescam", "removescam", "delmessages"])
    @commands.guild_only()
    @commands.has_guild_permissions(manage_messages=True)
    async def _purge(self, ctx: commands.Context, message: commands.MessageConverter = None):
        if message:
            message = message.content
        elif ctx.message.reference:
            message = (await ctx.channel.fetch_message(ctx.message.reference.message_id)).content
        else:
            await ctx.send("No message specified")
            return
        m = await ctx.send("Started purging messages...")
        clean = [0]
        await self.bot.purgemessage(ctx.guild, message, clean)
        await m.edit(content=f"Purged {clean[0]} messages!")

    @commands.command(name="mlog", aliases=["mainlog"])
    @commands.is_owner()
    async def _mlog(self, ctx: commands.Context):
        """Set the main log channel to the current channel"""
        webhook: nextcord.Webhook = None
        if len(await ctx.channel.webhooks()) <= 0:
            webhook = await ctx.channel.create_webhook(name="Scam Protection Webhook")
        else:
            webhook = (await ctx.channel.webhooks())[0]
        self.bot.config['log_webhook'] = str(webhook.id)
        self.bot.save_config()
        await ctx.send(f"Main (global) log webhook has been set to `{webhook.id}`.")

    @commands.command(name="log", aliases=["log_channel"])
    @commands.has_guild_permissions(administrator=True)
    async def _log(self, ctx: commands.Context, channel: commands.TextChannelConverter = None):
        """Set log channel for the current guild"""
        await ctx.send(f"Log channel has been set to <#{self.bot.set_log(ctx.guild.id, ctx.channel.id if not channel else channel.id)}> in this guild.")

    @commands.command(name="fuzzystate", aliases=["fzs"])
    @commands.guild_only()
    async def _fzs(self, ctx: commands.Context):
        state = self.bot.state
        ordered = {
            "▶️ Running since": f"<t:{state['start']}:F>",
            "❓ Enabled in this guild": f"**{self.bot.is_fuzzy(ctx.guild.id)}**\n",
            "⚠️ Total detections": len(state['detected']),
            "❗ Unique detections": len(state['unique']),
            "🗑️ Cleaned messages": state['cleaned']
        }
        ordstr = ""
        for k in ordered:
            ordstr += f"{k}: {ordered[k]}\n"
        embed = nextcord.Embed(title="Fuzzy state",
                               description=ordstr,
                               colour=nextcord.Colour.random(),
                               )
        embed.timestamp = datetime.now()
        embed.set_footer(text="Invite this bot to your servers to get scam protection!")
        await ctx.send(embed=embed)

    @commands.command(name="fuzzy", aliases=["togglefuzzy"])
    @commands.has_guild_permissions(administrator=True)
    async def _fuzzy(self, ctx: commands.Context):
        """Toggle fuzzy search for the current guild"""
        await ctx.send(f"Fuzzy search has been set to `{self.bot.toggle_fuzzy(ctx.guild.id)}` in this guild.")

    @commands.command(aliases=['invitelink', 'link'])
    async def invite(self, ctx):
        """Send a DM to user with invite link"""
        member = self.bot.get_member(
            ctx.message.guild.id, ctx.message.author.id)
        channel = await member.create_dm()
        embed = nextcord.Embed(title="Invite me!",
                               url=f"https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=2147560448&scope=bot",
                               description="So you want to invite me to a server to keep it clean? Here is the invite link you need!",
                               color=nextcord.Colour.random())
        embed.add_field(name="Invite link:",
                        value=f"https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=2147560448&scope=bot",
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
            title="About me", description="So what do you wanna know?", color=nextcord.Colour.random())
        embed.add_field(name="Who made the bot?",
                        value="The bot was made by BuyMyMojo#0308 on discord with massive help from grialion on Discord and GitHub", inline=False)
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
