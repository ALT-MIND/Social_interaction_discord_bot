import discord
regular_user = [["|hug  <упоминание человека>", 'Обними любимого человечка'],
                ["|handshake  <упоминание человека>",'#поприветствуй друга'],
                ["|press_f  <упоминание человека>", 'Press F to pay respect'],
                ["|gachi_fight  <упоминание человека>", 'Начать настоящую мужскую борьбу'],
                ['|ave_sun', 'Восславь СОЛНЦЕ'],
                ['|morning <упоминание человека or @everyone>', 'Пожелайте гражданам доброго утра'],
                ['|evening <упоминание человека or @everyone>', 'Пожелайте гражданам доброй ночи']]
moderator = [["|update_db  <all или ОДНА из тем>", "Обновление базы данных мемасиков"],
             ["|warn <<упоминание человека> <через запятую перечисли все грехи>",
              "Добавляет в Аллею славы новое предупреждение"]]

god = [["|regenerate_db", 'Регенерация базы данных']]


class help:

    def __init__(self):
        pass

    def generate_embed(self, embed, user_name):
        for date in user_name:
            embed.add_field(name=date[0], value=date[1], inline=False)
        return embed
    def regular_user_template(self, color):
        r, g, b = color
        embed = discord.Embed(title="**Похоже кому-то нужна помощь**",
                              description="Вот команды которыми ты можешь воспользоватся",
                              colour=discord.Colour.from_rgb(r, g, b))
        embed = self.generate_embed(embed, regular_user)
        return embed


    def moderator_template(self, color):
        r, g, b = color
        embed = discord.Embed(title="**Похоже кому-то нужна помощь**",
                              description="Вот команды которыми ты можешь воспользоватся",
                              colour=discord.Colour.from_rgb(r, g, b))
        embed.add_field(name="Взаимодействие с людьми", value='\u200b', inline=False)
        embed = self.generate_embed(embed, regular_user)
        embed.add_field(name="Взаимодействие с базой данных", value='\u200b', inline=False)
        embed = self.generate_embed(embed, moderator)
        return embed

    def god_template(self, color):
        r, g, b = color
        embed = discord.Embed(title="**Похоже кому-то нужна помощь**",
                              description="Вот команды которыми ты можешь воспользоватся",
                              colour=discord.Colour.from_rgb(r, g, b))
        embed.add_field(name="Взаимодействие с людьми", value='\u200b', inline=False)
        embed = self.generate_embed(embed, regular_user)
        embed.add_field(name="Взаимодействие с базой данных", value='\u200b', inline=False)
        embed = self.generate_embed(embed, moderator)
        embed = self.generate_embed(embed, god)
        return embed