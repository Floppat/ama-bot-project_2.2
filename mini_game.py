import discord

from users import registred, get_other_user


async def cmd() -> str:
    return ('/change_nick       (изменяет ник который будет отображатся лидербордах)\n'
            '/change_pet_name   (изменяет имя питомца)\n'
            '/leaderboard       (entity= users/pets ; page= номер страницы ; \n'
            'для users: tag/username/coins/quiz_record/xp , для pets: pet_name/str/xp\n'
            '/prehistory        (предистория, немного сюжета)\n'
            '/guide             (ввод в игру)\n'
            '/me                (данные о вас как о пользователе амы)\n'
            '/stats             (хар-ки вашего питомца)\n'
            '/train             (+сила; -здоровье; -выносливость)\n'
            '/feed              (+здоровье; +выносливость)\n'
            '/sleep             (полное восстановление выносливости)\n'
            '/attack            (-здоровье (ведь это же битва))\n'
            '/shop              (покупка артефактов)\n'
            '!cmd_game')

async def prehistory(interaction: discord.Interaction) -> str:
    await registred(interaction=interaction)
    return ('Давным-давно люди жили в мире с природой и животными...\n'
            'но не так давно, всего каких два века назад, люди забыли свою историю и начали загрязнять природу всё сильнее...\n'
            'Это породило маленьких монстров - Карков\n'
            'Карки хотят уничтожить всю жизнь на земле, и нагревают её, и не остановятся пока земля не превратится в большую печку!\n'
            'Спасите планету - победите всех Карков. Но... проблема в том что люди не видят Карков... Как же быть? Природа поможет! \n' 
            'Ваш питомец - возможно единственный в своём роде, может остановить Карков! Тренируёте его и спасите землю от Карков!\n')

async def guide(interaction: discord.Interaction) -> str:
    await registred(interaction=interaction)
    return ('Каждый день (до использования команды /sleep) вы можете 2 раза потренироватся, затем 1 раз поесть.\n'
            'За день можно 2 раза потренироватся, или 1 раз потренироватся и 1 раз подратся.\n'
            'Совет: лучше перед боем не тренероватся, ведь будет меньше здоровья, а поесть вы не сможете.\n'
            'Тактика про: каждый день 2 раза тренироваться и 1 раз есть, после того как набралось 10 атаки на следущий день идти в бой.\n' 
            'Также противник становится сильнее не по дням, а по боям, так что покупайте артефакты, ведь они повышают защиту.\n'
            'Важно: руководство для новичков и после покупки первого артефакта численные данные становятся неактуальны.\n')

async def user(interaction: discord.Interaction, user_tag: str):
    user = await registred(interaction=interaction)
    if user_tag == 'me':
        return f'{await user.__repr__()}'
    else:
        return await get_other_user(user_tag=user_tag)

async def stats(interaction: discord.Interaction):
    user = await registred(interaction=interaction)
    return f'{await user.pet.__repr__()}'

async def train(interaction: discord.Interaction):
    user = await registred(interaction=interaction)
    return await user.train()

async def feed(interaction: discord.Interaction):
    user = await registred(interaction=interaction)
    return await user.feed()

async def attack(interaction: discord.Interaction):
    user = await registred(interaction=interaction)
    return await user.attack(interaction=interaction)

async def sleep(interaction: discord.Interaction):
    user = await registred(interaction=interaction)
    return await user.sleep()

async def shop(interaction: discord.Interaction, item: str):
    user = await registred(interaction=interaction)
    return await user.shop(item=item)