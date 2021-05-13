import pygame
from random import *

# setup with level
def setup(level):
    global display_time
    # time calculation
    display_time = 5 - (level // 3)
    display_time = max(display_time, 1)

    # number calculation
    number_count = (level // 3) + 5
    number_count = min(number_count, 20)

    # create grid
    rows = 5
    columns = 9

    cell_size = 130
    button_size = 110
    screen_left_margin = 55
    screen_top_margin = 20

    grid = [[0 for col in range(columns)] for row in range(rows)]
    number = 1
    while number <= number_count:
        row_idx = randrange(0, rows)
        col_idx = randrange(0, columns)
        
        if grid[row_idx][col_idx] == 0:
            grid[row_idx][col_idx] = number
            number += 1

            # get button center
            center_x = screen_left_margin + (col_idx * cell_size) + (cell_size / 2)
            center_y = screen_top_margin + (row_idx * cell_size) + (cell_size / 2)

            # create number button
            button = pygame.Rect(0, 0, button_size, button_size)
            button.center = (center_x, center_y)

            number_buttons.append(button)



# Show stating screen
def display_start_screen():
    pygame.draw.circle(screen, WHITE, start_button.center, 60, 5)

    msg = game_font.render(f"{cur_level}", True, WHITE)
    msg_rect = msg.get_rect(center=start_button.center)

    screen.blit(msg, msg_rect)


def display_game_screen():
    global hidden

    if not hidden:
        elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
        if elapsed_time > display_time:
            hidden = True
    
    for idx, rect in enumerate(number_buttons, start = 1):
        if hidden:
            pygame.draw.rect(screen, WHITE, rect)
        else:
            # number text
            cell_text = game_font.render(str(idx), True, WHITE)
            text_rect = cell_text.get_rect(center=rect.center)
            screen.blit(cell_text, text_rect)


def check_buttons(pos):
    global start
    global start_ticks
    if start:
        check_number_buttons(pos)
    elif start_button.collidepoint(pos):
        start = True
        start_ticks = pygame.time.get_ticks()

def check_number_buttons(pos):
    global hidden
    global start
    global cur_level
    for button in number_buttons:
        if button.collidepoint(pos):
            if button == number_buttons[0]:
                del number_buttons[0]
                if not hidden:
                    hidden = True
            else:
                game_over()
            break
    
    if len(number_buttons) == 0:
        start = False
        hidden = False
        cur_level += 1
        setup(cur_level)

def game_over():
    global running
    running = False
    msg = game_font.render(f"Your level is {cur_level}", True, WHITE)
    msg_rect = msg.get_rect(center=(screen_width/2, screen_height/2))

    screen.fill(BLACK)
    screen.blit(msg, msg_rect)

# Start
pygame.init()
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Memory Game")
game_font = pygame.font.Font(None, 120)

# Variables
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)

# Tracking variables
start = False
hidden = False
number_buttons = []
display_time = None
start_ticks = None
cur_level = 1

# starting button
start_button = pygame.Rect(0, 0, 120, 120)
start_button.center = (120, screen_height - 120)

setup(cur_level)

# Main Loop
running = True
while running:
    click_pos = None
    # event 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            click_pos = pygame.mouse.get_pos()

    # Base screen
    screen.fill(BLACK)
    
    # starting screen
    if not start:
        display_start_screen()
    else:
        display_game_screen()

    if click_pos:
        check_buttons(click_pos)

    # update screen
    pygame.display.update()

# delay time
pygame.time.delay(5000)

# Game end
pygame.quit()