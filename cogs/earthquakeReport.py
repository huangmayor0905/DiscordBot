from discord.ext import commands, tasks
from logging.handlers import RotatingFileHandler
from datetime import datetime, timedelta, timezone
import asyncio
import discord
import json
import logging
import requests

# load config
with open("config.json", "r", encoding="utf8") as jfile:
    jdata = json.load(jfile)


# set up logging
log_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
log_file = "earthquake_report.log"

file_handler = RotatingFileHandler(log_file, maxBytes=1024 * 1024, backupCount=3)
file_handler.setFormatter(log_formatter)
file_handler.setLevel(logging.INFO)

logger = logging.getLogger("earthquake_report")
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)


def str_to_time(time_str):
    return datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")


class EarthquakeReport(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.earthquake_warning.start()
        self.eq_channel_id = int(jdata["guilds"]["eqReportChannelID"])
        self.eq_report_role_id = int(jdata["roles"]["eqReportID"])
        self.cwa_api_key = str(jdata["CWA_API_KEY"])
        self.last_processed_eq = None

    def cog_unload(self):
        self.earthquake_warning.cancel()

    @tasks.loop(minutes=1)
    async def earthquake_warning(self):
        channel = self.bot.get_channel(self.eq_channel_id)

        # Get channel lastest embed
        try:
            messages = [message async for message in channel.history(limit=1)]
            last_message_embed = (
                messages[0].embeds[0] if messages and messages[0].embeds else None
            )
        except Exception as e:
            logger.error(f"Error fetching message history: {e}")
            last_message_embed = None

        # Get earthquake data
        # 顯著有感地震報告
        bigEQurl = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/E-A0015-001?Authorization={self.cwa_api_key}&limit=1&format=JSON&AreaName="
        try:
            response = requests.get(bigEQurl)
            response.raise_for_status()
            bigEQdata = response.json()
        except requests.RequestException as e:
            logger.error(f"Error fetching big earthquake data: {e}")
            return

        # 小區域有感地震報告
        smallEQurl = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/E-A0016-001?Authorization={self.cwa_api_key}&limit=1&format=JSON&AreaName="
        try:
            response = requests.get(smallEQurl)
            response.raise_for_status()
            smallEQdata = response.json()
        except requests.RequestException as e:
            logger.error(f"Error fetching small earthquake data: {e}")
            return


        try:
            # 判斷哪個地震資料較新
            bigeqTime = str(bigEQdata["records"]["Earthquake"][0]["EarthquakeInfo"]["OriginTime"])
            smalleqTime = str(smallEQdata["records"]["Earthquake"][0]["EarthquakeInfo"]["OriginTime"])
            if str_to_time(bigeqTime) > str_to_time(smalleqTime):
                eqdata = bigEQdata
            else:
                eqdata = smallEQdata
        except KeyError as e:
            logger.error(f"Error processing earthquake data: missing key {e}")
            return
        
        # Check if the earthquake data is the same as the last processed one
        try:
            # 地震編號
            eqNo = str(eqdata["records"]["Earthquake"][0]["EarthquakeNo"])
            # 地震時間
            eqTime = str(eqdata["records"]["Earthquake"][0]["EarthquakeInfo"]["OriginTime"])
            eq_identifier = f"{eqNo}_{eqTime}"
            if self.last_processed_eq == eq_identifier:
                logger.info("No new earthquake data")
                return
        except KeyError as e:
            logger.error(f"Error processing earthquake data: missing key {e}")
            return

        try:
            iconURL = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSqn2zzgCgO91yRfyCEbvCOZmR8OZzOhOe-1w&s"
            # 地震報告圖片
            eqReportImage = eqdata["records"]["Earthquake"][0]["ReportImageURI"]
            # 地震報告網址
            eqWeb = eqdata["records"]["Earthquake"][0]["Web"]
            # 地震資料來源
            eqSource = eqdata["records"]["Earthquake"][0]["EarthquakeInfo"]["Source"]
            # 震央位置
            eqEpicenter = eqdata["records"]["Earthquake"][0]["EarthquakeInfo"]["Epicenter"]["Location"]
            # 芮氏規模
            eqMag = eqdata["records"]["Earthquake"][0]["EarthquakeInfo"]["EarthquakeMagnitude"]["MagnitudeValue"]

            # 轉換時間為時間戳
            tz = timezone(timedelta(hours=8))
            datetime_eqTime_stamp = datetime.strptime(eqTime, "%Y-%m-%d %H:%M:%S").replace(tzinfo=tz).timestamp()

            # embed message
            embed = discord.Embed(title="地震報告", color=0x28458A)
            embed.set_author(name=f"{eqSource}", url=f"{eqWeb}", icon_url=iconURL)
            embed.set_thumbnail(url=f"{eqReportImage}")
            embed.add_field(name="編號", value=f"{eqNo}", inline=True)
            embed.add_field(name="時間", value=f"{eqTime} (<t:{int(datetime_eqTime_stamp)}:R>)", inline=True)
            embed.add_field(name="震央", value=f"{eqEpicenter}", inline=False)
            embed.add_field(name="芮氏規模", value=f"{eqMag}", inline=False)

            # send message if last message is None or the time is different
            if (last_message_embed is None or last_message_embed.fields[1].value[:19] != eqTime):
                # 如果是顯著有感地震，就 @地震報告，否則不 @
                if eqNo[3:] != "000":
                    await channel.send(embed=embed, content=f"<@&{self.eq_report_role_id}>")
                else:
                    await channel.send(embed=embed)
                logger.info("Sent earthquake report")
                self.last_processed_eq = eq_identifier
        except KeyError as e:
            logger.error(f"Error processing earthquake data: missing key {e}")

    @earthquake_warning.before_loop
    async def before_earthquake_warning(self):
        await self.bot.wait_until_ready()

    @earthquake_warning.after_loop
    async def after_earthquake_warning(self):
        logger.info("Earthquake warning loop has stopped")


async def setup(bot: commands.Bot):
    await bot.add_cog(EarthquakeReport(bot))
