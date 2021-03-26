import discord


class help:

    def __init__(self):
        pass

    def regular_user_template(self, color):
        r, g, b = color
        embed = discord.Embed(title="**Похоже кому-то нужна помощь**",
                              description="Вот команды которыми ты можешь воспользоватся",
                              colour=discord.Colour.from_rgb(r, g, b))
        embed.add_field(name="  |hug  <упоминание человека>", value='Обними любимого человечка', inline=False)
        embed.add_field(name="  |handshake  <упоминание человека>", value='<я не придумал >', inline=False)
        embed.add_field(name="  |press_f  <упоминание человека>", value='Press F to pay respect', inline=False)
        embed.add_field(name="  |gachi_fight  <упоминание человека>", value='<я не придумал >', inline=False)
        return embed


    def moderator_template(self, color):
        r, g, b = color
        embed = discord.Embed(title="**Похоже кому-то нужна помощь**",
                              description="Вот команды которыми ты можешь воспользоватся",
                              colour=discord.Colour.from_rgb(r, g, b))
        embed.add_field(name="Взаимодействие с людьми", value='\u200b', inline=False)
        embed.add_field(name="  |hug  <упоминание человека>", value='Обними любимого человечка', inline=False)
        embed.add_field(name="  |handshake  <упоминание человека>", value='<я не придумал >', inline=False)
        embed.add_field(name="  |press_f  <упоминание человека>", value='Press F to pay respect', inline=False)
        embed.add_field(name="  |gachi_fight  <упоминание человека>", value='<я не придумал >', inline=False)
        embed.add_field(name="Взаимодействие с базой данных", value='\u200b', inline=False)
        embed.add_field(name="  |update_db  <all или тема из ^ >", value='Обновление базы данных мемасиков', inline=False)
        return embed

    def god_template(self, color):
        r, g, b = color
        embed = discord.Embed(title="**Похоже кому-то нужна помощь**",
                              description="Вот команды которыми ты можешь воспользоватся",
                              colour=discord.Colour.from_rgb(r, g, b))
        embed.add_field(name="Взаимодействие с людьми", value='\u200b', inline=False)
        embed.add_field(name="  |hug  <упоминание человека>", value='Обними любимого человечка', inline=False)
        embed.add_field(name="  |handshake  <упоминание человека>", value='<я не придумал >', inline=False)
        embed.add_field(name="  |press_f  <упоминание человека>", value='Press F to pay respect', inline=False)
        embed.add_field(name="  |gachi_fight  <упоминание человека>", value='<я не придумал >', inline=False)
        embed.add_field(name="Взаимодействие с базой данных", value='\u200b', inline=False)
        embed.add_field(name="  |update_db  <all или тема из ^ >", value='Обновление базы данных мемасиков', inline=False)
        embed.add_field(name="  |regenerate_db", value='Регенерация базы данных', inline=False)
        return embed