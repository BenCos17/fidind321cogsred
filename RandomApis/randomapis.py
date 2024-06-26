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
            async with session.get(f"https://some-random-api.com/canvas/overlay/comrade?avatar={avatar_url}") as resp:
                if resp.status != 200:
                    return await ctx.send('Error getting image...')
                data = io.BytesIO(await resp.read())
                await ctx.send(file=discord.File(data, 'comrade.png'))

    @commands.command()
    async def nobitches(self, ctx, *, message=""):
        if message:
            message = message.replace(" ", "+")
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://some-random-api.com/canvas/misc/nobitches?no=no+bitches+{message}") as resp:
                if resp.status != 200:
                    return await ctx.send('Error getting image...')
                data = io.BytesIO(await resp.read())
                await ctx.send(file=discord.File(data, 'nobitches.png'))

    @commands.command()
    async def hornyjail(self, ctx, *, user: commands.MemberConverter=None):
        user = user or ctx.author
        avatar_url = user.avatar_url_as(format='png', size=1024)
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://some-random-api.com/canvas/overlay/jail?avatar={avatar_url}") as resp:
                if resp.status != 200:
                    return await ctx.send('Error getting image...')
                data = io.BytesIO(await resp.read())
                await ctx.send(file=discord.File(data, 'hornyjail.png'))

    @commands.command()
    async def simp(self, ctx, *, user: commands.MemberConverter=None):
        user = user or ctx.author
        avatar_url = user.avatar_url_as(format='png', size=1024)
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://some-random-api.com/canvas/misc/simpcard?avatar={avatar_url}") as resp:
                if resp.status != 200:
                    return await ctx.send('Error getting image...')
                data = io.BytesIO(await resp.read())
                await ctx.send(file=discord.File(data, 'simpcard.png'))

    @commands.command()
    async def tonikawa(self, ctx, *, user: commands.MemberConverter=None):
        user = user or ctx.author
        avatar_url = user.avatar_url_as(format='png', size=1024)
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://some-random-api.com/canvas/misc/tonikawa?avatar={avatar_url}") as resp:
                if resp.status != 200:
                    return await ctx.send('Error getting image...')
                data = io.BytesIO(await resp.read())
                await ctx.send(file=discord.File(data, 'tonikawa.png'))

