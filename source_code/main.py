import time
import random
import pygame
from pygame.locals import *

SIZE = 40
BACKGROUND_COLOR = (131, 201, 119)


class Apple:
    def __init__(self, parent_screen):
        self.image = pygame.image.load("assets/apple.png").convert()
        self.parent_screen = parent_screen
        self.x = SIZE*3
        self.y = SIZE*3

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(0, 19)*SIZE
        self.y = random.randint(0, 14) * SIZE


class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load("assets/block.jpg").convert()
        self.x = [SIZE]*length
        self.y = [SIZE]*length
        self.direction = "right"

    def draw(self):
        self.parent_screen.fill(BACKGROUND_COLOR)
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def move_up(self):
        self.direction = "up"

    def move_down(self):
        self.direction = "down"

    def move_left(self):
        self.direction = "left"

    def move_right(self):
        self.direction = "right"

    def increase_len(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def walk(self):
        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i - 1]

        if self.direction == "down":
            self.y[0] += SIZE
        elif self.direction == "left":
            self.x[0] -= SIZE
        elif self.direction == "right":
            self.x[0] += SIZE
        elif self.direction == "up":
            self.y[0] -= SIZE

        self.draw()


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.play_background_music()
        pygame.display.set_caption("Snake And Apple Game")

        self.surface = pygame.display.set_mode((1000, 800))
        self.surface.fill(BACKGROUND_COLOR)
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    @staticmethod
    def is_collision(x1, y1, x2, y2):
        return x2 <= x1 < x2 + SIZE and y2 <= y1 < y2 + SIZE

    @staticmethod
    def play_sound(sound):
        sound = pygame.mixer.Sound(f"assets/{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    @staticmethod
    def play_background_music():
        pygame.mixer.music.load("assets/bg_music.mp3")
        pygame.mixer.music.play()

    def render_background(self):
        bg = pygame.image.load("assets/background.png")
        self.surface.blit(bg, (0, 0))

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # apple eating scenario
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("ding")
            self.snake.increase_len()
            self.apple.move()

        # itself collision
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("crash")
                raise "Game Over"

        # colliding with boundary
        if not (0 <= self.snake.x[0] <= 1000 and 0 <= self.snake.y[0] <= 800):
            self.play_sound('crash')
            raise "Hit the boundary error"

    def show_game_over(self):
        self.surface.fill(BACKGROUND_COLOR)
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game is Over ... Your Score : {self.snake.length}", True, (0, 0, 0))
        self.surface.blit(line1, (200, 300))
        line2 = font.render("To Play again press Enter ... To exit press Escape", True, (0, 0, 0))
        self.surface.blit(line2, (200, 350))
        pygame.display.flip()
        pygame.mixer.music.pause()

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score : {self.snake.length}", True, (0, 0, 0))
        self.surface.blit(score, (800, 10))

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(0.2)


if __name__ == '__main__':
    game = Game()
    game.run()
