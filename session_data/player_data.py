"""  """


class PlayerData:
    def __init__(self, client_socket, addr):
        self.client_socket = client_socket
        self.addr = addr

        # Кол-во ошибок при отправке данных. Если много ошибок - отключаем от сервера.
        self.errors = 0
