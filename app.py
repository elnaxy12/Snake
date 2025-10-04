import pygame
import sys
import random

# -------------------- CONFIG --------------------
CELL_SIZE = 32
GRID_WIDTH = 20
GRID_HEIGHT = 15
SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT
FPS = 8

# -------------------- INIT --------------------
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Pixel Game")
clock = pygame.time.Clock()

# -------------------- FONT & WARNA --------------------
font_big = pygame.font.SysFont("arial", 48, bold=True)
font_small = pygame.font.SysFont("arial", 28, bold=True)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 60, 60)
GRAY = (180, 180, 180)

# -------------------- LOAD SPRITES --------------------
head_up = pygame.image.load("assets/head_up.png").convert_alpha()
head_down = pygame.image.load("assets/head_down.png").convert_alpha()
head_left = pygame.image.load("assets/head_left.png").convert_alpha()
head_right = pygame.image.load("assets/head_right.png").convert_alpha()

body_h = pygame.image.load("assets/body_horizontal.png").convert_alpha()
body_v = pygame.image.load("assets/body_vertical.png").convert_alpha()
body_tl = pygame.image.load("assets/body_topleft.png").convert_alpha()
body_tr = pygame.image.load("assets/body_topright.png").convert_alpha()
body_bl = pygame.image.load("assets/body_bottomleft.png").convert_alpha()
body_br = pygame.image.load("assets/body_bottomright.png").convert_alpha()

tail_up = pygame.image.load("assets/tail_up.png").convert_alpha()
tail_down = pygame.image.load("assets/tail_down.png").convert_alpha()
tail_left = pygame.image.load("assets/tail_left.png").convert_alpha()
tail_right = pygame.image.load("assets/tail_right.png").convert_alpha()

food_sprite = pygame.image.load("assets/apple.png").convert_alpha()


# -------------------- GAME OVER SCREEN --------------------
overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
overlay.fill(BLACK)
screen.blit(overlay, (0, 0))


def game_over_screen(score):
    while True:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(0) 
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        # --- TEKS UTAMA ---
        game_over_text = font_big.render("GAME OVER", True, RED)
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 100))
        screen.blit(game_over_text, text_rect)

        score_text = font_small.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, SCREEN_HEIGHT//2 - 50))

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        

        # --- POSISI TOMBOL (rapi di tengah) ---
        button_width = 180
        button_height = 55
        gap = 20  
        start_rect = pygame.Rect(
            SCREEN_WIDTH//2 - button_width - gap//2, 
            SCREEN_HEIGHT//2 + 40, 
            button_width, 
            button_height
        )

        exit_rect = pygame.Rect(
            SCREEN_WIDTH//2 + gap//2, 
            SCREEN_HEIGHT//2 + 40, 
            button_width, 
            button_height
        )

        # --- GAMBAR TOMBOL ---
        pygame.draw.rect(screen, GRAY if start_rect.collidepoint(mouse) else WHITE, start_rect, border_radius=12)
        pygame.draw.rect(screen, GRAY if exit_rect.collidepoint(mouse) else WHITE, exit_rect, border_radius=12)

        start_text = font_small.render("RESTART", True, BLACK)
        exit_text = font_small.render("EXIT", True, BLACK)

        screen.blit(start_text, (start_rect.centerx - start_text.get_width()//2, start_rect.centery - start_text.get_height()//2))
        screen.blit(exit_text, (exit_rect.centerx - exit_text.get_width()//2, exit_rect.centery - exit_text.get_height()//2))

        pygame.display.flip()

        # --- EVENT HANDLER ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if click[0]:
            if start_rect.collidepoint(mouse):
                main()  
                return
            elif exit_rect.collidepoint(mouse):
                pygame.quit()
                sys.exit()



# -------------------- GAME FUNCTION --------------------
def main():
    snake = [
        (GRID_WIDTH // 2, GRID_HEIGHT // 2),       
        (GRID_WIDTH // 2 - 1, GRID_HEIGHT // 2)    
    ]
    direction = (1, 0)
    grow_snake = False
    started = False
    first_food = True

    def spawn_food():
        nonlocal first_food
        if first_food:
            pos = (GRID_WIDTH - 5, GRID_HEIGHT // 2)
            first_food = False
        else:
            while True:
                pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
                if pos not in snake:
                    break
        return pos

    food = spawn_food()

    def draw_snake():
        for i, segment in enumerate(snake):
            x, y = segment
            if i == 0:
                if direction == (1, 0):
                    screen.blit(head_right, (x*CELL_SIZE, y*CELL_SIZE))
                elif direction == (-1, 0):
                    screen.blit(head_left, (x*CELL_SIZE, y*CELL_SIZE))
                elif direction == (0, -1):
                    screen.blit(head_up, (x*CELL_SIZE, y*CELL_SIZE))
                elif direction == (0, 1):
                    screen.blit(head_down, (x*CELL_SIZE, y*CELL_SIZE))
            elif i == len(snake)-1:
                prev_x, prev_y = snake[i-1]
                if prev_x == x:
                    if prev_y < y:
                        screen.blit(tail_down, (x*CELL_SIZE, y*CELL_SIZE))
                    else:
                        screen.blit(tail_up, (x*CELL_SIZE, y*CELL_SIZE))
                elif prev_y == y:
                    if prev_x < x:
                        screen.blit(tail_right, (x*CELL_SIZE, y*CELL_SIZE))
                    else:
                        screen.blit(tail_left, (x*CELL_SIZE, y*CELL_SIZE))
            else:
                prev_x, prev_y = snake[i-1]
                next_x, next_y = snake[i+1]
                if prev_x == next_x:
                    screen.blit(body_v, (x*CELL_SIZE, y*CELL_SIZE))
                elif prev_y == next_y:
                    screen.blit(body_h, (x*CELL_SIZE, y*CELL_SIZE))
                else:
                    if (prev_x > x and next_y < y) or (next_x > x and prev_y < y):
                        screen.blit(body_tr, (x*CELL_SIZE, y*CELL_SIZE))
                    elif (prev_x < x and next_y < y) or (next_x < x and prev_y < y):
                        screen.blit(body_tl, (x*CELL_SIZE, y*CELL_SIZE))
                    elif (prev_x > x and next_y > y) or (next_x > x and prev_y > y):
                        screen.blit(body_br, (x*CELL_SIZE, y*CELL_SIZE))
                    elif (prev_x < x and next_y > y) or (next_x < x and prev_y > y):
                        screen.blit(body_bl, (x*CELL_SIZE, y*CELL_SIZE))

    def draw_board():
        colors = [(40, 40, 40), (60, 60, 60)]
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                color = colors[(x + y) % 2]
                pygame.draw.rect(screen, color, (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def move_snake():
        nonlocal grow_snake, food
        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT or
            new_head in snake):
            game_over_screen(len(snake) - 1)
            return

        snake.insert(0, new_head)

        if new_head == food:
            grow_snake = True
            food = spawn_food()
        if not grow_snake:
            snake.pop()
        else:
            grow_snake = False

    # -------- MAIN LOOP DALAM MAIN --------
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, 1):
                    direction = (0, -1)
                    started = True
                elif event.key == pygame.K_DOWN and direction != (0, -1):
                    direction = (0, 1)
                    started = True
                elif event.key == pygame.K_LEFT and direction != (1, 0):
                    direction = (-1, 0)
                    started = True
                elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                    direction = (1, 0)
                    started = True

        if started:
            move_snake()

        screen.fill(BLACK)
        draw_board()
        draw_snake()
        screen.blit(food_sprite, (food[0]*CELL_SIZE, food[1]*CELL_SIZE))

        pygame.display.flip()
        clock.tick(FPS)


# -------------------- START GAME --------------------
main()
