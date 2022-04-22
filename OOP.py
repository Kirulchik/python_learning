import datetime


class Profile:
    def __init__(self, name, surname, birthday_date):
        self.name = name
        self.surname = surname
        self.birthday_date = birthday_date

    def to_string(self):
        return '{} {}'.format(self.surname, self.name)

    def __str__(self):
        return self.to_string() + ' ' + str(self.age())

    def age(self):
        return int((datetime.datetime.now() - datetime.datetime.strptime(self.birthday_date, '%Y-%m-%d')).days / 365)


class Skill:
    def __init__(self, name, damage, type):
        self.name = name
        self.damage = damage
        self.type = type

    def get_name(self):
        return self.name


class Hero:
    def __init__(self, name, hp, skills):
        self.name = name
        self.hp = hp
        self.skills = skills

    def attack(self, other, applied_skill):
        other.hp -= applied_skill.damage

    def get_name(self):
        return self.name

    # def play_card(self, card, target):
    #     self.card.delete(card)
    #     card.play(target)


class MageHero(Hero):

    # def __init__(self, name, hp, skills):
    #     self.name = name
    #     self.hp = hp
    #     self.skills = skills

    def __init__(self, name, hp, skills, heal_amount):
        # Hero.__init__
        super().__init__(name, hp, skills)
        self.heal_amount = heal_amount

    def heal(self):
        self.hp += self.heal_amount

    def attack(self, other, skill):
        # Hero.attack()
        super().attack(other, skill)
        self.heal()


i = 0 # i int = 0
s = 's' # s str = 's'
fireball = Skill('fireball', 20, 'magic')
mage = MageHero('Jinna', 100, [fireball], 20)
hunter = Hero('Hunter', 100, [])

mage.attack(hunter, fireball)
mage.heal()
print(mage.hp)
print(hunter.hp)

def print_name(obj):
    print(obj.get_name())


print_name(mage)
print_name(fireball)

# 3 принципа:
# 1. Инкапсуляци: данные внутри
# 2. Наследование: (зло), унаследование данных и методов у класса предка
# 3. Полиморфизм: возможность определять одинаковый тип поведение(get_name) для разных классов
