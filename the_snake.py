from random import choice, randint

import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 12

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Родительский класс,
    который описывает игровой объект (позиция и цвет).
    """

    def __init__(self, body_color=APPLE_COLOR,
                 position=((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Метод отрисовки объекта на игровом поле,
        который будет переопределен в дочерних классах.
        """
        pass


class Apple(GameObject):
    """Дочерний класс класса GameObject,
    который описывает состояние "яблок" на игровом поле.
    """

    def __init__(self, body_color=APPLE_COLOR,
                 position=((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))):
        self.body_color = body_color
        self.position = position

    def randomize_position(self):
        """Метод, генерирующий случайное положение яблока на игровом поле."""
        width = randint(0, GRID_WIDTH) * GRID_SIZE
        height = randint(0, GRID_HEIGHT) * GRID_SIZE
        self.position = (width, height)

    def draw(self, surface):
        """Метод отрисовки яблока на игровом поле."""
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Дочерний класс класса GameObject, который описывает состояние "змейки"
    на игровом поле (позицию, цвет, направление движения, длину).
    """

    def __init__(self, body_color=SNAKE_COLOR):
        super().__init__(body_color)
        self.reset()
        self.position = self.positions[0]
        self.last = None

    def update_direction(self, next_direction):
        """Метод, определяющий текущее направление движения
        змейки по игровому полю.
        """
        self.direction = next_direction
        next_direction = None

    def get_head_position(self):
        """Метод, возвращающий координаты головы змейки."""
        return self.positions[0]

    def move(self):
        """Метод, обновляющий позицию змейки, добавляя новую голову
        в начало списка positions и удаляя последний элемент,
        если длина змейки не увеличилась.
        """
        current_head_position = self.get_head_position()
        x, y = self.direction
        new = ((current_head_position[0] + (x * GRID_SIZE)) % SCREEN_WIDTH,
               (current_head_position[1] + (y * GRID_SIZE)) % SCREEN_HEIGHT
               )
        if new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new)
            self.last = self.positions.pop() if (len(self.positions)
                                                 > self.length) else None

    def reset(self):
        """Метод, который сбрасывает змейку в начальное состояние
        после столкновения с собой.
        """
        global current_speed
        screen.fill(BOARD_BACKGROUND_COLOR)
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([RIGHT, LEFT, UP, DOWN])
        self.next_direction = None
        current_speed = SPEED

    def draw(self, surface):
        """Метод отрисовки змейки на игровом поле."""
        for position in self.positions[:-1]:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object):
    """Функция обработки нажатий клавиш игроком."""
    global next_direction
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                next_direction = RIGHT


def main():
    """Основная функция, описывающая основной цикл игры."""
    global current_speed
    snake = Snake()
    apple = Apple()
    apple.draw(screen)
    while True:
        clock.tick(current_speed)
        handle_keys(snake)
        if next_direction:
            snake.update_direction(next_direction)
        snake.move()
        if apple.position == snake.get_head_position():
            snake.length += 1
            apple.randomize_position()
            # проверка на наличие яблока в змейке
            if apple.position in snake.positions:
                while apple.position in snake.positions:
                    apple.randomize_position()
            current_speed += 1
        apple.draw(screen)
        snake.draw(screen)
        pygame.display.update()


next_direction = None
if __name__ == '__main__':
    main()
