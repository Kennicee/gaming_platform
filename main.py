import os
import sys
import pygame
from pygame.locals import QUIT, KEYDOWN, K_RETURN

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Gaming Platform")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GRAY = (50, 50, 50)

# Fonts
font_title = pygame.font.Font(None, 80)
font_menu = pygame.font.Font(None, 50)

# Menu options
menu_options = ["1. Tic Tac Toe", "2. Snake Game", "3. Quiz Game", "4. Rock Paper Scissors", "5. Exit"]

def draw_menu(selected_index):
    """Draw the menu on the screen."""
    screen.fill(GRAY)
    title_text = font_title.render("Gaming Platform", True, WHITE)
    screen.blit(title_text, ((SCREEN_WIDTH - title_text.get_width()) // 2, 50))

    for index, option in enumerate(menu_options):
        color = BLUE if index == selected_index else WHITE
        menu_text = font_menu.render(option, True, color)
        screen.blit(menu_text, (100, 200 + index * 60))

    pygame.display.flip()

def main():
    """Main menu loop."""
    selected_index = 0
    running = True

    while running:
        draw_menu(selected_index)

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(menu_options)
                elif event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(menu_options)
                elif event.key == K_RETURN:
                    if selected_index == 0:
                        os.system("python games/tic_tac_toe.py")
                    elif selected_index == 1:
                        os.system("python games/snake_game.py")
                    elif selected_index == 2:
                        os.system("python games/quiz_game.py")
                    elif selected_index == 3:
                        os.system("python games/rock_paper_scissors.py")
                    elif selected_index == 4:
                        running = False

if __name__ == "__main__":
    main()
