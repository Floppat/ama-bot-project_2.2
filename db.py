import sqlite3

import json
import discord
from discord.ext import commands

from config import database


class DB_Manager:
    def __init__(self, database_name: str):
        self.database = database_name

    def create_tables(self):
        con = sqlite3.connect(self.database)
        with con:
            con.execute('''
                CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY NOT NULL,
                    pet_id INTEGER,
                    tag TEXT,
                    username TEXT NOT NULL,
                    nickname VARCHAR(35),
                    status_id TEXT NOT NULL,
                    coins INTEGER,
                    quiz_record INTEGER,
                    register_date TEXT,
                    xp INTEGER, 
                    FOREIGN KEY(pet_id) REFERENCES pets(id),
                    FOREIGN KEY(status_id) REFERENCES status_keys(id)
            )''')

            con.execute('''
                CREATE TABLE IF NOT EXISTS pets(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    parent_id INTEGER,
                    pet_name VARCHAR(35) NOT NULL,
                    max_hp INTEGER NOT NULL,
                    hp INTEGER NOT NULL,
                    max_sp INTEGER NOT NULL,
                    sp INTEGER NOT NULL,
                    def INTEGER NOT NULL,
                    str INTEGER NOT NULL,
                    xp INTEGER NOT NULL,
                    max_str INTEGER NOT NULL,
                    min_def INTEGER NOT NULL,
                    avg INTEGER NOT NULL,
                    price INTEGER,
                    xp_price INTEGER,
                    FOREIGN KEY(parent_id) REFERENCES users(id) ON DELETE CASCADE
            )''')

            con.execute('''
                CREATE TABLE IF NOT EXISTS status_keys(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    status TEXT NOT NULL
            )''')
            con.commit()

            con.execute('''
                CREATE TABLE IF NOT EXISTS ai_history(
                    id INTEGER PRIMARY KEY NOT NULL,
                    history JSON NOT NULL
            )''')
            con.commit()

            con.execute('''
                CREATE TABLE IF NOT EXISTS ai_channels(
                    id INTEGER PRIMARY KEY NOT NULL,
                    enabled TEXT NOT NULL
            )''')
            con.commit()

    def new_user(self,
                user_id: int,
                pet_id: int | str, 
                tag: str,
                username: str | None, 
                nickname: str, 
                status_id: int, 
                coins: int, 
                quiz_record: int, 
                register_date: str,
                xp: int):
        
        con = sqlite3.connect(self.database)
        with con:
            con.execute(f'''
                INSERT INTO users VALUES
                    ({user_id},{pet_id},'{tag}','{username}',{nickname},{status_id},{coins},{quiz_record},'{register_date}',{xp})
            ''')
            con.commit()


    def new_pet(self,
                parent_id: int,
                pet_name: str,
                max_hp: int,
                hp: int,
                max_sp: int,
                sp: int,
                defense: int,
                str: int,
                xp: int,
                max_str: int,
                min_def: int,
                avg: int,
                price: int,
                xp_price: int):
        
        con = sqlite3.connect(self.database)
        with con:
            con.execute(f'''
                INSERT INTO pets (parent_id, pet_name, max_hp, hp, max_sp, sp, def, str, xp, max_str, min_def, avg, price, xp_price) VALUES
                    ({parent_id},'{pet_name}',{max_hp},{hp},{max_sp},{sp},{defense},{str},{xp},{max_str},{min_def},{avg},{price},{xp_price})
            ''')
            for row in con.execute(f'SELECT id FROM pets WHERE parent_id = {parent_id}'):
                con.execute(f'UPDATE users SET pet_id={row[0]} WHERE id={parent_id}')
            con.commit()


    def new_status(self, status_name: str):
        con = sqlite3.connect(self.database)
        with con:
            con.execute(f'INSERT INTO status_keys (status) VALUES ("{status_name}")')
            con.commit()


    def new_history_id(self, user_id: int, id_type):
        if id_type == 'user':
            text = 'ты бот задача которого поболтать с пользователем'
        elif id_type == 'chat':
            text = 'ты бот задача которого поболтать с пользователем. это - групповой чат. тут сообщения от разных пользователей.'
        else:
            print('type error')
            return
        messages = [{'role':'system', 'text': text}]
        con = sqlite3.connect(self.database)
        history = json.dumps(messages)
        with con:
            con.execute(f' INSERT INTO ai_history (id, history) VALUES (?,?)', (user_id, history))
            con.commit()


    def new_add_channel(self, ctx: commands.Context, bool_arg):
        con = sqlite3.connect(self.database)
        with con:
            con.execute(f'INSERT INTO ai_channels (id, enabled) VALUES (?,?)', (ctx.channel.id, bool_arg))
            con.commit()


    def change(self, table: str, PK: int, column: str, value: int | str | dict):
        con = sqlite3.connect(self.database)
        with con:
            con.execute(f'UPDATE {table} SET {column} = ? WHERE id = {PK}',(value,))
            con.commit()
        return 'успешно изменено'


    def delete(self,table: str, PK: int):
        con = sqlite3.connect(self.database)
        with con:
            con.execute(f'DELETE FROM {table} WHERE id = {PK}')
        return 'успешно удалено'


    def read(self, table: str, PK: int, *columns: tuple | str):
        con = sqlite3.connect(self.database)
        with con:
            cur = con.cursor()
            return cur.execute(f'SELECT {','.join(columns)} FROM {table} WHERE id = {PK}').fetchall()[0] # type: ignore


    def get_PK(self, table: str, col_name: str, col_content: int | str):
        con = sqlite3.connect(self.database)
        with con:
            cur = con.cursor()
            return cur.execute(f'SELECT id FROM {table} WHERE {col_name} = ?',(col_content,)).fetchall()[0][0]


    def leaderboard(self, table: str,page: int, order_by: str):
        con = sqlite3.connect(self.database)
        with con:
            current_page = {}
            offset = page*10 - 10
            limit = page*10
            place = page*10-9
            if table == 'pets':
                SQL_query = f'SELECT id, pet_name, {order_by} FROM {table} ORDER BY {order_by} DESC LIMIT {limit} OFFSET {offset}'
            elif table == 'users':
                SQL_query = f'SELECT nickname, {order_by} FROM {table} ORDER BY {order_by} DESC LIMIT {limit} OFFSET {offset}'
            for row in con.execute(SQL_query):
                current_page[place]= row
                place+=1
            return current_page

    def update(self, PK: int, history):
        con = sqlite3.connect(self.database)
        history = json.dumps(history)
        with con:
            con.execute(f'UPDATE ai_history SET history = ? WHERE id = {PK}',(history,))
            con.commit()
        return 'успешно изменено'
    
    def ai_read(self, PK: int):
        con = sqlite3.connect(self.database)
        with con:
            cur = con.cursor()
            try:
                return json.loads(cur.execute(f'SELECT history FROM ai_history WHERE id = {PK}').fetchall()[0][0])
            except IndexError:
                return False
    
    


# if __name__ == '__main__':
#     db = DB_Manager.init(database)
#     db.new_status('user')
#     db.new_status('administrator')