import datetime
import discord
from discord import app_commands, Interaction
from discord.ext import commands
from discord.utils import get

class Log(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            channel = get(member.guild.channels, name='join-leave')
            embed = discord.Embed(
                title=member.name,
                color=discord.Color.green()
            )
            embed.add_field(name="ID", value=member.id, inline=False)
            embed.add_field(name="Account Created", value=member.created_at, inline=False)
            embed.set_thumbnail(url=member.avatar.url)
            embed.timestamp = datetime.datetime.now()
            await channel.send(embed=embed)
        except Exception:
            pass

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        try:
            channel = get(member.guild.channels, name='join-leave')
            embed = discord.Embed(
                title=member.name,
                color=discord.Color.red()
            )
            embed.add_field(name="ID", value=member.id, inline=False)
            embed.add_field(name="Account Created", value=member.created_at, inline=False)
            embed.set_thumbnail(url=member.avatar.url)
            embed.timestamp = datetime.datetime.now()
            await channel.send(embed=embed)
        except Exception:
            pass

    @app_commands.command(name="log", description="This command will create or delete the join-leave channel where the logs are made.")
    async def log(self, interaction: Interaction):
        channel = discord.utils.get(interaction.guild.text_channels, name="join-leave")
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=False, add_reactions=False)
        }
        if channel:
            await channel.delete()
            embed = discord.Embed(
                title="Member Log Channel",
                description="The member log channel is now deleted which will stop the join/leave logs.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.guild.create_text_channel(name="join-leave", overwrites=overwrites)
            embed = discord.Embed(
                title="Member Log Channel",
                description="The member log channel is now created which will contain all join/leave logs.",
                color=discord.Color.green()
            )
            await interaction.response.send_message(embed=embed)

async def setup(client):
    await client.add_cog(Log(client))