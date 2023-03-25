import io
import aiohttp
import discord
from redbot.core import commands

class RandomApis(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def comrade(self, ctx, *, user: commands.MemberConverter=None):
        user = user or ctx.author
        avatar_url = user.avatar_url_as(format='png', size=1024)
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://some-random-api.ml/canvas/overlay/comrade?avatar={avatar_url}") as resp:
                if resp.status != 200:
                    return await ctx.send('Error getting image...')
                data = io.BytesIO(await resp.read())
                await ctx.send(file=discord.File(data, 'comrade.png'))

    @commands.command()
    async def nobitches(self, ctx, *, user: commands.MemberConverter = None):
        user = user or ctx.author
        avatar_url = user.avatar_url_as(format='png', size=1024)
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://some-random-api.ml/canvas/misc/nobitches?avatar={avatar_url}") as resp:
                if resp.status != 200:
                    return await ctx.send('Error getting image...')
                data = io.BytesIO(await resp.read())
        try:
            await ctx.send(file=discord.File(data, 'nobitches.png'))
        except discord.errors.HTTPException:
            await ctx.send('Error sending file, the file size may be too large.')

def setup(bot):
    bot.add_cog(RandomApis(bot))
