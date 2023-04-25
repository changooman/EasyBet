# bot.py
import os

import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands

load_dotenv()
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='/', intents=intents)
TOKEN = os.getenv('DISCORD_TOKEN')
extension_list = ['slotmachines', 'chohan', 'raffles', 'sportsbetting', 'easybetsregister']
@bot.command()
async def load(ctx, extension):
    bot.load_extension(extension)

@bot.command(name='la')
# @commands.has_any_role('EasyBet', 'Admin')
async def load_all(ctx):
    print("We're in!")
    for ext in extension_list:
        await bot.load_extension(ext)
    await bot.tree.sync()


@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(extension)

@bot.command()
async def reload(ctx, extension):
    bot.unload_extension(extension)
    bot.load_extension(extension)

bot.run(TOKEN)