import discord
from redbot.core import commands
from redbot.core.commands.errors import CheckFailure

class Post(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def can_send_message(self, ctx):
        if ctx.channel.permissions_for(ctx.me).send_messages and ctx.channel.permissions_for(ctx.author).send_messages:
            return True
        else:
            if not ctx.channel.permissions_for(ctx.me).send_messages:
                await ctx.send("I do not have permission to send messages in this channel.")
            if not ctx.channel.permissions_for(ctx.author).send_messages:
                await ctx.send("You do not have permission to send messages in this channel.")
            return False

    async def can_post_in_channel(self, ctx, channel):
        if ctx.channel == channel or ctx.author.permissions_in(channel).send_messages:
            return True
        else:
            await ctx.send(f"You do not have permission to send messages in {channel.mention}. Please make sure you have the necessary permissions to send messages and try again. If you are not sure what permissions you need, please check your own permissions or ask a server administrator.")
            return False

    @commands.command()
    @commands.check(lambda ctx: self.can_send_message(ctx))
    async def post(self, ctx, title, description, color, channel: discord.TextChannel):
        if not await self.can_post_in_channel(ctx, channel):
            return
        try:
            if color.startswith("#"):
                # if color starts with '#' it's a hexadecimal color code
                color_value = int(color[1:], 16)
            else:
                # otherwise, it's a color name
                color_value = getattr(discord.Colour, color.lower())().value

            embed = discord.Embed(title=title, description=description, color=color_value)
            await channel.send(embed=embed)

        except (KeyError, ValueError):
            await ctx.send(f"Invalid color '{color}'.")

        except discord.Forbidden:
            await ctx.send(f"I do not have permission to send messages in {channel.mention}. Please make sure I have the necessary permissions to send messages and try again. If you are not sure what permissions I need, please check your own permissions or ask a server administrator.")

    @commands.command()
    @commands.check(lambda ctx: self.can_send_message(ctx))
    async def postmessage(self, ctx, message, channel: discord.TextChannel):
        if not await self.can_post_in_channel(ctx, channel):
            return
        try:
            await channel.send(message)

        except discord.Forbidden:
            await ctx.send(f"I do not have permission to send messages in {channel.mention}. Please make sure I have the necessary permissions to send messages and try again. If you are not sure what permissions I need, please check your own permissions or ask a server administrator.")

def setup(bot):
    bot.add_cog(Post(bot))
