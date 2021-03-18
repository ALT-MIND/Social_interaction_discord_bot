import os
import sqlite3
import discord
import dropbox
from random import randint
from discord.ext import commands

TOKEN = os.environ['Discord']
DATABASE = os.environ['DATABASE']
UNIVERSAL_ANSWER = os.environ['UNIVERSAL_ANSWER']
STORAGE_TOKEN = os.environ['STORAGE_TOKEN']
NO = os.environ['NO_NO_NO']
BOT = commands.Bot(command_prefix='?')
STORAGE = dropbox.Dropbox(STORAGE_TOKEN)


def set_rand_color():
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)
    return r, g, b


async def get_put_database_data(command, get_or_put):
    global DATABASE
    if get_or_put == 'get':
        db = sqlite3.connect(DATABASE)
        cursor = db.cursor()
        cursor.execute(command)
        c = cursor.fetchone()
        db.close()
        return c
    elif get_or_put == 'put':
        db = sqlite3.connect(DATABASE)
        cursor = db.cursor()
        cursor.execute(command)
        db.commit()
        db.close()


async def get_gif(theme):
    end_point = await get_put_database_data(f'select max(id) from {theme}', 'get')
    if end_point[0] == None:
        return UNIVERSAL_ANSWER
    else:
        rand = randint(1, end_point[0])
        gif = await get_put_database_data(f'select URL from {theme} where id = {rand}', 'get')
        return gif[0]


async def download_file(file_path, file_name):
    metadata, f = STORAGE.files_download(file_path)
    file = open(file_name, 'wb')
    file.write(f.content)
    file.close()


async def put_update(theme):
    response = STORAGE.files_list_folder(path='/Social_interaction_discord_bot')
    if theme == 'all':
        for file_name in response.entries:
            await download_file(file_name.path_lower, file_name.name)
            with open(file_name.name, 'rt') as URL:
                read_URL = URL.readline()
                print(read_URL)
                await get_put_database_data(f"INSERT INTO {file_name.name}(URL) SELECT DISTINCT '{read_URL}' FROM {file_name.name} WHERE NOT EXISTS (SELECT URL FROM {file_name.name} WHERE URL = '{read_URL}')", 'put')
            os.remove(file_name.name)
    else:
        await download_file(f'/social_interaction_discord_bot/{theme}', theme)
        with open(theme, 'rt') as URL:
            read_URL = URL.readline()
            await get_put_database_data(f"INSERT INTO {theme}(URL) SELECT DISTINCT '{read_URL}' FROM {theme} WHERE NOT EXISTS (SELECT URL FROM {theme} WHERE URL = '{read_URL}')", 'put')
            os.remove(theme)


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
async def gachi_fight(ctx, arg: discord.User):
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


@BOT.command()
async def update_db(ctx, arg):
    await ctx.message.delete()
    await ctx.send('Обновляю базу данных')
    await put_update(arg)
    await ctx.send('База данных обновленна')


BOT.run(TOKEN)
