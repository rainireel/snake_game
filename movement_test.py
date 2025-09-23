import pygame
import sys

# Initialize Pygame
pygame.init()

# Game settings
WIDTH = 800
HEIGHT = 600
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Movement Test")
clock = pygame.time.Clock()

# Simple rectangle position
x = 400
y = 300
speed = 5

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Keyboard input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x -= speed
    if keys[pygame.K_RIGHT]:
        x += speed
    if keys[pygame.K_UP]:
        y -= speed
    if keys[pygame.K_DOWN]:
        y += speed
    
    # Fill screen
    screen.fill(BLACK)
    
    # Draw moving rectangle
    pygame.draw.rect(screen, RED, (x, y, 50, 50))
    
    # Update screen
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()