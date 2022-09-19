import ast


def from_server_init(data: str):
    """ Функция получения данных о ПЕРВОЙ игровой сессии лабиринта.
    Принимается в клиенте ОТ СЕРВЕРА.
    data - данные о лабиринте.
    (return) - (labirinth, pos_exit, pos_player, id_player, id_player_move). """

    # Пример: ["labirinth=[[0, 0], ...]", "pos_exit=(y, x)", ...]
    data_lst = data.split(";")[1:]

    # Пример: [ ["labirinth", "[[0, 0], ...]"], ["pos_exit", "(y, x)"], ...]
    for i in range(len(data_lst)):
        data_lst[i] = data_lst[i].split("=")

    # Преобразование лабиринта str; в вид = [[0, 0], ...].
    labirinth = ast.literal_eval(data_lst[0][1])

    # Преобразование выхода str; в вид = (y, x).
    pos_exit = ast.literal_eval(data_lst[1][1])

    # Преобразование позиций игроков str; в вид = [(y1, x1), (y2, x2), ...].
    pos_player = ast.literal_eval(data_lst[2][1])

    # Преобразование индекса игрока в pos_player. (int)
    id_player = int(data_lst[3][1])

    # Индекс игрока, который ходит в данный момент. (int)
    id_player_move = int(data_lst[4][1])

    return labirinth, pos_exit, pos_player, id_player, id_player_move


def from_server_update(data: str):
    """ Функция получения данных об обновлённых положениях игроков и того, кто сейчас ходит.
    Принимается в клиенте при отправке ОТ СЕРВЕРА.
    data - данные о позициях и текущем игроке, кто ходит.
    (return) - (pos_player, id_player_move, timer). """

    if data.count(";") > 5:
        return None, None, None, None

    # Пример: ["pos_player=[[y1, x1], [y2, x2], ...]", "id_player_move=index"]
    data_lst = data.split(";")[1:]

    # Пример: [ ["pos_player", "[[y1, x1], [y2, x2], ...]"], ["id_player_move", "index"]
    for i in range(len(data_lst)):
        data_lst[i] = data_lst[i].split("=")

    # Преобразование позиций игроков str; в вид = [(y1, x1), (y2, x2), ...].
    pos_player = ast.literal_eval(data_lst[0][1])

    # Индекс игрока, который сейчас ходит. (int)
    id_player_move = int(data_lst[1][1])

    # Таймер в секундах, сколь осталось на ход. (int)
    timer = int(data_lst[2][1])

    # Сломанные стены минотавром. [(y1, x1), ...]
    broken_walls = ast.literal_eval(data_lst[3][1])

    return pos_player, id_player_move, timer, broken_walls


def from_client_update(data: str):
    """ Функция получения данных об обновлённых положениях игроков и кол-ве ходов игрока в данный момент.
    Принимается на сервере при отправке ОТ КЛИЕНТА.
    data - данные о позициях и текущем игроке, кто ходит.
    (return) - (x, y, live, amount_move, broken_wall, visible, id_playere). """

    # Пример: ["pos_player=[[y1, x1], [y2, x2], ...]", "id_player_move=index"]
    data_lst = data.split(";")[1:]

    # Пример: [ ["pos_player", "[[y1, x1], [y2, x2], ...]"], ["id_player_move", "index"]
    for i in range(len(data_lst)):
        data_lst[i] = data_lst[i].split("=")

    # Новая координата x.
    new_x = int(data_lst[0][1])

    # Новая координата y.
    new_y = int(data_lst[1][1])

    # Индексы умерших игроков.
    if "[" in data_lst[2][1]:
        kill = ast.literal_eval(data_lst[2][1])
        live = kill
    # Статус жизни игрока.
    else:
        if "False" in data_lst[2][1]:
            live = False
        else:
            live = True

    # Кол-во оставшихся ходов у игрока.
    amount_move = int(data_lst[3][1])

    # Сломанная стена минотавром. Либо (y, x), либо ().
    broken_wall = ast.literal_eval(data_lst[4][1])

    # Сломанная стена минотавром. Либо (y, x), либо ().
    if "False" in data_lst[5][1]:
        visible = False
    else:
        visible = True

    # Индекс игрока, который отправляет данные.
    id_playere = int(data_lst[6][1])

    return new_x, new_y, live, amount_move, broken_wall, visible, id_playere
