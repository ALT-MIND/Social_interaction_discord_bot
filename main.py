import os
import discord
import psycopg2
import TenGiphPy
import dropbox
from random import randint
from discord.ext import commands

TOKEN = os.environ['Discord']
GIPHY = TenGiphPy.Giphy(token=os.environ['Giphy'])
TENOR = TenGiphPy.Tenor(token=os.environ['Tenor'])
DATABASE_URL = os.environ['DATABASE_URL']
BOT = commands.Bot(command_prefix='?')

def set_rand_color():
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)
    return r, g, b


async def get_database_data(command):
    global DATABASE_URL
    db = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = db.cursor()
    cursor.execute(command)
    c = cursor.fetchone()
    db.close()
    return c


async def get_gif(theme):
    w = randint(0, 100)
    if w % 2 == 0:
        url = TENOR.random(theme)
    else:
        url = GIPHY.random(tag=theme)['data']['images']['downsized_large']['url']
    return url


@BOT.command()
async def shake_hands(ctx, arg):
    await ctx.message.delete()
    gif = await get_gif('handshake')
    title = f'{ctx.message.author.mention} пожал руку {arg} :handshake:'
    r, g, b = set_rand_color()
    embed = discord.Embed(
        description=title,
        colour=discord.Colour.from_rgb(r, g, b)
    )
    embed.set_image(url=gif)
    await ctx.send(embed=embed)


@BOT.command()
async def press_f(ctx, arg):
    await ctx.message.delete()
    gif = await get_gif('press f')
    title = f'Pay respect {arg}'
    r, g, b = set_rand_color()
    embed = discord.Embed(
        description=title,
        colour=discord.Colour.from_rgb(r, g, b)
    )
    embed.set_image(url=gif)
    await ctx.send(embed=embed)

BOT.run(TOKEN)
