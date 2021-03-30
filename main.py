import os
import ast
import asyncio
import psycopg2
import discord
import dropbox
import help_template
from contextlib import closing
from random import randint
from discord.ext import commands
from discord.utils import get

TOKEN = os.environ['Discord']
STORAGE_TOKEN = os.environ['STORAGE_TOKEN']

DATABASE_URL = os.environ['DATABASE_URL']

GOD = os.environ['GOD']
MODERATORS = ast.literal_eval(os.environ['MODERATORS'])
UNIVERSAL_ANSWER = os.environ['UNIVERSAL_ANSWER']
NO = os.environ['NO_NO_NO']

BOT = commands.Bot(command_prefix='|', help_command=None)
STORAGE = dropbox.Dropbox(STORAGE_TOKEN)
HELP = help_template.help()


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
    with closing(psycopg2.connect(DATABASE_URL, sslmode='require')) as database:
        with database.cursor() as cursor:
            cursor.execute(f'select max(id) from {theme};')
            end_point = cursor.fetchone()[0]
            if end_point:
                rand = randint(1, end_point)
                cursor.execute(f'select URL from {theme} where id = {rand};')
                gif = cursor.fetchone()[0]
                return gif
            else:
                return UNIVERSAL_ANSWER


async def put_update(theme):
    file_list = STORAGE.files_list_folder(path='/Social_interaction_discord_bot')
    if theme == 'all':
        for file_name in file_list.entries:
            with closing(psycopg2.connect(DATABASE_URL, sslmode='require')) as database:
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
        with closing(psycopg2.connect(DATABASE_URL, sslmode='require')) as database:
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


async def re_gen_db():
    file_list = STORAGE.files_list_folder(path='/Social_interaction_discord_bot')
    with closing(psycopg2.connect(DATABASE_URL, sslmode='require')) as database:
        with database.cursor() as cursor:
            for table_name in file_list.entries:
                cursor.execute(f'drop table if exists {table_name.name};')
                database.commit()
                cursor.execute(f'create table {table_name.name}(ID serial primary key, URL text);')
                database.commit()
    await put_update('all')


@BOT.event
async def on_ready():
    await BOT.change_presence(activity=discord.Game(name='|help'))


@BOT.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.message.delete()
        message = await ctx.send(f'{ctx.message.author.mention} ты забыл упомянуть кого-либо')
        await asyncio.sleep(5)
        await message.delete()
    elif isinstance(error, commands.CommandError):
        await ctx.message.delete()
        message = await ctx.send(f'{ctx.message.author.mention} я незнаю что ты хочеш, посмотри |help')
        await asyncio.sleep(5)
        await message.delete()


@BOT.command()
async def help(ctx):
    await ctx.message.delete()
    if ctx.message.author.name + '#' + ctx.message.author.discriminator in GOD:
        embed = HELP.god_template(set_rand_color())
        await ctx.author.send(embed=embed)
    elif ctx.message.author.name + '#' + ctx.message.author.discriminator in MODERATORS:
        embed = HELP.moderator_template(set_rand_color())
        await ctx.author.send(embed=embed)
    else:
        embed = HELP.regular_user_template(set_rand_color())
        await ctx.send(embed=embed)


# -----------------social_interaction
@BOT.command()
async def gachi_fight(ctx, arg: discord.User):
    await ctx.message.delete()
    q = await BOT.fetch_user(int(arg.id))
    gif = await get_gif('gachi_fight')
    description = f'{ctx.message.author.mention} делает кусь за жепу {arg.mention}'
    r, g, b = set_rand_color()
    embed = discord.Embed(
        description=description,
        colour=discord.Colour.from_rgb(r, g, b))
    if str(q) == "ALT-MIND#2787":
        embed.set_image(url=NO)
    else:
        embed.set_image(url=gif)
    await ctx.send(embed=embed)


@BOT.command()
async def handshake(ctx, arg):
    await ctx.message.delete()
    gif = await get_gif('handshake')
    description = f'{ctx.message.author.mention} пожал руку {arg} :handshake:'
    r, g, b = set_rand_color()
    embed = discord.Embed(
        description=description,
        colour=discord.Colour.from_rgb(r, g, b))
    embed.set_image(url=gif)
    await ctx.send(embed=embed)


@BOT.command()
async def press_f(ctx, arg):
    await ctx.message.delete()
    gif = await get_gif('press_f')
    description = f'{ctx.message.author.mention} pay respects {arg}'
    r, g, b = set_rand_color()
    embed = discord.Embed(
        description=description,
        colour=discord.Colour.from_rgb(r, g, b))
    embed.set_image(url=gif)
    await ctx.send(embed=embed)


@BOT.command()
async def hug(ctx, arg):
    await ctx.message.delete()
    gif = await get_gif('hug')
    description = f':hugging:  {ctx.message.author.mention} обнимает {arg} :hugging: '
    r, g, b = set_rand_color()
    embed = discord.Embed(
        description=description,
        colour=discord.Colour.from_rgb(r, g, b))
    embed.set_image(url=gif)
    await ctx.send(embed=embed)


@BOT.command()
async def ave_sun(ctx):
    await ctx.message.delete()
    gif = await get_gif('ave_sun')
    r, g, b = set_rand_color()
    emoji = discord.utils.get(BOT.emojis, name='ave_sun')
    description = f'{ctx.message.author.mention} восславляет СОЛНЦЕ'
    embed = discord.Embed(
        title=f'{emoji} AVE SUN {emoji}',
        description=description,
        colour=discord.Colour.from_rgb(r, g, b))
    embed.set_image(url=gif)
    await ctx.send(embed=embed)


@BOT.command()
async def morning(ctx, arg):
    await ctx.message.delete()
    r, g, b = set_rand_color()
    gif = await get_gif('morning')
    if arg == '@everyone':
        if get(ctx.message.author.roles, name="Dungeon Master"):
            description = f'{ctx.message.author.mention} желает доброго утра {arg}'
        else:
            description = f'{ctx.message.author.mention} желает доброго утра'
    else:
        description = f'{ctx.message.author.mention} желает доброго утра {arg}'
    embed = discord.Embed(
        title=':sunrise: Доброе утро :sunrise:',
        description=description,
        colour=discord.Colour.from_rgb(r, g, b))
    embed.set_image(url=gif)
    await ctx.send(embed=embed)


@BOT.command()
async def evening(ctx, arg):
    await ctx.message.delete()
    r, g, b = set_rand_color()
    gif = await get_gif('evening')
    if arg == '@everyone':
        if get(ctx.message.author.roles, name="Dungeon Master"):
            description = f'{ctx.message.author.mention} желает доброй ночи {arg}'
        else:
            description = f'{ctx.message.author.mention} желает доброй ночи'
    else:
        description = f'{ctx.message.author.mention} желает доброй ночи {arg}'
    embed = discord.Embed(
        title=':milky_way: Доброй ночи :milky_way:',
        description=description,
        colour=discord.Colour.from_rgb(r, g, b))
    embed.set_image(url=gif)
    await ctx.send(embed=embed)
# -----------------social interaction

# -----------------moderation functions
@BOT.command()
async def update_db(ctx, arg):
    await ctx.message.delete()
    if ctx.message.author.name + '#' + ctx.message.author.discriminator in MODERATORS:
        await ctx.author.send('Обновляю базу данных')
        await put_update(arg)
        await ctx.author.send('База данных обновленна')


@BOT.command()
async def warn(ctx, member, *args):
    await ctx.message.delete()
    if get(ctx.message.author.roles, name='Серый Кардинал'):
        q = " ".join(args)
        w = q.split(',')
        reason = ""
        for i in w:
            reason += i + '\n'
        n = "\n"
        await ctx.send(f'{member} был предупреждён {ctx.author.mention} Причина: {n + reason}')
        embed = discord.Embed(title="Предупреждение")
        embed.add_field(name="Модератор", value=ctx.author.mention)
        embed.add_field(name="Предупреждённый", value=member)
        embed.add_field(name="Время в UTC", value=str(ctx.message.created_at)[:-7])
        embed.add_field(name="Причина", value=reason)
        embed.colour = discord.Colour.red()
        alley_channel = BOT.get_channel(825625052287467571)
        await alley_channel.send(embed=embed)
# -----------------moderation functions


# ----------------- gods functions
@BOT.command()
async def regenerate_db(ctx):
    if ctx.message.author.name + '#' + ctx.message.author.discriminator in GOD:
        await ctx.message.delete()
        await ctx.author.send('Регенерирую базу данных')
        await re_gen_db()
        await ctx.author.send('Регенерация прошла успешно')
# ----------------- gods functions

BOT.run(TOKEN)
