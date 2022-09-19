""" Модуль создаёт игровую сессию лабиринта при запуске сервера. """

import sys
sys.path.append('../')

from labirinth.generation_labirinth import generate_labirinth
from labirinth.generate_pos import generate_pos_boss, generate_pos_player

from settings import amount_skins

import random


def create_session(total_amount_player: int, width, height):
    """ Функция создаёт данные для игры в лабиринт.
    total_amount_player - всего игроков в игре(int).
    width - ширина лабиринта(int).
    height - высота лабиринта(int).
    (return) - (amount_player, labirinth, pos_exit, pos_player). """

    # Создание игровой сессии и данных для игры.
    labirinth, pos_exit = generate_labirinth(width, height)

    # Настройка кол-ва игроков и минотавров:
    # Кол-во минотавров.
    amount_boss = abs(int(input("Amount bosses = ")))

    # Кол-во обычных игроков.
    # Балансирую кол-во минотавров и обычных игроков. Можно только треть от всех игроков.
    if total_amount_player // amount_boss < 3:
        amount_boss = total_amount_player // 3

        # Фикс бага, при котором кол-во минотавров == 0.
        if amount_boss == 0 and total_amount_player > 1:
            amount_boss = 1

    # Кол-во игроков зависит от кол-ва минотавров.
    amount_player = total_amount_player - amount_boss

    # Генерация позиций для игроков и боссов:
    pos_player = generate_pos_player(labirinth, pos_exit, amount_player)
    pos_boss = generate_pos_boss(labirinth, pos_exit, amount_boss)

    # Объединяю людей и минотавров в один список.
    pos_player.extend(pos_boss)
    # Перетусовываю позиции игроков и минотавров.
    random.shuffle(pos_player)

    # Собираю информацию об игроках.
    pos_player_tmp = []
    for i, pos in enumerate(pos_player):
        boss_check = False
        if pos in pos_boss:
            boss_check = True

        # Добавляем данные об игроках.
        pos_player_tmp.append(
            {
                "y": pos_player[i][0],
                "x": pos_player[i][1],
                "boss": boss_check,
                "live": True,
                "nickname": "noname",
                "visible": True,
                "skin": random.randint(0, amount_skins)
            }
        )

    # Итоговый список pos_player.
    pos_player = pos_player_tmp
    print(f"Start server {pos_player = }")

    return amount_player, labirinth, pos_exit, pos_player
