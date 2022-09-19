""" Модуль реализует графический интерфейс главного меню игры. """


from PyQt5 import QtCore, QtGui, QtWidgets


class UiMainWindow(object):
    """ Графический дизайн главного меню. """

    def setupUi(self, main_window):
        """ Метод создания объектов кнопок, текста и т.д.  """

        main_window.setObjectName("main_window")
        main_window.setWindowIcon(QtGui.QIcon("interface\\labirinth_icon.png"))

        self.btn_play = QtWidgets.QPushButton(main_window)
        self.btn_play.setGeometry(QtCore.QRect(46, 110, 110, 30))
        font = QtGui.QFont()
        font.setFamily("OCR A")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.btn_play.setFont(font)
        self.btn_play.setStyleSheet("background-color: rgb(226, 184, 69);\n"
"border: 3px solid black;\n"
"border-radius: 10px;")
        self.btn_play.setObjectName("btn_play")

        self.btn_exit = QtWidgets.QPushButton(main_window)
        self.btn_exit.setGeometry(QtCore.QRect(46, 170, 110, 30))
        font = QtGui.QFont()
        font.setFamily("OCR A")
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.btn_exit.setFont(font)
        self.btn_exit.setStyleSheet("background-color: rgb(226, 184, 69);\n"
"border: 3px solid black;\n"
"border-radius: 10px;")
        self.btn_exit.setObjectName("btn_exit")

        self.label_labirinth = QtWidgets.QLabel(main_window)
        self.label_labirinth.setGeometry(QtCore.QRect(23, 40, 181, 41))
        font = QtGui.QFont()
        font.setFamily("OCR A")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_labirinth.setFont(font)
        self.label_labirinth.setObjectName("label_labirinth")

        self.img_labirinth = QtWidgets.QLabel(main_window)
        self.img_labirinth.setGeometry(QtCore.QRect(201, 0, 400, 400))
        self.img_labirinth.setPixmap(QtGui.QPixmap("interface\\labirinth.png"))
        self.img_labirinth.setObjectName("img_labirinth")

        self.label_developer = QtWidgets.QLabel(main_window)
        self.label_developer.setGeometry(QtCore.QRect(55, 337, 121, 16))
        font = QtGui.QFont()
        font.setFamily("OCR A")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_developer.setFont(font)
        self.label_developer.setObjectName("label_developer")

        self.label_morph1max = QtWidgets.QLabel(main_window)
        self.label_morph1max.setGeometry(QtCore.QRect(69, 360, 101, 16))
        font = QtGui.QFont()
        font.setFamily("OCR A")
        font.setPointSize(9)
        self.label_morph1max.setFont(font)
        self.label_morph1max.setObjectName("label_morph1max")

        self.retranslateUi(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslateUi(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("main_window", "Dialog"))
        self.btn_play.setText(_translate("main_window", "Играть"))
        self.btn_exit.setText(_translate("main_window", "Выйти"))
        self.label_labirinth.setText(_translate("main_window", "LABIRINTH"))
        self.label_developer.setText(_translate("main_window", "Разработчик:"))
        self.label_morph1max.setText(_translate("main_window", "morph1max"))
