import discord
from discord.ext import commands

from ya import Ai
from functional import db, fetch_args


def handle_AI(message: discord.Message, additional):
    ai = Ai(db.ai_read(message.channel.id)) # type: ignore
    ai.new_prompt(additional + message.content)
    asis = ai.gpt()
    ai.asis_ans(asis)
    db.update(message.channel.id, ai.get_history())
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
                if db.ai_read(ctx.channel.id) is False:
                    db.new_history_id(ctx.channel.id,'user' if ctx.guild is None else 'chat')
                return 'Все ответы вымышлены и не отражают мнения создателя/бота\nВсе данные могут быть некорректны'
        except IndexError:
            db.new_add_channel(ctx, 'True')
            if db.ai_read(ctx.channel.id) is False:
                db.new_history_id(ctx.channel.id,'user' if ctx.guild is None else 'chat')
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

async def ai_message(message: discord.Message):
    try:
        if (db.read('ai_channels',message.channel.id,'enabled'))[0] == 'True':
            if message.guild is None:
                check_reg(message)
                await message.reply(handle_AI(message, ''))
            elif 1294711574233092217 in [user.id for user in message.mentions]:
                check_reg(message)
                await message.reply(handle_AI(message, f'{message.author.name} написал: '))
    except IndexError:
        pass
