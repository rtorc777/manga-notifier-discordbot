from discord.ext import commands, tasks
from dotenv import load_dotenv
import discord
import os
import datetime
from scraper import scrape_manga, get_user_list, remove_manga, remove_all_manga, check_chapters, check_all_users

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    check_for_latest.start()
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


@bot.command()
async def removeall(ctx):
    user_id = str(ctx.message.author.id)
    remove = remove_all_manga(user_id)
    await ctx.send(remove)
        

def create_embed(manga):
    url = next(iter(manga))
    title = manga[url]["title"]
    latest_chapter = manga[url]["latest_chapter"]

    embed = discord.Embed(
        title = f'__{title}__',
    )
    embed.add_field(name = "", value=f"**Link**: [HERE]({url})\n\n**Latest**: {latest_chapter}", inline=False)
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


@bot.command()
async def check(ctx):
    user_id = str(ctx.message.author.id)
    updates = check_chapters(user_id)

    if updates:
        for manga in updates: 
            embed = create_new_embed(manga)
            await ctx.message.author.send(embed=embed)
    else:
        await ctx.send("No manga updates")
        

@bot.command()
async def checkall(ctx):
    updates = check_all_users()

    if updates:
        for id in updates:
            user = bot.get_user(int(id))
            
            for manga in updates[id]:
                embed = create_new_embed(manga)
                await user.send(embed=embed)
    else:
        await ctx.send("No manga updates")


def create_new_embed(manga):
    url = next(iter(manga))
    latest_chapter = manga[url]["latest_chapter"]
    latest_chapter_link = manga[url]["latest_chapter_link"]
    
    embed = create_embed(manga)
    embed.color = discord.Color.blue()
    embed.set_field_at(index=0, name = "", value=f"**New Chapter Release!**\n\n**Name: **: {latest_chapter}\n\n**Link**: [HERE]({latest_chapter_link})", inline=False)
    return embed


@bot.event
async def on_reaction_add(reaction, user):
    message = reaction.message
    await message.delete()


utc = datetime.timezone.utc

times = [
    datetime.time(hour=10, tzinfo=utc), #6AM EST
    datetime.time(hour=22, tzinfo=utc)  #6PM EST
]

@tasks.loop(time=times)
async def check_for_latest():
    updates = check_all_users()

    if updates:
        for id in updates:
            user = bot.get_user(int(id))
            
            for manga in updates[id]:
                embed = create_new_embed(manga)
                await user.send(embed=embed)


bot.run(BOT_TOKEN)