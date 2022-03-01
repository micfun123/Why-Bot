import discord
import datetime
import urllib.request
from discord.ext import commands
from dotenv import load_dotenv
import os
from utils import get_url_json, get_url_image, plugin_enabled
import json

load_dotenv()

API_KEY = os.environ['NASA']

class Nasa(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command(usage = "apod", description = "Astronomy Picture of the day", help = "This command shows the  NASA astronomy picture of the day", extras={"category": ""})
    @commands.check(plugin_enabled)
    async def apod(self, ctx, extra:str=None):
        """
        NASA Astronomy Picture of the Day
        """
        
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        url = 'https://api.nasa.gov/planetary/apod?api_key={NASA}&thumbs=True&hd'
        response = requests.get(url.format(NASA=API_KEY))
        data = response.json()
        embed = discord.Embed(title=data['title'], description=data['explanation'], color=0x00168B)
        if data["media_type"] == "image":
            embed.set_image(url=data["hdurl"])
        elif data["media_type"] == "video":
                embed.set_image(url=data['thumbnail'])
        embed.add_field(name='Link to image of the day/video', value=data['url'], inline=False)
        embed.set_footer(text=f'{date}')
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Nasa(client))
