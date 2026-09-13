import random

import pygame

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Ball properties
BALL_SIZE = 20
BALL_SPEED_X = 5
BALL_SPEED_Y = 5

# Paddle properties
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
PADDLE_SPEED = 10

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("One Player Pong")

# Ball position
ball_x = SCREEN_WIDTH // 2
ball_y = SCREEN_HEIGHT // 2

# Ball direction
ball_dx = BALL_SPEED_X
ball_dy = BALL_SPEED_Y

# Paddle position
paddle_y = SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the paddle
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and paddle_y > 0:
        paddle_y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and paddle_y < SCREEN_HEIGHT - PADDLE_HEIGHT:
        paddle_y += PADDLE_SPEED

    # Move the ball
    ball_x += ball_dx
    ball_y += ball_dy

    # Ball collision with top and bottom
    if ball_y <= 0 or ball_y >= SCREEN_HEIGHT - BALL_SIZE:
        ball_dy *= -1

    # Ball collision with paddle
    if (ball_x <= PADDLE_WIDTH and paddle_y < ball_y < paddle_y + PADDLE_HEIGHT):
        ball_dx *= -1

    # Ball out of bounds
    if ball_x < 0:
        ball_x = SCREEN_WIDTH // 2
        ball_y = SCREEN_HEIGHT // 2
        ball_dx = BALL_SPEED_X * random.choice([-1, 1])
        ball_dy = BALL_SPEED_Y * random.choice([-1, 1])

    # Clear the screen
    screen.fill(BLACK)

    # Draw the ball
    pygame.draw.rect(screen, WHITE, (ball_x, ball_y, BALL_SIZE, BALL_SIZE))

    # Draw the paddle
    pygame.draw.rect(screen, WHITE, (0, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))

    # Update the display
    pygame.display.flip()

    # Frame rate
    pygame.time.Clock().tick(60)

pygame.quit()
