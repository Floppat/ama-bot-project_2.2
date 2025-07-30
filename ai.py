import discord
from discord.ext import commands

from ya import Ai
from functional import db, fetch_args


async def handle_AI(message: discord.Message, additional):
    ai = Ai(await db.ai_read(message.channel.id)) # type: ignore
    await ai.new_prompt(additional + message.content)
    asis = await ai.gpt()
    await ai.asis_ans(asis)
    await db.update(message.channel.id, await ai.get_history())
    return asis

async def check_reg(message):
    try:
        await db.ai_read(message.channel.id)
    except IndexError:
        return'используй /start чтобы начать'

async def init(ctx: commands.Context):
    valid_options = ['disable', 'enable']
    options = await fetch_args('ai', ctx.message.content)

    if options[1] not in valid_options:
        return 'wrong argument'
    elif options[1] == 'enable':
        try: 
            status = (await db.read('ai_channels',ctx.channel.id,'enabled'))[0]
            if status == 'True':
                return 'в этом канале уже включен ИИ'
            else:
                await db.change('ai_channels',ctx.channel.id,'enabled', 'True')
                if await db.ai_read(ctx.channel.id) is False:
                    await db.new_ai_history(ctx.channel.id,'user' if ctx.guild is None else 'chat')
                return 'Все ответы вымышлены и не отражают мнения создателя/бота\nВсе данные могут быть некорректны'
        except IndexError:
            await db.new_ai_channel(ctx, 'True')
            if await db.ai_read(ctx.channel.id) is False:
                await db.new_ai_history(ctx.channel.id,'user' if ctx.guild is None else 'chat')
            return 'Все ответы вымышлены и не отражают мнения создателя/бота\nВсе данные могут быть некорректны'
    elif options[1] == 'disable':
        try: 
            status = (await db.read('ai_channels',ctx.channel.id,'enabled'))[0]
            if status == 'False':
                return 'в этом канале уже отключен ИИ'
            else:
                await db.change('ai_channels',ctx.channel.id,'enabled', 'False')
                return 'успешно отключено'
        except IndexError:
            return 'в этом канале уже отключен ИИ'

async def ai_message(message: discord.Message):
    try:
        if (await db.read('ai_channels',message.channel.id,'enabled'))[0] == 'True':
            if message.guild is None:
                await check_reg(message)
                await message.reply(await handle_AI(message, ''))
            elif 1294711574233092217 in [user.id for user in message.mentions]:
                await check_reg(message)
                await message.reply(await handle_AI(message, f'{message.author.name} написал: '))
    except IndexError:
        pass
