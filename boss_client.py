""" В данном модуле реализовано следующее:
1. Логика игры от лица минотавра.
2. Клиентская часть.
3. Отрисовка игры. """


import pygame
import random

from session_data.session_data import MoveData

from settings import width, height, title, step
from settings import chance_break_wall, chance_speed

from media.skins import boss_img, labirinth_icon

from media.sounds import sound_hit, sound_break_wall
from media.sounds import sound_move1, sound_move2

from player_client import Player


clock = pygame.time.Clock()


class Boss(Player):
    """ Подкласс игрока.
    Визуализация сгенерированного лабиринта от лица минотавра. """

    def __init__(self, client_socket, labirinth, pos_player, id_player, id_player_move):

        # Определение полей объекта об игровой сессии.
        super().__init__(
            # Игровая сессия:
            client_socket=client_socket,
            labirinth=labirinth,
            pos_player=pos_player,
            id_player=id_player,
            id_player_move=id_player_move,
            # Данные об игроке и лабиринте:
            x=pos_player[id_player]["x"],
            y=pos_player[id_player]["y"],
            width_labirinth=len(labirinth[0]),
            height_labirinth=len(labirinth),
        )

        # 1) Данные о ходах в игре:
        # Кол-во ходов у игрока на данный момент.
        if id_player == id_player_move:
            self.move_data = MoveData(amount_move=2, id_player_move=id_player_move)
            self.move_data.flag_start_move = True
        else:
            self.move_data = MoveData(amount_move=0, id_player_move=id_player_move)

        # 2) Данные об убитых игроках в данный момент.
        self.death_players = []


    def start(self):
        """ Метод запуска пользователя от лица минотавра.
        (return) - None """

        # Создание визуализации.
        pygame.init()

        self.draw_data.src = pygame.display.set_mode( (width, height) )

        self.draw_data.src.fill( (0, 0, 0) )
        pygame.display.set_caption(title)
        pygame.display.set_icon(labirinth_icon)
        self.run()


    def _send_data_server(self):
        """ Функция отправки данных серверу.
        UPD: отправка не live:bool, а kill:list.
        (return) - None """

        # Если кончились ходы у игрока, который сейчас ходит
        # - отправляем данные другим игрокам.
        if self.move_data.id_player_move == self.session.id_player:
            update_player_data = f"update_player_data;x={self.x};y={self.y};kill={self.death_players};amount_move={self.move_data.amount_move};broken_wall={self.skills.broken_wall};visible=True;id_player={self.session.id_player};"
            self.client_socket.send(update_player_data.encode())


    def _update_move_human(self):
        """ (boss) Функция для обновления положения минотавра при нажатии кнопок.
        (return) - None """

        # Перебор нажатых клавиш и событий.
        pygame.event.clear()
        event =  pygame.event.wait(130)  # Ждём 130 мс.

    # ХОД: Если скиллы не активированы и игрок делает движение.
        if event.type == pygame.KEYDOWN and self.skills.activate_break is False:

            # Идёт вверх.
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                if self.session.labirinth[self.y-1][self.x] != 0:
                    self.y -= 1
                    self.move_data.amount_move -= 1
                    # Звук хода.
                    if random.choice([True, False]):
                        sound_move1.play()
                    else:
                        sound_move2.play()

            # Идёт вниз.
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                if self.session.labirinth[self.y+1][self.x] != 0:
                    self.y += 1
                    self.move_data.amount_move -= 1

                    if random.choice([True, False]):
                        sound_move1.play()
                    else:
                        sound_move2.play()

            # Идёт влево.
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                if self.session.labirinth[self.y][self.x-1] != 0:
                    self.x -= 1
                    self.move_data.amount_move -= 1

                    if random.choice([True, False]):
                        sound_move1.play()
                    else:
                        sound_move2.play()

            # Идёт вправо.
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                if self.session.labirinth[self.y][self.x+1] != 0:
                    self.x += 1
                    self.move_data.amount_move -= 1

                    if random.choice([True, False]):
                        sound_move1.play()
                    else:
                        sound_move2.play()

            # Нажата ульта: сломать стену.
            elif event.key == pygame.K_r:
                # Способность готова к применению.
                if self.skills.ready_break is True:
                    self.skills.activate_break = True

            # Передача хода.
            elif self.move_data.amount_move != 0 and event.key == pygame.K_RETURN:
                self.move_data.amount_move = 0

    # УЛЬТА: если игрок активировал скилл и ломает стену.
        elif event.type == pygame.KEYDOWN and self.skills.activate_break is True:
            # Ломает вверхнюю стену.
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                if self.y-1 > 1 and self.session.labirinth[self.y-1][self.x] == 0:
                    self.skills.broken_wall = (self.y-1, self.x)
                    self.move_data.amount_move -= 1
                    self.skills.clear_flags_break()
                    sound_break_wall.play()

            # Ломает нижнюю стену.
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                if self.y+1 < self.height_labirinth-1 and self.session.labirinth[self.y+1][self.x] == 0:
                    self.skills.broken_wall = (self.y+1, self.x)
                    self.move_data.amount_move -= 1
                    self.skills.clear_flags_break()
                    sound_break_wall.play()

            # Ломает левую стену.
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                if self.x-1 > 1 and self.session.labirinth[self.y][self.x-1] == 0:
                    self.skills.broken_wall = (self.y, self.x-1)
                    self.move_data.amount_move -= 1
                    self.skills.clear_flags_break()
                    sound_break_wall.play()

            # Ломает правую стену.
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                if self.x+1 < self.width_labirinth-1 and self.session.labirinth[self.y][self.x+1] == 0:
                    self.skills.broken_wall = (self.y, self.x+1)
                    self.move_data.amount_move -= 1
                    self.skills.clear_flags_break()
                    sound_break_wall.play()

            # Игрок передумал использовать ульту.
            elif event.key == pygame.K_r:
                self.skills.activate_break = False

            # Передача хода.
            elif self.move_data.amount_move != 0 and event.key == pygame.K_KP_ENTER:
                self.skills.activate_break = False
                self.move_data.amount_move = 0

        pygame.event.clear()

        self.death_players = []
        # Если встал на ячейку игрока - он проиграл.
        for i, tmp_player in enumerate(self.session.pos_player):

            if tmp_player["boss"] is False and tmp_player["live"] and tmp_player["y"] == self.y and tmp_player["x"] == self.x:
                self.death_players.append(i)
                sound_hit.play()


    def _draw_main_human(self):
        """ Отрисовка текущего минотавра.
        (return) - None """

        x_center = self.draw_data.place_draw_main_human[1] * step + step // 2
        y_center = self.draw_data.place_draw_main_human[0] * step + step // 2

        # Получается форму прямоугольника изображения.
        boss_img_rect = boss_img.get_rect(center=(
                # Центр ячейки, куда должна встать изображение (по x).
                x_center,
                # Центр ячейки, куда должна встать изображение (по y).
                y_center + 14
            )
        )

        # Отрисовываем.
        self.draw_data.src.blit(boss_img, boss_img_rect)

        # Текст ника.
        text = self.draw_data.my_fonts["nick"].render(f'{self.session.pos_player[self.session.id_player]["nickname"]}', True, (0, 0, 0))
        place = text.get_rect(center=(x_center + 7, y_center - 52))
        self.draw_data.src.blit(text, place)


    def _define_arrows(self, tmp_labirinth):
        """ Функция для определения присутствия тех или иных стреток. Работает для минотавра:
        либо для хода, либо для ломания стен.
        tmp_labirinth - часть лабиринта, которую отрисуем. [[], [], ...]
        (return) - None """

        # Определение стрелок, которые нужны. Зависит от положения игрока place_draw_main_human.
        y_draw_human = self.draw_data.place_draw_main_human[0]
        x_draw_human = self.draw_data.place_draw_main_human[1]

        # Если минотавр делает ход.
        if not self.skills.activate_break:
            try:
                if tmp_labirinth[y_draw_human-1][x_draw_human] != 0:
                    self.draw_data.arrows["top"] = True
            except IndexError:
                pass

            try:
                if tmp_labirinth[y_draw_human+1][x_draw_human] != 0:
                    self.draw_data.arrows["bottom"] = True
            except IndexError:
                pass

            try:
                if tmp_labirinth[y_draw_human][x_draw_human-1] != 0:
                    self.draw_data.arrows["left"] = True
            except IndexError:
                pass

            try:
                if tmp_labirinth[y_draw_human][x_draw_human+1] != 0:
                    self.draw_data.arrows["right"] = True
            except IndexError:
                pass

        # Если минотавр выбирает стену для разрушения.
        # Нельзя разрушать выходные стены лабиринта.
        else:
            try:
                if y_draw_human >= 2 and tmp_labirinth[y_draw_human-1][x_draw_human] == 0:
                    self.draw_data.arrows["top"] = True
            except IndexError:
                pass

            try:
                if y_draw_human <= 2 and tmp_labirinth[y_draw_human+1][x_draw_human] == 0:
                    self.draw_data.arrows["bottom"] = True
            except IndexError:
                pass

            try:
                if x_draw_human >= 2 and tmp_labirinth[y_draw_human][x_draw_human-1] == 0:
                    self.draw_data.arrows["left"] = True
            except IndexError:
                pass

            try:
                if x_draw_human <= 2 and tmp_labirinth[y_draw_human][x_draw_human+1] == 0:
                    self.draw_data.arrows["right"] = True
            except IndexError:
                pass


    def _random_chance(self):
        """ (Минотавр) Модуль даёт скиллы минотавру с какой-то вероятность.
        (return) - Nnoe """

        self.skills.activate_speed = False

        # Ломать стены.
        if random.randint(0, 100) <= chance_break_wall:
            self.skills.ready_break = True

        # Пассивка ускорения.
        if random.randint(0, 100) <= chance_speed:
            self.move_data.amount_move = 3
            self.skills.activate_speed = True
