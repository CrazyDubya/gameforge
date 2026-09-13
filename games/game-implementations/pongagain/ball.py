import pygame


class Ball:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed_x = 3
        self.speed_y = 3

    def update(self):
        self.rect.move_ip(self.speed_x, self.speed_y)

    def bounce(self):
        self.speed_x *= -1

    def reverse_x(self):
        self.speed_x *= -1

    def reverse_y(self):
        self.speed_y *= -1

    def render(self, window):
        pygame.draw.ellipse(window, (255, 255, 255), self.rect)
