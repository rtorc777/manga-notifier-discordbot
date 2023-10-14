from discord.ext import commands
from dotenv import load_dotenv
import discord
import os
from scraper import scrape_manga, get_user_list, remove_manga

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
async def add(ctx, url):
    user_id = str(ctx.message.author.id)

    scraper = scrape_manga(url, user_id)
    if isinstance(scraper, dict):
        heading = scraper[url]["title"]
        latest_chapter = scraper[url]["latest_chapter"]
        embed = discord.Embed(
            color = discord.Color.dark_purple(),
            title = f'__{heading}__',
            description = f"**Latest Chapter**: {latest_chapter}"
        )

        embed.set_footer(text=f"Succesfully added manga to tracking list")
        embed.set_image(url=scraper[url]["image"])

        await ctx.send(embed=embed)
    else:
        await ctx.send(scraper)


@bot.command()
async def remove(ctx, id):
    id = int(id)
    user_id = str(ctx.message.author.id)

    remove = remove_manga(user_id, id)
    await ctx.send(remove)


@bot.command()
async def list(ctx):
    user = ctx.message.author
    user_id = str(ctx.message.author.id)
    #id = bot.get_user(int(user))
    list = get_user_list(user_id)

    if isinstance(list, str):
        await ctx.send(list) 
    else:
        embed = discord.Embed(
            color = discord.Color.dark_blue(),
            title = str(user.name) + "'s List"
        )

        for id, links in enumerate(list):
            for link, manga in links.items():
                title = manga["title"]
                embed.add_field(name = f'__{title}__', value=f"**Link**: [HERE]({link})\n **ID**: {id}\n **Latest**: " + manga["latest_chapter"], inline=False)

        await ctx.send(embed=embed)
        
bot.run(BOT_TOKEN)