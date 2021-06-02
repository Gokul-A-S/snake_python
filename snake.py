import pygame
from pygame.locals import *
import time
import random

SIZE = 35


class Apple:
    def __init__(self, parent_surface):
        self.parent_surface = parent_surface
        self.image = pygame.image.load("res/apple.png").convert()
        self.x = SIZE * random.randint(0, 27)
        self.y = SIZE * random.randint(2, 15)

    def draw(self):
        self.parent_surface.blit(self.image, (self.x, self.y))
        for i in range(game.snake.length):
            if self.x == game.snake.x[i] and self.y == game.snake.y[i]:
                self.x = SIZE * random.randint(0, 27)
                self.y = SIZE * random.randint(2, 15)

        game.display_score()
        pygame.display.flip()

    def move(self):
        self.x = random.randint(0, 27) * SIZE
        self.y = random.randint(2, 15) * SIZE
        self.draw()


class Snake:
    def __init__(self, parent_surface, length):
        self.length = length
        self.parent_surface = parent_surface
        self.block = pygame.image.load("res/block.png").convert()
        self.x = [SIZE] * length
        self.y = [SIZE] * length
        self.direction = "right"

    def draw(self):
        self.parent_surface.fill((0, 255, 100))
        for i in range(self.length):
            self.parent_surface.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def increase_length(self):
        eat_sound = pygame.mixer.Sound("res/apple_eat.wav")
        eat_sound.play()
        self.x.append(-1)
        self.y.append(-1)
        self.length += 1

    def move_up(self):
        if self.direction == "down":
            game.game_over()
        self.direction = "up"

    def move_down(self):
        if self.direction == "up":
            game.game_over()
        self.direction = "down"

    def move_right(self):
        if self.direction == "left":
            game.game_over()
        self.direction = "right"

    def move_left(self):
        if self.direction == "right":
            game.game_over()
        self.direction = "left"

    def walk(self):
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == "up":
            self.y[0] -= SIZE
        if self.direction == "down":
            self.y[0] += SIZE
        if self.direction == "right":
            self.x[0] += SIZE
        if self.direction == "left":
            self.x[0] -= SIZE


class GameOverErr(Exception):
    pass


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption('Snake')
        icon = pygame.image.load("res/icon.png")
        pygame.display.set_icon(icon)
        self.flag = False
        self.surface = pygame.display.set_mode((980, 595))
        self.running = True
        self.pause = False
        self.surface.fill((0, 255, 100))
        self.snake = Snake(self.surface, 2)
        self.snake.draw()
        self.apple = Apple(self.surface)

    def display_score(self):
        font = pygame.font.SysFont("arial black", 20)
        score = font.render(f"Score {self.snake.length * 10 - 20}", True, (0, 0, 0))
        self.surface.blit(score, (870, 0))
        pygame.display.flip()

    def is_collision(self, xs, ys, xa, ya):
        if xs == xa:
            if ys == ya:
                self.snake.increase_length()
                self.apple.move()
                return True

    def is_out_of_boundary(self):
        if (self.snake.x[0] > 950 or self.snake.x[0] < 0) or (self.snake.y[0] > 565 or self.snake.y[0] < 0):
            self.snake.x[0] = random.randint(0, 27) * SIZE
            self.snake.y[0] = random.randint(2, 15) * SIZE
            raise GameOverErr

    def is_self_collision(self):
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                raise GameOverErr

    def game_over(self):
        self.pause = True
        self.surface.fill((10, 10, 10))
        game_over_sound = pygame.mixer.Sound("res/game_over.wav")
        game_over_sound.play()
        font = pygame.font.SysFont("arial black", 40)
        game_over = font.render(f"Game Over! You Scored {self.snake.length * 10 - 20}", True, (255, 255, 255))
        self.surface.blit(game_over, (200, 250))
        pygame.display.flip()

    def play(self):
        self.snake.walk()
        self.snake.draw()
        self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y)
        self.apple.draw()

        self.is_self_collision()
        self.is_out_of_boundary()
        time.sleep(0.2)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.running = False
                    elif event.key == K_UP:
                        if not self.flag:
                            self.snake.move_up()
                    elif event.key == K_DOWN:
                        if not self.flag:
                            self.snake.move_down()
                    elif event.key == K_RIGHT:
                        if not self.flag:
                            self.snake.move_right()
                    elif event.key == K_LEFT:
                        if not self.flag:
                            self.snake.move_left()
                    elif event.key == K_RETURN:
                        if self.pause and not self.flag:
                            self.snake.length = 2
                            self.pause = False
                    elif event.key == K_SPACE:
                        if not self.pause:
                            self.pause = True
                            text = pygame.font.SysFont("arial black", 35)
                            pause = text.render("Press F to continue", True, (0, 0, 0))
                            self.surface.blit(pause, (300, 250))
                            pygame.display.flip()
                            self.flag = True
                    elif event.key == K_f:
                        self.flag = False
                        self.pause = False

                elif event.type == QUIT:
                    self.running = False

            pygame.time.Clock().tick(30)
            try:
                if not self.pause:
                    self.play()
            except GameOverErr:
                self.game_over()


if __name__ == '__main__':
    game = Game()
    game.run()
