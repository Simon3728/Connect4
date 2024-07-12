"""
This file defines the main game logic and graphical components for playing Connect 4 with a graphical user interface (GUI).
It includes functions to draw the game board, handle player interactions, display game over popups, and manage the game loop.
"""
import pygame as pg
from game.game import Game
from game.player import HumanPlayer
from algorithms.minimax import MinimaxPlayer, MinimaxPlayer2
from algorithms.mcts import MCTSPlayer

# Define some colors
WHITE = (237, 235, 216)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
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
button_width = 100
button_height = 50

def draw_board(screen, board, current_turn, font):
    """
    Draw the game board on the screen, including player turn indication.
    """
    if current_turn == 1:
        turn_text = font.render(f"Player {current_turn}'s Turn", True, BLACK, YELLOW)
        turn_rect = turn_text.get_rect(center=(width // 2, SQUARESIZE // 2 + PADDING))
        screen.blit(turn_text, turn_rect)
    else:
        turn_text = font.render(f"Player {current_turn}'s Turn", True, BLACK, RED)
        turn_rect = turn_text.get_rect(center=(width // 2, SQUARESIZE // 2 + PADDING))
        screen.blit(turn_text, turn_rect)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if c == 0 and r == 0:
                pg.draw.rect(screen, BLUE, (c * SQUARESIZE + PADDING, r * SQUARESIZE + SQUARESIZE + PADDING, SQUARESIZE, SQUARESIZE), border_top_left_radius=10)
            elif c == COLUMN_COUNT - 1 and r == 0:
                pg.draw.rect(screen, BLUE, (c * SQUARESIZE + PADDING, r * SQUARESIZE + SQUARESIZE + PADDING, SQUARESIZE, SQUARESIZE), border_top_right_radius=10)
            elif c == 0 and r == ROW_COUNT - 1:
                pg.draw.rect(screen, BLUE, (c * SQUARESIZE + PADDING, r * SQUARESIZE + SQUARESIZE + PADDING, SQUARESIZE, SQUARESIZE), border_bottom_left_radius=10)
            elif c == COLUMN_COUNT - 1 and r == ROW_COUNT - 1:
                pg.draw.rect(screen, BLUE, (c * SQUARESIZE + PADDING, r * SQUARESIZE + SQUARESIZE + PADDING, SQUARESIZE, SQUARESIZE), border_bottom_right_radius=10)
            else:
                pg.draw.rect(screen, BLUE, (c * SQUARESIZE + PADDING, r * SQUARESIZE + SQUARESIZE + PADDING, SQUARESIZE, SQUARESIZE))
            pg.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE / 2 + PADDING), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2 + PADDING)), RADIUS + 2)  
            pg.draw.circle(screen, WHITE, (int(c * SQUARESIZE + SQUARESIZE / 2 + PADDING), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2 + PADDING)), RADIUS)  
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pg.draw.circle(screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE / 2 + PADDING), height - int(r * SQUARESIZE + SQUARESIZE / 2 + PADDING)), RADIUS)
            elif board[r][c] == 2:
                pg.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2 + PADDING), height - int(r * SQUARESIZE + SQUARESIZE / 2 + PADDING)), RADIUS)
    pg.display.update()

def draw_menu_button(screen, font):
    """
    Draw the menu button on the screen and handle its interaction.
    """
    mouse = pg.mouse.get_pos()
    click = pg.mouse.get_pressed()
    button_color = BUTTON_COLOR
    button_rect = pg.Rect(width - button_width - PADDING, PADDING, button_width, button_height)

    if button_rect.collidepoint(mouse):
        button_color = BUTTON_HOVER_COLOR
        if click[0] == 1:
            return True
    
    pg.draw.rect(screen, button_color, button_rect)
    text = font.render("Menu", True, WHITE)
    screen.blit(text, (width - button_width - PADDING + 10, PADDING + 10))
    return False

def show_game_over_popup(screen, winner, font):
    """
    Show a game over popup with options to play again, return to menu, or exit.
    """
    popup_width, popup_height = 400, 300
    popup_x = (width - popup_width) // 2
    popup_y = (height - popup_height) // 2
    popup_rect = pg.Rect(popup_x, popup_y, popup_width, popup_height)

    # Draw the popup background
    popup_surface = pg.Surface((popup_width, popup_height), pg.SRCALPHA)
    popup_surface.fill((255, 255, 255, 215))
    screen.blit(popup_surface, (popup_x, popup_y))

    # Display winner text
    winner_text = font.render(f"{winner} wins!", True, BLACK)
    winner_rect = winner_text.get_rect(center=(width // 2, popup_y + 50))
    screen.blit(winner_text, winner_rect)
    
    # Define button labels
    play_again_text = font.render("AGAIN", True, WHITE)
    menu_text = font.render("MENU", True, WHITE)
    leave_text = font.render("EXIT", True, WHITE)

    # Define button dimensions based on text size
    button_width = play_again_text.get_width() + 20
    button_height = play_again_text.get_height() + 20
    
    # Calculate total width of all buttons and spacing
    total_button_width = 3 * button_width
    total_spacing = popup_width - total_button_width
    spacing = total_spacing // 4  # Four gaps between and outside the buttons

    # Define button areas
    play_again_button = pg.Rect(popup_x + spacing, popup_y + 200, button_width, button_height)
    menu_button = pg.Rect(play_again_button.right + spacing, popup_y + 200, button_width, button_height)
    leave_button = pg.Rect(menu_button.right + spacing, popup_y + 200, button_width, button_height)
    
    # Draw buttons
    pg.draw.rect(screen, BUTTON_COLOR, play_again_button)
    pg.draw.rect(screen, BUTTON_COLOR, menu_button)
    pg.draw.rect(screen, BUTTON_COLOR, leave_button)
    
    # Blit text on buttons
    screen.blit(play_again_text, play_again_text.get_rect(center=play_again_button.center))
    screen.blit(menu_text, menu_text.get_rect(center=menu_button.center))
    screen.blit(leave_text, leave_text.get_rect(center=leave_button.center))

    pg.display.update()

    # Wait for user input on the popup
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return -1
            if event.type == pg.MOUSEBUTTONDOWN:
                if play_again_button.collidepoint(event.pos):
                    return 1
                elif menu_button.collidepoint(event.pos):
                    return 0
                elif leave_button.collidepoint(event.pos):
                    return -1

def play_game(screen, player1, player2, font):
    """
    Run the main game loop, handling player moves and updating the display.
    """
    game = Game()
    moves = ''
    game.current_turn = 1
    draw_board(screen, game.board.reverse_rows(), game.current_turn, font)

    pg.display.set_caption("Connect 4")
    while True:
        if game.current_turn == 1:
            if isinstance(player1, MinimaxPlayer2) or isinstance(player1, MinimaxPlayer):
                col = player1.get_move(game.board, moves)
            else:
                col = player1.get_move(game.board, PADDING, SQUARESIZE)
        else:
            if isinstance(player2, MinimaxPlayer) or isinstance(player2, MCTSPlayer):
                col = player2.get_move(game.board, moves)
            else:
                col = player2.get_move(game.board, PADDING, SQUARESIZE)        
        if col is not None:
            moves += str(col + 1)
            if game.current_turn == 1:
                if game.board.is_valid_move(col):
                    game.board.drop_piece(col, 1)
                    if game.board.check_winner(1):
                        print("Player 1 wins!")
                        result = show_game_over_popup(screen, "Player 1", font)
                        return result
                    game.current_turn = 2
            else:
                if game.board.is_valid_move(col):
                    game.board.drop_piece(col, 2)
                    if game.board.check_winner(2):
                        print("Player 2 wins!")
                        result = show_game_over_popup(screen, "Player 2", font)
                        return result
                    game.current_turn = 1

            draw_board(screen, game.board.reverse_rows(), game.current_turn, font)

        draw_board(screen, game.board.reverse_rows(), game.current_turn, font)
        if draw_menu_button(screen, font):
            return 0
        
        pg.display.update()

def create_player(player1_selection, player2_selection):
    """
    Create player instances based on the selection from the dropdown menu.
    """
    if player1_selection == "HumanPlayer":
        player1 = HumanPlayer('Player 1', 1)
    elif player1_selection == "MinimaxPlayer":
        player1 = MinimaxPlayer('Player 1', 1)
    elif player1_selection == "MCTSPlayer":
        player1 = MCTSPlayer('Player 1', 1)
    else:
        player1 = None

    if player2_selection == "HumanPlayer":
        player2 = HumanPlayer('Player 2', 2)
    elif player2_selection == "MinimaxPlayer":
        player2 = MinimaxPlayer('Player 2', 2)
    elif player2_selection == "MCTSPlayer":
        player2 = MCTSPlayer('Player 2', 2)
    else:
        player2 = None

    return player1, player2
