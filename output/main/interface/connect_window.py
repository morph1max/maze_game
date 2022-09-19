""" Модуль реализует интерфейс с подключением игрока к игре. """

from PyQt5 import QtCore, QtGui, QtWidgets


class UiConnectWindow(object):
    """ Графический дизайн подключения игрока и ввода данных. """

    def setupUi(self, connect_window):
        """ Метод созданий графических объектов. """

        connect_window.setObjectName("connect_window")

        # self.label_connect = QtWidgets.QLabel(connect_window)
        # self.label_connect.setGeometry(QtCore.QRect(10, 10, 181, 41))
        # font = QtGui.QFont()
        # font.setFamily("OCR A")
        # font.setPointSize(16)
        # font.setBold(True)
        # font.setWeight(75)
        # self.label_connect.setFont(font)
        # self.label_connect.setObjectName("label_connect")

        self.label_name = QtWidgets.QLabel(connect_window)
        self.label_name.setGeometry(QtCore.QRect(15, 10, 51, 16))
        font = QtGui.QFont()
        font.setFamily("OCR A")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_name.setFont(font)
        self.label_name.setObjectName("label_name")

        self.input_name = QtWidgets.QLineEdit(connect_window)
        self.input_name.setGeometry(QtCore.QRect(15, 30, 170, 28))
        font = QtGui.QFont()
        font.setFamily("OCR A Std")
        font.setPointSize(11)
        self.input_name.setFont(font)
        self.input_name.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border: 3px solid black;\n"
"border-radius: 10px;")
        self.input_name.setMaxLength(9)
        self.input_name.setObjectName("input_name")

        self.label_host = QtWidgets.QLabel(connect_window)
        self.label_host.setGeometry(QtCore.QRect(15, 80, 61, 16))
        font = QtGui.QFont()
        font.setFamily("OCR A")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_host.setFont(font)
        self.label_host.setObjectName("label_host")

        self.input_host = QtWidgets.QLineEdit(connect_window)
        self.input_host.setGeometry(QtCore.QRect(15, 110, 170, 28))
        # self.input_host.setText("26.164.33.225")
        self.input_host.setText("localhost")
        font = QtGui.QFont()
        font.setFamily("OCR A")
        font.setPointSize(11)
        self.input_host.setFont(font)
        self.input_host.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border: 3px solid black;\n"
"border-radius: 10px;")
        self.input_host.setMaxLength(30)
        self.input_host.setObjectName("input_host")

        self.label_port = QtWidgets.QLabel(connect_window)
        self.label_port.setGeometry(QtCore.QRect(15, 160, 61, 16))
        font = QtGui.QFont()
        font.setFamily("OCR A")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_port.setFont(font)
        self.label_port.setObjectName("label_port")

        self.input_port = QtWidgets.QLineEdit(connect_window)
        self.input_port.setGeometry(QtCore.QRect(15, 190, 170, 28))
        font = QtGui.QFont()
        font.setFamily("OCR A")
        font.setPointSize(11)
        self.input_port.setFont(font)
        self.input_port.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border: 3px solid black;\n"
"border-radius: 10px;")
        self.input_port.setMaxLength(5)
        self.input_port.setObjectName("input_port")
        self.input_port.setText("9090")

        self.btn_back = QtWidgets.QPushButton(connect_window)
        self.btn_back.setGeometry(QtCore.QRect(60, 235, 80, 26))
        font = QtGui.QFont()
        font.setFamily("OCR A")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.btn_back.setFont(font)
        self.btn_back.setStyleSheet("background-color: rgb(226, 184, 69);\n"
"border: 3px solid black;\n"
"border-radius: 10px;")
        self.btn_back.setObjectName("btn_back")

        self.btn_connect = QtWidgets.QPushButton(connect_window)
        self.btn_connect.setGeometry(QtCore.QRect(25, 280, 150, 26))
        font = QtGui.QFont()
        font.setFamily("OCR A")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.btn_connect.setFont(font)
        self.btn_connect.setStyleSheet("background-color: rgb(226, 184, 69);\n"
"border: 3px solid black;\n"
"border-radius: 10px;")
        self.btn_connect.setObjectName("btn_connect")

        self.label_developer = QtWidgets.QLabel(connect_window)
        self.label_developer.setGeometry(QtCore.QRect(55, 337, 121, 16))
        font = QtGui.QFont()
        font.setFamily("OCR A")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_developer.setFont(font)
        self.label_developer.setObjectName("label_developer")

        self.label_morph1max = QtWidgets.QLabel(connect_window)
        self.label_morph1max.setGeometry(QtCore.QRect(69, 360, 101, 16))
        font = QtGui.QFont()
        font.setFamily("OCR A")
        font.setPointSize(9)
        self.label_morph1max.setFont(font)
        self.label_morph1max.setObjectName("label_morph1max")

        self.img_labirinth = QtWidgets.QLabel(connect_window)
        self.img_labirinth.setGeometry(QtCore.QRect(201, 0, 400, 400))
        self.img_labirinth.setText("")
        self.img_labirinth.setPixmap(QtGui.QPixmap("interface\\labirinth.png"))
        self.img_labirinth.setObjectName("img_labirinth")

        self.retranslateUi(connect_window)
        QtCore.QMetaObject.connectSlotsByName(connect_window)

    def retranslateUi(self, connect_window):
        _translate = QtCore.QCoreApplication.translate
        connect_window.setWindowTitle(_translate("connect_window", "Dialog"))
        self.label_name.setText(_translate("connect_window", "Имя:"))
        # self.label_connect.setText(_translate("connect_window", "ПОДКЛЮЧЕНИЕ"))
        self.btn_connect.setText(_translate("connect_window", "Подключиться"))
        self.btn_back.setText(_translate("connect_window", "Назад"))
        self.label_host.setText(_translate("connect_window", "Хост:"))
        self.label_port.setText(_translate("connect_window", "Порт:"))
        self.label_developer.setText(_translate("connect_window", "Разработчик:"))
        self.label_morph1max.setText(_translate("connect_window", "morph1max"))
