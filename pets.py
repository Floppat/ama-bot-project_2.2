from __future__ import annotations
import random


class Pet:
    def __init__(self, stats):
        self.id = stats[0]
        self.parent_id  = stats[1]
        self.name  = stats[2]
        self.max_hp  = stats[3]
        self.hp  = stats[4]
        self.max_sp  = stats[5]
        self.sp  = stats[6]
        self.defense = stats[7]
        self.str = stats[8]
        self.xp = stats[9]
        self.max_str = stats[10]
        self.min_def  = stats[11]
        self.avg  = stats[12]
        self.price  = stats[13]
        self.xp_price = stats[14]


    def __repr__(self) -> str:
        return (f'--- Информация о питомце {self.name} ---\n'
                f'    | здоровье: {self.hp}/{self.max_hp}\n'
                f'    | стамина: {self.sp}/{self.max_sp}\n'
                f'    | защита: {self.defense}\n'
                f'    | сила: {self.str}\n'
                f'    | опыт: {self.xp}')


    def __bool__(self) -> bool:
        return self.hp > 0
    def can_attack(self) -> bool:
        return self.sp >= 60
    def attack(self, target_pet):
        damage_dealt = self.str - target_pet.defense
        damage_dealt = damage_dealt if damage_dealt > 0 else 0
        target_pet.hp -= damage_dealt
        target_pet.hp = target_pet.hp if target_pet.hp > 0 else 0


    def can_feed(self) -> bool:
        return self.hp <= 80
    def feed(self):
        self.hp += 20

    def can_sleep(self) -> bool:
        return self.sp <= 40
    def sleep(self):
        self.sp = self.max_sp
    

    def can_train(self) -> bool:
        return self.hp >= 20 and self.sp >= 40
    def train(self):
        self.hp -= 10
        self.sp -= 40
        self.str += 2
        self.xp += 1


    def shop(self) -> str:
        return (f' | стоимость: {self.price}\n'
                f' | необходимо опыта чтобы купить: {self.xp_price}\n'
                f' | стамина: {self.sp}/{self.max_sp}\n'
                f' | защита: {self.sp}/{self.max_sp}\n')



class Enemy:
    def __init__(self, target_pet):
        self.str = random.randint(target_pet.avg, target_pet.max_str)
        self.hp = random.randint(50, 100)
        self.defense = random.randint(target_pet.min_def, target_pet.avg)


    def __repr__(self) -> str:
        return (f'<Здоровье врага: {self.hp},'
                f'сила врага: {self.str}, защита врага: {self.defense}>')


    def __bool__(self) -> bool:
        return self.hp > 0
    def attack(self, target_pet):
        damage_dealt = self.str - target_pet.defense
        damage_dealt = damage_dealt if damage_dealt > 0 else 0
        target_pet.hp -= damage_dealt
        target_pet.hp = target_pet.hp if target_pet.hp > 0 else 0