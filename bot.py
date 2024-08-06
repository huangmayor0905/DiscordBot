import discord  # 導入discord
import os
import asyncio
import random as rd
import json
from discord import app_commands
from discord.ext import commands


# 權限管理、前綴命令
intents = discord.Intents.all()
intents.message_content = True
intents.members = True  # 啟用成員意圖
bot = commands.Bot(command_prefix="$", intents=intents)


with open("config.json", "r", encoding="utf8") as jfile:
    jdata = json.load(jfile)


# 開機
@bot.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType.playing, name="Discord")
    await bot.change_presence(activity=activity)
    await bot.tree.sync()
    print(f'>>> "{bot.user}" is logged in! <<<')


# 載入 cogs
@bot.command()
async def load(ctx, extension):
    bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"Loaded {extension} done.")


# 卸載 cogs
@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")
    await ctx.send(f"Unloaded {extension} done.")


# 重新載入 cogs
@bot.command()
async def reload(ctx, extension):
    bot.reload_extension(f"cogs.{extension}")
    await ctx.send(f"Reloaded {extension} done.")


async def load_extension():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            print(f">>> {filename[:-3]} is loaded! <<<")


async def main():
    async with bot:
        await load_extension()
        await bot.start(jdata["botToken"])


if __name__ == "__main__":
    asyncio.run(main())
