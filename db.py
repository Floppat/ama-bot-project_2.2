import aiosqlite
import json
from discord.ext import commands

from config import database


class DB_Manager:
    def __init__(self, database_name: str):
        self.database = database_name


    async def create_tables(self):
        async with aiosqlite.connect(self.database) as con:
            await con.execute('''
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

            await con.execute('''
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

            await con.execute('''
                CREATE TABLE IF NOT EXISTS status_keys(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    status TEXT NOT NULL
            )''')

            await con.execute('''
                CREATE TABLE IF NOT EXISTS ai_history(
                    id INTEGER PRIMARY KEY NOT NULL,
                    history JSON NOT NULL
            )''')

            await con.execute('''
                CREATE TABLE IF NOT EXISTS ai_channels(
                    id INTEGER PRIMARY KEY NOT NULL,
                    enabled TEXT NOT NULL
            )''')
            await con.commit()


    async def new_user(self,
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
        
        async with aiosqlite.connect(self.database) as con:
            await con.execute(f'''
                INSERT INTO users VALUES
                    ({user_id},{pet_id},'{tag}','{username}','{nickname}',{status_id},{coins},{quiz_record},'{register_date}',{xp})
            ''')
            await con.commit()


    async def new_pet(self,
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
        
        async with aiosqlite.connect(self.database) as con:
            await con.execute(f'''
                INSERT INTO pets (parent_id, pet_name, max_hp, hp, max_sp, sp, def, str, xp, max_str, min_def, avg, price, xp_price) VALUES
                    ({parent_id},'{pet_name}',{max_hp},{hp},{max_sp},{sp},{defense},{str},{xp},{max_str},{min_def},{avg},{price},{xp_price})
            ''')
            async with con.execute(f'SELECT id FROM pets WHERE parent_id = {parent_id}') as cur:
                async for row in cur:
                    await con.execute(f'UPDATE users SET pet_id={row[0]} WHERE id={parent_id}')
            await con.commit()


    async def new_status_key(self, status_name: str):
        async with aiosqlite.connect(self.database) as con:
            await con.execute(f'INSERT INTO status_keys (status) VALUES ("{status_name}")')
            await con.commit()


    async def new_ai_history(self, user_id: int, id_type):
        if id_type == 'user':
            text = 'ты бот задача которого поболтать с пользователем'
        elif id_type == 'chat':
            text = 'ты бот задача которого поболтать с пользователем. это - групповой чат. тут сообщения от разных пользователей. "<@1294711574233092217>" - это упоминание тебя, оно не несёт смысловой нагрузки. может присутствовать в сообщении или нет. игнорируй это'
        else:
            print('type error')
            return
        messages = [{'role':'system', 'text': text}]
        history = json.dumps(messages)
        async with aiosqlite.connect(self.database) as con:
            await con.execute(f' INSERT INTO ai_history (id, history) VALUES (?,?)', (user_id, history))
            await con.commit()


    async def new_ai_channel(self, ctx: commands.Context, bool_arg):
        async with aiosqlite.connect(self.database) as con:
            await con.execute(f'INSERT INTO ai_channels (id, enabled) VALUES (?,?)', (ctx.channel.id, bool_arg))
            await con.commit()


    async def change(self, table: str, PK: int, column: str, value: int | str | dict):
        async with aiosqlite.connect(self.database) as con:
            await con.execute(f'UPDATE {table} SET {column} = ? WHERE id = {PK}',(value,))
            await con.commit()
        return 'успешно изменено'


    async def delete(self,table: str, PK: int):
        async with aiosqlite.connect(self.database) as con:
            await con.execute(f'DELETE FROM {table} WHERE id = {PK}')
            await con.commit()
        return 'успешно удалено'


    async def read(self, table: str, PK: int, *columns: tuple | str):
        async with aiosqlite.connect(self.database) as con:                     
            return (await (await con.execute(f'SELECT {','.join(columns)} FROM {table} WHERE id = {PK}')).fetchall())[0] # type: ignore


    async def get_PK(self, table: str, col_name: str, col_content: int | str):
        async with aiosqlite.connect(self.database) as con:
            return (await (await con.execute(f'SELECT id FROM {table} WHERE {col_name} = ?',(col_content,))).fetchall())[0][0] # type: ignore


    async def leaderboard(self, table: str,page: int, order_by: str):
        async with aiosqlite.connect(self.database) as con:
            current_page = {}
            offset = page*10 - 10
            limit = page*10
            place = page*10-9
            if table == 'pets':
                SQL_query = f'SELECT id, pet_name, {order_by} FROM {table} ORDER BY {order_by} DESC LIMIT {limit} OFFSET {offset}'
            elif table == 'users':
                SQL_query = f'SELECT nickname, {order_by} FROM {table} ORDER BY {order_by} DESC LIMIT {limit} OFFSET {offset}'
            async with con.execute(SQL_query) as cur:
                async for row in cur:
                    current_page[place]= row
                    place+=1
            return current_page


    async def update(self, PK: int, history):
        history = json.dumps(history)
        async with aiosqlite.connect(self.database) as con:
            await con.execute(f'UPDATE ai_history SET history = ? WHERE id = {PK}',(history,))
            await con.commit()


    async def ai_read(self, PK: int):
        async with aiosqlite.connect(self.database) as con:
            try:
                return json.loads((await (await con.execute(f'SELECT history FROM ai_history WHERE id = {PK}')).fetchall())[0][0]) # type: ignore
            except IndexError:
                return False



if __name__ == '__main__':
    import asyncio
    async def main():
        db = DB_Manager(database)
        await db.create_tables()
        # await db.new_status_key('user')
        # await db.new_status_key('administrator')
        # await db.new_status_key('superuser')
    asyncio.run(main())