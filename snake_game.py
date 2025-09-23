import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Game settings
WIDTH = 800
HEIGHT = 600
GRID_SIZE = 20 # Each snake segment and food item will be this size
FPS = 10     # Game speed (frames per second)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)       # Snake Head
GREEN = (0, 255, 0)     # Food
DARK_GREEN = (0, 150, 0) # Snake Body
BLUE = (0, 0, 255)      # Walls

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game - Enhanced Collisions")
clock = pygame.time.Clock()

# --- Game Variables ---

# Snake starts with 3 segments
snake_segments = [
    {'x': WIDTH // 2, 'y': HEIGHT // 2},          # Head
    {'x': WIDTH // 2 - GRID_SIZE, 'y': HEIGHT // 2}, # Body 1
    {'x': WIDTH // 2 - (2 * GRID_SIZE), 'y': HEIGHT // 2}, # Body 2
]

# Food position (will be updated)
food_position = {'x': 0, 'y': 0}

# Score
score = 0
font = pygame.font.Font(None, 36) # Default font, size 36

# Game state
game_over = False
collision_cause = "" # To store what caused game over (wall, self)

# Initial direction of the snake
current_direction = 'RIGHT'
direction_buffer = [] # To handle quick successive key presses

# --- Functions for game logic (to be filled in) ---

def spawn_food():
    """Generates random coordinates for food, ensuring it's on the grid and not on the snake."""
    global food_position
    while True:
        # Food coordinates must be multiples of GRID_SIZE
        new_x = random.randrange(GRID_SIZE, WIDTH - GRID_SIZE, GRID_SIZE)
        new_y = random.randrange(GRID_SIZE, HEIGHT - GRID_SIZE, GRID_SIZE)
        
        food_position = {'x': new_x, 'y': new_y}
        
        # Check if food spawns on the snake
        overlap = False
        for segment in snake_segments:
            if segment['x'] == food_position['x'] and segment['y'] == food_position['y']:
                overlap = True
                break
        if not overlap:
            break # Valid food position found

def move_snake():
    """Updates the position of snake segments based on current_direction."""
    global game_over, collision_cause

    # Get the head's current position
    head_x = snake_segments[0]['x']
    head_y = snake_segments[0]['y']

    # Create new head position based on current_direction
    new_head = {'x': head_x, 'y': head_y}
    if current_direction == 'UP':
        new_head['y'] -= GRID_SIZE
    elif current_direction == 'DOWN':
        new_head['y'] += GRID_SIZE
    elif current_direction == 'LEFT':
        new_head['x'] -= GRID_SIZE
    elif current_direction == 'RIGHT':
        new_head['x'] += GRID_SIZE

    # Insert new head at the beginning of the list
    snake_segments.insert(0, new_head)

    # --- Collision Checks ---
    # These will be detailed in separate functions, but called here

    # Temporarily remove the tail if no food eaten
    # If food is eaten, the tail is NOT removed, making the snake grow.
    # This logic will be added when we implement food collision properly.
    if new_head['x'] == food_position['x'] and new_head['y'] == food_position['y']:
        # Food eaten, don't pop tail (snake grows), spawn new food
        pass # We'll fill this in with actual food logic later
    else:
        snake_segments.pop() # Remove the last segment (tail)
    
    # Placeholder for game over conditions
    # if check_wall_collision():
    #     game_over = True
    #     collision_cause = "wall"
    # if check_self_collision():
    #     game_over = True
    #     collision_cause = "self"

def draw_elements():
    """Draws the snake, food, walls, and score on the screen."""
    screen.fill(BLACK) # Clear screen

    # Draw walls (blue rectangles around the edge)
    pygame.draw.rect(screen, BLUE, (0, 0, WIDTH, GRID_SIZE)) # Top wall
    pygame.draw.rect(screen, BLUE, (0, HEIGHT - GRID_SIZE, WIDTH, GRID_SIZE)) # Bottom wall
    pygame.draw.rect(screen, BLUE, (0, 0, GRID_SIZE, HEIGHT)) # Left wall
    pygame.draw.rect(screen, BLUE, (WIDTH - GRID_SIZE, 0, GRID_SIZE, HEIGHT)) # Right wall

    # Draw food
    pygame.draw.rect(screen, GREEN, (food_position['x'], food_position['y'], GRID_SIZE, GRID_SIZE))

    # Draw snake segments
    for i, segment in enumerate(snake_segments):
        color = RED if i == 0 else DARK_GREEN # Head is red, body is dark green
        pygame.draw.rect(screen, color, (segment['x'], segment['y'], GRID_SIZE, GRID_SIZE))
        # Optional: Draw numbers on segments for debugging
        # segment_num_text = font.render(str(i), True, WHITE)
        # screen.blit(segment_num_text, (segment['x'] + 2, segment['y'] + 2))

    # Draw score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (GRID_SIZE, GRID_SIZE + 10)) # Adjust position for visibility
    
    # Draw length
    length_text = font.render(f"Length: {len(snake_segments)}", True, WHITE)
    screen.blit(length_text, (GRID_SIZE, GRID_SIZE + 50))

def show_game_over_screen():
    """Displays the game over message and final score."""
    game_over_message = font.render("GAME OVER!", True, RED)
    cause_message = font.render(f"Cause: {collision_cause} collision", True, WHITE)
    final_score_message = font.render(f"Final Score: {score}", True, WHITE)
    restart_message = font.render("Press R to Restart", True, WHITE)

    screen.blit(game_over_message, (WIDTH // 2 - game_over_message.get_width() // 2, HEIGHT // 2 - 100))
    screen.blit(cause_message, (WIDTH // 2 - cause_message.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(final_score_message, (WIDTH // 2 - final_score_message.get_width() // 2, HEIGHT // 2))
    screen.blit(restart_message, (WIDTH // 2 - restart_message.get_width() // 2, HEIGHT // 2 + 50))

def reset_game():
    """Resets all game variables to their initial state."""
    global snake_segments, food_position, score, game_over, current_direction, collision_cause, direction_buffer
    snake_segments = [
        {'x': WIDTH // 2, 'y': HEIGHT // 2},
        {'x': WIDTH // 2 - GRID_SIZE, 'y': HEIGHT // 2},
        {'x': WIDTH // 2 - (2 * GRID_SIZE), 'y': HEIGHT // 2},
    ]
    spawn_food()
    score = 0
    game_over = False
    current_direction = 'RIGHT'
    collision_cause = ""
    direction_buffer = []

# Initial setup calls
spawn_food()

# --- Main Game Loop ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                reset_game()
            
            # Store direction changes in a buffer to prevent 180 degree turns
            if not game_over:
                if event.key == pygame.K_UP and current_direction != 'DOWN':
                    direction_buffer.append('UP')
                elif event.key == pygame.K_DOWN and current_direction != 'UP':
                    direction_buffer.append('DOWN')
                elif event.key == pygame.K_LEFT and current_direction != 'RIGHT':
                    direction_buffer.append('LEFT')
                elif event.key == pygame.K_RIGHT and current_direction != 'LEFT':
                    direction_buffer.append('RIGHT')

    if not game_over:
        # Process direction buffer for smooth turns
        if direction_buffer:
            current_direction = direction_buffer.pop(0)

        move_snake() # This is where the snake moves
    
    draw_elements() # Draw everything
    
    if game_over:
        show_game_over_screen()

    pygame.display.flip() # Update the full display Surface to the screen
    clock.tick(FPS) # Control the game speed

pygame.quit()
sys.exit()