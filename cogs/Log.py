import datetime
import nextcord
from nextcord import slash_command, Interaction
from nextcord.ext import commands
from nextcord.utils import get

class Log(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            channel = get(member.guild.channels, name='join-leave')
            embed = nextcord.Embed(
                title=member.name,
                color=nextcord.Color.green()
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
            embed = nextcord.Embed(
                title=member.name,
                color=nextcord.Color.red()
            )
            embed.add_field(name="ID", value=member.id, inline=False)
            embed.add_field(name="Account Created", value=member.created_at, inline=False)
            embed.set_thumbnail(url=member.avatar.url)
            embed.timestamp = datetime.datetime.now()
            await channel.send(embed=embed)
        except Exception:
            pass

    @slash_command(name="log", description="This command will create or delete the join-leave channel where the logs are made.")
    async def log(self, interaction: Interaction):
        channel = nextcord.utils.get(interaction.guild.text_channels, name="join-leave")
        overwrites = {
            interaction.guild.default_role: nextcord.PermissionOverwrite(read_messages=True, send_messages=False, add_reactions=False)
        }
        if channel:
            await channel.delete()
            embed = nextcord.Embed(
                title="Member Log Channel",
                description="The member log channel is now deleted which will stop the join/leave logs.",
                color=nextcord.Color.red()
            )
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.guild.create_text_channel(name="join-leave", overwrites=overwrites)
            embed = nextcord.Embed(
                title="Member Log Channel",
                description="The member log channel is now created which will contain all join/leave logs.",
                color=nextcord.Color.green()
            )
            await interaction.response.send_message(embed=embed)

async def setup(client):
    await client.add_cog(Log(client))