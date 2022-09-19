"""  """


class ServerData:

    def __init__(self, server_socket, total_amount_player, amount_player, labirinth, pos_player, pos_exit):
        # Данные о сокете.
        self.server_socket = server_socket

        # Данные об игроках.
        self.total_amount_player = total_amount_player
        self.amount_player = amount_player
        self.amount_boss = total_amount_player - amount_player

        # Данные о лабиринте.
        self.labirinth = labirinth
        # Список сломанных стен.
        self.broken_walls = []

        self.pos_player = pos_player
        self.pos_exit = pos_exit

        # Индекс игрока в pos_player, который сейчас ходит.
        self.id_player_move = 0

        # Таймер хода игрока.
        self.timer = 0


    def init_data_send(self, player_id):
        """ Метод готовит все данные об игровой сессии новому игроку.
        player_id - индекс данного игрока в players_lst(int).
        (return) - init_data(str). """

        init_data = "init_player;"
        init_data += f"labirinth={self.labirinth};pos_exit={self.pos_exit};pos_player={self.pos_player};"
        init_data += f"player_id={player_id};id_player_move={self.id_player_move};"
        return init_data


    def pos_player_data_send(self):
        """ Метод возвращает позиции игроков и индекс игрока, который сейчас ходит.
        (return) - pos_player_data(str). """

        pos_player_data = "update_player_data;"
        pos_player_data += f"pos_player={self.pos_player};id_player_move={self.id_player_move};timer={int(self.timer)};broken_walls={self.broken_walls};"
        return pos_player_data
