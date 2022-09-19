""" Модуль содержит звуки для игры и меню. """


import pygame


# Звуки:
pygame.mixer.init()

# Начало хода игрока.
sound_start_move1 = pygame.mixer.Sound("media/sound/move_player1.ogg")
sound_start_move1.set_volume(0.2)

sound_start_move2 = pygame.mixer.Sound("media/sound/move_player2.ogg")
sound_start_move2.set_volume(0.1)

# Минотавр кого-то убил.
sound_hit = pygame.mixer.Sound("media/sound/hit.ogg")
sound_hit.set_volume(0.2)

# Минотавр сломал стену.
sound_break_wall = pygame.mixer.Sound("media/sound/break_wall.ogg")
sound_break_wall.set_volume(0.3)

# Игрок стал невидимым.
sound_invisibility = pygame.mixer.Sound("media/sound/invisibility.ogg")
sound_invisibility.set_volume(0.03)

# Клик мыши в меню.
sound_mouse = pygame.mixer.Sound("media/sound/mouse.ogg")
sound_mouse.set_volume(0.05)

# Звуки хода персонажа.
sound_move1 = pygame.mixer.Sound("media/sound/stone1.ogg")
sound_move1.set_volume(0.5)
sound_move2 = pygame.mixer.Sound("media/sound/stone2.ogg")
sound_move2.set_volume(0.5)
