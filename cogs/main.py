import discord
import random as rd
from discord.ext import commands
from core.classes import Cog_Extension
from discord import app_commands


class Main(Cog_Extension):
    # Cog 的寫法：
    # @bot.command() -> @commands.command()
    # bot -> self.bot

    # ping
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"{round(self.bot.latency * 1000)} (ms)")

    # say hi
    @commands.command()
    async def hi(self, ctx):
        await ctx.send("hi there!")

    # bot say
    @commands.command()
    async def say(self, ctx, *, msg):
        await ctx.message.delete()
        await ctx.send(msg)

    # clear message
    @commands.command()
    async def clean(self, ctx, num: int):
        await ctx.channel.purge(limit=num + 1)

    # name指令顯示名稱，description指令顯示敘述
    # name的名稱，中、英文皆可，但不能使用大寫英文
    @app_commands.command(name="hello", description="Hello, world!")
    async def hello(self, interaction: discord.Interaction):
        # 回覆使用者的訊息
        await interaction.response.send_message("Hello, world!")

    @app_commands.command(name="123", description="123")
    async def onetwothree(self, interaction: discord.Interaction):
        # 回覆使用者的訊息
        await interaction.response.send_message("123")


async def setup(bot):
    await bot.add_cog(Main(bot))
