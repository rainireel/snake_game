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

# Game States
class GameState:
    MENU = "menu"
    PLAYING = "playing"
    GAME_OVER = "game_over"
    PAUSED = "paused"

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)       # Snake Head
GREEN = (0, 255, 0)     # Food
DARK_GREEN = (0, 150, 0) # Snake Body
BLUE = (0, 0, 255)      # Walls
GRAY = (128, 128, 128)  # Menu items
YELLOW = (255, 255, 0)  # Highlighted menu items

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game - Enhanced Game States")
clock = pygame.time.Clock()

# --- Game Variables ---

# Current game state
current_state = GameState.MENU

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
high_score = 0
font = pygame.font.Font(None, 36) # Default font, size 36
large_font = pygame.font.Font(None, 72) # Large font for titles

# Game over information
collision_cause = "" # To store what caused game over (wall, self)

# Initial direction of the snake
current_direction = 'RIGHT'
direction_buffer = [] # To handle quick successive key presses

# Menu selection
menu_selection = 0
game_over_selection = 0

# --- Functions for game logic ---

def check_wall_collision():
    """Check if snake head hits the walls."""
    head = snake_segments[0]
    return (head['x'] < GRID_SIZE or 
            head['x'] >= WIDTH - GRID_SIZE or 
            head['y'] < GRID_SIZE or 
            head['y'] >= HEIGHT - GRID_SIZE)

def check_self_collision():
    """Check if snake head hits its own body."""
    head = snake_segments[0]
    for segment in snake_segments[1:]:
        if head['x'] == segment['x'] and head['y'] == segment['y']:
            return True
    return False

def spawn_food():
    """Generates random coordinates for food, ensuring it's on the grid and not on the snake or walls."""
    global food_position
    while True:
        # Food coordinates must be multiples of GRID_SIZE
        # Ensure food spawns within the playable area (GRID_SIZE to WIDTH/HEIGHT - 2*GRID_SIZE for walls)
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

# Ensure this function is exactly as below in your snake_game.py
def move_snake():
    """Updates the position of snake segments based on current_direction."""
    global current_state, collision_cause, score, food_position, high_score

    # Get the head's current position
    head_x = snake_segments[0]['x']
    head_y = snake_segments[0]['y']

    # Calculate new head position based on current_direction
    new_head_x = head_x
    new_head_y = head_y
    
    if current_direction == 'UP':
        new_head_y -= GRID_SIZE
    elif current_direction == 'DOWN':
        new_head_y += GRID_SIZE
    elif current_direction == 'LEFT':
        new_head_x -= GRID_SIZE
    elif current_direction == 'RIGHT':
        new_head_x += GRID_SIZE

    new_head = {'x': new_head_x, 'y': new_head_y}

    # Add the new head to the beginning of the snake
    snake_segments.insert(0, new_head)

    # Check for food collision (AFTER new head is added, but BEFORE popping tail)
    food_eaten = False
    if new_head['x'] == food_position['x'] and new_head['y'] == food_position['y']:
        score += 10
        spawn_food() # Food eaten, so spawn new food
        food_eaten = True # Mark that food was eaten so snake grows
        # print(f"Food eaten! Score: {score}, Length: {len(snake_segments)}") # Debug line (optional)

    # If food was NOT eaten, remove the last segment (tail) to keep length consistent
    if not food_eaten:
        snake_segments.pop() 
    
    # Check for collisions
    if check_wall_collision():
        current_state = GameState.GAME_OVER
        collision_cause = "wall"
        if score > high_score:
            high_score = score
    elif check_self_collision():
        current_state = GameState.GAME_OVER
        collision_cause = "self"
        if score > high_score:
            high_score = score

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

def show_main_menu():
    """Displays the main menu with options."""
    screen.fill(BLACK)
    
    # Title
    title = large_font.render("SNAKE GAME", True, WHITE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))
    
    # Menu options
    menu_options = ["Start Game", "Quit"]
    y_offset = HEIGHT // 2
    
    for i, option in enumerate(menu_options):
        color = YELLOW if i == menu_selection else WHITE
        text = font.render(option, True, color)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y_offset + i * 50))
    
    # Instructions
    instructions = [
        "Use arrow keys to navigate",
        "Press ENTER to select",
        "Use arrow keys during game to control snake"
    ]
    
    for i, instruction in enumerate(instructions):
        text = font.render(instruction, True, GRAY)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 100 + i * 25))

def show_game_over_screen():
    """Displays the enhanced game over screen with options."""
    screen.fill(BLACK)
    
    # Game Over title
    game_over_title = large_font.render("GAME OVER!", True, RED)
    screen.blit(game_over_title, (WIDTH // 2 - game_over_title.get_width() // 2, HEIGHT // 6))
    
    # Cause and score information
    cause_message = font.render(f"Cause: {collision_cause.title()} collision", True, WHITE)
    screen.blit(cause_message, (WIDTH // 2 - cause_message.get_width() // 2, HEIGHT // 3))
    
    final_score_message = font.render(f"Final Score: {score}", True, WHITE)
    screen.blit(final_score_message, (WIDTH // 2 - final_score_message.get_width() // 2, HEIGHT // 3 + 40))
    
    if high_score > 0:
        high_score_message = font.render(f"High Score: {high_score}", True, YELLOW)
        screen.blit(high_score_message, (WIDTH // 2 - high_score_message.get_width() // 2, HEIGHT // 3 + 80))
    
    # Menu options
    menu_options = ["Play Again", "Main Menu", "Quit"]
    y_offset = HEIGHT // 2 + 50
    
    for i, option in enumerate(menu_options):
        color = YELLOW if i == game_over_selection else WHITE
        text = font.render(option, True, color)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y_offset + i * 50))
    
    # Instructions
    instruction = font.render("Use UP/DOWN arrows and ENTER to select", True, GRAY)
    screen.blit(instruction, (WIDTH // 2 - instruction.get_width() // 2, HEIGHT - 50))

def reset_game():
    """Resets all game variables to their initial state."""
    global snake_segments, food_position, score, current_direction, collision_cause, direction_buffer, current_state
    snake_segments = [
        {'x': WIDTH // 2, 'y': HEIGHT // 2},
        {'x': WIDTH // 2 - GRID_SIZE, 'y': HEIGHT // 2},
        {'x': WIDTH // 2 - (2 * GRID_SIZE), 'y': HEIGHT // 2},
    ]
    spawn_food()
    score = 0
    current_state = GameState.PLAYING
    current_direction = 'RIGHT'
    collision_cause = ""
    direction_buffer = []

def start_new_game():
    """Starts a new game from the menu."""
    reset_game()

def handle_menu_input(event):
    """Handles input for the main menu."""
    global menu_selection, current_state
    
    if event.key == pygame.K_UP:
        menu_selection = (menu_selection - 1) % 2
    elif event.key == pygame.K_DOWN:
        menu_selection = (menu_selection + 1) % 2
    elif event.key == pygame.K_RETURN:
        if menu_selection == 0:  # Start Game
            start_new_game()
        elif menu_selection == 1:  # Quit
            return False
    return True

def handle_game_over_input(event):
    """Handles input for the game over screen."""
    global game_over_selection, current_state
    
    if event.key == pygame.K_UP:
        game_over_selection = (game_over_selection - 1) % 3
    elif event.key == pygame.K_DOWN:
        game_over_selection = (game_over_selection + 1) % 3
    elif event.key == pygame.K_RETURN:
        if game_over_selection == 0:  # Play Again
            start_new_game()
        elif game_over_selection == 1:  # Main Menu
            current_state = GameState.MENU
            game_over_selection = 0
        elif game_over_selection == 2:  # Quit
            return False
    return True

# Initial setup calls
spawn_food()

# --- Main Game Loop ---
running = True
while running:
    # 1. Event Handling (Input)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            # Handle different states
            if current_state == GameState.MENU:
                running = handle_menu_input(event)
            elif current_state == GameState.GAME_OVER:
                running = handle_game_over_input(event)
            elif current_state == GameState.PLAYING:
                # Handle game controls
                if event.key == pygame.K_UP and current_direction != 'DOWN':
                    direction_buffer.append('UP')
                elif event.key == pygame.K_DOWN and current_direction != 'UP':
                    direction_buffer.append('DOWN')
                elif event.key == pygame.K_LEFT and current_direction != 'RIGHT':
                    direction_buffer.append('LEFT')
                elif event.key == pygame.K_RIGHT and current_direction != 'LEFT':
                    direction_buffer.append('RIGHT')
                elif event.key == pygame.K_ESCAPE:
                    current_state = GameState.MENU

    # 2. Game Logic Update
    if current_state == GameState.PLAYING:
        # If there are buffered directions, pop the oldest one
        if direction_buffer:
            current_direction = direction_buffer.pop(0)

        move_snake() # This is where the snake's position is updated

    # 3. Drawing (Rendering)
    if current_state == GameState.MENU:
        show_main_menu()
    elif current_state == GameState.PLAYING:
        draw_elements() # Draw all game components
    elif current_state == GameState.GAME_OVER:
        show_game_over_screen()

    # Update the full display Surface to the screen
    pygame.display.flip() 
    # Control the game speed (FPS)
    clock.tick(FPS) 

pygame.quit()
sys.exit()