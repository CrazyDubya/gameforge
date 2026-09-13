import pygame
import random

class Ball:
    def __init__(self, x, y, radius, color, speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed_x = speed
        self.speed_y = speed
        self.rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)
        
    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)
        
    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.rect.center = (self.x, self.y)
        
    def reset(self, window_width, window_height):
        self.x = window_width // 2
        self.y = window_height // 2
        self.speed_x = random.choice([-self.speed_x, self.speed_x])
        self.speed_y = random.choice([-self.speed_y, self.speed_y])
