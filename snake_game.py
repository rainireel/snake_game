import pygame
import sys

# Initialize Pygame
pygame.init()

# Game settings
WIDTH = 800
HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PLAYER_SPEED = 5

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Snake Game - Use Arrow Keys!")
clock = pygame.time.Clock()

# Player position
player_x = WIDTH // 2
player_y = HEIGHT // 2

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Get keyboard input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT] and player_x < WIDTH - 50:
        player_x += PLAYER_SPEED
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= PLAYER_SPEED
    if keys[pygame.K_DOWN] and player_y < HEIGHT - 50:
        player_y += PLAYER_SPEED
    
    # Fill screen
    screen.fill(BLACK)
    
    # Draw player (red square)
    pygame.draw.rect(screen, RED, (player_x, player_y, 50, 50))
    
    # Update screen
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()