import discord

from config import database
from db import DB_Manager


db = DB_Manager(database)
async def tables():
    await db.create_tables()

class AccessDeined(Exception):
    pass

async def plus_xp(interaction: discord.Interaction):
    await db.change('users',interaction.user.id,'xp',(await db.read('users',interaction.user.id,'xp'))[0]+1)

async def check_status(interaction: discord.Interaction,user_tag: str, sudo:bool):
    my_status = (await db.read('users',interaction.user.id,'status_id'))[0]
    their_status = (await db.read('users',await db.get_PK('users','tag',user_tag),'status_id'))[0]
    if their_status >= my_status:
        raise AccessDeined
    elif sudo is True and int(my_status) != 3:
        raise AccessDeined

async def change_status(interaction: discord.Interaction, status_id: int, user_tag: str):
    try:
        await check_status(interaction, user_tag, True)
        return await db.change('users',await db.get_PK('users','tag',user_tag),'status_id',status_id) + f' новый статус: {(await db.read('status_keys',status_id,'status'))[0]}'
    except IndexError:
        return 'Указан неверный тег или такой пользователь не пользовался ботом.'
    except AccessDeined:
        return 'Недостаточно прав чтобы выполнить.'

async def delete_user(interaction: discord.Interaction, user_tag: str):
    try:
        await check_status(interaction, user_tag, True)
        return db.delete('users',await db.get_PK('users','tag',user_tag))
    except IndexError:
        return 'Указан неверный тег или такой пользователь не пользовался ботом.'
    except AccessDeined:
        return 'Недостаточно прав чтобы выполнить.'


async def fetch_args(command: str, source: str) -> list[str]:
    return source.removeprefix(command).strip().split()