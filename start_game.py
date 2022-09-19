""" Модуль запуска сессии игры. """


import os
import sys
import pygame

from player_client import Player
from boss_client import Boss
from spectator_client import Spectator


def start_game(nickname, host, port):
    """ Функция запуска игровой сессии.
    Запуск от лица игрока/минотавра/зрителя.
    (return) - None """

    try:
        player = Player(nickname=nickname, host=host, port=int(port))
        # Запуск игры от лица игрока.
        player.start()

    # Ошибка подключения.
    except:
        pygame.display.quit()
        os.system("end_window.py error_server")
        sys.exit()

    if player.flag_death is False and player.flag_win is False:

        try:
            boss =  Boss(
                        player.client_socket, player.session.labirinth,
                        player.session.pos_player, player.session.id_player,
                        player.move_data.id_player_move
                    )
            boss.start()
        # Ошибка подключения.
        except:
            pygame.display.quit()
            os.system("end_window.py error_server")
            sys.exit()

        if boss.flag_win:
            my_result_game = "Статус: вы поймали всех игроков."
        elif boss.flag_death:
            my_result_game = "Статус: все игроки сбежали из лабиринта."
        elif boss.flag_afk:
            my_result_game = "Статус: вы были кикнуты за бездействие."

        try:
            spectator = Spectator(
                boss.client_socket,
                boss.session.labirinth,
                player.session.pos_exit,
                boss.session.pos_player,
                boss.move_data.id_player_move,
                my_result_game
            )
            spectator.start()
        # Ошибка подключения.
        except:
            pygame.display.quit()
            os.system("end_window.py error_server")
            sys.exit()

    else:
        if player.flag_win:
            my_result_game = "Статус: вы сбежали из лабиринта."
        elif player.flag_death:
            my_result_game = "Статус: вы попали в лапы минотавру."
        elif player.flag_afk:
            my_result_game = "Статус: вы были кикнуты за бездействие."

        try:
            spectator = Spectator(
                player.client_socket,
                player.session.labirinth,
                player.session.pos_exit,
                player.session.pos_player,
                player.move_data.id_player_move,
                my_result_game
            )
            spectator.start()
        # Ошибка подключения.
        except:
            pygame.display.quit()
            os.system("end_window.py error_server")
            sys.exit()

    if spectator.flag_boss_win:
        os.system("end_window.py boss_win")
    else:
        os.system("end_window.py player_win")

    # Заркываем сокет.
    spectator.client_socket.close()


if __name__ == "__main__":
    # os.system("taskkill /f /im cmd.exe")

    start_game(sys.argv[1], sys.argv[2], sys.argv[3])
