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
SPEED = 13

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

    def __init__(self, body_color=APPLE_COLOR):
        self.body_color = body_color
        self.position = self.randomize_position()

    def randomize_position(self):
        """Метод, генерирующий случайное положение яблока на игровом поле."""
        width = randint(0, GRID_WIDTH) * GRID_SIZE
        height = randint(0, GRID_HEIGHT) * GRID_SIZE
        return (width, height)

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

    def __init__(self):
        self.length = 1
        self.body_color = SNAKE_COLOR
        self.direction = RIGHT
        self.last = None
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.next_direction = None
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    def update_direction(self):
        """Метод, определяющий текущее направление движения
        змейки по игровому полю.
        """
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Метод, возвращающий координаты головы змейки."""
        return self.positions[0]

    def move(self):
        """Метод, обновляющий позицию змейки, добавляя новую голову
        в начало списка positions и удаляя последний элемент,
        если длина змейки не увеличилась.
        """
        self.last = self.positions[-1]
        current_head_position = self.get_head_position()
        new_head_position = (current_head_position[0]
                             + self.direction[0] * GRID_SIZE,
                             current_head_position[1]
                             + self.direction[1] * GRID_SIZE)

        if new_head_position[0] > SCREEN_WIDTH:
            new_head_position = (new_head_position[0] - SCREEN_WIDTH,
                                 new_head_position[1])
        if new_head_position[0] < 0:
            new_head_position = (new_head_position[0] + SCREEN_WIDTH,
                                 new_head_position[1])
        if new_head_position[1] > SCREEN_HEIGHT:
            new_head_position = (new_head_position[0],
                                 new_head_position[1] - SCREEN_HEIGHT)
        if new_head_position[1] < 0:
            new_head_position = (new_head_position[0],
                                 new_head_position[1] + SCREEN_HEIGHT)

        if new_head_position in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new_head_position)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        """Метод, который сбрасывает змейку в начальное состояние
        после столкновения с собой.
        """
        screen.fill(BOARD_BACKGROUND_COLOR)
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = choice([RIGHT, LEFT, UP, DOWN])
        self.next_direction = None

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
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная функция, описывающая основной цикл игры."""
    snake = Snake()
    apple = Apple()
    apple.draw(screen)
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if apple.position == snake.get_head_position():
            snake.length += 1
            apple = Apple()
        apple.draw(screen)
        snake.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()
