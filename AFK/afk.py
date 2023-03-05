import discord
import typing
from redbot.core import commands, checks
from datetime import datetime

class AFKCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.afk_users = set()
        self.afk_reasons = {}

    async def _set_afk(self, user, reason=None):
        if user.id not in self.afk_users:
            try:
                await user.edit(nick='[AFK] ' + user.display_name)
            except discord.Forbidden:
                pass
            self.afk_users.add(user.id)
            if reason:
                self.afk_reasons[user.id] = reason[:25]
            embed = discord.Embed(
                title='AFK status updated',
                description='You are now marked as AFK.',
                color=discord.Color.dark_orange()
            )
            await user.send(embed=embed)

    async def _remove_afk(self, user):
        if user.id in self.afk_users:
            try:
                await user.edit(nick=user.display_name[6:])
            except discord.Forbidden:
                pass
            self.afk_users.remove(user.id)
            if user.id in self.afk_reasons:
                del self.afk_reasons[user.id]
            embed = discord.Embed(
                title='AFK status updated',
                description='You are no longer marked as AFK.',
                color=discord.Color.dark_green()
            )
            await user.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content == '!AFK':
            await self._set_afk(message.author)

    @commands.command()
    async def afk(self, ctx, *, reason=None):
        await self._set_afk(ctx.author, reason)
        if reason:
            embed = discord.Embed(
                title='AFK status updated',
                description=f'You are now marked as AFK. Reason: {reason[:100]}',
                color=discord.Color.dark_orange()
            )
        else:
            embed = discord.Embed(
                title='AFK status updated',
                description='You are now marked as AFK.',
                color=discord.Color.dark_orange()
            )
        await ctx.send(embed=embed)

    @commands.command()
    async def back(self, ctx):
        await self._remove_afk(ctx.author)
        embed = discord.Embed(
            title='AFK status updated',
            description='You are no longer marked as AFK.',
            color=discord.Color.dark_green()
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def isafk(self, ctx, user: typing.Union[discord.Member, int]):
        if isinstance(user, int):
            user = discord.utils.get(ctx.guild.members, id=user)
        if user.id in self.afk_users:
            reason = self.afk_reasons.get(user.id, '')
            timestamp = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
            embed = discord.Embed(
                title='AFK status',
                description=f'{user.display_name} is AFK since {timestamp}. Reason: {reason}',
                color=discord.Color.dark_orange()
            )
            embed.set_footer(text=f"AFK since {timestamp}")
        else:
            embed = discord.Embed(
                title='AFK status',
                description=f'{user.display_name} is not AFK.',
                color=discord.Color.dark_green()
            )
        await ctx.send(embed=embed)

    @isafk.error
    async def _set_afk(self, user, reason=None):
        pass
