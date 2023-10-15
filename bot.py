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


@bot.event
async def on_command_error(ctx, err):
    await ctx.send("Invalid arguments")


@bot.command()
async def add(ctx, url):
    user_id = str(ctx.message.author.id)
    manga = scrape_manga(url, user_id)

    if isinstance(manga, dict):
        embed = create_embed(manga)
        embed.color = discord.Color.green()
        embed.set_footer(text="Succesfully added manga to tracking list")

        await ctx.send(embed=embed)
    else:
        await ctx.send(manga)


@bot.command()
async def remove(ctx, id: int):
    user_id = str(ctx.message.author.id)
    id = int(id)
    manga = remove_manga(user_id, id)

    if isinstance(manga, dict):
        embed = create_embed(manga)
        embed.color = discord.Color.dark_red()
        embed.set_footer(text="Succesfully removed manga from tracking list")

        await ctx.send(embed=embed)
    else:
        await ctx.send(manga)
        

def create_embed(manga):
    url = next(iter(manga))
    title = manga[url]["title"]
    latest_chapter = manga[url]["latest_chapter"]

    embed = discord.Embed(
        color = discord.Color.green(),
        title = f'__{title}__',
    )

    embed.add_field(name = "", value=f"**Link**: [HERE]({url})\n\n **Latest**: {latest_chapter}", inline=False)
    embed.set_image(url=manga[url]["image"])

    return embed


@bot.command()
async def list(ctx):
    user = ctx.message.author
    user_id = str(ctx.message.author.id)
    list = get_user_list(user_id)

    if isinstance(list, str):
        await ctx.send(list) 
    else:
        embed = discord.Embed(
            color = discord.Color.dark_blue(),
            title = str(user.name) + "'s List"
        )

        for id, urls in enumerate(list):
            for url, manga in urls.items():
                title = manga["title"]
                embed.add_field(name = f'__{title}__ ({id})', value=f"**Link**: [HERE]({url})\n **Latest**: " + manga["latest_chapter"] + "\n\u200B", inline=False)

        await ctx.send(embed=embed)


bot.run(BOT_TOKEN)