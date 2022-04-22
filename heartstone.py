from typing import List
import random
from enum import Enum


class Target:
    def __init__(self, hp: int):
        self.hp = hp

    def take_damage(self, amount):
        self.hp -= amount

    def heal(self, amount):
        self.hp += amount


class Hero(Target):
    def get_name(self):
        pass


class Creature(Target):
    def __init__(self, hp: int, attack: int, name: str):
        self.name = name
        self.attack = attack
        super().__init__(hp)

    def __str__(self):
        return '[{} | {}]'.format(self.attack, self.hp)


class MageHero(Hero):
    def __init__(self, hp: int):
        super().__init__(hp)

    def get_name(self):
        return 'Mage'


class HunterHero(Hero):
    def __init__(self, hp: int):
        super().__init__(hp)

    def get_name(self):
        return 'Hunter'


class Card:
    def __init__(self, mana: int, name: str, action):
        self.name = name
        self.mana = mana
        self.action = action

    def __str__(self):
        return '[{} {}]'.format(self.mana, self.name)


class Desk:
    max_creatures_amount: int = 7

    def __init__(self):
        self.creatures: List[Creature] = []

    def __str__(self):
        desk_str = ''
        for creature in self.creatures:
            desk_str += str(creature)
        return desk_str

    def play_creature(self, creature: Creature) -> bool:
        if len(self.creatures) >= self.max_creatures_amount:
            return False

        self.creatures.append(creature)
        return True


class Player:
    def __init__(self, hero: Hero, mana: int, deck: List[Card], name: str):
        self.name = name
        self.deck = deck
        self.mana = mana
        self.current_mana = mana
        self.hero = hero
        self.desk = Desk()
        self.hand_cards: List[Card] = []

    # todo: в руке должно быть не больше чем 10 карт
    def draw_cards(self, count: int):
        count = min(count, len(self.deck))
        # рандомно вытягиваем карточки из колоды
        cards_to_draw = [self.deck.pop(random.randrange(len(self.deck))) for _ in range(count)]
        # extend = добавляет массив в массив. Пример: [1,2,3].extend([4,5,6]) == [1,2,3,4,5,6]
        self.hand_cards.extend(cards_to_draw)

    def print_cards(self, hidden: bool):
        cards_str = ''
        for card in self.hand_cards:
            if hidden:
                cards_str += '[] '
            else:
                cards_str += str(card)
        return cards_str


class PlayerAction(Enum):
    PLAY_CARD = '1'
    PLAY_ABILITY = '2'
    END_TURN = '3'


class ActionType(Enum):
    TARGET_ACTION = 1
    DESC_ACTION = 2


class TargetAction:
    type = ActionType.TARGET_ACTION

    def play(self, player: Player, target: Target):
        pass


class DescAction:
    type = ActionType.DESC_ACTION

    def play(self, player: Player):
        pass


Action = TargetAction | DescAction


class Heal(TargetAction):
    def __init__(self, amount: int):
        self.amount = amount

    def play(self, player: Player, target: Target) -> bool:
        target.heal(self.amount)
        return True


class Attack(TargetAction):
    def __init__(self, amount: int):
        self.amount = amount

    def play(self, player: Player, target: Target) -> bool:
        target.take_damage(self.amount)
        return True


class SummonCreature(DescAction):
    def __init__(self, creature: Creature):
        self.creature = creature

    def play(self, player: Player):
        return player.desk.play_creature(self.creature)


class Game:
    turn_number: int = 0
    current_player: Player = None
    enemy_player: Player = None

    def __init__(self, player1: Player, player2: Player):
        self.player2 = player2
        self.player1 = player1

    def print_table(self):
        print('------ Turn {} ------'.format(self.turn_number))
        print('--- Enemy mana: {}/{} --- Enemy Hero: {} --- Enemy HP: {}---'.format(
            self.enemy_player.current_mana,
            self.enemy_player.mana,
            self.enemy_player.hero.get_name(),
            self.enemy_player.hero.hp))
        print('--- Cards {} ---'.format(self.enemy_player.print_cards(True)))
        print('--- Enemy Desc : {} ---'.format(self.enemy_player.desk))
        print('--- My desc: {} --- '.format(self.current_player.desk))
        print('--- My cards: {} ---'.format(self.current_player.print_cards(False)))
        print('--- Mana: {}/{} --- Hero: {} --- HP: {} ---\n'.format(
            self.current_player.current_mana,
            self.current_player.mana,
            self.current_player.hero.get_name(),
            self.current_player.hero.hp))

    def switch_players(self):
        tmp: Player = self.enemy_player
        self.enemy_player = self.current_player
        self.current_player = tmp

    def choose_card(self) -> int:
        for i, card in enumerate(self.current_player.hand_cards):
            print('{} - card {}'.format(i, card))
        card = input('Choose card: ')

        if not card.isdigit():
            return self.choose_card()
        number_card = int(card)
        if not len(self.current_player.hand_cards) > number_card >= 0:
            return self.choose_card()
        return number_card

    def choose_target(self, action: TargetAction) -> Target:
        isEnemy = True
        if type(action) == Heal:
            isEnemy = False
            print('0 - Hero')
        elif type(action) == Attack:
            print('0 - Enemy Hero')

        for i, creature in enumerate(self.enemy_player.desk.creatures):
            print('{} - creature {}'.format(i + 1, creature))
        target = input('Choose target: ')

        if not target.isdigit():
            return self.choose_target(action)
        number_target = int(target)
        if number_target == 0:
            if isEnemy:
                return self.enemy_player.hero
            return self.current_player.hero

        if not len(self.enemy_player.desk.creatures) + 1 > number_target >= 1:
            return self.choose_target(action)

        return self.enemy_player.desk.creatures[number_target - 1]

    # todo: сделать ability
    def play_ability(self):
        return

    # todo: сделать play_card
    def play_card(self, number_card) -> bool:
        card = self.current_player.hand_cards[number_card]
        if self.current_player.current_mana < card.mana:
            return False

        result = False
        if card.action.type == ActionType.DESC_ACTION:
            result = card.action.play(self.current_player)
        elif card.action.type == ActionType.TARGET_ACTION:
            result = card.action.play(self.current_player, self.choose_target(card.action))

        if result:
            self.current_player.current_mana -= card.mana
            self.current_player.hand_cards.pop(number_card)
        return result

    def player_action(self) -> bool:
        print('{} - Play Card'.format(PlayerAction.PLAY_CARD.value))
        print('{} - Play Ability'.format(PlayerAction.PLAY_ABILITY.value))
        print('{} - End Turn'.format(PlayerAction.END_TURN.value))
        action = input('player {} make turn: '.format(self.current_player.name))
        match action:
            case PlayerAction.PLAY_CARD.value:
                if len(self.current_player.hand_cards) == 0:
                    print('Your hand is empty')
                    return False
                card = self.choose_card()
                self.play_card(card)
                return False
            case PlayerAction.PLAY_ABILITY.value:
                self.play_ability()
                return False
            case PlayerAction.END_TURN.value:
                return True
            case _:
                print('Ти дурень!')
                self.player_action()
                return False

    def turn(self):
        self.turn_number += 1
        self.current_player.draw_cards(1)
        if self.current_player.mana <= 10:
            self.current_player.mana += 1
        self.current_player.current_mana = self.current_player.mana
        is_turn_finished = False
        while not is_turn_finished:
            self.print_table()
            is_turn_finished = self.player_action()

        self.switch_players()
        print('\n' * 10)

    def start(self):
        self.current_player = self.player1
        self.enemy_player = self.player2
        while not self.is_game_finished():
            self.turn()

    def is_game_finished(self) -> bool:
        if self.current_player.hero.hp == 0:
            return True
        if self.enemy_player.hero.hp == 0:
            return True
        return False

player1 = Player(MageHero(30), 1, [
    Card(3, 'Fireball', Attack(6)),
    Card(3, 'Moon Light', Heal(5)),
    Card(1, 'Wgrlrgrlr', SummonCreature(Creature(3, 2, 'Murlok'))),
    Card(2, 'Ice Blast', Attack(3)),
    Card(5, 'Princess Touch', Heal(8)),
    Card(10, 'Fire Blast', Attack(14)),
    Card(5, 'Russian', SummonCreature(Creature(1, 3, 'Dick'))),
    Card(2, 'Ukrainian', SummonCreature(Creature(5, 7, 'Knight'))),
    Card(4, 'Warrior', SummonCreature(Creature(4, 5, 'Warrior'))),
    Card(4, 'Bad Fireball', Attack(5)),
    Card(6, 'Epic Moon Light', Heal(10)),
    Card(2, 'Your Death', SummonCreature(Creature(5, 2, 'Vova'))),
    Card(3, 'Blast', Attack(5)),
    Card(1, 'Princess', Heal(3)),
    Card(7, 'Wave', Attack(11)),
], 'Kirill')
player2 = Player(HunterHero(30), 1, [
    Card(3, 'Fireball', Attack(6)),
    Card(3, 'Moon Light', Heal(5)),
    Card(1, 'Wgrlrgrlr', SummonCreature(Creature(3, 2, 'Murlok'))),
    Card(2, 'Ice Blast', Attack(3)),
    Card(5, 'Princess Touch', Heal(8)),
    Card(10, 'Fire Blast', Attack(14)),
    Card(5, 'Russian', SummonCreature(Creature(1, 3, 'Dick'))),
    Card(2, 'Ukrainian', SummonCreature(Creature(5, 7, 'Knight'))),
    Card(4, 'Warrior', SummonCreature(Creature(4, 5, 'Warrior'))),
    Card(4, 'Bad Fireball', Attack(5)),
    Card(6, 'Epic Moon Light', Heal(10)),
    Card(2, 'Your Death', SummonCreature(Creature(5, 2, 'Vova'))),
    Card(3, 'Blast', Attack(5)),
    Card(1, 'Princess', Heal(3)),
    Card(7, 'Wave', Attack(11)),
], 'Vova')
Game(player1, player2).start()

a = 1
b = 2

tmp = a
a = b
b = tmp
