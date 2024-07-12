"""
Main file for the PyGame to play Connect 4 with a graphical user interface (GUI).
This script sets up the game window, defines colors and constants, and runs the main game loop.
Players can be selected from a dropdown menu, and the game supports both human and AI players.
"""
import pygame as pg
import sys
from pygame_menu import DropDown, PlayButton, run_menu
from pygame_game import create_player, play_game

# Define some colors
WHITE = (237, 235, 216)
BLACK = (0, 0, 0)
COLOR_INACTIVE = (100, 80, 255)
COLOR_ACTIVE = (100, 200, 255)
COLOR_LIST_INACTIVE = (255, 100, 100)
COLOR_LIST_ACTIVE = (255, 150, 150)
BUTTON_COLOR = (37, 156, 73)
BUTTON_HOVER_COLOR = (100, 200, 100)

# Define some constants
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)
PADDING = 20
width = COLUMN_COUNT * SQUARESIZE + 2 * PADDING
height = (ROW_COUNT + 1) * SQUARESIZE + 2 * PADDING
size = (width, height)

# Initialize pygame
pg.init()

# Set up the display
screen = pg.display.set_mode(size)
pg.display.set_caption("Connect 4")
heading_font = pg.font.SysFont("monospace", 75)
font = pg.font.SysFont("monospace", 30)

def main():
    """
    Main function to run the Connect 4 game with a graphical user interface.
    Sets up the game window, dropdown menus for player selection, and the play button.
    Handles the game loop, including event processing and game state updates.
    """
    clock = pg.time.Clock()
    running = True
    again = False
    dropdown_width = 300  

    player1_dropdown = DropDown(
        [COLOR_INACTIVE, COLOR_ACTIVE],
        [COLOR_LIST_INACTIVE, COLOR_LIST_ACTIVE],
        width // 4 - dropdown_width // 2, height // 2 - 25, dropdown_width, 50, 
        font, 
        "Player 1", ["HumanPlayer", "MinimaxPlayer", "MCTSPlayer"])

    player2_dropdown = DropDown(
        [COLOR_INACTIVE, COLOR_ACTIVE],
        [COLOR_LIST_INACTIVE, COLOR_LIST_ACTIVE],
        3 * width // 4 - dropdown_width // 2, height // 2 - 25, dropdown_width, 50, 
        font, 
        "Player 2", ["HumanPlayer", "MinimaxPlayer", "MCTSPlayer"])

    play_button = PlayButton(width // 2 - 25, height // 2 + 100, 50, BUTTON_COLOR, BUTTON_HOVER_COLOR)
    
    while running:
        clock.tick(30)
        event_list = pg.event.get()

        menu = run_menu(screen, event_list, play_button, player1_dropdown, player2_dropdown, WHITE, heading_font, font, width, height)
        if menu == 0:
            running = False
        elif menu == 1 and (player1_dropdown.main != "Player 1" and player2_dropdown.main != "Player 2" or again):
            player1, player2 = create_player(player1_dropdown.main, player2_dropdown.main)
            if again:
                again = False
            if player1 is not None and player2 is not None:
                screen.fill(WHITE)
                pg.display.flip()
                
                # -1 indicates to leave the game
                game_run = play_game(screen, player1, player2, font)
                if game_run == -1:
                    break
                # 0 indicates to return to the menu
                elif game_run == 0:
                    screen.fill(WHITE)
                    continue
                # 1 indicates to play again
                elif game_run == 1:
                    again = True
                    
        pg.display.flip()

    pg.quit()
    sys.exit()

if __name__ == "__main__":
    main()
