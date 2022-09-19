""" Модуль реализации серверной части игры. """


import socket
import time

from functions.func_decode_data import from_client_update
from session_data.create_session import create_session

from session_data.server_data import ServerData
from session_data.player_data import PlayerData

from settings import fps, time_move


def next_move_player(server_data: ServerData):
    """ Функция определяет какой игрок будет хотедить следующим.
    (return) - server_data(ServerData). """

    # Следующий игрок ходит, который живой.
    while True:
        print("Игрок ходил секунд = ", server_data.timer)
        server_data.id_player_move += 1
        if server_data.id_player_move >= server_data.total_amount_player:
            server_data.id_player_move = 0

        if server_data.pos_player[server_data.id_player_move]["live"]:
            server_data.timer = 0
            break
        print("Skip player id = ", server_data.id_player_move)
    print("next player id = ", server_data.id_player_move)

    return server_data


def server():
    """ Реализация сервера. """

    # Параметры лабиринта.
    _width = abs(int(input("Width = ")))
    _height = abs(int(input("Height = ")))
    if _width < 5:
        _width = 5
    if _height < 5:
        _height = 5

    # Кол-во всего игроков в игре.
    _total_amount_player = abs(int(input("Total amount players = ")))

    # Настройка серверного сокета.
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

    server_address = ("26.164.33.225", 9090)
    # server_address = ("26.135.101.73", 9090)
    server_socket.bind(server_address)
    server_socket.setblocking(0)
    server_socket.listen(_total_amount_player)

    # Создание данных сессии.
    _amount_player, _labirinth, _pos_exit, _pos_player = create_session(_total_amount_player, _width, _height)

    # На протяжении игровой сессии тут будут храниться все данные о лабиринте и игроках.
    server_data = ServerData(server_socket, _total_amount_player, _amount_player, _labirinth, _pos_player, _pos_exit)

    # Список игроков, подключённых к серверу.
    players_lst = []

    # Флаг, что все игроки подключились и можно начинать игру.
    flag_all_player_connect = False

    # Таймер для подсчёта времени хода игрока.
    tmp_timer = None

    # Результат игры.
    result_game = None

# 1) Запуск сервера.
    running = True
    while running:

        # Для таймера хода.
        if not tmp_timer:
            tmp_timer = time.time()

        # Ждём подключения
        try:
            new_socket, addr = server_socket.accept()
            new_socket.setblocking(0)
        except:
            addr = None

# 2) Инициализация клиента.
        if addr and addr not in [tmp_addr.addr for tmp_addr in players_lst]:
            if len(players_lst) >= server_data.total_amount_player:
                continue

            players_lst.append(PlayerData(new_socket, addr))
            print("PLAYER JOIN")

            # Заранее немного ждём ник от клиента.
            time.sleep(0.5)

            # Принимаем ник подключившегося игрока.
            try:
                nickname = new_socket.recv(4096)
                nickname = nickname.decode()
            except:
                nickname = f"player{len(players_lst)-1}"

            # Сохраняем ник.
            server_data.pos_player[len(players_lst)-1]["nickname"] = nickname

            # Данные об игровой сессии на отправку новому игроку.
            init_data = server_data.init_data_send(len(players_lst)-1)

            # Отправка первых данных новому игроку.
            try:
                new_socket.send(init_data.encode())
            except:
                pass

        # Если игрок уже подключён - принимаем и обновляем все данные.
        else:
            # Если клиент отправил данные - читаем их.
            for player1 in players_lst:

                # Получаем данные от игроков.
                try:
                    data = player1.client_socket.recv(4096)  # Если никто не отправил - вызывается исключение.
                    data = data.decode()
                except:
                    data = None

# 3) Приём данных от клиентов.
                if data and "update_player_data" in data:

                    # Если игрок проиграл.
                    if "death_player" in data:
                        print("death_player")
                        server_data.amount_player -= 1

                        # Если последний игрок умер - конец игры. Минотавры победили.
                        if server_data.amount_player == 0:
                            result_game = "boss_win;"
                            running = False
                            break

                    # Если минотавр отлюкчился от игры.
                    elif "death_boss" in data:
                        print("death_boss")
                        server_data.amount_boss -= 1

                        # Если все минотавры вышли - игрока победили.
                        if server_data.amount_boss == 0:
                            result_game = "player_win;"
                            running = False
                            break

                    # Если игрок убежал из лабиринта.
                    elif "win_player" in data:
                        print("win_player")
                        server_data.amount_player -= 1

                        # Если последний игрок победил - победили игроки.
                        if server_data.amount_player == 0:
                            result_game = "player_win;"
                            running = False
                            break

                    # Получаем обновления данных от игроков.
                    new_x, new_y, live, amount_move, broken_wall, visible, id_player = from_client_update(data)

                    # Вносим обновления в серверные данные игроков.
                    server_data.pos_player[id_player]["x"] = new_x
                    server_data.pos_player[id_player]["y"] = new_y

                    # Если минотавр убил игроков.
                    if isinstance(live, list):
                        killed = live
                        for idx in killed:
                            server_data.pos_player[idx]["live"] = False
                    # Обнолвяем статус жизни у игрока.
                    else:
                        server_data.pos_player[id_player]["live"] = live

                    # Если была сломана новая стена.
                    if len(broken_wall) > 0 and broken_wall not in server_data.broken_walls:
                        server_data.labirinth[broken_wall[0]][broken_wall[1]] = 1
                        server_data.broken_walls.append(broken_wall)

                    # Обновляется видимость игрока. Если он нажал ульту инвиза, то
                    # статус обновляется.
                    server_data.pos_player[id_player]["visible"] = visible

                    # У игрока кончились ходы, или он умер - передаём ход следующему игроку.
                    if (amount_move == 0 and server_data.id_player_move == id_player) or server_data.pos_player[id_player]["live"] is False:
                        server_data = next_move_player(server_data)

# 4) Готовим данные для отправки.
        # Следим за теймером хода игрока. Если вышел за пределы - игрок умирает.
        if server_data.timer > time_move:
            server_data.pos_player[server_data.id_player_move]["live"] = None

            # Вычитаем из счётчика классов игрока.
            if server_data.pos_player[server_data.id_player_move]["boss"]:
                server_data.amount_boss -= 1
            else:
                server_data.amount_player -= 1

            # Проверяем, не остался ли пуст какой-то из типов игроков.
            # Если пуст - выжившая сторона победила.
            if server_data.amount_player == 0:
                running = False
                result_game = "boss_win;"
            elif server_data.amount_boss == 0:
                running = False
                result_game = "player_win;"

            # Если ещё есть оба типа игроков в живых - передаём ход другому игроку.
            else:
                server_data = next_move_player(server_data)

        # Не выходит за рамки.
        elif flag_all_player_connect:
            server_data.timer = server_data.timer + (time.time() - tmp_timer)

            # Проверяем, не остался ли пуст какой-то из типов игроков.
            if server_data.amount_player == 0:
                running = False
                result_game = "boss_win;"
            elif server_data.amount_boss == 0:
                running = False
                result_game = "player_win;"
        
        # Снова засекаем время.
        tmp_timer = time.time()

        # Подготовка данных для отправки:
        data = server_data.pos_player_data_send()

        # Когда все игроки подключились - объявляем старт игры и игроки могут начать ходить. Одноразовый вызов.
        if len(players_lst) == server_data.total_amount_player and flag_all_player_connect is False:
            flag_all_player_connect = True
            data = "all_player_connect"
            server_data.timer = 0
            server_working_time = 10

        elif running:
            server_working_time = 1
        # После окончания игры сервер ещё работает некоторое время.
        else:
            print(f"{result_game = }")
            data = result_game
            server_working_time = 100

# 5) Отправка данных.
        for _ in range(server_working_time):

            # Отправляем всем игрокам новые положения игроков и кто сейчас ходит.
            for player in players_lst:

                try:
                    player.client_socket.send(data.encode())
                    player.errors = 0
                except:
                    # Если данные не отправились - значит что-то у игрока с соединением.
                    player.errors += 1
                    if player.errors >= 500:
                        # Отключившийся игрок умирает.
                        server_data.pos_player[players_lst.index(player)]["live"] = False
                        players_lst.remove(player)
                        print("KICK PLAYER")

            time.sleep(1 / fps + 0.02)

# 6) Закрытие сокетов.
    # Закрываем соединение со всеми после игры.
    for player in players_lst:
        player.client_socket.close()

    # Закрываем сервер.
    server_socket.close()


if __name__ == "__main__":
    server()
