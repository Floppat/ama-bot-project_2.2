import discord
from discord.ext import commands

from config import token
import functional as fn
from users import registred
from embeds import bcmd,lb_embed
import mini_game
import bullshit
import global_warming 
import ai

bot = commands.Bot(command_prefix='!', intents = discord.Intents.all())


@bot.event
async def on_ready():
    print(f'Бот {bot.user.name} готов.') # type: ignore
    synced = await bot.tree.sync()
    print(f'{len(synced)} / команды доступны.')

    
@bot.tree.command(name='cmd', description='все команды бота')
async def cmd(interaction: discord.Interaction) -> None:
    registred(interaction=interaction)
    await interaction.response.send_message(embed=bcmd)
    fn.plus_xp(interaction=interaction)

@bot.tree.command(name='change_nick', description='изменить ник отображаемый в лидербордах')
async def change_nick(interaction: discord.Interaction, new_nick: str)-> None:
    registred(interaction=interaction)
    await interaction.response.send_message(fn.db.change('users',interaction.user.id,'nickname',new_nick))
    fn.plus_xp(interaction=interaction)

@bot.tree.command(name='change_pet_name', description='изменить кличку питомца')
async def change_pet_name(interaction: discord.Interaction, new_name: str)-> None:
    registred(interaction=interaction)
    await interaction.response.send_message(fn.db.change('pets',(fn.db.read('users',interaction.user.id,'pet_id'))[0],'pet_name',new_name))
    fn.plus_xp(interaction=interaction)

@bot.tree.command(name='leaderboard', description='используйте !cmd для руководства')
async def leaderboard(interaction: discord.Interaction, entity: str, page: int, parameter: str) -> None:
    registred(interaction=interaction)
    page = fn.db.leaderboard(entity,page,parameter) # type: ignore
    await interaction.response.send_message(embed=lb_embed(page,entity,parameter))
    fn.plus_xp(interaction=interaction)


@bot.tree.command(name='change_status', description='изменить статус пользователя')
async def change_status(interaction: discord.Interaction, status_id: int, user_tag: str)-> None:
    registred(interaction=interaction)
    await interaction.response.send_message(fn.change_status(interaction=interaction,status_id=status_id,user_tag=user_tag))

@bot.tree.command(name='delete_user', description='удалить пользователя из базы данных')
async def delete_user(interaction: discord.Interaction, user_tag: str)-> None:
    registred(interaction=interaction)
    await interaction.response.send_message(fn.delete_user(interaction=interaction, user_tag=user_tag))


@bot.command('cmd_game')
async def cmd_game(ctx: commands.Context) -> None:
    await ctx.send(mini_game.cmd())

@bot.tree.command(name='prehistory', description='ура сюжет')
async def prehistory(interaction: discord.Interaction) -> None:
    await interaction.response.send_message(mini_game.prehistory(interaction=interaction))
    fn.plus_xp(interaction=interaction)

@bot.tree.command(name='guide', description='Отображает справку по игре')
async def guide(interaction: discord.Interaction) -> None:
    await interaction.response.send_message(mini_game.guide(interaction=interaction))
    fn.plus_xp(interaction=interaction)

@bot.tree.command(name='user', description='информация о вас (user_tag=me) или другом пользователе')
async def user(interaction: discord.Interaction, user_tag: str) -> None:
    await interaction.response.send_message(mini_game.user(interaction=interaction, user_tag=user_tag))
    fn.plus_xp(interaction=interaction)

@bot.tree.command(name='stats', description='Отображает хар-ки питомца')
async def stats(interaction: discord.Interaction) -> None:
    await interaction.response.send_message(mini_game.stats(interaction=interaction))
    fn.plus_xp(interaction=interaction)

@bot.tree.command(name='train', description='Потренируйте питомца!')
async def train(interaction: discord.Interaction) -> None:
    await interaction.response.send_message(mini_game.train(interaction=interaction))
    fn.plus_xp(interaction=interaction)

@bot.tree.command(name='feed', description='Покормите питомца!')
async def feed(interaction: discord.Interaction) -> None:
    await interaction.response.send_message(mini_game.feed(interaction=interaction))
    fn.plus_xp(interaction=interaction)

@bot.tree.command(name='attack', description=' Настало время драки!')
async def attack(interaction: discord.Interaction) -> None:
    await mini_game.attack(interaction=interaction)
    fn.plus_xp(interaction=interaction)

@bot.tree.command(name='sleep', description='У-устал')
async def sleep(interaction: discord.Interaction) -> None:
    await interaction.response.send_message(mini_game.sleep(interaction=interaction))
    fn.plus_xp(interaction=interaction)

@bot.tree.command(name='shop', description='Напишите ? или help если не знаете ассортимент')
async def shop(interaction: discord.Interaction, item: str) -> None:
    await interaction.response.send_message(mini_game.shop(interaction=interaction, item=item))
    fn.plus_xp(interaction=interaction)


@bot.command('cmd_bullshit')
async def cmd_bullshit(ctx: commands.Context) -> None:
    await ctx.send(bullshit.cmd())

@bot.command('hi')
async def hi(ctx: commands.Context) -> None:
    await ctx.send(bullshit.hi())

@bot.command('his')
async def his(ctx: commands.Context) -> None:
    await ctx.send(bullshit.his())

@bot.command('hist')
async def hist(ctx: commands.Context) -> None:
    await ctx.send(bullshit.hist())

@bot.command('histo')
async def histo(ctx: commands.Context) -> None:
    await ctx.send(bullshit.histo())

@bot.command('pet')
async def pet(ctx: commands.Context) -> None:
    await bullshit.pet(ctx=ctx)


@bot.command('cmd_warming')
async def cmd_warming(ctx: commands.Context) -> None:
    await ctx.send(global_warming.cmd())

@bot.command('about')
async def about(ctx: commands.Context) -> None:
    await ctx.send(global_warming.about())

@bot.command('reasons')
async def reasons(ctx: commands.Context) -> None:
    await ctx.send(global_warming.reasons())

@bot.command('how_help')
async def how_help(ctx: commands.Context) -> None:
    await ctx.send(global_warming.how_help())

@bot.tree.command(name='quiz', description='небольшая викторина о глобальном потеплении')
async def quiz(interaction: discord.Interaction) -> None:
    await global_warming.quiz(interaction=interaction)
    fn.plus_xp(interaction=interaction)


@bot.command('ai')
async def ai_channel(ctx: commands.Context) -> None:
    await ctx.send(ai.init(ctx = ctx))
@bot.event
async def on_message(message: discord.Message):
    await bot.process_commands(message)
    if message.author.id == bot.user.id: # type: ignore
        return
    await ai.ai_message(message)
    


bot.run(token)