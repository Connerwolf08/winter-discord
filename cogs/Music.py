import json
from unicodedata import name
import nextwave
import nextcord
from nextcord import slash_command, SlashOption, Interaction
from nextcord.ext import commands

with open("./setup/config.json") as file_path:
    config = json.load(file_path)

ico = "https://mir-s3-cdn-cf.behance.net/project_modules/disp/58fbeb70425615.5ba2f09187599.gif"

class Music(commands.Cog):
    def __init__(self, client):
        self.client = client

    @slash_command(name="play", description="Used to play a song in the channel you are in. [A WIP Command]")
    async def play(self, interaction: Interaction, track: str = SlashOption(name="track", description="The name of the track you want to search on youtube. [urls not supported]")):
        try:
            vc = await interaction.user.voice.channel.connect(cls=nextwave.Player)
        except Exception:
            vc: nextwave.Player = interaction.guild.voice_client

        node = nextwave.NodePool.get_node().identifier
        get_track = await nextwave.YouTubeTrack.search(track, return_first=True)
        thumb = get_track.thumb
        await vc.play(get_track)
        await interaction.response.defer()
        embed = nextcord.Embed(
            title="Music Player - Playing",
            description=get_track,
            colour=nextcord.Colour.green()
        )
        embed.set_thumbnail(url=thumb)
        embed.set_footer(text=f"Connected to Node: {node}", icon_url=ico)
        await interaction.followup.send(embed=embed)

    @slash_command(name="pause", description="Used to pause a song while you talk or something else.")
    async def pause(self, interaction: Interaction):
        node = nextwave.NodePool.get_node().identifier
        vc:nextwave.Player = interaction.guild.voice_client
        await interaction.response.defer()

        try:
            await vc.pause()
            embed = nextcord.Embed(
                title="Music Player - Paused",
                description= vc.track,
                colour=nextcord.Colour.gold()
            )
            embed.set_footer(text=f"Connected to Node: {node}", icon_url=ico)
            await interaction.followup.send(embed=embed)    
        except Exception as e:
            embed = nextcord.Embed(
                title="Music Player",
                description= "A song is already paused in the player.",
                colour=nextcord.Colour.orange()
            )
            embed.set_footer(text=f"Connected to Node: {node}", icon_url=ico)
            await interaction.followup.send(embed=embed)
            print(e)

    @slash_command(name="resume", description="Used to resume a song after you done talking or something.")
    async def resume(self, interaction: Interaction):
        node = nextwave.NodePool.get_node().identifier
        vc:nextwave.Player = interaction.guild.voice_client
        await interaction.response.defer()
            
        try:
            await vc.resume()
            embed = nextcord.Embed(
                title="Music Player - Resumed",
                description= vc.track,
                colour=nextcord.Colour.green()
            )
            embed.set_footer(text=f"Connected to Node: {node}", icon_url=ico)
            await interaction.followup.send(embed=embed)
        except Exception as e:
            embed = nextcord.Embed(
                title="Music Player",
                description= "A song is already playing in the player.",
                colour=nextcord.Colour.orange()
            )
            embed.set_footer(text=f"Connected to Node: {node}", icon_url=ico)
            await interaction.followup.send(embed=embed)
            print(e)

    @slash_command(name="skip", description="Used to skip the current song [Queue may not work]")
    async def skip(self, interaction: Interaction):
        node = nextwave.NodePool.get_node().identifier
        vc:nextwave.Player = interaction.guild.voice_client
        await interaction.response.defer()

        try:
            embed = nextcord.Embed(
                title="Music Player - Skipped",
                description= vc.track,
                colour=nextcord.Colour.red()
            )
            embed.set_footer(text=f"Connected to Node: {node}", icon_url=ico)
            await vc.stop()
            await interaction.followup.send(embed=embed)
        except Exception as e :
            embed = nextcord.Embed(
                title="Music Player",
                description= "No song is being played in the player.",
                colour=nextcord.Colour.orange()
            )
            embed.set_footer(text=f"Connected to Node: N/A", icon_url=ico)
            await interaction.followup.send(embed=embed)
            print(e)

def setup(client):
    client.add_cog(Music(client))
    