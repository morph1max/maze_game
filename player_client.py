""" В данном модуле реализовано следующее:
1. Логика игры от лица игрока.
2. Клиентская часть.
3. Отрисовка игры. """


import pygame
import socket
import random
import time

from functions.func_decode_data import from_server_init, from_server_update

from session_data.session_data import Session, DrawData, MoveData
from skills import Skills

from functions.func_draw import _draw_line, _draw_rect, _draw_text

from settings import width, height, title, fps, step, time_move  # Настройки игры.
from settings import chance_invisibility, chance_break_wall, chance_speed

from media.skins import boss_img, rip_img, exit_img  # Остальные скины.
from media.skins import my_player_skin_lst, other_player_skin_lst  # Скины игрока.
from media.skins import labirinth_icon

from media.sounds import sound_start_move1, sound_start_move2, sound_hit, sound_invisibility
from media.sounds import sound_move1, sound_move2

clock = pygame.time.Clock()


class Player:
    """ Класс игрока.
    Визуализация сгенерированного лабиринта от лица игрока. """

    def __init__(
            self,
            # Игровая сессия:
            client_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM),
            labirinth=None,
            pos_player=None,
            pos_exit=None,
            id_player=None,
            id_player_move=None,
            # Данные об игроке и лабиринте:
            x=None,
            y=None,
            width_labirinth=None,
            height_labirinth=None,
            nickname="noname",
            host="localhost",
            port=9090
        ):

        # 1) Данные об интернет-соединении:
        # Интернет-сокет текущего игрока.
        self.client_socket = client_socket
        # Адресс сервера.
        self.server_addr = (host, port)
        # Ник игрока.
        self.nickname = nickname
        # Скин игрока.
        self.skin_idx = None

        # Если создался игрок - подключаем его к серверу.
        # Если создался минотавр - он уже подключён к серверу.
        if self.whoami() == "Player":
            self.client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            self.client_socket.connect(self.server_addr)

        # 2) Данные о старте/конце игры:
        # Флаг победы пользователя. Если победил - переходит в Spectator.
        self.flag_win = False
        # Флаг смерти/проигрыша. Если умер/проиграл - переходит в Spectator.
        self.flag_death = False
        # Флаг бездействия игрока. Становится True при истечении времени таймера.
        self.flag_afk = False
        # Флаг, что все игроки подключились и можно  начать вдигаться.
        self.flag_all_player_connect = False

        # 3) Вспомогательные данные о лабиринте:
        # Ширина/высота лабиринта.
        self.width_labirinth = width_labirinth
        self.height_labirinth = height_labirinth

        # 4) Координаты пользователя.
        self.x = x
        self.y = y

        # 4) Основные данные об игровой сессии(лабиринт, другие игроки, выход):
        self.session = Session(
            labirinth=labirinth, pos_exit=pos_exit, pos_player=pos_player, id_player=id_player
        )

        # 5) Данные о ходах в игре:
        self.move_data = MoveData(id_player_move=id_player_move)

        # 6) Данные об отрисовке объектов:
        self.draw_data = DrawData()

        # 7) Данные о скиллах игрока/минотавра:
        self.skills = Skills()


    def start(self):
        """ Метод запуска пользователя.
        Если текущий пользователь игрок - игра продолжается.
        Если минотавр - пользователь пересоздаётся в минотавра.
        (return) - None """

        # Если текущий игрок не минотавр - запускаем игру.
        # Первое соединение с сервером.
        if self._init_data_server():

            pygame.init()

            self.draw_data.src = pygame.display.set_mode( (width, height) )

            self.draw_data.src.fill( (0, 0, 0) )
            pygame.display.set_caption(title)
            pygame.display.set_icon(labirinth_icon)
            self.run()


    def _init_data_server(self):
        """ Функция соединения с сервером для инициализации игрока.
        (return) - None """

        # Если запуск игрока был в первый раз.
        self.client_socket.send(f"{self.nickname}".encode())

        # Получение данных от сервера.
        data = self.client_socket.recv(4096)
        data = data.decode()

        # Инициализация данных об игровой сессии.
        self.session.labirinth, self.session.pos_exit, self.session.pos_player, self.session.id_player, self.move_data.id_player_move = from_server_init(data)
        self.width_labirinth = len(self.session.labirinth[0])
        self.height_labirinth = len(self.session.labirinth)

        # Определяю координаты игрока.
        self.x = self.session.pos_player[self.session.id_player]["x"]
        self.y = self.session.pos_player[self.session.id_player]["y"]

        # Рандомный скин.
        self.skin_idx = self.session.pos_player[self.session.id_player]["skin"]

        # Если текущий игрок минотавр - запускаем другой клиент.
        if self.session.pos_player[self.session.id_player]['boss']:
            return False

        # Начался мой ход.
        if self.move_data.id_player_move == self.session.id_player and self.move_data.flag_start_move is False:
            self.move_data.amount_move = 2
            self.move_data.flag_start_move = True

        return True


    def run(self):
        """ Главная функция работы игры.
        (return) - None """

        while True:
            flag = self.update()  # Продолжение игры зависит от действия пользователя.
            if flag is False:
                self.exit_game()
                break

            self.draw()
            clock.tick(fps)


    def update(self):
        """ Метод обновления данных лабиринта.
        (return) - True-игра продолжается; False-выход. """

        # Обнуление всех счётчиков и флагов.
        self._restart_data()
        self._recv_data_server()

        # Конец игры.
        if self.flag_win or self.flag_death or self.flag_afk:
            return False

        # Если есть ходы - игрок ходит.
        elif self.move_data.amount_move > 0 and self.flag_all_player_connect:
            self._update_move_human()

            # Реже отправляем данные серверу, чтобы была меньше нагрузка.
            if random.choice([True, False]):
                self._send_data_server()

        # Если ходов 0, а ход до сих пор мой - отправляем данные.
        # Для фикса бага.
        elif self.move_data.amount_move == 0 and self.move_data.flag_start_move:
            self._send_data_server()

        # Фиксит баг зависания игры во время ожидания хода.
        self._check_exit()

        return True


    def _restart_data(self):
        """ Функция обнуления и обновления данных и флагов.
        (return) - None """

         # Обнуление всех счётчиков и флагов.
        self.draw_data.arrows = {"left": False, "right": False, "top": False, "bottom": False}
        self.draw_data.place_draw_main_human = [2, 2]
        self.draw_data.place_draw_other_human = []
        self.draw_data.place_draw_exit = None

        self.draw_data.flag_r = False
        self.draw_data.flag_enter = False
        self.draw_data.flag_speed = False


    def _recv_data_server(self):
        """ Функция получения данных от сервера.
        (return) - None """

        # Получение данных от сервера.
        data = self.client_socket.recv(4096)
        data = data.decode()

        # Обновление текущих положений игроков на карте.
        # А также узнаём, кто ходит в данный момент.
        if "update_player_data" in data:

            tmp_pos_player, tmp_id_player_move, tmp_timer, tmp_broken_walls = from_server_update(data)

            # Если есть корректно считанные данные - сохраняем.
            if tmp_pos_player:
                self.session.pos_player, self.move_data.id_player_move, self.move_data.timer = tmp_pos_player, tmp_id_player_move, tmp_timer
                
                # Разрушаю сломанные стены.
                for broken_wall in tmp_broken_walls:
                    self.session.labirinth[broken_wall[0]][broken_wall[1]] = 1
            else:
                return None

            # Начался мой ход.
            if self.move_data.id_player_move == self.session.id_player and self.move_data.flag_start_move is False:
                # Засыпаем в начале хода, чтобы пред. игрок завершил отправку
                # своих данных и не мешал серверу.
                time.sleep(0.5)
                self.move_data.amount_move = 2
                self.move_data.flag_start_move = True
                self._random_chance()

                # Звук начала хода.
                if random.choice([True, False]):
                    sound_start_move1.play()
                else:
                    sound_start_move2.play()

                # Перед стартом хода очищаем сломанную стену.
                if self.whoami() == "Boss":
                    self.skills.broken_wall = ()

            # Если не мой ход - начинаю ждать его.
            if self.move_data.id_player_move != self.session.id_player:
                self.move_data.amount_move = 0
                self.move_data.flag_start_move = False

            # Если вышел таймер за афк - переходим за зрителя.
            if self.session.pos_player[self.session.id_player]["live"] is None:
                self.flag_afk = True

            # Синхронизация жизни игрока за время чужих ходов.
            if self.whoami() == "Player" and self.session.pos_player[self.session.id_player]["live"] is False:
                self.flag_death = True
                sound_hit.play()

        # Все игроки подключились к серверу и можно начать играть.
        elif "all_player_connect" in data:
            self.flag_all_player_connect = True

        # Если сервер отправил "boss_win" - минотавры победили.
        elif "boss_win" in data and data.count(";") == 1:

            if self.whoami() == "Player":
                self.flag_death = True
            else:
                self.flag_win = True

        # Если сервер отправил "player_win" - игроки победили.
        elif "player_win" in data and data.count(";") == 1:

            if self.whoami() == "Player":
                self.flag_win = True
            else:
                self.flag_death = True


    def _random_chance(self):
        """ (Игрок) Модуль даёт скиллы игроку с какой-то вероятность.
        (return) - Nnoe """

        self.skills.activate_invisible = False

        if random.randint(0, 100) <= chance_invisibility:
            self.skills.ready_invisible = True


    def _send_data_server(self):
        """ Функция отправки данных серверу.
        (return) - None """

        # Отправляем данные другим игрокам.
        if self.move_data.id_player_move == self.session.id_player:
            update_player_data = f"update_player_data;x={self.x};y={self.y};live={not self.flag_death};amount_move={self.move_data.amount_move};broken_wall=();visible={not self.skills.activate_invisible};id_player={self.session.id_player};"
            self.client_socket.send(update_player_data.encode())


    def _check_exit(self):
        """ Метод проверки выхода из игры.
        (return) - None """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.flag_death = True


    def _update_move_human(self):
        """ (player) Функция для обновления положения игрока при нажатии кнопок.
        (return) - None """

        pygame.event.clear()
        event =  pygame.event.wait(130)  # Ждём 130 мс.

        # Выход из игры.
        if event.type == pygame.QUIT:
            self.flag_death = True

        # Нажатие кнопок.
        elif event.type == pygame.KEYDOWN:

            # Защита от краша.
            try:

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

                # Передача хода.
                elif self.move_data.amount_move != 0 and event.key == pygame.K_RETURN:
                    self.move_data.amount_move = 0

                # Если игрок нажал ульту: невидимость.
                elif self.skills.ready_invisible and event.key == pygame.K_r:
                    self.skills.activate_invisible = True
                    self.skills.ready_invisible = False
                    sound_invisibility.play()

            except IndexError:
                pass

        # Очистка нажатых событий.
        pygame.event.clear()

        # Если встал на ячейку выхода.
        if self.session.pos_exit[0] == self.y and self.session.pos_exit[1] == self.x:
            self.flag_win = True

        # Если встал на ячейку минотавра - проиграл.
        for tmp_player in self.session.pos_player:

            if tmp_player["boss"] and tmp_player["y"] == self.y and tmp_player["x"] == self.x:
                self.flag_death = True


    def draw(self):
        """ Обновление визуализации лабиринта.
        (return) - None """

        # Пока игра продолжается - отрисовываем.
        self._draw_part_labirinth()
        self._draw_other_human()
        self._draw_main_human()
        if self.whoami() == "Player":
            self._draw_exit()
        self._draw_info_game()
        self._draw_skills()

        # Если сейчас мой ход - рисуем стрелки.
        if self.move_data.amount_move > 0:
            self._draw_arrows()

        # Если не все игроки подключились - пишем, что ждём их.
        if self.flag_all_player_connect is False:
            self._draw_wait_players()

        # Обновляем экран.
        pygame.display.flip()


    def _draw_wait_players(self):
        """ Метод отрисовывает надпись "Ждём остальных игроков...".
        Срабатывает, когда flag_all_player_connect=False.
        (return) - None """

        color_text = (255, 255, 255)  # white
        color_rect = (0, 0, 0)  # black

        # Прямоугольник.
        pygame.draw.rect(
            self.draw_data.src,
            color_rect,
            pygame.Rect( (0, 270, 640, 100) ),  # pos (x, y, width, height)
        )

        # Текст.
        text = self.draw_data.my_fonts["big_info"].render('Ждём всех игроков...', True, color_text)
        place = text.get_rect(center=(320, 320))
        self.draw_data.src.blit(text, place)


    def _draw_part_labirinth(self):
        """ Отрисовка части лабиринта.
        (return) - None """

        # Редактирование координат игрока для отрисовки.
        y_human, x_human = self.__change_coord_human()

        # Беру часть лабиринта для генерации.
        tmp_labirinth = []
        for place_y, num in enumerate(range(-2, 3, 1)):
            try:
                part_labirinth = self.session.labirinth[y_human+num][x_human-2:x_human+3]
            except IndexError:
                continue

            # Есть ли в этой части лабиринта выход.
            if 2 in part_labirinth:

                # От лица игрока рисуем выход на экране.
                if self.whoami() == "Player":
                    self.draw_data.place_draw_exit = [place_y, part_labirinth.index(2)]

                # От лица минотавра закрашиваем выход из лабиринта.
                else:
                    part_labirinth = [i if i != 2 else 0 for i in part_labirinth]

            tmp_labirinth.append(part_labirinth)

            # Есть ли в этой части лабиринта другие игроки.
            self._define_other_human(y_human+num, [tmp_x for tmp_x in range(x_human-2, x_human+3)], place_y)

        # Определяю стрелки для отрисовки.
        self._define_arrows(tmp_labirinth)

        color_path = (226, 184, 69)  # orange-yellow.
        color_wall = (73, 43, 13)  # brown.

        # Генерация части лабиринта.
        for y in range(len(tmp_labirinth)):
            for x in range(len(tmp_labirinth[0])):

                if tmp_labirinth[y][x] != 0:  # Дорога
                    pygame.draw.rect(self.draw_data.src, color_path, pygame.Rect(
                            # Стартовые координаты x1, y1.
                            x * step, y * step,
                            # Конечные координаты x2, y2.
                            (x + 1) * step, (y + 1) * step,
                        )
                    )

                else:  # Стены.
                    pygame.draw.rect(self.draw_data.src, color_wall, pygame.Rect(
                            # Стартовые координаты x1, y1.
                            x * step, y * step,
                            # Конечные координаты x2, y2.
                            (x + 1) * step, (y + 1) * step,
                        )
                    )


    def __change_coord_human(self):
        """ Функция редактирования координат игрока на краю лабиринта для отрисовки.
        (return) - None """

        # Текущие координаты игрока.
        y_human = self.y
        x_human = self.x

        # Если человек стоит в самом внизу/верху.
        if y_human - 2 < 0:
            y_human += 1
            self.draw_data.place_draw_main_human[0] -= 1
        elif y_human + 2  >= self.height_labirinth:
            y_human -= 1
            self.draw_data.place_draw_main_human[0] += 1

        # Если человек стоит в справа/слева.
        if x_human - 2 < 0:
            x_human += 1
            self.draw_data.place_draw_main_human[1] -= 1
        elif x_human + 2  >= self.width_labirinth:
            x_human -= 1
            self.draw_data.place_draw_main_human[1] += 1

        return y_human, x_human


    def _define_other_human(self, y, x_lst, place_y):
        """ Функция определяет, есть ли в этой части лабиринта другие игроки.
        y - координата y части лабиринта(int).
        x_lst - координаты x части лабиринта(list).
        place_y - ячейка y в этой части лабиринтаю(int).
        (return) - None """

        for tmp_pos in self.session.pos_player:

            # Пропускаем текущего игрока.
            if tmp_pos == self.session.pos_player[self.session.id_player]:
                continue

            # Сверка координат и проверка на видимость игрока.
            if tmp_pos["y"] == y and tmp_pos["x"] in x_lst and tmp_pos["visible"]:

                # Добавление позиции другого игрока для отрисовки.
                tmp_dict = {
                    "place_y": place_y, "place_x": x_lst.index(tmp_pos["x"]),
                    "boss": tmp_pos["boss"], "live": tmp_pos["live"],
                    "skin": tmp_pos["skin"], "nickname": tmp_pos["nickname"]
                }
                self.draw_data.place_draw_other_human.append(tmp_dict)


    def _define_arrows(self, tmp_labirinth):
        """ Функция для определения присутствия тех или иных стреток.
        tmp_labirinth - часть лабиринта, которую отрисуем. [[], [], ...]
        (return) - None """

        # Определение стрелок, которые нужны. Зависит от положения игрока place_draw_main_human.
        y_draw_human = self.draw_data.place_draw_main_human[0]
        x_draw_human = self.draw_data.place_draw_main_human[1]

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


    def _draw_main_human(self):
        """ Отрисовка текущего игрока и его ника.
        (return) - None """

        x_center = self.draw_data.place_draw_main_human[1] * step + step // 2
        y_center = self.draw_data.place_draw_main_human[0] * step + step // 2

        # Мой скин.
        player_img = my_player_skin_lst[self.skin_idx]

        # Получается форму прямоугольника изображения.
        player_img_rect = player_img.get_rect(center=(
                # Центр ячейки, куда должна встать изображение (по x).
                x_center,
                # Центр ячейки, куда должна встать изображение (по y).
                y_center + 14
            )
        )

        # Если нажата невидимость - скин становится прозрачным.
        if self.skills.activate_invisible:
            player_img.set_alpha(60)
        else:
            player_img.set_alpha(255)

        # Отрисовываем игрока.
        self.draw_data.src.blit(player_img, player_img_rect)

        # Текст ника.
        text = self.draw_data.my_fonts["nick"].render(f'{self.session.pos_player[self.session.id_player]["nickname"]}', True, (0, 0, 0))
        place = text.get_rect(center=(x_center, y_center - 52))
        self.draw_data.src.blit(text, place)


    def _draw_other_human(self):
        """ Отрисовка других игроков.
        Отрисовка игроков/минотавров/убитых.
        (return) - None """

        for tmp_place_draw in self.draw_data.place_draw_other_human:

            x_center = tmp_place_draw["place_x"] * step + step // 2
            y_center = tmp_place_draw["place_y"] * step + step // 2

            # Скин другого игрока.
            player_img = other_player_skin_lst[tmp_place_draw["skin"]]

            # Если живой игрок.
            if tmp_place_draw["boss"] is False and tmp_place_draw["live"]:
                player_img_rect = player_img.get_rect(center=(
                        # Центр ячейки, куда должна встать изображение (по ширине).
                        x_center,
                        # Центр ячейки, куда должна встать изображение (по высоте).
                        y_center + 14
                    )
                )
                self.draw_data.src.blit(player_img, player_img_rect)

            # Если проигравший игрок.
            elif tmp_place_draw["boss"] is False and tmp_place_draw["live"] is False:
                rip_img_rect = rip_img.get_rect(center=(
                        # Центр ячейки, куда должна встать изображение (по ширине).
                        x_center,
                        # Центр ячейки, куда должна встать изображение (по высоте).
                        y_center + 19
                    )
                )
                self.draw_data.src.blit(rip_img, rip_img_rect)

            # Если минотавр.
            else:
                boss_img_rect = boss_img.get_rect(center=(
                        # Центр ячейки, куда должна встать изображение (по ширине).
                        x_center,
                        # Центр ячейки, куда должна встать изображение (по высоте).
                        y_center + 14
                    )
                )
                self.draw_data.src.blit(boss_img, boss_img_rect)

            # Текст ника.
            text = self.draw_data.my_fonts["nick"].render(f'{tmp_place_draw["nickname"]}', True, (0, 0, 0))
            place = text.get_rect(center=(x_center, y_center - 52))
            if tmp_place_draw["boss"]:
                place = text.get_rect(center=(x_center + 7, y_center - 52))
            self.draw_data.src.blit(text, place)


    def _draw_arrows(self):
        """ Функция отрисовки строк для игрока.
        (return) - None """

        color = (58, 210, 79)  # Green.

        # Если игра ещё не начинал - стрелки красного цвета.
        if self.flag_all_player_connect is False:
            color = (226, 45, 87)  # Red.

        # Веерхня стрелка.
        if self.draw_data.arrows["top"]:
            y_top_center = self.draw_data.place_draw_main_human[0] * step - 64
            x_top_center = self.draw_data.place_draw_main_human[1] * step + 64
            pygame.draw.polygon(
                self.draw_data.src, color,
                [
                    [x_top_center - 30, y_top_center + 30],
                    [x_top_center, y_top_center],
                    [x_top_center + 30, y_top_center + 30]
                ]
            )

        # Нижняя стрелка.
        if self.draw_data.arrows["bottom"]:
            y_top_center = (self.draw_data.place_draw_main_human[0] + 1) * step + 64
            x_top_center = self.draw_data.place_draw_main_human[1] * step + 64
            pygame.draw.polygon(
                self.draw_data.src, color,
                [
                    [x_top_center - 30, y_top_center - 30],
                    [x_top_center, y_top_center],
                    [x_top_center + 30, y_top_center - 30]
                ]
            )

        # Левая стрелка.
        if self.draw_data.arrows["left"]:
            y_top_center = self.draw_data.place_draw_main_human[0] * step + 64
            x_top_center = self.draw_data.place_draw_main_human[1] * step - 64
            pygame.draw.polygon(
                self.draw_data.src, color,
                [
                    [x_top_center + 30, y_top_center - 30],
                    [x_top_center, y_top_center],
                    [x_top_center + 30, y_top_center + 30]
                ]
            )

        # Правая стрелка.
        if self.draw_data.arrows["right"]:
            y_top_center = self.draw_data.place_draw_main_human[0] * step + 64
            x_top_center = (self.draw_data.place_draw_main_human[1] + 2) * step - 64
            pygame.draw.polygon(
                self.draw_data.src, color,
                [
                    [x_top_center - 30, y_top_center - 30],
                    [x_top_center, y_top_center],
                    [x_top_center - 30, y_top_center + 30]
                ]
            )


    def _draw_exit(self):
        """ Отрисовка выхода из лабиринта.
        (return) - None """

        if self.draw_data.place_draw_exit:
            exit_img_rect = exit_img.get_rect(center=(
                    # Центр ячейки, куда должна встать изображение (по ширине).
                    self.draw_data.place_draw_exit[1] * step + step // 2,
                    # Центр ячейки, куда должна встать изображение (по высоте).
                    self.draw_data.place_draw_exit[0] * step + step // 2 + 14
                )
            )
            self.draw_data.src.blit(exit_img, exit_img_rect)


    def _draw_info_game(self):
        """ Метод отрисовки информации для игрока.
        (return) - None """

        pygame.draw.rect(
            self.draw_data.src,
            (0, 0, 0),  # Чёрный цвет.
            (0, 640, 640, 740)
        )

        color_step = (255, 255, 255)

        color_player = (255, 255, 255)
        if self.session.id_player == self.move_data.id_player_move:
            color_player = (226, 184, 69)  # orange

        color_timer = (255, 255, 255)
        if self.move_data.timer > 50:
            color_timer = (255, 51, 51)  # red

        # Шаги.
        text = self.draw_data.my_fonts["info"].render(f'Шагов: {self.move_data.amount_move}', True, color_step)
        place = text.get_rect(center=(494, 655))
        self.draw_data.src.blit(text, place)

        # Игрок ходит.
        text = self.draw_data.my_fonts["info"].render(f'Ходит: {self.session.pos_player[self.move_data.id_player_move]["nickname"]}', True, color_player)
        place = text.get_rect(center=(511, 685))
        self.draw_data.src.blit(text, place)

        # Таймер.
        text = self.draw_data.my_fonts["info"].render(f'Таймер: {time_move - self.move_data.timer} с.', True, color_timer)
        place = text.get_rect(center=(508, 715))
        self.draw_data.src.blit(text, place)


    def _draw_skills(self):
        """ Метод отрисовываем данные о скиллах игрока.
        (return) - None """

        # Объекты незакрашенных прямоугольников.
        rect_r = pygame.Rect( (20, 650, 70, 70) )
        rect_enter = pygame.Rect( (110, 650, 140, 70) )
        rect_speed = pygame.Rect( (270, 650, 70, 70) )

        # Мышь на кпопке "R".
        if rect_r.collidepoint(pygame.mouse.get_pos()):
            self.draw_data.flag_r = True
        # Мышь на кпопке "Enter".
        elif rect_enter.collidepoint(pygame.mouse.get_pos()):
            self.draw_data.flag_enter = True
        # Мышь на кпопке "+0|+1".
        elif self.whoami() == "Boss" and rect_speed.collidepoint(pygame.mouse.get_pos()):
            self.draw_data.flag_speed = True

    # Скилл невидимости/ломания стены.
        # Если способность доступна.
        if self.flag_all_player_connect and (self.skills.ready_invisible or self.skills.ready_break):
            color_skill = (34, 243, 90)  # green
        else:
            color_skill = (255, 51, 51)  # red
            # Рисуем две линии, если скилл отсутствует.
            if self.draw_data.flag_r is False:
                _draw_line(self.draw_data.src, color_skill, [20, 650], [90, 720], 4)
                _draw_line(self.draw_data.src, color_skill, [90, 650], [20, 720], 4)

        # Текст способности.
        if self.draw_data.flag_r:
            # Описание для ульты минотавра.
            if self.whoami() == "Boss":
                _draw_text(pygame.font.Font(None, 19), self.draw_data.src, "Break wall", color_skill, (55, 665))
                _draw_text(pygame.font.Font(None, 19), self.draw_data.src, "-1 шаг", color_skill, (56, 685))
                _draw_text(pygame.font.Font(None, 17), self.draw_data.src, f"Шанс: {chance_break_wall}%", color_skill, (56, 705))
            else:
                _draw_text(pygame.font.Font(None, 22), self.draw_data.src, "Invisible", color_skill, (56, 665))
                _draw_text(pygame.font.Font(None, 19), self.draw_data.src, "на 1 ход", color_skill, (56, 685))
                _draw_text(pygame.font.Font(None, 17), self.draw_data.src, f"Шанс: {chance_speed}%", color_skill, (56, 705))
        else:
            _draw_text(self.draw_data.my_fonts["big_info"], self.draw_data.src, "R", color_skill, (56, 686))

        # Отрисовка незакрашенного прямоугольника для активного скилла.
        _draw_rect(self.draw_data.src, color_skill, rect_r, 4)

    # Пропуск хода.
        # Если есть ходы - можем передать ход.
        if self.flag_all_player_connect and self.move_data.amount_move != 0:
            color_enter = (34, 243, 90)  # green
        else:
            color_enter = (255, 51, 51)  # red
            # Рисуем две линии, если ходы отсутствует.
            if self.draw_data.flag_enter is False:
                _draw_line(self.draw_data.src, color_enter, [110, 650], [250, 720], 4)
                _draw_line(self.draw_data.src, color_enter, [250, 650], [110, 720], 4)

        # Слово "Enter".
        if self.draw_data.flag_enter:
            _draw_text(pygame.font.Font(None, 26), self.draw_data.src, "Пропуск хода", color_enter, (180, 687))
        else:
            _draw_text(self.draw_data.my_fonts["big_info"], self.draw_data.src, "Enter", color_enter, (180, 687))

        # Отрисовка незакрашенного прямоугольника для пропуска хода "Enter".
        _draw_rect(self.draw_data.src, color_enter, rect_enter, 4)

    # Пассивка ускорения у минотавра.
        if self.whoami() == "Boss":
            color_speed = (226, 184, 69) # Orange

            speed_text = "+0"
            if self.skills.activate_speed:
                speed_text = "+1"

            # Слово "+0|+1".
            if self.draw_data.flag_speed:
                _draw_text(pygame.font.Font(None, 23), self.draw_data.src, "Speed", color_speed, (306, 665))
                _draw_text(pygame.font.Font(None, 19), self.draw_data.src, "Доп. шаг", color_speed, (306, 685))
                _draw_text(pygame.font.Font(None, 17), self.draw_data.src, f"Шанс: {chance_speed}%", color_speed, (306, 705))
            else:
                _draw_text(self.draw_data.my_fonts["big_info"], self.draw_data.src, speed_text, color_speed, (305, 685))

            # Отрисовка незакрашенного прямоугольника пассивки "+0|+1".
            _draw_rect(self.draw_data.src, color_speed, rect_speed, 4)


    def whoami(self):
        """ Метод возвращает название класса текущего объекта.
        (return) - str """

        return type(self).__name__


    def exit_game(self):
        """ Функция завершает текущую сессию игрока и заканчивает сессию игрока.
        А также уведомляет сервер, что текущий игрок проиграл.
        Сервер знает индекс текущего игрокаю
        (return) - None """

        update_player_data = f"x={self.x};y={self.y};live={False};amount_move=0;broken_wall=();visible=True;id_player={self.session.id_player};"

        # Если проиграл.
        if self.flag_death:
            if self.whoami() == "Player":
                update_player_data = "update_player_data_death_player;" + update_player_data
            else:
                update_player_data = "update_player_data_death_boss;" + update_player_data
            self.client_socket.send(update_player_data.encode())

        # Если победил.
        elif self.flag_win:
            update_player_data = "update_player_data_win_player;" + update_player_data
            self.client_socket.send(update_player_data.encode())

        pygame.display.quit()
