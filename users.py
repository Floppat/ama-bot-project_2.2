from copy import deepcopy
from discord import Interaction
import datetime

from pets import Enemy, Pet
from functional import db


class User:
    def __init__(self, data: tuple):
        self.user_id = data[0]
        self.pet_PK = data[1]
        if None in db.read('users',data[0],'pet_id'):
            db.new_pet(data[0],'дружок',100,100,100,100,1,2,0,5,1,1,0,0)
        self.pet = Pet(db.read('pets', (db.read('users',data[0],'pet_id'))[0], '*'))
        self.tag = data[2]
        self.username = data[3]
        self.nickname = data[4]
        self.status_PK = data[5]
        self.status = (db.read('status_keys', data[5], 'status'))[0]
        self.coins = data[6]
        self.quiz_record = data[7]
        self.register_date = data[8]
        self.xp = data[9]
        self.right_answers = 0


    def __repr__(self) -> str:
        return (f'--- Информация об игроке {self.nickname} ---\n'
                f'    | username: {self.username}\n'
                f'    | монеты: {self.coins}\n'
                f'    | рекорд в квизе: {self.quiz_record}\n'
                f'    | впервые с амой: {self.register_date}\n'
                f'    | опыт: {self.xp}\n'
                f'    | питомец: {(db.read('pets',self.pet_PK,'pet_name'))[0]}\n{self.pet}')


    def train(self):
        if not self.pet.can_train():
            return 'Сперва вашему питомцу следует восстановить силы.'
        self.pet.train()
        db.change('pets',self.pet_PK,'hp',self.pet.hp)
        db.change('pets',self.pet_PK,'sp',self.pet.sp)
        db.change('pets',self.pet_PK,'str',self.pet.str)
        db.change('pets',self.pet_PK,'xp',self.pet.xp)
        return f'Питомец прошёл изнурительные тренировки:\n{self.pet}'



    def feed(self):
        if not self.pet.can_feed():
            return 'Ваш питомец не голоден.'
        self.pet.feed()
        db.change('pets',self.pet_PK,'hp',self.pet.hp)
        return f'Питомец сытно поел.\n{self.pet}'


    def attack(self, interaction: Interaction):
        if not self.pet.can_attack():
            msg = 'Сперва вашему питомцу следует восстановить силы.'
        enemy = Enemy(target_pet=self.pet)
        now_enemy=deepcopy(enemy)
        self.pet.sp -= 60
        while True:
            enemy.attack(target_pet=self.pet)
            self.pet.attack(target_pet=enemy)

            if not self.pet:
                msg =f'Вы проиграли! Ваш враг был:{now_enemy}\nВаши характеристики:\n{self.pet}'
                break

            if not enemy:
                self.coins += 100
                self.pet.max_str += 2
                self.pet.avg += 2
                self.pet.min_def += 1
                msg = (f'Вы выиграли. Противник стал сильнее. Ваш враг был:{now_enemy}\n'
                        'Вы заработали 100 монет.\n'
                        f'Итого монет: {self.coins}\n'
                        f'Ваши характеристики:\n{self.pet}')
                break
        db.change('pets',self.pet_PK,'hp',self.pet.hp)
        db.change('pets',self.pet_PK,'sp',self.pet.sp)
        db.change('users',self.user_id,'coins',self.coins)
        db.change('pets',self.pet_PK,'max_str',self.pet.max_str)
        db.change('pets',self.pet_PK,'avg',self.pet.avg)
        db.change('pets',self.pet_PK,'min_def',self.pet.min_def)
        return msg


    def sleep(self):
        if not self.pet.can_sleep():
            return 'Ваш питомец ещё не устал.'
        self.pet.sleep()
        db.change('pets',self.pet_PK,'sp',self.pet.sp)
        return f'Питомец выспался:\n{self.pet}'


    def shop(self, item: str):
        shop_pets = {
            '1': Pet((self.pet_PK,self.user_id,self.pet.name,self.pet.max_hp,self.pet.hp,120,120,5,2,0,self.pet.max_str,self.pet.min_def,self.pet.avg,400,7)),
            '2': Pet((self.pet_PK,self.user_id,self.pet.name,self.pet.max_hp,self.pet.hp,140,140,10,2,0,self.pet.max_str,self.pet.min_def,self.pet.avg,800,13)),
            '3': Pet((self.pet_PK,self.user_id,self.pet.name,self.pet.max_hp,self.pet.hp,160,160,15,2,0,self.pet.max_str,self.pet.min_def,self.pet.avg,1200,19)),
            '4': Pet((self.pet_PK,self.user_id,self.pet.name,self.pet.max_hp,self.pet.hp,180,180,20,2,0,self.pet.max_str,self.pet.min_def,self.pet.avg,1600,25)),
            '5': Pet((self.pet_PK,self.user_id,self.pet.name,self.pet.max_hp,self.pet.hp,200,200,25,2,0,self.pet.max_str,self.pet.min_def,self.pet.avg,2000,31))
        }
        message_items = '\n'.join([f'{item=}; {shop_pets[item].shop()}' for item in shop_pets])

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
        db.change('pets',self.pet_PK,'max_sp',self.pet.max_sp)
        db.change('pets',self.pet_PK,'sp',self.pet.sp)
        db.change('pets',self.pet_PK,'def',self.pet.defense)
        db.change('pets',self.pet_PK,'str',self.pet.str)
        db.change('pets',self.pet_PK,'xp',self.pet.xp)
        db.change('users',self.user_id,'coins',self.coins)
        return f'Ваш пет надел артефакт:\n{self.pet}'


    def right_answer(self):
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
        db.change('users',self.user_id,'quiz_record',self.quiz_record)
        self.right_answers = 0


def registred(interaction: Interaction):
    try:
        user = db.read('users',interaction.user.id,'*')
    except IndexError:
        db.new_user(interaction.user.id,'NULL',interaction.user.name,interaction.user.global_name,'игрок со странным именем',1,0,0,str(datetime.datetime.now()).split()[0],0)
        user = db.read('users',interaction.user.id,'*')
    return User(user)

def get_other_user(user_tag: str):
    try:
        other_user =  db.read('users',db.get_PK('users','tag',user_tag),'*')
        return User(other_user)
    except IndexError:
        return 'Указан неверный тег или такой пользователь не пользовался ботом.'