import discord
from discord.ext import commands

from ya import Ai
from functional import db, fetch_args



def handle_AI(message, additional):
    ai = Ai(db.ai_read(message.channel.id)) # загрузка памяти
    ai.new_prompt(additional + message.text) # вписываю запрос
    asis = ai.gpt() # генерирую ответ
    ai.asis_ans(asis) # сохраняю ответ
    db.update(message.channel.id, ai.get_history()) # обновляю бд
    return asis

def check_reg(message):
    try:
        db.ai_read(message.channel.id)
    except IndexError:
        return'используй /start чтобы начать'

def init(ctx: commands.Context):
    valid_options = ['disable', 'enable']
    options = fetch_args('ai', ctx.message.content)


    if options[1] not in valid_options:
        return 'wrong argument'
    elif options[1] == 'enable':
        try: 
            status = (db.read('ai_channels',ctx.channel.id,'enabled'))[0]
            if status == 'True':
                return 'в этом канале уже включен ИИ'
            else:
                db.change('ai_channels',ctx.channel.id,'enabled', 'True')
                return 'Все ответы вымышлены и не отражают мнения создателя/бота\nВсе данные могут быть некорректны'
        except IndexError:
            db.new_add_channel(ctx, 'True')
            return 'Все ответы вымышлены и не отражают мнения создателя/бота\nВсе данные могут быть некорректны'
    elif options[1] == 'disable':
        try: 
            status = (db.read('ai_channels',ctx.channel.id,'enabled'))[0]
            if status == 'False':
                return 'в этом канале уже отключен ИИ'
            else:
                db.change('ai_channels',ctx.channel.id,'enabled', 'False')
                return 'успешно отключено'
        except IndexError:
            return 'в этом канале уже отключен ИИ'
        
    

async def ai_message(message: discord.Message): # message: telebot.types.Message
    # if message.from_user.id == message.chat.id: #проверка - групповой чат или лс
    #     check_reg(message)
    #     handle_AI(message, '')
    # elif (message.text is not None and ("@" + str((bot.get_me()).username)) in message.text) or (message.reply_to_message is not None and message.reply_to_message.from_user.id == (bot.get_me()).id): # нечто сложное что написал не я
    #     check_reg(message)
    #     handle_AI(message, f'{message.from_user.full_name} написал: ')
    # else:
    #     pass
    try:
        if (db.read('ai_channels',message.channel.id,'enabled'))[0] == 'True':
            if message.guild is None: #проверка - групповой чат или лс
                check_reg(message)
                await message.reply(handle_AI(message, ''))
            # elif (message.text is not None and ("@" + str((bot.get_me()).username)) in message.text) or (message.reply_to_message is not None and message.reply_to_message.from_user.id == (bot.get_me()).id): # нечто сложное что написал не я
            #      check_reg(message)
            #      handle_AI(message, f'{message.from_user.full_name} написал: ')
        else:
            pass
    except IndexError:
        pass
