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

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My First Python Game!")
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
    
    # Fill screen
    screen.fill(BLACK)
    
    # Draw player (red square)
    pygame.draw.rect(screen, RED, (player_x, player_y, 50, 50))
    
    # Update screen
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()