""" Модуль содержит классы скиллов игрока и минотавра. """


class Skills:
    """ Класс содержит скиллы игрока и минотавра.
    Скиллы игрока:
    1. Невидимость: игрок становится невидым для других игроков (шанс 10%).
    Скиллы минотавра:
    1. Ломать стены: (шанс 5%).
    2. Ускорение: минотавр ходит не 2 хода, а 3 (шанс 30%)."""

    def __init__(self):
        # 1) Скиллы игрока:
        self.ready_invisible = False
        self.activate_invisible = False

        # 2) Скиллы миноатвра.
        # Способность ломать стены:
        self.ready_break = False
        self.activate_break = False
        # Координаты сломанной стены (y, x).
        self.broken_wall = ()

        # Усуорение +1 к ходу минотавра.
        self.activate_speed = False


    def clear_flag_invisible(self):
        """ (Игрок) Метод обнуления флагов об инвизе игрока.
        Очищается после использования скилла игроков.
        (return) - None """

        self.ready_invisible = False
        self.activate_invisible = False


    def clear_flags_break(self):
        """ (Минотавр) Метод обнуления флагов о ломании стен.
        Очищается после использования скилла минотавром.
        (return) - None """

        self.ready_break = False
        self.activate_break = False
