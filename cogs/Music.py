import json
import wavelink
import discord
from discord import app_commands, Interaction
from discord.ext import commands

with open("./setup/config.json") as file_path:
    config = json.load(file_path)

ico = "https://mir-s3-cdn-cf.behance.net/project_modules/disp/58fbeb70425615.5ba2f09187599.gif"

class Music(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="play", description="Used to play a song in the channel you are in. [A WIP Command]")
    @app_commands.describe(track="The name of the track you want to search on youtube. [urls not supported]")
    async def play(self, interaction: Interaction, track: str):
        try:
            vc = await interaction.user.voice.channel.connect(cls=wavelink.Player)
        except Exception:
            vc: wavelink.Player = interaction.guild.voice_client

        node = wavelink.NodePool.get_node().identifier
        get_track = await wavelink.YouTubeTrack.search(track, return_first=True)
        thumb = get_track.thumb
        await vc.play(get_track)
        await interaction.response.defer()
        embed = discord.Embed(
            title="Music Player - Playing",
            description=get_track,
            colour=discord.Colour.green()
        )
        embed.set_thumbnail(url=thumb)
        embed.set_footer(text=f"Connected to Node: {node}", icon_url=ico)
        await interaction.followup.send(embed=embed)

    @app_commands.command(name="pause", description="Used to pause a song while you talk or something else.")
    async def pause(self, interaction: Interaction):
        node = wavelink.NodePool.get_node().identifier
        vc:wavelink.Player = interaction.guild.voice_client
        await interaction.response.defer()

        if vc.is_paused():
            embed = discord.Embed(
                title="Music Player",
                description= "A song is already paused in the player.",
                colour=discord.Colour.orange()
            )
            embed.set_footer(text=f"Connected to Node: {node}", icon_url=ico)
            await interaction.followup.send(embed=embed)
        else:
            await vc.pause()
            embed = discord.Embed(
                title="Music Player - Paused",
                description= vc.track,
                colour=discord.Colour.gold()
            )
            embed.set_footer(text=f"Connected to Node: {node}", icon_url=ico)
            await interaction.followup.send(embed=embed)    

    @app_commands.command(name="resume", description="Used to resume a song after you done talking or something.")
    async def resume(self, interaction: Interaction):
        node = wavelink.NodePool.get_node().identifier
        vc:wavelink.Player = interaction.guild.voice_client
        await interaction.response.defer()

        if vc.is_playing():
            embed = discord.Embed(
                title="Music Player",
                description= "A song is already playing in the player.",
                colour=discord.Colour.orange()
            )
            embed.set_footer(text=f"Connected to Node: {node}", icon_url=ico)
            await interaction.followup.send(embed=embed)
        else:
            await vc.resume()
            embed = discord.Embed(
                title="Music Player - Resumed",
                description= vc.track,
                colour=discord.Colour.green()
            )
            embed.set_footer(text=f"Connected to Node: {node}", icon_url=ico)
            await interaction.followup.send(embed=embed)

    @app_commands.command(name="skip", description="Used to skip the current song [Queue may not work]")
    async def skip(self, interaction: Interaction):
        node = wavelink.NodePool.get_node().identifier
        vc:wavelink.Player = interaction.guild.voice_client
        await interaction.response.defer()

        if vc.is_playing():
            embed = discord.Embed(
                title="Music Player - Skipped",
                description= vc.track,
                colour=discord.Colour.red()
            )
            embed.set_footer(text=f"Connected to Node: {node}", icon_url=ico)
            await vc.stop()
            await interaction.followup.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Music Player",
                description= "No song is being played in the player.",
                colour=discord.Colour.orange()
            )
            embed.set_footer(text=f"Connected to Node: N/A", icon_url=ico)
            await interaction.followup.send(embed=embed)

async def setup(client):
    await client.add_cog(Music(client))
    