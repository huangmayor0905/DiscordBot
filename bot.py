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


with open("setting.json", "r", encoding="utf8") as jfile:
    jdata = json.load(jfile)


## 開機
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
        await bot.start(jdata["DISCORD_TOKEN"])


if __name__ == "__main__":
    asyncio.run(main())

# https://discord.com/oauth2/authorize?client_id=1211861121678581760&permissions=8&integration_type=0&scope=bot

# valorantMap = [
#     "深海遺珠", "極地寒港", "劫境之地", "雙塔迷城", "蓮華古城", "天漠之峽", "熱帶樂園", "遺落境地", "義境空島",
#     "日落之城", "深窟幽境"
# ]

# valorantMap = ["深海遺珠", "劫境之地", "雙塔迷城", "蓮華古城", "天漠之峽", "遺落境地", "義境空島"]

# valorantAgent = [
#     "Iso", "Clove", "Brimstone", "Phoenix", "Sage", "Sova", "Viper", "Cypher",
#     "Reyna", "Killjoy", "Breach", "Omen", "Jett", "Raze", "Skye", "Yoru",
#     "Astra", "KAY/O", "Chamber", "Neon", "Fade", "Harbor", "Gekko", "Deadlock"
# ]


# teacherSay = [
#     "弱", "沒有用的東西", "上課不可以用電腦", "這樣很不尊重老師", "你們家長同意你們早退我沒有意見", "你們要為自己負責",
#     "上課拉，怎麼還在講話勒", "老師的臉都被你們丟光了", "你們這群混蛋", "這就是我們班", "遲到的還是會遲到", "永遠改不過來",
#     "沒用的東西", "做人不要那麼乘機", "別人去吃屎，你也要跟著去吃是嗎？", "你怎麼會這麼豬頭呢？？？", "豬頭！",
#     "你們班什麼時候衣服才可以全部穿對", "我要說幾次，不准用免洗筷（摔）", "放學前給我檢查才能走"
# ]


# @bot.event
# async def on_message(message):
#     if message.author == bot.user:
#         return
#     if message.content == "hi":
#         await message.channel.send("hi")

#     if message.author == bot.user:
#         return
#     if message.content.startswith("你好"):
#         await message.channel.send("你好啊!")


# @bot.slash_command(name="dice", description="擲骰子")
# async def dice(ctx):
#     await ctx.respond(rd.randint(1, 6))


# @bot.slash_command(name="teacher_says", description="老師說")
# async def teacher_says(ctx):
#     await ctx.respond(teacherSay[rd.randint(0, len(teacherSay) - 1)])


# @bot.slash_command(name="random_map", description="隨機地圖")
# async def map(ctx):
#     await ctx.respond(valorantMap[rd.randint(0, len(valorantMap) - 1)])


# @bot.slash_command(name="random_agent", description="隨機特務")
# async def agent(ctx):
#     await ctx.respond(valorantAgent[rd.randint(0, len(valorantAgent) - 1)])


# @bot.command(description="加入語音頻道")
# async def join(ctx):
#     channel = ctx.author.voice.channel
#     await channel.connect()
#     await ctx.send(f"已加入語音頻道：{ctx.author.voice.channel.name}")


# @bot.command(description="離開語音頻道")
# async def leave(ctx):
#     voice_client = ctx.guild.voice_client
#     await voice_client.disconnect()
#     await ctx.send(f"已離開語音頻道：{ctx.author.voice.channel.name}")

# bot.run(jdata["DISCORD_TOKEN"])  # 運行機器人
