import pygame

class Paddle:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)
        
    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)
        
    def move(self, dy):
        self.y += dy
        self.rect.y = self.y
