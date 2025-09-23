import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Game settings
WIDTH = 800
HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PLAYER_SPEED = 5
FOOD_SIZE = 20

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game - Eat the Green Food!")
clock = pygame.time.Clock()

# Player (snake) position
player_x = WIDTH // 2
player_y = HEIGHT // 2
player_size = 50

# Food position (random)
food_x = random.randint(0, WIDTH - FOOD_SIZE)
food_y = random.randint(0, HEIGHT - FOOD_SIZE)

# Score
score = 0
font = pygame.font.Font(None, 36)  # Default font

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
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
        player_x += PLAYER_SPEED
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= PLAYER_SPEED
    if keys[pygame.K_DOWN] and player_y < HEIGHT - player_size:
        player_y += PLAYER_SPEED
    
    # Check if snake eats food
    if (player_x < food_x + FOOD_SIZE and
        player_x + player_size > food_x and
        player_y < food_y + FOOD_SIZE and
        player_y + player_size > food_y):
        # Snake ate the food!
        score += 10
        food_x = random.randint(0, WIDTH - FOOD_SIZE)
        food_y = random.randint(0, HEIGHT - FOOD_SIZE)
        player_size += 5  # Snake grows when it eats!
    
    # Fill screen
    screen.fill(BLACK)
    
    # Draw food (green square)
    pygame.draw.rect(screen, GREEN, (food_x, food_y, FOOD_SIZE, FOOD_SIZE))
    
    # Draw player (red snake)
    pygame.draw.rect(screen, RED, (player_x, player_y, player_size, player_size))
    
    # Draw score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    # Update screen
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()