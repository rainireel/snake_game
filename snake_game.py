import pygame
import sys
import random

# Initialize Pygame
pygame.init()
pygame.mixer.init()


# Game settings
WIDTH = 800
HEIGHT = 600
GRID_SIZE = 20 # Each snake segment and food item will be this size
# Difficulty Settings
DIFFICULTY_LEVELS = {
    'Easy': 10,
    'Medium': 15,
    'Hard': 20
}
current_difficulty = 'Easy'
current_fps = DIFFICULTY_LEVELS[current_difficulty]

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

# Food (will be updated with type, color, etc.)
food = {}

# Food Types
FOOD_TYPES = {
    'NORMAL': {'color': GREEN, 'points': 10},
    'BONUS': {'color': YELLOW, 'points': 25},
    'SPECIAL': {'color': (138, 43, 226), 'points': 50} # BlueViolet for special
}

# Score
score = 0
high_scores = [] # List to store top scores
HIGH_SCORE_FILE = "high_scores.txt"
font = pygame.font.Font(None, 36) # Default font, size 36
large_font = pygame.font.Font(None, 72) # Large font for titles

# --- Sound Effects ---
chew_sound = pygame.mixer.Sound('assets/sounds/chew.wav')
death_sound = pygame.mixer.Sound('assets/sounds/death.wav')
hiss_sound = pygame.mixer.Sound('assets/sounds/hiss.wav')

# --- Background Music ---
try:
    pygame.mixer.music.load('assets/sounds/background.mp3')
    pygame.mixer.music.set_volume(0.5) # Set volume to 50%
    pygame.mixer.music.play(-1) # Play in a loop
except pygame.error:
    print("Background music 'assets/sounds/background.mp3' not found or could not be played.")


def load_high_scores():
    """Loads high scores from a file."""
    try:
        with open(HIGH_SCORE_FILE, "r") as f:
            return sorted([int(line.strip()) for line in f.readlines()], reverse=True)[:5]
    except FileNotFoundError:
        return [] # Return empty list if file doesn't exist

def save_high_scores():
    """Saves the high scores to a file."""
    with open(HIGH_SCORE_FILE, "w") as f:
        for score_item in high_scores:
            f.write(f"{score_item}\n")

# Game over information
collision_cause = "" # To store what caused game over (wall, self)

# Initial direction of the snake
current_direction = 'RIGHT'
direction_buffer = [] # To handle quick successive key presses

# Menu selection
menu_selection = 0 # 0: Start, 1: Difficulty, 2: Quit
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
    """Generates a new food item with a random type and position."""
    global food

    # Determine food type (e.g., 80% normal, 15% bonus, 5% special)
    food_type_name = random.choices(['NORMAL', 'BONUS', 'SPECIAL'], weights=[0.8, 0.15, 0.05], k=1)[0]
    food_type_info = FOOD_TYPES[food_type_name]

    while True:
        new_x = random.randrange(GRID_SIZE, WIDTH - GRID_SIZE, GRID_SIZE)
        new_y = random.randrange(GRID_SIZE, HEIGHT - GRID_SIZE, GRID_SIZE)
        
        # Check if food spawns on the snake
        overlap = False
        for segment in snake_segments:
            if segment['x'] == new_x and segment['y'] == new_y:
                overlap = True
                break
        
        if not overlap:
            food = {
                'x': new_x, 
                'y': new_y, 
                'type': food_type_name,
                'color': food_type_info['color'],
                'points': food_type_info['points']
            }
            break # Valid food position found

# Ensure this function is exactly as below in your snake_game.py
def move_snake():
    """Updates the position of snake segments based on current_direction."""
    global current_state, collision_cause, score, food, high_scores

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
    if new_head['x'] == food['x'] and new_head['y'] == food['y']:
        chew_sound.play()
        score += food['points'] # Add points based on food type
        spawn_food() # Food eaten, so spawn new food
        food_eaten = True # Mark that food was eaten so snake grows

        # Increase speed every 50 points
        if score % 50 == 0:
            global current_fps
            current_fps = min(current_fps + 2, 30) # Increase FPS by 2, max 30

    # If food was NOT eaten, remove the last segment (tail) to keep length consistent
    if not food_eaten:
        snake_segments.pop() 
    
    # Check for collisions
    # --- Collision Checks ---
    collided = False
    if check_wall_collision():
        collision_cause = "wall"
        collided = True
    elif check_self_collision():
        collision_cause = "self"
        collided = True

    if collided:
        death_sound.play()
        current_state = GameState.GAME_OVER
        # Update high scores
        high_scores.append(score)
        high_scores.sort(reverse=True)
        high_scores = high_scores[:5] # Keep only top 5
        save_high_scores()

def draw_elements():
    """Draws the snake, food, walls, and score on the screen."""
    screen.fill(BLACK) # Clear screen

    # Draw walls (blue rectangles around the edge)
    pygame.draw.rect(screen, BLUE, (0, 0, WIDTH, GRID_SIZE)) # Top wall
    pygame.draw.rect(screen, BLUE, (0, HEIGHT - GRID_SIZE, WIDTH, GRID_SIZE)) # Bottom wall
    pygame.draw.rect(screen, BLUE, (0, 0, GRID_SIZE, HEIGHT)) # Left wall
    pygame.draw.rect(screen, BLUE, (WIDTH - GRID_SIZE, 0, GRID_SIZE, HEIGHT)) # Right wall

    # Draw food (as an apple)
    apple_radius = GRID_SIZE // 2
    apple_center = (food['x'] + apple_radius, food['y'] + apple_radius)
    pygame.draw.circle(screen, food['color'], apple_center, apple_radius)
    # Stem
    stem_rect = pygame.Rect(food['x'] + apple_radius - 2, food['y'] - 5, 4, 5)
    pygame.draw.rect(screen, (139, 69, 19), stem_rect) # SaddleBrown color

    # Draw snake segments
    for i, segment in enumerate(snake_segments):
        rect = pygame.Rect(segment['x'], segment['y'], GRID_SIZE, GRID_SIZE)
        
        if i == 0: # Head
            pygame.draw.rect(screen, RED, rect)
            # Eyes
            eye_size = 3
            if current_direction in ['UP', 'DOWN']:
                eye1 = pygame.Rect(segment['x'] + 3, segment['y'] + 5, eye_size, eye_size)
                eye2 = pygame.Rect(segment['x'] + GRID_SIZE - 6, segment['y'] + 5, eye_size, eye_size)
            else: # LEFT or RIGHT
                eye1 = pygame.Rect(segment['x'] + 5, segment['y'] + 3, eye_size, eye_size)
                eye2 = pygame.Rect(segment['x'] + 5, segment['y'] + GRID_SIZE - 6, eye_size, eye_size)
            pygame.draw.rect(screen, BLACK, eye1)
            pygame.draw.rect(screen, BLACK, eye2)

        elif i == len(snake_segments) - 1: # Tail
            # Draw a slightly smaller rectangle for a tapered look
            tail_rect = pygame.Rect(segment['x'] + 2, segment['y'] + 2, GRID_SIZE - 4, GRID_SIZE - 4)
            pygame.draw.rect(screen, DARK_GREEN, tail_rect)
        else: # Body
            # Alternate colors for body segments
            color = DARK_GREEN if i % 2 == 0 else (0, 200, 0)
            pygame.draw.rect(screen, color, rect)
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
    """Displays the main menu with options, difficulty, and high scores."""
    screen.fill(BLACK)
    
    # Title
    title = large_font.render("SNAKE GAME", True, WHITE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

    # Menu options
    menu_options = ["Start Game", f"Difficulty: {current_difficulty}", "Quit"]
    y_offset = 200
    for i, option in enumerate(menu_options):
        color = YELLOW if i == menu_selection else WHITE
        text = font.render(option, True, color)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y_offset + i * 50))

    # High Scores Display
    high_score_title = font.render("Top 5 High Scores:", True, YELLOW)
    screen.blit(high_score_title, (50, 150))
    if not high_scores:
        no_scores_text = font.render("No scores yet!", True, WHITE)
        screen.blit(no_scores_text, (50, 200))
    else:
        for i, hs in enumerate(high_scores):
            hs_text = font.render(f"{i+1}. {hs}", True, WHITE)
            screen.blit(hs_text, (50, 200 + i * 40))

    # Instructions
    instruction_text = font.render("Use arrow keys to navigate & ENTER to select", True, GRAY)
    screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT - 50))

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
    
    if high_scores:
        high_score_message = font.render(f"High Score: {high_scores[0]}", True, YELLOW)
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
    global snake_segments, food, score, current_direction, collision_cause, direction_buffer, current_state, current_fps
    snake_segments = [
        {'x': WIDTH // 2, 'y': HEIGHT // 2},
        {'x': WIDTH // 2 - GRID_SIZE, 'y': HEIGHT // 2},
        {'x': WIDTH // 2 - (2 * GRID_SIZE), 'y': HEIGHT // 2},
    ]
    spawn_food()
    score = 0
    current_state = GameState.PLAYING
    current_fps = DIFFICULTY_LEVELS[current_difficulty] # Reset speed to current difficulty
    current_direction = 'RIGHT'
    collision_cause = ""
    direction_buffer = []

def start_new_game():
    """Starts a new game from the menu."""
    reset_game()

def handle_menu_input(event):
    """Handles input for the main menu."""
    global menu_selection, current_state, current_difficulty, current_fps
    
    if event.key == pygame.K_UP:
        menu_selection = (menu_selection - 1) % 3
    elif event.key == pygame.K_DOWN:
        menu_selection = (menu_selection + 1) % 3
    elif event.key == pygame.K_RETURN:
        if menu_selection == 0:  # Start Game
            start_new_game()
        elif menu_selection == 1:  # Change Difficulty
            difficulty_options = list(DIFFICULTY_LEVELS.keys())
            current_index = difficulty_options.index(current_difficulty)
            current_difficulty = difficulty_options[(current_index + 1) % len(difficulty_options)]
            current_fps = DIFFICULTY_LEVELS[current_difficulty]
        elif menu_selection == 2:  # Quit
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
high_scores = load_high_scores()
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
    clock.tick(current_fps) 

pygame.quit()
sys.exit()
