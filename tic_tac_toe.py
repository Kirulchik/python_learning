import re
from enum import Enum

tiles = [
    [' ', ' ', ' '],
    [' ', ' ', ' '],
    [' ', ' ', ' '],
]


# Oбратная диагональ
# def print_diagonal(arr):
#     for i, value in enumerate(arr):
#         print(value[len(value)-1-i])

# None
def print_tiles(tiles):
    print('--------')
    for tile in tiles:
        print(tile)


# bool
def check_all_symbols_filled(tiles, default_value):
    for row in tiles:
        for symbol in row:
            if default_value == symbol:
                return False

    return True

class Result(Enum):
    WIN = 1
    DRAW = 2
    NOT_FINISHED = 3

# returns Result
def is_game_finished(tiles):
    default_value = ' '
    # rows
    for i, tile in enumerate(tiles):
        all_symbols_equal = True
        curent_symbol = None
        for symbol in tile:
            if curent_symbol == None:
                curent_symbol = symbol

            if curent_symbol != symbol or symbol == default_value:
                all_symbols_equal = False
                break

        if all_symbols_equal:
            return Result.WIN

    # columns
    for i, _ in enumerate(tiles):
        all_symbols_equal = True
        curent_symbol = None
        for j, _ in enumerate(tiles[i]):
            if curent_symbol == None:
                curent_symbol = tiles[j][i]

            if curent_symbol != tiles[j][i] or tiles[j][i] == default_value:
                all_symbols_equal = False
                break

        if all_symbols_equal:
            return Result.WIN

    # diagonals
    all_symbols_equal = True
    all_symbols_equal_reverse = True
    curent_symbol = None
    curent_symbol_reverse = None
    for i, _ in enumerate(tiles):
        reverse_element = tiles[i][len(tiles[i]) - 1 - i]
        element = tiles[i][i]
        if curent_symbol == None:
            curent_symbol = element

        if curent_symbol != element or element == default_value:
            all_symbols_equal = False

        if curent_symbol_reverse == None:
            curent_symbol_reverse = reverse_element

        if curent_symbol_reverse != reverse_element or reverse_element == default_value:
            all_symbols_equal_reverse = False

        if not all_symbols_equal and not all_symbols_equal_reverse:
            break

    if all_symbols_equal:
        return Result.WIN
    if all_symbols_equal_reverse:
        return Result.WIN

    # DRAW
    if check_all_symbols_filled(tiles, default_value):
        return Result.DRAW

    return Result.NOT_FINISHED


def start_game():
    player1 = "1"  # input('Enter first player name:')
    player2 = '2'  # input('enter second player name:')

    curent_player = player1
    symbol = 'x'
    default_symbol = ' '
    while True:
        x = input('player {} turn'.format(curent_player))
        # регулярные выражения
        if not (re.match(r'[1-3]{1},[1-3]{1}', x) and len(x) == 3):
            print('не то!')
            continue
        xy = x.split(',')
        i, j = int(xy[0]) - 1, int(xy[1]) - 1
        if tiles[i][j] != default_symbol:
            print('давай другое!')
            continue
        tiles[i][j] = symbol
        print_tiles(tiles)

        result = is_game_finished(tiles)
        if result != Result.NOT_FINISHED:
            break

        if curent_player == player1:
            curent_player = player2
            symbol = 'o'
        else:
            curent_player = player1
            symbol = 'x'

    if result == Result.WIN:
        res = 'Player {} won'.format(curent_player)
    else:
        res = 'Draw'

    print('Game finished, {}'.format(res))


start_game()

