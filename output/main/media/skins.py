""" Модуль содержит скины для игроков. """


import pygame


labirinth_icon = pygame.image.load("media/img/labirinth_icon.png")

# Скины ТЕКУЩЕГО игрока. (Для фикса бага).
my_player0_img = pygame.image.load("media/img/cowboy100.png")
my_player1_img = pygame.image.load("media/img/boy100.png")
my_player2_img = pygame.image.load("media/img/girl100.png")
my_player3_img = pygame.image.load("media/img/cat100.png")
# Список скинов.
my_player_skin_lst = [my_player0_img, my_player1_img, my_player2_img, my_player3_img]

# Скины ОСТАЛЬНЫХ игроков. (Для фикса бага).
other_player0_img = pygame.image.load("media/img/cowboy100.png")
other_player1_img = pygame.image.load("media/img/boy100.png")
other_player2_img = pygame.image.load("media/img/girl100.png")
other_player3_img = pygame.image.load("media/img/cat100.png")
# Список скинов.
other_player_skin_lst = [other_player0_img, other_player1_img, other_player2_img, other_player3_img]

boss_img = pygame.image.load("media/img/minotaur100.png")
rip_img = pygame.image.load("media/img/rip90.png")
exit_img = pygame.image.load("media/img/cup100.png")
