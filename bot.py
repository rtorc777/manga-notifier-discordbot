from discord.ext import commands
from dotenv import load_dotenv
import discord
import os
from scraper import scrape_manga

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Manga bot is ready!")
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("Manga bot is ready!")

@bot.command()
async def hello(ctx):
    await ctx.send('https://avt.mkklcdnv6temp.com/47/c/17-1583496962.jpg')

@bot.command()
async def test(ctx, link):
    scraper = scrape_manga(link)
    await ctx.send(scraper)

bot.run(BOT_TOKEN)