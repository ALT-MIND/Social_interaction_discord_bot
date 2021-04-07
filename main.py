import os
import ast
import psycopg2
import asyncio
import discord
import dropbox
from datetime import datetime, timedelta, timezone
from contextlib import closing
from random import randint
from discord.ext import commands, tasks
from discord.utils import get
import help_template

TOKEN = os.environ['Discord']
STORAGE_TOKEN = os.environ['STORAGE_TOKEN']

DATABASE_URL = os.environ['DATABASE_URL']

GOD = os.environ['GOD']
MODERATORS = ast.literal_eval(os.environ['MODERATORS'])
UNIVERSAL_ANSWER = os.environ['UNIVERSAL_ANSWER']
NO = os.environ['NO_NO_NO']

GUILD = None
GUILD_ID = os.environ['GUILD_ID']
ALLEY_CHANNEL = os.environ['ALLEY_CHANNEL']
INTENTS = discord.Intents.all()
BOT = commands.Bot(command_prefix='|', help_command=None, intents=INTENTS)
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
                    cursor.execute(f'select URL from {file_name.name};')
                    values = cursor.fetchall()
                    db_values = []
                    for value in values:
                        db_values.append(value[0])
                    download_file(file_name.path_lower, file_name.name)
                    with open(file_name.name, 'rt') as URLs:
                        for URL in URLs:
                            if URL not in db_values:
                                cursor.execute(f"insert into {file_name.name}(URL) values('{URL}');")
                                database.commit()
                    os.remove(file_name.name)
    else:
        with closing(psycopg2.connect(DATABASE_URL, sslmode='require')) as database:
            with database.cursor() as cursor:
                cursor.execute(f'select URL from {theme};')
                values = cursor.fetchall()
                db_values = []
                for value in values:
                    db_values.append(value[0])
                download_file(f'/social_interaction_discord_bot/{theme}', theme)
                with open(theme) as URLs:
                    for URL in URLs:
                        if URL not in db_values:
                            cursor.execute(f"insert into {theme}(URL) values('{URL}');")
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
    global GUILD
    await BOT.change_presence(activity=discord.Game(name='|help'))
    GUILD = BOT.get_guild(int(GUILD_ID))
    job.start()


@BOT.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.message.delete()
        message = await ctx.send(f'{ctx.message.author.mention} ты забыл упомянуть кого-либо')
        await asyncio.sleep(5)
        await message.delete()
    elif isinstance(error, commands.CommandError):
        await ctx.message.delete()
        message = await ctx.send(f'{ctx.message.author.mention} я незнаю что ты хочешь, посмотри |help')
        await asyncio.sleep(10)
        await message.delete()


@tasks.loop(seconds=10)
async def job():
    global GUILD
    with closing(psycopg2.connect(DATABASE_URL, sslmode='require')) as database:
        with database.cursor() as cursor:
            cursor.execute('SELECT user_id FROM potential_slave;')
            dates = cursor.fetchall()
            try:
                usernames = [x[0] for x in dates]
                cursor.execute('SELECT time_to_get_out_of_slavery FROM potential_slave;')
                time = [x[0] for x in cursor.fetchall()]
                slaves = dict(zip(usernames, time))
                time_now = datetime.isoformat(datetime.now(timezone.utc) +
                                              timedelta(hours=3), sep=' ').split('.')[0]
                for slave in slaves:
                    if slaves[slave] == None:
                        pass
                    elif slaves[slave] < time_now:
                        cursor.execute(f'select warning_message_id,evils,number_of_correctional_labor,' +
                                       f"number_of_warning from potential_slave where user_id ='{slave}';")
                        warn_message_id, evils, num_of_cor_labor, num_of_warn = cursor.fetchall()[0]
                        alley_channel = GUILD.get_channel(int(ALLEY_CHANNEL))
                        warn_message = await alley_channel.fetch_message(warn_message_id)
                        member = await GUILD.fetch_member(slave)
                        await member.remove_roles(get(member.guild.roles, name="Slave"))
                        embed = discord.Embed(title="Карта нарушителя", color=0xcbff00)
                        embed.add_field(name="Нарушитель", value=member.mention, inline=True)
                        embed.add_field(name="Количество отработок", value=num_of_cor_labor,
                                        inline=True)
                        embed.add_field(name=" В данный момент в slave?", value=":negative_squared_cross_mark:",
                                        inline=True)
                        embed.add_field(name="Количество полученных предупреждений",
                                        value="0", inline=False)
                        embed.add_field(name="Нарушения:", value=evils.replace(',', '\n'), inline=False)
                        await warn_message.edit(embed=embed)
                        cursor.execute(f'update potential_slave set time_to_get_out_of_slavery = NULL ' +
                                       f'where user_id ={slave};')
                        database.commit()
            except IndexError:
                pass
            except TypeError:
                pass


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
async def bite_ass(ctx, arg: discord.User):
    await ctx.message.delete()
    q = await BOT.fetch_user(int(arg.id))
    gif = await get_gif('bite_ass')
    description = f'{ctx.message.author.mention} делает кусь за жепу {arg.mention}'
    r, g, b = set_rand_color()
    embed = discord.Embed(
        description=description,
        colour=discord.Colour.from_rgb(r, g, b))
    if str(q) == GOD:
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
async def warn(ctx, member: discord.Member, *args):
    await ctx.message.delete()

    if get(ctx.message.author.roles, name='Серый Кардинал') or get(ctx.message.author.roles, name='Памагат'):
        q = " ".join(args)
        new_evils = q.split(',')
        with closing(psycopg2.connect(DATABASE_URL, sslmode='require')) as database:
            with database.cursor() as cursor:

                cursor.execute(f"select warning_message_id from potential_slave where user_id = {member.id} ;")
                if cursor.fetchall():

                    cursor.execute(f'select warning_message_id,evils,number_of_correctional_labor,' +
                                   f"number_of_warning from potential_slave where user_id ='{member.id}';")
                    warn_message_id, db_evils, num_of_cor_labor, num_of_warn = cursor.fetchall()[0]
                    alley_channel = BOT.get_channel(int(ALLEY_CHANNEL))
                    warn_massage = await alley_channel.fetch_message(warn_message_id)
                    evils = db_evils.split(',')
                    for evil in new_evils:
                        if evil not in db_evils:
                            evils.append(evil)
                    evils = ",".join(evils)

                    if num_of_warn + len(new_evils) > 3:
                        embed = discord.Embed(title="Карта нарушителя", color=0xff0000)
                        embed.add_field(name="Нарушитель", value=member.mention, inline=True)
                        embed.add_field(name="Количество отработок", value=num_of_cor_labor + 1,
                                        inline=True)
                        embed.add_field(name=" В данный момент в slave?", value=":white_check_mark:", inline=True)
                        embed.add_field(name="Количество полученных предупреждений",
                                        value="0", inline=False)
                        embed.add_field(name="Нарушения:", value=evils.replace(',', '\n'), inline=False)
                        await warn_massage.edit(embed=embed)
                        time = datetime.isoformat(datetime.now(timezone.utc) +
                                                  timedelta(hours=24 + 3), sep=' ').split('.')[0]
                        cursor.execute(f"update potential_slave set time_to_get_out_of_slavery = '{time}', " +
                                       f"evils = '{evils}'," +
                                       f'number_of_warning = 0,' +
                                       f'number_of_correctional_labor = {num_of_cor_labor + 1}' +
                                       f" where user_id = '{member.id}';")
                        database.commit()
                        await member.add_roles(get(member.guild.roles, name="Slave"))

                    else:
                        embed = discord.Embed(title="Карта нарушителя", color=0xff8200)
                        embed.add_field(name="Нарушитель", value=member.mention, inline=True)
                        embed.add_field(name="Количество отработок", value=num_of_cor_labor,
                                        inline=True)
                        embed.add_field(name=" В данный момент в slave?", value=":negative_squared_cross_mark:",
                                        inline=True)
                        embed.add_field(name="Количество полученных предупреждений",
                                        value=str(num_of_warn + len(new_evils)), inline=False)
                        embed.add_field(name="Нарушения:", value=evils.replace(',', '\n'), inline=False)
                        await warn_massage.edit(embed=embed)
                        cursor.execute(f"update potential_slave set evils = '{evils}'," +
                                       f" number_of_warning = {num_of_warn + len(new_evils)}" +
                                       f" where user_id = '{member.id}';")
                        database.commit()

                else:
                    embed = discord.Embed(title="Карта нарушителя", color=0xff8200)
                    embed.add_field(name="Нарушитель", value=member.mention, inline=True)
                    embed.add_field(name="Количество отработок", value='0',
                                    inline=True)
                    embed.add_field(name=" В данный момент в slave?", value=":negative_squared_cross_mark: ",
                                    inline=True)
                    embed.add_field(name="Количество полученных предупреждений",
                                    value=str(len(new_evils)), inline=False)
                    embed.add_field(name="Нарушения:", value="\n".join(new_evils), inline=False)
                    alley_channel = BOT.get_channel(int(ALLEY_CHANNEL))
                    warn_message = await alley_channel.send(embed=embed)
                    cursor.execute(f"insert into potential_slave(user_id, warning_message_id," +
                                   f"evils, number_of_warning, number_of_correctional_labor)" +
                                   f" values('{member.id}', {warn_message.id}, '{','.join(new_evils)}'," +
                                   f"{len(new_evils)}, 0) ")
                    database.commit()

        reason = ''
        for i in new_evils:
            reason += i + '\n'
        n = '\n'
        await ctx.send(f'{member.mention} был предупреждён {ctx.author.mention} Причина: {n + reason}')
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
