import pygame
import random

# Initialize pygame and mixer
pygame.init()
pygame.mixer.init()

# Window setup
WIDTH, HEIGHT = 600, 400
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🐍 Snake Game")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED   = (255, 0, 0)
BLACK = (0, 0, 0)

# Snake and game settings
snake_block = 20
snake_speed = 10

# Fonts
font = pygame.font.SysFont("comicsansms", 30)
small_font = pygame.font.SysFont("comicsansms", 20)

# Load sounds (make sure .wav files are in same folder)
EAT_SOUND = pygame.mixer.Sound("eat.wav")
GAME_OVER_SOUND = pygame.mixer.Sound("gameover.wav")

def draw_snake(snake_list):
    for x, y in snake_list:
        pygame.draw.rect(win, GREEN, [x, y, snake_block, snake_block])

def show_score(score):
    text = font.render(f"Score: {score}", True, WHITE)
    win.blit(text, [10, 10])

def show_message(text, color, y_offset=0, size="normal"):
    current_font = font if size == "normal" else small_font
    msg = current_font.render(text, True, color)
    text_rect = msg.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
    win.blit(msg, text_rect)

def game_loop():
    x = WIDTH // 2
    y = HEIGHT // 2
    x_change = 0
    y_change = 0

    snake_list = []
    length = 1
    speed = snake_speed

    food_x = random.randint(0, (WIDTH - snake_block) // snake_block) * snake_block
    food_y = random.randint(0, (HEIGHT - snake_block) // snake_block) * snake_block

    clock = pygame.time.Clock()
    game_over = False
    game_close = False

    while not game_over:
        while game_close:
            win.fill(BLACK)
            show_message("Game Over!", RED, -40)
            show_message("Press C to Play Again", WHITE, 10, size="small")
            show_message("Press Q to Quit", WHITE, 40, size="small")
            show_message(f"Your Score: {length - 1}", WHITE, 80, size="small")
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    elif event.key == pygame.K_c:
                        game_loop()
                elif event.type == pygame.QUIT:
                    game_over = True
                    game_close = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_change == 0:
                    x_change = -snake_block
                    y_change = 0
                elif event.key == pygame.K_RIGHT and x_change == 0:
                    x_change = snake_block
                    y_change = 0
                elif event.key == pygame.K_UP and y_change == 0:
                    y_change = -snake_block
                    x_change = 0
                elif event.key == pygame.K_DOWN and y_change == 0:
                    y_change = snake_block
                    x_change = 0

        x += x_change
        y += y_change

        # Boundary check
        if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0:
            GAME_OVER_SOUND.play()
            game_close = True

        win.fill(BLACK)
        pygame.draw.rect(win, RED, [food_x, food_y, snake_block, snake_block])

        snake_head = [x, y]
        snake_list.append(snake_head)
        if len(snake_list) > length:
            del snake_list[0]

        # Self-collision
        for block in snake_list[:-1]:
            if block == snake_head:
                GAME_OVER_SOUND.play()
                game_close = True

        draw_snake(snake_list)
        show_score(length - 1)
        pygame.display.update()

        # Eat food
        if x == food_x and y == food_y:
            EAT_SOUND.play()
            food_x = random.randint(0, (WIDTH - snake_block) // snake_block) * snake_block
            food_y = random.randint(0, (HEIGHT - snake_block) // snake_block) * snake_block
            length += 1
            speed += 1  # Increase speed for challenge

        clock.tick(speed)

    pygame.quit()
    quit()

# Start the game
game_loop()
