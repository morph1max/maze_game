""" Модуль содержит функции для отрисовки элементов в игре. """


import pygame


def _draw_line(src, color, dot1, dot2, width):
    """ Отрисовка прямой линии. """

    pygame.draw.line(
        src,
        color,
        dot1,
        dot2,
        width  # ширина.
    )


def _draw_text(my_font, src, text, color, center):
    """ Отрисовка текста. """

    text = my_font.render(text, True, color)
    place = text.get_rect(center=center)
    src.blit(text, place)


def _draw_rect(src, color, rect, width):
    """ Отрисовка незакрашенного прямоугольника. """

    pygame.draw.rect(
        src,
        color,
        rect,  # pos (x, y, width, height)
        width  # толщина.
    )
