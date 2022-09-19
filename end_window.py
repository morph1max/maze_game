""" Модуль реализует интерфейс итогового окна с выводом результата игры. """


from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import os

from media.sounds import sound_mouse


class UiEndWindow(object):
    """ Класс реализует интерфейс окончания игры. """

    def setupUi(self, end_window):
        self.end_window = end_window

        end_window.setObjectName("end_window")
        end_window.setStyleSheet("background-color: rgb(0, 0, 0);")

        self.btn_continue = QtWidgets.QPushButton(end_window)
        self.btn_continue.setGeometry(QtCore.QRect(410, 340, 150, 30))
        font = QtGui.QFont()
        font.setFamily("OCR A Std")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.btn_continue.setFont(font)
        self.btn_continue.setStyleSheet("background-color: rgb(226, 184, 69);\n"
"border: 3px solid black;\n"
"border-radius: 10px;")
        self.btn_continue.setObjectName("btn_continue")
        # Событие при нажатии на кнопку.
        self.btn_continue.clicked.connect(self.event_continue)

        self.label_win = QtWidgets.QLabel(end_window)
        font = QtGui.QFont()
        font.setFamily("OCR A Std")
        font.setPointSize(30)
        font.setBold(True)
        font.setWeight(75)
        self.label_win.setFont(font)
        self.label_win.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_win.setObjectName("label_win")

        self.retranslateUi(end_window)
        QtCore.QMetaObject.connectSlotsByName(end_window)

    def retranslateUi(self, end_window):
        _translate = QtCore.QCoreApplication.translate
        end_window.setWindowTitle(_translate("end_window", "Конец игры"))
        self.btn_continue.setText(_translate("end_window", "Продолжить"))
        self.label_win.setText(_translate("end_window", "Минотавры победили!"))

    def error_end(self):
        """ Ошибка подключения. """

        _translate = QtCore.QCoreApplication.translate
        self.label_win.setText(_translate("end_window", "Ошибка подключения"))

    def error_server(self):
        """ Ошибка на стороне сервера. """

        _translate = QtCore.QCoreApplication.translate
        self.label_win.setText(_translate("end_window", "Сервер поломался"))
        self.label_win.move(105, 140)

    def boss_win(self):
        """ Победили минотавры. """

        _translate = QtCore.QCoreApplication.translate
        self.label_win.setText(_translate("end_window", "Минотавры победили!"))
        self.label_win.move(95, 140)

    def player_win(self):
        """ Победили люди. """

        _translate = QtCore.QCoreApplication.translate
        self.label_win.setText(_translate("end_window", "Люди победили!"))
        self.label_win.move(257, 260)

    def event_continue(self):
        """ Метод срабатывает при нажатии на кнопку "Продолжить".
        Открывается окно "Главное меню".
        (return) - None """

        # Звук мыши.
        sound_mouse.play()

        self.end_window.close()
        os.system("main.py")


if __name__ == "__main__":
    # os.system("taskkill /f /im cmd.exe")

    # Разрешение экрана.
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    app = QtWidgets.QApplication(sys.argv)
    end_window = QtWidgets.QDialog()
    end_window.setWindowTitle('Labirinth')
    end_window.setWindowIcon(QtGui.QIcon("media/img/labirinth_icon.png"))
    end_window.setFixedSize(600, 400)
    ui = UiEndWindow()
    ui.setupUi(end_window)

    # Отображение итога игры.
    if sys.argv[-1] == "error_end":
        ui.error_end()
    elif sys.argv[-1] == "error_server":
        ui.error_server()
    elif sys.argv[-1] == "player_win":
        ui.player_win()
    elif sys.argv[-1] == "boss_win":
        ui.boss_win()

    end_window.show()
    sys.exit(app.exec_())
