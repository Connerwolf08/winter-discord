import asyncio
import nextwave
import os
import json
import nextcord
from nextcord.ext import commands, tasks
from setup.funcs import db_write

with open("./setup/config.json") as file_path:
    config = json.load(file_path)

intents = nextcord.Intents.all()
client = commands.Bot(command_prefix=config["main"]["prefix"], intents=intents, application_id="1001495565319815228", help_command=None)

# nextwave node creation

async def connect_nodes():
    await client.wait_until_ready()
    await nextwave.NodePool.create_node(bot=client,
                                        host=config["nextwave"]["host"],
                                        port=config["nextwave"]["port"],
                                        password=config["nextwave"]["password"],
                                        https=config["nextwave"]["https"])

# nextwave ON_READY event for the node

@client.event
async def on_nextwave_node_ready(node: nextwave.Node):
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
    watching = nextcord.ActivityType.watching
    playing = nextcord.ActivityType.playing
    listening = nextcord.ActivityType.listening
    streaming = nextcord.ActivityType.streaming
    competing = nextcord.ActivityType.competing
    
    if type == "w":
        obj = nextcord.Activity(name=content,type=watching)
        return obj        

    if type == "p":
        obj = nextcord.Activity(name=content,type=playing)
        return obj
    
    if type == "l":
        obj = nextcord.Activity(name=content,type=listening)
        return obj

    if type == "s":
        obj = nextcord.Activity(name=content,type=streaming)
        return obj

    if type == "c":
        obj = nextcord.Activity(name=content,type=competing)
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
        fmt = 0
        for guild in client.guilds:
            try:
                fmt = fmt + 1
                await client.tree.sync(guild=guild)
            except Exception:
                pass
        client.tree.copy_global_to(guild=guild)
        await ctx.send(f"Synced: {fmt} Guilds with commands.")
    except Exception as e:
        await ctx.send(f"Sync Error: {e}")

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
        if development_mode:
            await client.start(config["test"]["token"])
        else:
            await client.start(config["main"]["token"])

asyncio.run(main())