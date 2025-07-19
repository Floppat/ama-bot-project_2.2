import discord

from config import database
from db import DB_Manager


db =  DB_Manager.init(database)
#db.create_tables()


def plus_xp(interaction: discord.Interaction):
    db.change('users',interaction.user.id,'xp',(db.read('users',interaction.user.id,'xp'))[0]+1)

def change_status(interaction: discord.Interaction, status_id: int, user_tag: str):
    if int((db.read('users',interaction.user.id,'status_id'))[0]) == 2:
        try:
            return db.change('users',db.get_PK('users','tag',user_tag),'status_id',status_id)
        except IndexError:
            return 'Указан неверный тег или такой пользователь не пользовался ботом.'
    else:
        return 'Недостаточно прав чтобы выполнить.'
    
def delete_user(interaction: discord.Interaction, user_tag: str):
    if int((db.read('users',interaction.user.id,'status_id'))[0]) == 2:
        try:
            return db.delete('users',db.get_PK('users','tag',user_tag))
        except IndexError:
            return 'Указан неверный тег или такой пользователь не пользовался ботом.'
    
    else:
        return 'Недостаточно прав чтобы выполнить.'


def fetch_args(command: str, source: str) -> list[str]:
    return source.removeprefix(command).strip().split()