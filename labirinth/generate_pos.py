""" Модуль предназначен для генерации позиций n игроков.
Генерирует n игроков и m минотавров. """

import random


def manhattan_dist(x1, y1, x2, y2):
    """ Функция для рассчёта Манхэтоновоского расстояния. """

    return abs((x1 - x2) + (y1 - y2))


def generate_pos_player(labirinth: list, exit_pos: tuple, amount: int):
    """ Функция создания спавна n-игроков в лабиринте вдали от выхода
    и не в одной ячейке.

    labirinth - сгенерированный лабиринт(list).
    exit_pos - координаты выхода(tuple)=(y, x).
    amount - количество игроков для спавна(int).
    (return) - список координат [[y, x], ...]. """

    width = len(labirinth[0])
    height = len(labirinth)

    # Дистанция, дальше которой можно расположить игрока.
    good_manh_dist = manhattan_dist(1, 1, height-1, width-1) / 3

    # Список координат расположения игроков.
    pos_player_lst = []

    # Счётчик найденных координа для игроков.
    counter = amount
    while counter:
        x = random.randint(1, width-1)
        y = random.randint(1, height-1)

        if manhattan_dist(exit_pos[1], exit_pos[0], x, y) > good_manh_dist:
            if labirinth[y][x] != 0 and [y, x] not in pos_player_lst:
                counter -= 1
                pos_player_lst.append( [y, x] )

    return pos_player_lst


def generate_pos_boss(labirinth: list, exit_pos: tuple, amount: int):
    """ Функция создания спавна n-минотавров в лабиринте недалеко от выхода
    и не в одной ячейке.

    labirinth - сгенерированный лабиринт(list).
    exit_pos - координаты выхода(tuple)=(y, x).
    amount - количество минотавров для спавна(int).
    (return) - список координат [[y, x], ...]. """

    width = len(labirinth[0])
    height = len(labirinth)

    # Дистанция, дальше которой нельзя расположить расположить минотавра.
    bad_manh_dist = manhattan_dist(1, 1, height-1, width-1) / 3

    # Список координат расположения игроков.
    pos_boss_lst = []

    # Счётчик найденных координа для игроков.
    counter = amount
    while counter:
        x = random.randint(1, width-1)
        y = random.randint(1, height-1)

        tmp_manhattan_dist = manhattan_dist(exit_pos[1], exit_pos[0], x, y)
        if tmp_manhattan_dist < bad_manh_dist and tmp_manhattan_dist != 0:
            if labirinth[y][x] != 0 and [y, x] not in pos_boss_lst:
                counter -= 1
                pos_boss_lst.append( [y, x] )

    return pos_boss_lst
