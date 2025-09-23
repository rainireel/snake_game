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
BLUE = (0, 0, 255)
PLAYER_SPEED = 5
FOOD_SIZE = 20

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game - Don't Hit the Walls!")
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
font = pygame.font.Font(None, 36)

# Game state
game_over = False

def show_game_over():
    game_over_text = font.render("GAME OVER! Press R to restart", True, WHITE)
    final_score = font.render(f"Final Score: {score}", True, WHITE)
    screen.blit(game_over_text, (WIDTH//2 - 180, HEIGHT//2 - 50))
    screen.blit(final_score, (WIDTH//2 - 100, HEIGHT//2))

def reset_game():
    global player_x, player_y, player_size, food_x, food_y, score, game_over
    player_x = WIDTH // 2
    player_y = HEIGHT // 2
    player_size = 50
    food_x = random.randint(0, WIDTH - FOOD_SIZE)
    food_y = random.randint(0, HEIGHT - FOOD_SIZE)
    score = 0
    game_over = False

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                reset_game()
    
    if not game_over:
        # Get keyboard input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            player_x += PLAYER_SPEED
        if keys[pygame.K_UP]:
            player_y -= PLAYER_SPEED
        if keys[pygame.K_DOWN]:
            player_y += PLAYER_SPEED
        
        # Check wall collisions (game over condition)
        if (player_x <= 0 or player_x >= WIDTH - player_size or 
            player_y <= 0 or player_y >= HEIGHT - player_size):
            game_over = True
        
        # Check if snake eats food
        if (player_x < food_x + FOOD_SIZE and
            player_x + player_size > food_x and
            player_y < food_y + FOOD_SIZE and
            player_y + player_size > food_y):
            # Snake ate the food!
            score += 10
            food_x = random.randint(0, WIDTH - FOOD_SIZE)
            food_y = random.randint(0, HEIGHT - FOOD_SIZE)
            player_size += 5
    
    # Fill screen
    screen.fill(BLACK)
    
    # Draw boundary walls
    pygame.draw.rect(screen, BLUE, (0, 0, WIDTH, 5))  # Top
    pygame.draw.rect(screen, BLUE, (0, 0, 5, HEIGHT))  # Left
    pygame.draw.rect(screen, BLUE, (WIDTH-5, 0, 5, HEIGHT))  # Right
    pygame.draw.rect(screen, BLUE, (0, HEIGHT-5, WIDTH, 5))  # Bottom
    
    # Draw food (green square)
    pygame.draw.rect(screen, GREEN, (food_x, food_y, FOOD_SIZE, FOOD_SIZE))
    
    # Draw player (red snake)
    pygame.draw.rect(screen, RED, (player_x, player_y, player_size, player_size))
    
    # Draw score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    # Show game over screen
    if game_over:
        show_game_over()
    
    # Update screen
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()