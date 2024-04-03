import discord
from redbot.core import commands
from redbot.core.commands.errors import CheckFailure

class Post(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    async def can_send_message(self, ctx, channel):
        if channel is None:
            return False
        if channel.permissions_for(ctx.me).send_messages and channel.permissions_for(ctx.author).send_messages:
            return True
        else:
            if not channel.permissions_for(ctx.me).send_messages:
                await ctx.send("I do not have permission to send messages in that channel.")
            if not channel.permissions_for(ctx.author).send_messages:
                await ctx.send("You do not have permission to send messages in that channel.")
            return False

    @commands.command()
    async def post(self, ctx, title, description, color, channel: discord.TextChannel = None):
        if not await self.can_send_message(ctx, channel):
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
    async def postmessage(self, ctx, message, channel: discord.TextChannel = None):
        if not await self.can_send_message(ctx, channel):
            return
        try:
            await channel.send(message)

        except discord.Forbidden:
            await ctx.send(f"I do not have permission to send messages in {channel.mention}. Please make sure I have the necessary permissions to send messages and try again. If you are not sure what permissions I need, please check your own permissions or ask a server administrator for help.")

def setup(bot):
    bot.add_cog(Post(bot))
