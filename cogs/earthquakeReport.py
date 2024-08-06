from discord.ext import commands, tasks
from logging.handlers import RotatingFileHandler
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


class EarthquakeReport(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.earthquake_warning.start()
        self.eq_channel_id = 1269606076291092480
        self.eq_report_role_id = 1269980566661632103
        self.cwa_api_key = str(jdata["CWA_API_KEY"])

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
        url = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/E-A0015-001?Authorization={self.cwa_api_key}&limit=1&format=JSON&AreaName="
        try:
            response = requests.get(url)
            response.raise_for_status()
            eqdata = response.json()
        except requests.RequestException as e:
            logger.error(f"Error fetching earthquake data: {e}")
            return

        try:
            data = eqdata["records"]["Earthquake"][0]

            eqEarthquakeNo = str(data["EarthquakeNo"])
            eqReportImageURI = data["ReportImageURI"]
            eqWeb = data["Web"]
            eqOriginTime = data["EarthquakeInfo"]["OriginTime"]
            eqSource = data["EarthquakeInfo"]["Source"]
            eqEpicenter = data["EarthquakeInfo"]["Epicenter"]["Location"]
            eqMag = data["EarthquakeInfo"]["EarthquakeMagnitude"]["MagnitudeValue"]

            # embed message
            embed = discord.Embed(title="地震報告", color=0x28458A)
            embed.set_author(
                name=f"{eqSource}",
                url=f"{eqWeb}",
                icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSqn2zzgCgO91yRfyCEbvCOZmR8OZzOhOe-1w&s",
            )
            embed.set_thumbnail(url=f"{eqReportImageURI}")
            embed.add_field(name="編號", value=f"{eqEarthquakeNo}", inline=True)
            embed.add_field(name="時間", value=f"{eqOriginTime}", inline=True)
            embed.add_field(name="震央", value=f"{eqEpicenter}", inline=False)
            embed.add_field(name="芮氏規模", value=f"{eqMag}", inline=False)

            # send message
            if (
                last_message_embed is None
                or last_message_embed.fields[0].value != eqEarthquakeNo
            ):
                await channel.send(embed=embed, content=f"<@&{self.eq_report_role_id}>")
                logger.info("Sent earthquake report")
        except KeyError as e:
            logger.error(f"Error processing earthquake data: missing key {e}")

    @earthquake_warning.before_loop
    async def before_earthquake_warning(self):
        await self.bot.wait_until_ready()


async def setup(bot: commands.Bot):
    await bot.add_cog(EarthquakeReport(bot))
