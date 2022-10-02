import json
import datetime
import discord
from discord.ext import commands
from discord import app_commands, Interaction
from setup.funcs import praw_get

class Meme(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    with open("./setup/config.json") as file_path:
        config = json.load(file_path)

    @app_commands.command(name='meme', description="A way to get memes from secret sources..........Reddit.")
    async def meme(self, interaction: Interaction):
        meme = await praw_get("Memes")
        embed = discord.Embed(
            title= meme.title,
            color= discord.Color.random()
        )
        embed.set_image(url=meme.url)
        embed.set_footer(text=f"👍: {meme.ups} | 💭: {meme.num_comments}",icon_url=interaction.user.avatar.url)
        embed.timestamp = datetime.datetime.utcnow()
        await interaction.response.send_message(embed=embed)

async def setup(client):
    await client.add_cog(Meme(client))