""" Модуль содержит код интерфейса. """
# https://medium.com/nuances-of-programming/python-pyqt5-современные-графические-интерфейсы-для-windows-macos-и-linux-6cf43b6900c1
# pyuic5 interface/main_window.ui -o interface/main_window.py -x

import sys
import os
import time

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication

from interface.connect_window import UiConnectWindow
from interface.main_window import UiMainWindow

from media.sounds import sound_mouse


class Interface:
    """ Класс реализует интерфейс меню игры. """

    def __init__(self):
        self.first_start = True
        self.event_back()

    def event_play(self):
        """ Метод срабатываем при нажатии на кнопку "Играть"
        и открывает следующее окно "Присоединиться".
        (return) - None """

        # Звук клика.
        sound_mouse.play()

        self.window = QtWidgets.QDialog()
        self.ui = UiConnectWindow()
        self.ui.setupUi(self.window)

        # Обработка событий при нажатии на кнопку.
        self.ui.btn_back.clicked.connect(self.event_back)
        self.ui.btn_connect.clicked.connect(self.event_connect)
        widget.addWidget(self.window)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def event_exit(self):
        """ (Гл. меню) Метод срабатывает при нажатии кнопки "Выход".
        (return) - None """

        # Звук мыши.
        sound_mouse.play()
        time.sleep(0.25)

        exit()

    def event_back(self):
        """ (Подключение) Метод срабатывает при нажатии на кнопку "Назад"
        и возвращается в главное меню.
        (return) - None """

        # Звук мыши.
        if self.first_start is False:
            sound_mouse.play()
        else:
            self.first_start = False

        self.window = QtWidgets.QDialog()
        self.ui = UiMainWindow()
        self.ui.setupUi(self.window)

        # Обработка событий при нажатии на кнопку.
        self.ui.btn_play.clicked.connect(self.event_play)
        self.ui.btn_exit.clicked.connect(self.event_exit)
        widget.addWidget(self.window)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def event_connect(self):
        """ (Подключение) Метод срабатывает при нажатии на кнопку "Подключиться"
        и пытается подключится к серверу.
        (return) - None """

        # Звук мыши.
        sound_mouse.play()

        nickname = self.ui.input_name.text()
        host = self.ui.input_host.text()
        port = self.ui.input_port.text()

        if len(nickname) == 0:
            nickname = "noname"
        if len(port) == 0:
            port = "9090"

        # Закрытие интерфеса меню.
        widget.close()
        os.system(f"start_game.py {nickname} {host} {port}")


if __name__ == "__main__":
    # os.system("taskkill /f /im cmd.exe")

    # Разрешение экрана.
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    # Созданий окна.
    app = QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()

    interface = Interface()

    widget.setFixedSize(600, 400)
    widget.move(280, 60)
    widget.setWindowTitle('Labirinth')
    widget.setWindowIcon(QtGui.QIcon("media/img/labirinth_icon.png"))

    widget.show()

    # Выход по нажатию на крестик.
    sys.exit(app.exec_())
