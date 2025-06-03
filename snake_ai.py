import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 640, 480
CELL_SIZE = 20
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Self Playing Snake')
clock = pygame.time.Clock()

class Snake:
    def __init__(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.length = 1

    def head(self):
        return self.positions[0]

    def turn(self, dir):
        if (dir[0] * -1, dir[1] * -1) == self.direction:
            return
        self.direction = dir

    def move(self):
        cur = self.head()
        x, y = self.direction
        new = ((cur[0] + x) % GRID_WIDTH, (cur[1] + y) % GRID_HEIGHT)
        if new in self.positions[2:]:
            raise Exception('Game Over')
        self.positions.insert(0, new)
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self, surface):
        for pos in self.positions:
            rect = pygame.Rect(pos[0]*CELL_SIZE, pos[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, GREEN, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)

class Food:
    def __init__(self, snake):
        self.position = (0, 0)
        self.place(snake)

    def place(self, snake):
        while True:
            pos = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
            if pos not in snake.positions:
                self.position = pos
                break

    def draw(self, surface):
        rect = pygame.Rect(self.position[0]*CELL_SIZE, self.position[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(surface, RED, rect)
        pygame.draw.rect(surface, BLACK, rect, 1)

# Simple AI using BFS to find path to food
from collections import deque

def bfs(snake, food):
    start = snake.head()
    queue = deque([[start]])
    visited = {start}
    while queue:
        path = queue.popleft()
        x, y = path[-1]
        if (x, y) == food.position:
            return path[1:]  # skip the starting point
        for dir in [UP, DOWN, LEFT, RIGHT]:
            nx = (x + dir[0]) % GRID_WIDTH
            ny = (y + dir[1]) % GRID_HEIGHT
            if (nx, ny) in visited or (nx, ny) in snake.positions:
                continue
            visited.add((nx, ny))
            queue.append(path + [(nx, ny)])
    return []

# Main game loop

def main():
    snake = Snake()
    food = Food(snake)
    path = []
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if not path:
            path = bfs(snake, food)
            if not path:
                # No path found; choose random direction
                snake.turn(random.choice([UP, DOWN, LEFT, RIGHT]))
        if path:
            next_cell = path.pop(0)
            dir = (next_cell[0] - snake.head()[0], next_cell[1] - snake.head()[1])
            dir = (dir[0] and (1 if dir[0]>0 else -1), dir[1] and (1 if dir[1]>0 else -1))
            snake.turn(dir)

        try:
            snake.move()
        except Exception:
            print('Game Over')
            pygame.quit()
            return

        if snake.head() == food.position:
            snake.length += 1
            food.place(snake)
            path = []  # recompute path

        screen.fill(WHITE)
        food.draw(screen)
        snake.draw(screen)
        pygame.display.update()
        clock.tick(10)

if __name__ == '__main__':
    main()
