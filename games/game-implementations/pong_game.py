import pygame
import random
from paddle import Paddle
from ball import Ball

# Initialize Pygame
pygame.init()

# Set up the game window
window_width = 800
window_height = 600
game_window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("One Player Pong")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create game objects
paddle_width = 100
paddle_height = 20
paddle = Paddle(window_width // 2 - paddle_width // 2, window_height - 50, paddle_width, paddle_height, WHITE)
ball = Ball(window_width // 2, window_height // 2, 10, WHITE, 5)

# Set up the game clock
clock = pygame.time.Clock()

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Update game state
    
    # Render the game
    game_window.fill(BLACK)
    
    pygame.display.update()
    clock.tick(60)  # Limit to 60 FPS

# Quit the game
pygame.quit()
