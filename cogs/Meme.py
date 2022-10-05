import json
import datetime
import nextcord
from nextcord.ext import commands
from nextcord import slash_command, Interaction
from setup.funcs import praw_get

class Meme(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    with open("./setup/config.json") as file_path:
        config = json.load(file_path)

    @slash_command(name='meme', description="A way to get memes from secret sources..........Reddit.")
    async def meme(self, interaction: Interaction):
        meme = await praw_get("Memes")
        embed = nextcord.Embed(
            title= meme.title,
            color= nextcord.Color.random()
        )
        embed.set_image(url=meme.url)
        embed.set_footer(text=f"👍: {meme.ups} | 💭: {meme.num_comments}",icon_url=interaction.user.avatar.url)
        embed.timestamp = datetime.datetime.utcnow()
        await interaction.response.send_message(embed=embed)

def setup(client):
    client.add_cog(Meme(client))