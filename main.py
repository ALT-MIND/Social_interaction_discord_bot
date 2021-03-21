import os
import psycopg2
import discord
import dropbox
from contextlib import closing
from random import randint
from discord.ext import commands

TOKEN = os.environ['Discord']
STORAGE_TOKEN = os.environ['STORAGE_TOKEN']

DB_NAME = os.environ['DB_NAME']
DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']

UNIVERSAL_ANSWER = os.environ['UNIVERSAL_ANSWER']
NO = os.environ['NO_NO_NO']

BOT = commands.Bot(command_prefix='|')
STORAGE = dropbox.Dropbox(STORAGE_TOKEN)


def set_rand_color():
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)
    return r, g, b


def download_file(file_path, file_name):
    metadata, f = STORAGE.files_download(file_path)
    file = open(file_name, 'wb')
    file.write(f.content)
    file.close()


async def get_gif(theme):
    with closing(psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD)) as database:
        with database.cursor() as cursor:
            cursor.execute(f'select max(id) from {theme};')
            end_point = cursor.fetchone()[0]
            if end_point == None:
                return UNIVERSAL_ANSWER
            else:
                rand = randint(1, end_point)
                cursor.execute(f'select URL from {theme} where id = {rand};')
                gif = cursor.fetchone()[0]
                return gif


async def put_update(theme):
    file_list = STORAGE.files_list_folder(path='/Social_interaction_discord_bot')
    if theme == 'all':
        for file_name in file_list.entries:
            with closing(psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD)) as database:
                with database.cursor() as cursor:
                    cursor.execute(f'select URL from {file_name.name}')
                    values = cursor.fetchall()
                    db_values = []
                    for value in values:
                        db_values.append(value[0])
                    download_file(file_name.path_lower, file_name.name)
                    with open(file_name.name, 'rt') as URLs:
                        for URL in URLs:
                            if URL not in db_values:
                                cursor.execute(f"insert into {file_name.name}(URL) values('{URL}')")
                                database.commit()
                    os.remove(file_name.name)
    else:
        with closing(psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD)) as database:
            with database.cursor() as cursor:
                cursor.execute(f'select URL from {theme}')
                values = cursor.fetchall()
                db_values = []
                for value in values:
                    db_values.append(value[0])
                download_file(f'/social_interaction_discord_bot/{theme}', theme)
                with open(theme) as URLs:
                    for URL in URLs:
                        if URL not in db_values:
                            cursor.execute(f"insert into {theme}(URL) values('{URL}')")
                            database.commit()
                    os.remove(theme)


@BOT.command()
async def gachi_fight(ctx, arg: discord.User):
    await ctx.message.delete()
    q = await BOT.fetch_user(int(arg.id))
    gif = await get_gif('gachi_fight')
    title = f'{ctx.message.author.mention} укусил за жепу {arg.mention}'
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
