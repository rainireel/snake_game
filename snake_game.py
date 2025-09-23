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
FOOD_SIZE = 20

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Snake Game - Complete Collision Detection")
clock = pygame.time.Clock()

# Snake segments
snake_segments = [
    {'x': WIDTH // 2, 'y': HEIGHT // 2, 'size': 20},      # Head
    {'x': WIDTH // 2 - 20, 'y': HEIGHT // 2, 'size': 20}, # Body segment 1
    {'x': WIDTH // 2 - 40, 'y': HEIGHT // 2, 'size': 20}, # Body segment 2
]

# Food position
food_x = random.randint(50, WIDTH - 50)
food_y = random.randint(50, HEIGHT - 50)

# Game state
score = 0
game_over = False
font = pygame.font.Font(None, 36)

# ==================== COLLISION DETECTION FUNCTIONS ====================

def check_self_collision():
    """Check if snake head collides with any body segment"""
    head = snake_segments[0]
    for segment in snake_segments[1:]:  # Skip head
        if (head['x'] < segment['x'] + segment['size'] and
            head['x'] + head['size'] > segment['x'] and
            head['y'] < segment['y'] + segment['size'] and
            head['y'] + head['size'] > segment['y']):
            return True  # Self-collision detected
    return False

def check_wall_collision():
    """Check if snake hits the walls"""
    head = snake_segments[0]
    return (head['x'] <= 0 or head['x'] >= WIDTH - head['size'] or 
            head['y'] <= 0 or head['y'] >= HEIGHT - head['size'])

def check_food_collision():
    """Check if snake head collides with food"""
    head = snake_segments[0]
    return (head['x'] < food_x + FOOD_SIZE and
            head['x'] + head['size'] > food_x and
            head['y'] < food_y + FOOD_SIZE and
            head['y'] + head['size'] > food_y)

# ==================== GAME LOGIC FUNCTIONS ====================

def move_snake(direction):
    """Move the snake in the given direction"""
    # Move body segments (each follows the previous one)
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

def add_segment():
    """Add a new segment to the snake when it eats food"""
    last_segment = snake_segments[-1]
    new_segment = {
        'x': last_segment['x'],
        'y': last_segment['y'],
        'size': last_segment['size']
    }
    snake_segments.append(new_segment)

def spawn_food():
    """Spawn food in a random position that doesn't overlap with snake"""
    global food_x, food_y
    while True:
        food_x = random.randint(20, WIDTH - 40)
        food_y = random.randint(20, HEIGHT - 40)
        
        # Check if food overlaps with any snake segment
        overlap = False
        for segment in snake_segments:
            if (food_x < segment['x'] + segment['size'] and
                food_x + FOOD_SIZE > segment['x'] and
                food_y < segment['y'] + segment['size'] and
                food_y + FOOD_SIZE > segment['y']):
                overlap = True
                break
        
        if not overlap:
            break  # Found a valid position

def show_game_over(collision_type):
    """Display game over screen with collision info"""
    game_over_text = font.render("GAME OVER! Press R to restart", True, RED)
    final_score = font.render(f"Final Score: {score}", True, WHITE)
    
    # Different messages based on collision type
    if collision_type == "wall":
        cause_text = font.render("Cause: Hit the wall!", True, WHITE)
    elif collision_type == "self":
        cause_text = font.render("Cause: Ate yourself!", True, WHITE)
    else:
        cause_text = font.render("Cause: Unknown", True, WHITE)
    
    screen.blit(game_over_text, (WIDTH//2 - 180, HEIGHT//2 - 60))
    screen.blit(final_score, (WIDTH//2 - 100, HEIGHT//2 - 20))
    screen.blit(cause_text, (WIDTH//2 - 100, HEIGHT//2 + 20))

def reset_game():
    """Reset the game to initial state"""
    global snake_segments, food_x, food_y, score, game_over
    snake_segments = [
        {'x': WIDTH // 2, 'y': HEIGHT // 2, 'size': 20},
        {'x': WIDTH // 2 - 20, 'y': HEIGHT // 2, 'size': 20},
        {'x': WIDTH // 2 - 40, 'y': HEIGHT // 2, 'size': 20},
    ]
    spawn_food()
    score = 0
    game_over = False

# ==================== MAIN GAME LOOP ====================

# Game variables
current_direction = 'RIGHT'
direction_changed = False

# Initial food spawn
spawn_food()

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
                direction_changed = False
    
    if not game_over:
        # Get keyboard input (prevent 180° turns)
        keys = pygame.key.get_pressed()
        if not direction_changed:
            if keys[pygame.K_LEFT] and current_direction != 'RIGHT':
                current_direction = 'LEFT'
                direction_changed = True
            elif keys[pygame.K_RIGHT] and current_direction != 'LEFT':
                current_direction = 'RIGHT'
                direction_changed = True
            elif keys[pygame.K_UP] and current_direction != 'DOWN':
                current_direction = 'UP'
                direction_changed = True
            elif keys[pygame.K_DOWN] and current_direction != 'UP':
                current_direction = 'DOWN'
                direction_changed = True
        
        # Move snake
        move_snake(current_direction)
        direction_changed = False
        
        # ===== COLLISION DETECTION =====
        collision_type = None
        
        # Wall collision check
        if check_wall_collision():
            game_over = True
            collision_type = "wall"
            print("🚧 Wall collision detected!")
        
        # Self-collision check (only if not already game over)
        if not game_over and check_self_collision():
            game_over = True
            collision_type = "self"
            print("💥 Self-collision detected!")
        
        # Food collision check
        if not game_over and check_food_collision():
            score += 10
            spawn_food()  # Spawn new food in valid position
            add_segment()  # Snake grows
            print("🍎 Food collected! Score:", score)
    
    # ===== RENDERING =====
    # Fill screen
    screen.fill(BLACK)
    
    # Draw boundary walls
    pygame.draw.rect(screen, BLUE, (0, 0, WIDTH, 5))
    pygame.draw.rect(screen, BLUE, (0, 0, 5, HEIGHT))
    pygame.draw.rect(screen, BLUE, (WIDTH-5, 0, 5, HEIGHT))
    pygame.draw.rect(screen, BLUE, (0, HEIGHT-5, WIDTH, 5))
    
    # Draw food
    pygame.draw.rect(screen, GREEN, (food_x, food_y, FOOD_SIZE, FOOD_SIZE))
    
    # Draw snake (head is red, body is dark green)
    for i, segment in enumerate(snake_segments):
        color = RED if i == 0 else DARK_GREEN
        pygame.draw.rect(screen, color, (segment['x'], segment['y'], segment['size'], segment['size']))
    
    # Draw UI information
    score_text = font.render(f"Score: {score}", True, WHITE)
    length_text = font.render(f"Length: {len(snake_segments)}", True, WHITE)
    
    screen.blit(score_text, (10, 10))
    screen.blit(length_text, (10, 50))
    
    # Draw collision status
    collision_status = f"Collisions: Wall({check_wall_collision()}) Self({check_self_collision()})"
    collision_text = font.render(collision_status, True, WHITE)
    screen.blit(collision_text, (10, 90))
    
    # Show game over screen if applicable
    if game_over:
        show_game_over(collision_type)
    
    # Update screen
    pygame.display.flip()
    clock.tick(15)  # Game speed

pygame.quit()
sys.exit()