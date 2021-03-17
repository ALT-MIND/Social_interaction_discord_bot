import os
import sqlite3
import discord
from random import randint
from discord.ext import commands

TOKEN = os.environ['Discord']
DATABASE = os.environ['DATABASE']
BOT = commands.Bot(command_prefix='?')
UNIVERSAL_ANSWER = os.environ['UNIVERSAL_ANSWER']
NO = os.environ['NO_NO_NO']
def set_rand_color():
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)
    return r, g, b


async def get_database_data(command):
    global DATABASE
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    cursor.execute(command)
    c = cursor.fetchone()
    db.close()
    return c


async def get_gif(theme):
    end_point = await get_database_data(f'select max(id) from {theme}')
    if end_point[0] == None:
        return UNIVERSAL_ANSWER
    else:
        rand = randint(1, end_point[0])
        gif = await get_database_data(f'select URL from {theme} where id = {rand}')
        return gif[0]


@BOT.command()
async def handshake(ctx, arg, ):
    await ctx.message.delete()
    gif = await get_gif('handshake')
    title = f'{ctx.message.author.mention} пожал руку {arg} :handshake:'
    r, g, b = set_rand_color()
    embed = discord.Embed(
        description=title,
        colour=discord.Colour.from_rgb(r, g, b))
    embed.set_image(url=gif)
    await ctx.send(embed=embed)


@BOT.command()
async def press_f(ctx, arg):
    await ctx.message.delete()
    gif = await get_gif('press_f')
    title = f'{ctx.message.author.mention} pay respects {arg}'
    r, g, b = set_rand_color()
    embed = discord.Embed(
        description=title,
        colour=discord.Colour.from_rgb(r, g, b))
    embed.set_image(url=gif)
    await ctx.send(embed=embed)


@BOT.command()
async def gachi_fight(ctx, arg : discord.User):
    await ctx.message.delete()
    q = await BOT.fetch_user(int(arg.id))
    gif = await get_gif('gachi_fight')
    title = f'{ctx.message.author.mention} ? {arg.mention}'
    r, g, b = set_rand_color()
    embed = discord.Embed(
        description=title,
        colour=discord.Colour.from_rgb(r, g, b))
    print(q)
    if str(q) == "AlexGeek#2787":
        embed.set_image(url=NO)
    else:
        embed.set_image(url=gif)
    await ctx.send(embed=embed)

@BOT.command()
async def hug(ctx, arg):
    await ctx.message.delete()
    gif = await get_gif('hug')
    title = f':hugging:  {ctx.message.author.mention} обнимает {arg} :hugging: '
    r, g, b = set_rand_color()
    embed = discord.Embed(
        description=title,
        colour=discord.Colour.from_rgb(r, g, b))
    embed.set_image(url=gif)
    await ctx.send(embed=embed)


BOT.run(TOKEN)
