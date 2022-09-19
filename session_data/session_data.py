""" Модуль классов для реализации сессии игроков. """


import pygame


class Session:
    """ Содержит главные данные об игровой сессии. """

    def __init__(self, labirinth=None, pos_exit=None, pos_player=None, id_player=None):
        # Лабиринт: список списков.
        self.labirinth = labirinth
        # Координаты выхода labirinth. (y, x)
        self.pos_exit = pos_exit
        # Координаты положения всех игроков в labirinth. [(y1, x1), (y2, x2), ...]
        self.pos_player = pos_player
        # Индекс текущего игрока в pos_player.
        self.id_player = id_player


class DrawData:
    """ Соедржит данные об отрисовке объектов. """

    def __init__(self):
        # Окно pygame.
        self.src = None
        # Шрифт для текста.
        pygame.font.init()
        self.my_fonts = {
            "info": pygame.font.Font(None, 22),
            "nick": pygame.font.Font(None, 22),
            "big_info": pygame.font.Font(None, 60),
        }
        # Позиция текущего игрока для отрисовки. [y, x]
        self.place_draw_main_human = [2, 2]
        # Позиция остальных игроков для отрисовки. [[y1, x1, "boss"], [y2, x2, "player"], ...]
        self.place_draw_other_human = []
        # Позиция выхода для отрисовки.
        self.place_draw_exit = None
        # Словарь для отрисовки стрелок, куда можно идти.
        self.arrows = {"left": False, "right": False, "top": False, "bottom": False}

        # Флаги, определяющие позиции мыши на кнопках.
        # Мышь на кнопке ульты.
        self.flag_r = False
        self.flag_enter = False
        self.flag_speed = False


class MoveData:
    """ Данные о ходах в игре. """

    def __init__(self, amount_move=0, id_player_move=None, flag_start_move=False, timer=0):
        # Кол-во ходов у игрока на данный момент.
        self.amount_move = amount_move
        # Индекс игрока, который сейчас ходит.
        self.id_player_move = id_player_move
        # Флажок: только что начался мой ход. ДЛЯ ФИКСА БАГА.
        self.flag_start_move = flag_start_move
        # Таймер в секундах сколько осталось времени на ход у игрока.
        self.timer = timer
