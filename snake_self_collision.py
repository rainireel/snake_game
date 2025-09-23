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
DARK_GREEN = (0, 200, 0)
PLAYER_SPEED = 5

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game - Self-Collision Test")
clock = pygame.time.Clock()

# Snake as multiple segments (for self-collision testing)
snake_segments = [
    {'x': WIDTH // 2, 'y': HEIGHT // 2, 'size': 20},      # Head (segment 0)
    {'x': WIDTH // 2 - 20, 'y': HEIGHT // 2, 'size': 20}, # Body segment 1
    {'x': WIDTH // 2 - 40, 'y': HEIGHT // 2, 'size': 20}, # Body segment 2
    {'x': WIDTH // 2 - 60, 'y': HEIGHT // 2, 'size': 20}, # Body segment 3
]

# Game state
score = 0
game_over = False
font = pygame.font.Font(None, 36)

def check_self_collision():
    """
    Check if snake head collides with any part of its body
    Returns True if collision detected, False otherwise
    """
    head = snake_segments[0]  # First segment is the head
    
    # Check collision with each body segment (skip head itself)
    for i, segment in enumerate(snake_segments[1:], start=1):
        # Simple rectangle collision detection
        if (head['x'] < segment['x'] + segment['size'] and
            head['x'] + head['size'] > segment['x'] and
            head['y'] < segment['y'] + segment['size'] and
            head['y'] + head['size'] > segment['y']):
            return True  # Collision detected!
    
    return False  # No collision

def move_snake(direction):
    """Move the snake in the given direction"""
    # Move body segments (each segment follows the one before it)
    for i in range(len(snake_segments)-1, 0, -1):
        snake_segments[i]['x'] = snake_segments[i-1]['x']
        snake_segments[i]['y'] = snake_segments[i-1]['y']
    
    # Move head based on direction
    if direction == 'LEFT':
        snake_segments[0]['x'] -= PLAYER_SPEED
    elif direction == 'RIGHT':
        snake_segments[0]['x'] += PLAYER_SPEED
    elif direction == 'UP':
        snake_segments[0]['y'] -= PLAYER_SPEED
    elif direction == 'DOWN':
        snake_segments[0]['y'] += PLAYER_SPEED

def show_collision_debug():
    """Show debug information about collision detection"""
    head = snake_segments[0]
    debug_text = [
        f"Head: ({head['x']}, {head['y']})",
        f"Segments: {len(snake_segments)}",
        f"Self-Collision: {check_self_collision()}",
        "Collision Test: Head vs Each Body Segment:"
    ]
    
    for i, segment in enumerate(snake_segments[1:], start=1):
        collision = (head['x'] < segment['x'] + segment['size'] and
                    head['x'] + head['size'] > segment['x'] and
                    head['y'] < segment['y'] + segment['size'] and
                    head['y'] + head['size'] > segment['y'])
        debug_text.append(f"Segment {i}: ({segment['x']}, {segment['y']}) -> Collision: {collision}")
    
    return debug_text

def show_game_over():
    """Display game over screen with collision info"""
    game_over_text = font.render("SELF-COLLISION! Game Over - Press R to restart", True, RED)
    final_score = font.render(f"Final Score: {score}", True, WHITE)
    collision_info = font.render(f"Snake Length: {len(snake_segments)} - Head hit body segment!", True, WHITE)
    
    screen.blit(game_over_text, (WIDTH//2 - 250, HEIGHT//2 - 60))
    screen.blit(final_score, (WIDTH//2 - 100, HEIGHT//2 - 20))
    screen.blit(collision_info, (WIDTH//2 - 200, HEIGHT//2 + 20))

def reset_game():
    """Reset the game to initial state"""
    global snake_segments, score, game_over
    snake_segments = [
        {'x': WIDTH // 2, 'y': HEIGHT // 2, 'size': 20},
        {'x': WIDTH // 2 - 20, 'y': HEIGHT // 2, 'size': 20},
        {'x': WIDTH // 2 - 40, 'y': HEIGHT // 2, 'size': 20},
        {'x': WIDTH // 2 - 60, 'y': HEIGHT // 2, 'size': 20},
    ]
    score = 0
    game_over = False

# Game variables
current_direction = 'RIGHT'

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                reset_game()
                current_direction = 'RIGHT'
    
    if not game_over:
        # Get keyboard input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            current_direction = 'LEFT'
        elif keys[pygame.K_RIGHT]:
            current_direction = 'RIGHT'
        elif keys[pygame.K_UP]:
            current_direction = 'UP'
        elif keys[pygame.K_DOWN]:
            current_direction = 'DOWN'
        
        # Move snake
        move_snake(current_direction)
        
        # Check self-collision (THE MAIN FEATURE WE'RE TESTING)
        if check_self_collision():
            game_over = True
            print("🎯 Self-Collision Detected! Game Over!")
        
        # Simple scoring - just for testing
        score += 0.1  # Small increment to see progress
    
    # Fill screen
    screen.fill(BLACK)
    
    # Draw boundary walls
    pygame.draw.rect(screen, BLUE, (0, 0, WIDTH, 5))
    pygame.draw.rect(screen, BLUE, (0, 0, 5, HEIGHT))
    pygame.draw.rect(screen, BLUE, (WIDTH-5, 0, 5, HEIGHT))
    pygame.draw.rect(screen, BLUE, (0, HEIGHT-5, WIDTH, 5))
    
    # Draw snake segments with different colors
    for i, segment in enumerate(snake_segments):
        if i == 0:  # Head
            color = RED
        else:  # Body
            color = DARK_GREEN
        pygame.draw.rect(screen, color, (segment['x'], segment['y'], segment['size'], segment['size']))
        
        # Draw segment numbers for debugging
        segment_text = font.render(str(i), True, WHITE)
        screen.blit(segment_text, (segment['x'] + 5, segment['y'] + 5))
    
    # Draw score and info
    score_text = font.render(f"Score: {int(score)}", True, WHITE)
    length_text = font.render(f"Length: {len(snake_segments)}", True, WHITE)
    collision_text = font.render(f"Self-Collision: {check_self_collision()}", True, WHITE)
    
    screen.blit(score_text, (10, 10))
    screen.blit(length_text, (10, 50))
    screen.blit(collision_text, (10, 90))
    
    # Instructions
    instructions = font.render("Try to make the head hit the body segments!", True, GREEN)
    screen.blit(instructions, (WIDTH//2 - 200, HEIGHT - 40))
    
    # Show game over screen
    if game_over:
        show_game_over()
        
        # Show debug info in console
        print("\n=== COLLISION DEBUG INFO ===")
        debug_info = show_collision_debug()
        for line in debug_info:
            print(line)
        print("============================\n")
    
    # Update screen
    pygame.display.flip()
    clock.tick(10)  # Slow speed for testing collisions

pygame.quit()
sys.exit()