import discord
from discord.ext import commands
import logging
import asyncio
import random
import time
import os

client = commands.Bot(command_prefix="Mike")
footer_text = "Open Mic"

@client.event
async def on_ready():
    print("Logged in as:")
    print(client.user.name)
    print(client.user.id)
    print("---------------")
    await client.change_presence(game=discord.Game(name='wit Huskie'))
    
client.run(os.environ['BOT_TOKEN'])
