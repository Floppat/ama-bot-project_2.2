import discord
from discord.ext import commands
import pathlib

from functional import fetch_args


def cmd() -> str:
    return ('!hi              (1.0)\n'
            '!his             (2.0)\n'
            '!hist            (2.1)\n'
            '!histo           (telebot)\n'
            '!pet\n'
            '!cmd_bullshit')

def hi() -> str:
    return 'just wanted do cool bot... 27/04/24'
def his() -> str:
    return 'big improvement and firs try to add bd... 05/10/24'
def hist() -> str:
    return 'finally normal SQLite db... 09/03/25'
def histo() -> str:
    return 'first attempt to do telebot port... 19/04/25 \nsecond attempt to do telebot port... 05/06/25'
    

async def pet(ctx: commands.Context) -> None:
    valid_images = [image.name for image in pathlib.Path('img/pet/').iterdir()]
    images = fetch_args('pet', ctx.message.content)

    for image in images:
        if f'{image}.gif' in valid_images:
            await ctx.send(file=discord.File(f'img/pet/{image}.gif'))