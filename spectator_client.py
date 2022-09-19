""" Модуль реализует клиент со стороны зрителя. """


from player_client import Player
import pygame

from functions.func_decode_data import from_server_update
from settings import width, height, step
from media.skins import labirinth_icon


title = "Spectator"


class Spectator(Player):
    """ Визуализация сгенерированного лабиринта от лица игрока. """

    def __init__(self, client_socket, labirinth, pos_exit, pos_player, id_player_move, my_result_game):
        # Определение полей объекта об игровой сессии.
        super().__init__(
            # Игровая сессия:
            client_socket=client_socket,
            labirinth=labirinth,
            pos_player=pos_player,
            pos_exit=pos_exit,
            id_player_move=id_player_move,
            x=pos_player[id_player_move]["x"],
            y=pos_player[id_player_move]["y"],
            width_labirinth=len(labirinth[0]),
            height_labirinth=len(labirinth)
        )

        self.my_result_game = my_result_game

        # Флаги для учёта победы чьей-то стороны.
        self.flag_player_win = False
        self.flag_boss_win = False


    def start(self):
        """ Метод запуска пользователя от лица зрителя.
        (return) - None """

         # Создание визуализации.
        pygame.init()

        self.draw_data.src = pygame.display.set_mode( (width, height) )

        self.draw_data.src.fill( (0, 0, 0) )
        pygame.display.set_caption(title)
        pygame.display.set_icon(labirinth_icon)
        self.run()


    def update(self):
        """ Метод обновления данных лабиринта.
        (return) - True-игра продолжается; False-выход. """

        # Обнуление всех счётчиков и флагов.
        self._restart_data()
        self._recv_data_server()

        # Конец игры.
        if self.flag_player_win or self.flag_boss_win:
            return False

        # Изменение положения камеры.
        self._update_move_human()

        # Фиксит баг зависания игры во время ожидания хода.
        self._check_exit()

        return True


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

        # Если сервер отправил "boss_win" или "player_win" - конец игры.
        elif "boss_win" in data:
            self.flag_boss_win = True
        elif "player_win" in data:
            self.flag_player_win = True


    def _update_move_human(self):
        """ (player) Функция для обновления положения игрока при нажатии кнопок.
        (return) - None """

        print("spectator", f"{self.x = }", f"{self.y = }")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.flag_death = True

            # Нажатие кнопок для движения камеры.
            elif event.type == pygame.KEYDOWN:
                print("key")

                # Идёт вверх.
                if event.key == pygame.K_w:
                    if self.y > 2:
                        print("top")
                        self.y -= 1

                # Идёт вниз.
                elif event.key == pygame.K_s:
                    if self.y < self.height_labirinth - 3:
                        print("bot")
                        self.y += 1

                # Идёт влево.
                elif event.key == pygame.K_a:
                    if self.x > 2:
                        print("left")
                        self.x -= 1

                # Идёт вправо.
                elif event.key == pygame.K_d:
                    if self.x < self.width_labirinth - 3:
                        print("right")
                        self.x += 1


    def draw(self):
        """ Обновление визуализации лабиринта.
        (return) - None """

        # Пока игра продолжается - отрисовываем.
        self._draw_part_labirinth()
        self._draw_other_human()
        self._draw_exit()
        self._draw_info_game()
        self._draw_info_my_result()

        # Обновляем экран.
        pygame.display.flip()


    def _draw_part_labirinth(self):
        """ Отрисовка части лабиринта.
        (return) - None """

        # Редактирование координат игрока для отрисовки.
        y_human, x_human = self.y, self.x

        # Беру часть лабиринта для генерации.
        tmp_labirinth = []
        for place_y, num in enumerate(range(-2, 3, 1)):
            try:
                part_labirinth = self.session.labirinth[y_human+num][x_human-2:x_human+3]
            except IndexError:
                continue

            # Есть ли в этой части лабиринта выход.
            if 2 in part_labirinth:
                self.draw_data.place_draw_exit = [place_y, part_labirinth.index(2)]

            tmp_labirinth.append(part_labirinth)

            # Есть ли в этой части лабиринта другие игроки.
            self._define_other_human(y_human+num, [tmp_x for tmp_x in range(x_human-2, x_human+3)], place_y)

        color_path = (226, 184, 69)  # orange-yellow.
        color_wall = (73, 43, 13)  # black-blue.

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


    def _define_other_human(self, y, x_lst, place_y):
        """ Функция определяет, есть ли в этой части лабиринта другие игроки.
        y - координата y части лабиринта(int).
        x_lst - координаты x части лабиринта(list).
        place_y - ячейка y в этой части лабиринтаю(int).
        (return) - None """

        for tmp_pos in self.session.pos_player:

            # Сверка координат и проверка на видимость игрока.
            if tmp_pos["y"] == y and tmp_pos["x"] in x_lst and tmp_pos["visible"]:

                # Добавление позиции другого игрока для отрисовки.
                tmp_dict = {
                    "place_y": place_y, "place_x": x_lst.index(tmp_pos["x"]),
                    "boss": tmp_pos["boss"], "live": tmp_pos["live"],
                    "skin": tmp_pos["skin"], "nickname": tmp_pos["nickname"]
                }
                self.draw_data.place_draw_other_human.append(tmp_dict)


    def _draw_info_my_result(self):
        """ Метод отрисовывает статус игрока, перешедшего за зрителей. """

        color_text = (226, 184, 69)  # orange

        # Текст: статус завершения игрока.
        text = self.draw_data.my_fonts["info"].render(self.my_result_game, True, color_text)
        place = text.get_rect(center=(150, 685))
        self.draw_data.src.blit(text, place)


    def exit_game(self):
        """ Функция завершает текущую сессию игрока и заканчивает сессию игрока.
        А также уведомляет сервер, что текущий игрок проиграл.
        Сервер знает индекс текущего игрокаю
        (return) - None """

        pygame.display.quit()
