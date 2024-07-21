import discord
import json
from discord.ext import commands
from core.classes import Cog_Extension

with open("config.json", "r", encoding="utf8") as jfile:
    jdata = json.load(jfile)


class Event(Cog_Extension):
    # Cog 的寫法：
    # @bot.command() -> @commands.command()
    # bot -> self.bot

    # welcome message
    @commands.Cog.listener()
    async def on_member_join(self, member):
        wel_channel = self.bot.get_channel(int(jdata["WELCOME_CHANNEL"]))
        await wel_channel.send(f"歡迎 {member.mention} 加入！")

    # leave message
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        leave_channel = self.bot.get_channel(int(jdata["LEAVE_CHANNEL"]))
        await leave_channel.send(f"{member.mention} 滾遠點")

    # listen message
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        monitor = self.bot.get_channel(int(jdata["MONITOR_CHANNEL"]))
        await monitor.send(
            f'{before.author} 將 "{before.content}" 修改成 "{after.content}"'
        )

    @commands.Cog.listener()
    async def on_message_delete(self, msg):
        monitor = self.bot.get_channel(int(jdata["MONITOR_CHANNEL"]))
        await monitor.send(f'{msg.author} 刪除了 "{msg.content}"')

    # listen voice channel
    @commands.Cog.listener()
    async def on_voice_state_update(
        self,
        member: discord.Member,
        before: discord.VoiceState,
        after: discord.VoiceState,
    ):
        if before.channel is None and after.channel is not None:
            print(f"{member} join {after.channel}")
        elif before.channel is not None and after.channel is None:
            print(f"{member} leave {before.channel}")
        else:
            print(f"{member} move from {before.channel} to {after.channel}")
        # 檢查離開的頻道是否為專屬語音頻道，並且現在是空的
        if (
            before.channel
            and before.channel.members == []
            and before.channel.name.endswith("的頻道")
        ):
            await before.channel.delete()
            print(f"Deleted empty custom channel: {before.channel.name}")

        # 檢查是否加入了設定的動態語音頻道
        if after.channel and after.channel.id == int(jdata["DYNAMIC_CHANNEL"]):
            # 創建一個新的語音頻道，名稱為使用者名稱的頻道
            new_channel = await after.channel.guild.create_voice_channel(
                name=f"【{member.display_name}】的頻道",
                category=after.channel.category,
                rtc_region=after.channel.rtc_region,
            )
            # 將使用者移動到新創建的語音頻道
            await member.move_to(new_channel)
            print(
                f"Created and moved {member} to their own channel: {new_channel.name}"
            )

    # QQ TT
    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.content == "QQ" and msg.author != self.bot.user:
            await msg.channel.send("幫 QQ")
        if msg.content == "TT" and msg.author != self.bot.user:
            await msg.channel.send("幫 TT")


async def setup(bot):
    await bot.add_cog(Event(bot))
