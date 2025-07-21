import discord

from config import database
from db import DB_Manager


db = DB_Manager(database)
db.create_tables()

class AccessDeined(Exception):
    pass

def plus_xp(interaction: discord.Interaction):
    db.change('users',interaction.user.id,'xp',(db.read('users',interaction.user.id,'xp'))[0]+1)

def check_status(interaction: discord.Interaction,user_tag: str, sudo:bool):
    my_status = db.read('users',interaction.user.id,'status_id')[0]
    their_status = db.read('users',db.get_PK('users','tag',user_tag),'status_id')[0]
    if their_status >= my_status:
        raise AccessDeined
    elif sudo is True and int(my_status) != 3:
        raise AccessDeined

def change_status(interaction: discord.Interaction, status_id: int, user_tag: str):
    try:
        check_status(interaction, user_tag, True)
        return db.change('users',db.get_PK('users','tag',user_tag),'status_id',status_id) + f' новый статус: {db.read('status_keys',status_id,'status')[0]}'
    except IndexError:
        return 'Указан неверный тег или такой пользователь не пользовался ботом.'
    except AccessDeined:
        return 'Недостаточно прав чтобы выполнить.'

def delete_user(interaction: discord.Interaction, user_tag: str):
    try:
        check_status(interaction, user_tag, True)
        return db.delete('users',db.get_PK('users','tag',user_tag))
    except IndexError:
        return 'Указан неверный тег или такой пользователь не пользовался ботом.'
    except AccessDeined:
        return 'Недостаточно прав чтобы выполнить.'


def fetch_args(command: str, source: str) -> list[str]:
    return source.removeprefix(command).strip().split()