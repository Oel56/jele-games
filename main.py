import pygame
import sys
import random
import os

pygame.init()
pygame.mixer.init()

CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
WIDTH, HEIGHT = GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE

BLACK = (15, 15, 15)
GREEN = (0, 255, 100)
RED = (255, 60, 60)
WHITE = (240, 240, 240)
GRAY = (40, 40, 40)

pygame.font.init()
FONT_LARGE = pygame.font.Font(None, 72)
FONT_MEDIUM = pygame.font.Font(None, 36)
FONT_SMALL = pygame.font.Font(None, 28)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🐍 Snake Game!!")
clock = pygame.time.Clock()

def reset_game():
    snake = [(5, 5), (4, 5), (3, 5)]
    direction = (1, 0)
    food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
    score = 0
    return snake, direction, food, score

def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

def draw_snake(snake):
    for i, (x, y) in enumerate(snake):
        color = GREEN if i == 0 else (0, 180, 60)
        pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE - 1, CELL_SIZE - 1))

def draw_food(food):
    pygame.draw.rect(screen, RED, (food[0] * CELL_SIZE, food[1] * CELL_SIZE, CELL_SIZE - 1, CELL_SIZE - 1))

def draw_text(text, font, color, x, y, center=True):
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(x, y)) if center else surface.get_rect(topleft=(x, y))
    screen.blit(surface, rect)

HIGHSCORE_FILE = "highscore.txt"
if not os.path.exists(HIGHSCORE_FILE):
    with open(HIGHSCORE_FILE, "w") as f:
        f.write("0")

def get_highscore():
    with open(HIGHSCORE_FILE, "r") as f:
        return int(f.read().strip())

def save_highscore(score):
    high = get_highscore()
    if score > high:
        with open(HIGHSCORE_FILE, "w") as f:
            f.write(str(score))

def game_loop():
    snake, direction, food, score = reset_game()
    running = True
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, 1):
                    direction = (0, -1)
                elif event.key == pygame.K_DOWN and direction != (0, -1):
                    direction = (0, 1)
                elif event.key == pygame.K_LEFT and direction != (1, 0):
                    direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                    direction = (1, 0)
                elif event.key == pygame.K_r and game_over:
                    return  
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        if not game_over:
            
            new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
            snake.insert(0, new_head)

            
            if new_head == food:
                score += 1
                food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            else:
                snake.pop()

            
            if (
                new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
                new_head[1] < 0 or new_head[1] >= GRID_HEIGHT or
                new_head in snake[1:]
            ):
                game_over = True
                save_highscore(score)

        
        screen.fill(BLACK)
        draw_grid()
        draw_snake(snake)
        draw_food(food)
        draw_text(f"Score: {score}", FONT_SMALL, WHITE, 60, 20, center=False)
        draw_text(f"High: {get_highscore()}", FONT_SMALL, WHITE, WIDTH - 120, 20, center=False)

        if game_over:
            draw_text("GAME OVER", FONT_LARGE, RED, WIDTH // 2, HEIGHT // 2 - 20)
            draw_text("Press R to Restart or ESC to Quit", FONT_MEDIUM, WHITE, WIDTH // 2, HEIGHT // 2 + 40)

        pygame.display.flip()

        
        clock.tick(10 + score // 2)


while True:
    game_loop()
