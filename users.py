from copy import deepcopy
from discord import Interaction
import datetime

from pets import Enemy, Pet
from functional import db


class User:
    @classmethod
    async def init(cls, data: tuple):
        self = cls()
        self.user_id = data[0]
        self.pet_PK = data[1]
        if None in await db.read('users',data[0],'pet_id'):
            await db.new_pet(data[0],'дружок',100,100,100,100,1,2,0,5,1,1,0,0)
        self.pet = Pet(await db.read('pets', (await db.read('users',data[0],'pet_id'))[0], '*'))
        self.tag = data[2]
        self.username = data[3]
        self.nickname = data[4]
        self.status_PK = data[5]
        self.status = (await db.read('status_keys', data[5], 'status'))[0]
        self.coins = data[6]
        self.quiz_record = data[7]
        self.register_date = data[8]
        self.xp = data[9]
        self.right_answers = 0
        return self

    async def __repr__(self) -> str:
        return (f'--- Информация об игроке {self.nickname} ---\n'
                f'    | username: {self.username}\n'
                f'    | монеты: {self.coins}\n'
                f'    | рекорд в квизе: {self.quiz_record}\n'
                f'    | впервые с амой: {self.register_date}\n'
                f'    | опыт: {self.xp}\n'
                f'    | питомец: {(await db.read('pets',self.pet_PK,'pet_name'))[0]}\n{await self.pet.__repr__()}')


    async def train(self):
        if not await self.pet.can_train():
            return 'Сперва вашему питомцу следует восстановить силы.'
        await self.pet.train()
        await db.change('pets',self.pet_PK,'hp',self.pet.hp)
        await db.change('pets',self.pet_PK,'sp',self.pet.sp)
        await db.change('pets',self.pet_PK,'str',self.pet.str)
        await db.change('pets',self.pet_PK,'xp',self.pet.xp)
        return f'Питомец прошёл изнурительные тренировки:\n{await self.pet.__repr__()}'



    async def feed(self):
        if not await self.pet.can_feed():
            return 'Ваш питомец не голоден.'
        await self.pet.feed()
        await db.change('pets',self.pet_PK,'hp',self.pet.hp)
        return f'Питомец сытно поел.\n{await self.pet.__repr__()}'


    async def attack(self, interaction: Interaction):
        if not await self.pet.can_attack():
            msg = 'Сперва вашему питомцу следует восстановить силы.'
        enemy = Enemy(target_pet=self.pet)
        now_enemy=deepcopy(enemy)
        self.pet.sp -= 60
        while True:
            await enemy.attack(target_pet=self.pet)
            await self.pet.attack(target_pet=enemy)

            if not await self.pet.__bool__():
                msg =f'Вы проиграли! Ваш враг был:{await now_enemy.__repr__()}\nВаши характеристики:\n{await self.pet.__repr__()}'
                break

            if not await enemy.__bool__():
                self.coins += 100
                self.pet.max_str += 2
                self.pet.avg += 2
                self.pet.min_def += 1
                msg = (f'Вы выиграли. Противник стал сильнее. Ваш враг был:{await now_enemy.__repr__()}\n'
                        'Вы заработали 100 монет.\n'
                        f'Итого монет: {self.coins}\n'
                        f'Ваши характеристики:\n{await self.pet.__repr__()}')
                break
        await db.change('pets',self.pet_PK,'hp',self.pet.hp)
        await db.change('pets',self.pet_PK,'sp',self.pet.sp)
        await db.change('users',self.user_id,'coins',self.coins)
        await db.change('pets',self.pet_PK,'max_str',self.pet.max_str)
        await db.change('pets',self.pet_PK,'avg',self.pet.avg)
        await db.change('pets',self.pet_PK,'min_def',self.pet.min_def)
        return msg


    async def sleep(self):
        if not await self.pet.can_sleep():
            return 'Ваш питомец ещё не устал.'
        await self.pet.sleep()
        await db.change('pets',self.pet_PK,'sp',self.pet.sp)
        return f'Питомец выспался:\n{await self.pet.__repr__()}'


    async def shop(self, item: str):
        shop_pets = {
            '1': Pet((self.pet_PK,self.user_id,self.pet.name,self.pet.max_hp,self.pet.hp,120,120,5,2,0,self.pet.max_str,self.pet.min_def,self.pet.avg,400,7)),
            '2': Pet((self.pet_PK,self.user_id,self.pet.name,self.pet.max_hp,self.pet.hp,140,140,15,2,0,self.pet.max_str,self.pet.min_def,self.pet.avg,800,13)),
            '3': Pet((self.pet_PK,self.user_id,self.pet.name,self.pet.max_hp,self.pet.hp,160,160,25,2,0,self.pet.max_str,self.pet.min_def,self.pet.avg,1200,19)),
            '4': Pet((self.pet_PK,self.user_id,self.pet.name,self.pet.max_hp,self.pet.hp,180,180,35,2,0,self.pet.max_str,self.pet.min_def,self.pet.avg,1600,25)),
            '5': Pet((self.pet_PK,self.user_id,self.pet.name,self.pet.max_hp,self.pet.hp,200,200,45,2,0,self.pet.max_str,self.pet.min_def,self.pet.avg,2000,31))
        }
        message_items = '\n'.join([f'{item=}; {await shop_pets[item].shop()}' for item in shop_pets])

        if item not in shop_pets or item in ('?', 'help', 'items'):
            return (f'Важно! При покупке артефактов сбрасывается опыт и сила (так как для питомца подобное снаряжение в новинку).\n'
                    f'Также, враги слабее не станут. Игра рассчитана на убить время когда вам скучно, не торопитесь.\n'
                    f'Доступные для покупки артефакты:\n{message_items}')

        if self.coins < shop_pets[item].price:
            return f'Недостаточно монет: чтобы купить этот артефакт, нужно {shop_pets[item].price} монет.'
        elif self.pet.xp < shop_pets[item].xp_price:
            return f'Недостаточно опыта: чтобы купить этот артефакт, нужно {shop_pets[item].xp_price} опыта.'

        self.coins -= shop_pets[item].price
        self.pet = deepcopy(shop_pets[item])
        await db.change('pets',self.pet_PK,'max_sp',self.pet.max_sp)
        await db.change('pets',self.pet_PK,'sp',self.pet.sp)
        await db.change('pets',self.pet_PK,'def',self.pet.defense)
        await db.change('pets',self.pet_PK,'str',self.pet.str)
        await db.change('pets',self.pet_PK,'xp',self.pet.xp)
        await db.change('users',self.user_id,'coins',self.coins)
        return f'Ваш пет надел артефакт:\n{await self.pet.__repr__()}'


    async def right_answer(self):
        self.right_answers+=1
    async def quizresult(self, interaction: Interaction):
        if self.right_answers == 5:
            job = ', хорошая работа!'
        elif self.right_answers >= 0 and self.right_answers <= 2:
            job = ', попробуйте почитать о глобальном потеплении ещё раз!'
        elif self.right_answers >= 3 and self.right_answers <= 4:
            job = ', неплохой результат, повторите теорию и попробуйте ещё раз!'
        if self.right_answers > self.quiz_record:
            self.quiz_record = self.right_answers
        await interaction.response.send_message(content=f'Вы набрали {self.right_answers}/5 очков{job}\n'
                                                        f'Рекорд:{self.quiz_record}/5 очков.')
        await db.change('users',self.user_id,'quiz_record',self.quiz_record)
        self.right_answers = 0


async def registred(interaction: Interaction):
    try:
        user = await db.read('users',interaction.user.id,'*')
    except IndexError:
        await db.new_user(interaction.user.id,'NULL',interaction.user.name,interaction.user.global_name,'игрок со странным именем',1,0,0,str(datetime.datetime.now()).split()[0],0)
        user = await db.read('users',interaction.user.id,'*')
    return await User.init(user)

async def get_other_user(user_tag: str):
    try:
        other_user =  await db.read('users',await db.get_PK('users','tag',user_tag),'*')
        return await (await User.init(other_user)).__repr__()
    except IndexError:
        return 'Указан неверный тег или такой пользователь не пользовался ботом.'