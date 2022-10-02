import asyncio
import wavelink
import os
import json
import discord
from discord.ext import commands, tasks
from setup.funcs import db_write

with open("./setup/config.json") as file_path:
    config = json.load(file_path)

intents = discord.Intents.all()
client = commands.Bot(command_prefix=config["main"]["prefix"], intents=intents, application_id="1001495565319815228", help_command=None)

# Wavelink node creation

async def connect_nodes():
    await client.wait_until_ready()
    await wavelink.NodePool.create_node(bot=client,
                                        host=config["wavelink"]["host"],
                                        port=config["wavelink"]["port"],
                                        password=config["wavelink"]["password"],
                                        https=config["wavelink"]["https"])

# Wavelink ON_READY event for the node

@client.event
async def on_wavelink_node_ready(node: wavelink.Node):
    print(f'Node: {node.identifier}')

# ON_READY event for the bot

@client.event
async def on_ready():
    print(f"Login: {client.user}")
    client.loop.create_task(connect_nodes())
    await presence_manager.start()

# Core Functions

def ping():
    obj = f"{round(client.latency*100)}ms"
    return obj

def guilds_count():
    obj = len(client.guilds)
    return obj

def member_count():
    members = []
    for guild in client.guilds:
        for member in guild.members:
            members.append(member.id)
    obj = len(members)
    return obj

def activity(content, type):
    watching = discord.ActivityType.watching
    playing = discord.ActivityType.playing
    listening = discord.ActivityType.listening
    streaming = discord.ActivityType.streaming
    competing = discord.ActivityType.competing
    
    if type == "w":
        obj = discord.Activity(name=content,type=watching)
        return obj        

    if type == "p":
        obj = discord.Activity(name=content,type=playing)
        return obj
    
    if type == "l":
        obj = discord.Activity(name=content,type=listening)
        return obj

    if type == "s":
        obj = discord.Activity(name=content,type=streaming)
        return obj

    if type == "c":
        obj = discord.Activity(name=content,type=competing)
        return obj

async def invite(id):
    guild = await client.fetch_guild(id)
    inv = await guild.create_invite()
    return inv

# Core Database Functions

def write_guilds():
    db_write("DROP TABLE IF EXISTS Guilds")
    db_write("CREATE TABLE IF NOT EXISTS Guilds (ID bigint, Member_Count int, Owner_ID bigint)")
    for guild in client.guilds:
        db_write(f"INSERT INTO Guilds VALUES ({guild.id}, {guild.member_count}, {guild.owner_id})")

# Extension Control Slashes

@client.command()
@commands.is_owner()
async def sync(ctx):
    try:
        fmt = await client.tree.sync(guild=ctx.guild)
        await ctx.send(f"Synced: {len(fmt)} Commands")
    except Exception:
        await ctx.send("Sync Error")

@client.command()
@commands.is_owner()
async def load(ctx, extension):
    await client.load_extension(f"cogs.{extension}")
    await ctx.send(f"Loaded: {extension}")

@client.command()
@commands.is_owner()
async def unload(ctx, extension):
    await client.unload_extension(f"cogs.{extension}")
    await ctx.send(f"Unloaded: {extension}")

# Tasks Loops

@tasks.loop(seconds=30)
async def presence_manager():
    await client.change_presence(activity=activity(f"in {guilds_count()} Servers","w"))
    await asyncio.sleep(10)
    await client.change_presence(activity=activity(f"{member_count()} Members","l"))
    await asyncio.sleep(10)
    await client.change_presence(activity=activity("Game of Thrones", "c"))
    await asyncio.sleep(10)

# Extension Loader

async def load():
    counter = 0
    for extension in os.listdir("./cogs"):
        if extension.endswith(".py"):
            await client.load_extension(f"cogs.{extension[:-3]}")
            counter = counter + 1
            print(f"[{counter}] {extension[:-3]}")

# Main Function

async def main(development_mode: bool = False):
    async with client:
        await load()
        client.tree.copy_global_to(guild=discord.Object(id=config["main"]["guild-id"]))
        if development_mode:
            await client.start(config["test"]["token"])
        else:
            await client.start(config["main"]["token"])

asyncio.run(main(True))