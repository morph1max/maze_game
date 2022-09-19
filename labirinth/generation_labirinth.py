""" Модуль генерации лабиринтов """

import random


class Connect:
    """ Класс для соединений вершин. """

    def __init__(self, connect_lst=[]):
        """ Инициализация объекта Connect.
        Поля:
        connect_lst(list) - список объединения точек в одну группу. """

        self.connect_lst = connect_lst

class Group:
    """ Класс группы элементов в лабиринте. """

    def __init__(self, group_id: int):
        """ Инициализация объекта Group.
        Поля:
        id(int) - айди группы.
        connection(Connect) - связи текущей группы с другими. """

        self.id = group_id
        self.connection = Connect([self])

    def add_connect(self, add_group):
        """ Метод добавления новой группы к текущей
        add_group(Group) - группа, которую нужно объединить с текущей. """

        min_id = min(self.id, add_group.id)

        # Объединяем связи обеих групп в одну.
        connect_lst = self.connection.connect_lst + add_group.connection.connect_lst
        new_connection = Connect(connect_lst)

        # Обновляем связи и id текущей группы и добавляемой.
        for temp_gr in connect_lst:
            temp_gr.id = min_id
            temp_gr.connection = new_connection

    def __repr__(self):
        return f"{self.id}"


def generate_labirinth(width, height):
    """ Функция генерации лабиринта с помощью алгоритма Краскала
    width(int) - ширина лабиринта.
    height(int) - высота лабиринта.
    (return) - (лабиринт с выходом, координаты выхода)=(labirinth, (y, x)). """

    labirinth = []  # Результирующий лабиринт.

    id_group = 1
    # Генерация стартового лабиринта без дорог.
    for i in range(height * 2):
        temp = []
        if i % 2 == 0:
            for k in range(width * 2):
                if k % 2 == 0:
                    temp.append(Group(id_group))
                    id_group += 1
                else:
                    if k < width * 2 - 1: temp.append(0)
                    else: break
        else:
            if i < height * 2 - 1:
                temp = [0 for _ in range(width * 2 - 1)]
            else:
                break
        labirinth.append(temp)

    # Координаты точек-групп в списке labirinth.
    coord_dots = [(y, x) for y in range(len(labirinth)) for x in range(len(labirinth[0])) if labirinth[y][x] != 0]

    # Создание дорог между точками.
    for _ in range(height * width):
        action = ['left', 'right', 'bottom', 'top']

        # Выбирается рандомная точка из лабиринта.
        random_dot = random.choice(coord_dots)

        temp_x = random_dot[1]
        temp_y = random_dot[0]

        # Рандомное действие-ход в лево/право/верх/вниз.
        for i in range(4):
            random_action = random.choice(action)

            # Соединяем текущую и левую точку, если они из разных групп.
            if random_action == 'left':
                if random_dot[1] != 0:
                    current_group = labirinth[temp_y][temp_x]
                    left_group = labirinth[temp_y][temp_x-2]

                    if current_group.id != left_group.id:
                        current_group.add_connect(left_group)
                        labirinth[temp_y][temp_x-1] = current_group
                        break
                action.remove('left')  # Если действие не исполнено - удаляем.

            # Соединяем текущую и правую точку, если они из разных групп.
            elif random_action == 'right':
                if random_dot[1] < len(labirinth[0])-1:
                    current_group = labirinth[temp_y][temp_x]
                    right_group = labirinth[temp_y][temp_x+2]

                    if current_group.id != right_group.id:
                        current_group.add_connect(right_group)
                        labirinth[temp_y][temp_x+1] = current_group
                        break
                action.remove('right')  # Если действие не исполнено - удаляем.

            # Соединяем текущую и нижнюю точку, если они из разных групп.
            elif random_action == 'bottom':
                if random_dot[0] < len(labirinth)-1:
                    current_group = labirinth[temp_y][temp_x]
                    bottom_group = labirinth[temp_y+2][temp_x]

                    if current_group.id != bottom_group.id:
                        current_group.add_connect(bottom_group)
                        labirinth[temp_y+1][temp_x] = current_group
                        break
                action.remove('bottom')  # Если действие не исполнено - удаляем.

            # Соединяем текущую и верхнюю точку, если они из разных групп.
            elif random_action == 'top':
                if random_dot[0] != 0:
                    current_group = labirinth[temp_y][temp_x]
                    top_group = labirinth[temp_y-2][temp_x]

                    if current_group.id != top_group.id:
                        current_group.add_connect(top_group)
                        labirinth[temp_y-1][temp_x] = current_group
                        break
                action.remove('top')  # Если действие не исполнено - удаляем.

        coord_dots.remove(random_dot)  # Удаление просмотренной точки.

    # Выявление несоединённых групп, а далее их соединение.
    for y in range(0, len(labirinth), 2):

        # Смотрим, есть ли в строке несколько групп или нет.
        uniq_el_lst = list(set([i.id for i in labirinth[y] if isinstance(i, Group)]))
        if len(uniq_el_lst) > 1:

            for x in range(0, len(labirinth[0]), 2):

                current_group = labirinth[y][x]
                if isinstance(current_group, Group) and current_group.id > 1:
                    # Соединение с левой группой.
                    if x > 1:
                        current_group = labirinth[y][x]
                        left_group = labirinth[y][x-2]

                        if current_group.id != left_group.id:
                            current_group.add_connect(left_group)
                            labirinth[y][x-1] = current_group

                    # Соединение с нижней группой.
                    elif y < len(labirinth) - 1:
                        current_group = labirinth[y][x]
                        bottom_group = labirinth[y+2][x]

                        if current_group.id != bottom_group.id:
                            current_group.add_connect(bottom_group)
                            labirinth[y+1][x] = current_group

                    # Соединение с правой группой.
                    elif x < len(labirinth[0]) - 1:
                        current_group = labirinth[y][x]
                        right_group = labirinth[y][x+2]

                        if current_group.id != right_group.id:
                            current_group.add_connect(right_group)
                            labirinth[y][x+1] = current_group

                    # Соединение с верхней верхней.
                    elif y > 1:
                        current_group = labirinth[y][x]
                        top_group = labirinth[y-2][x]

                        if current_group.id != top_group.id:
                            current_group.add_connect(top_group)
                            labirinth[y-1][x] = current_group

    # Добавление стен на границе лабиринта.
    for lst in labirinth:
        lst.insert(0, 0)
        lst.append(0)
    null_lst = [0 for _ in range(len(labirinth[0]))]
    labirinth.insert(0, null_lst)
    labirinth.append(null_lst)

    # Привожу к нормальному виду лабиринт.
    labirinth = [[0 if el == 0 else 1 for el in labirinth[i]] for i in range(len(labirinth))]

    # Создаю рандомный выход из лабиринта.
    labirinth, pos_exit = random_exit(labirinth)

    return labirinth, pos_exit


def random_exit(labirinth):
    """ Функция рандомно создаёт выход из лабиринта. Помечается двойкой в лабиринте.
    labirinth - лабиринт(list).
    (return) - (лабиринт с выходом, координаты выхода)=(labirinth, (y, x)). """

    width = len(labirinth[0])
    height = len(labirinth)

    side = ['left', 'right', 'bottom', 'top']

    flag = True
    pos_exit = None
    while flag:
        # Выход будет сверху/снизу лабиринта.
        random_side = random.choice(side)

        if random_side == "left":
            random_id = random.randint(1, height-1)
            if labirinth[random_id][1] != 0:
                labirinth[random_id][0] = 2
                flag = False
                pos_exit = (random_id, 0)

        elif random_side == "right":
            random_id = random.randint(1, height-1)
            if labirinth[random_id][-2] != 0:
                labirinth[random_id][-1] = 2
                flag = False
                pos_exit = (random_id, width-1)

        elif random_side == "top":
            random_id = random.randint(1, width-1)
            if labirinth[1][random_id] != 0:
                labirinth[0][random_id] = 2
                flag = False
                pos_exit = (0, random_id)

        elif random_side == "bottom":
            random_id = random.randint(1, width-1)
            if labirinth[-2][random_id] != 0:
                labirinth[-1][random_id] = 2
                flag = False
                pos_exit = (height-1, random_id)

    return labirinth, pos_exit
