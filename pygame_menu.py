"""
This file defines the graphical components used in the PyGame Connect 4 menu, 
including dropdown for player selection and a play button. 
"""
import pygame as pg

# Define some colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLOR_INACTIVE = (100, 80, 255)
COLOR_ACTIVE = (100, 200, 255)
COLOR_LIST_INACTIVE = (255, 100, 100)
COLOR_LIST_ACTIVE = (255, 150, 150)

class DropDown():
    def __init__(self, color_menu, color_option, x, y, w, h, font, main, options):
        """
        Initialize the dropdown menu.
        """
        self.color_menu = color_menu
        self.color_option = color_option
        self.rect = pg.Rect(x, y, w, h)
        self.font = font
        self.main = main
        self.options = options
        self.draw_menu = False
        self.menu_active = False
        self.active_option = -1

    def draw(self, surf):
        """
        Draw the dropdown menu and its options on the screen.
        """
        pg.draw.rect(surf, self.color_menu[self.menu_active], self.rect, 0)
        msg = self.font.render(self.main, 1, (0, 0, 0))
        surf.blit(msg, msg.get_rect(center=self.rect.center))

        if self.draw_menu:
            for i, text in enumerate(self.options):
                rect = self.rect.copy()
                rect.y += (i + 1) * self.rect.height
                pg.draw.rect(surf, self.color_option[1 if i == self.active_option else 0], rect, 0)
                msg = self.font.render(text, 1, (0, 0, 0))
                surf.blit(msg, msg.get_rect(center=rect.center))

    def update(self, event_list):
        """
        Update the state of the dropdown menu based on user interactions.
        """
        mpos = pg.mouse.get_pos()
        self.menu_active = self.rect.collidepoint(mpos)

        self.active_option = -1
        for i in range(len(self.options)):
            rect = self.rect.copy()
            rect.y += (i + 1) * self.rect.height
            if rect.collidepoint(mpos):
                self.active_option = i
                break

        if not self.menu_active and self.active_option == -1:
            self.draw_menu = False

        for event in event_list:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if self.menu_active:
                    self.draw_menu = not self.draw_menu
                elif self.draw_menu and self.active_option >= 0:
                    self.draw_menu = False
                    return self.active_option
        return -1

class PlayButton:
    def __init__(self, x, y, size, color, hover_color):
        """
        Initialize the play button.
        """
        self.rect = pg.Rect(x, y, size, size)
        self.color = color
        self.hover_color = hover_color
        self.pressed = False
        self.hovered = False

    def draw(self, surf):
        """
        Draw the play button on the screen.
        """
        color = self.hover_color if self.hovered else self.color
        pg.draw.polygon(surf, color, [(self.rect.left, self.rect.top), 
                                      (self.rect.left, self.rect.bottom), 
                                      (self.rect.right, self.rect.centery)])
    
    def update(self, event_list):
        """
        Update the state of the play button based on user interactions.
        """
        mpos = pg.mouse.get_pos()
        self.hovered = self.rect.collidepoint(mpos)
        for event in event_list:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and self.hovered:
                self.pressed = True
                return True
        return False

def run_menu(screen, event_list, play_button, player1_dropdown, player2_dropdown, background_color, heading_font, font, width, height):
    """
    Run the main menu to select players and start the game.
    """
    for event in event_list:
        if event.type == pg.QUIT:
            return 0

    player1_option = player1_dropdown.update(event_list)
    if player1_option >= 0:
        player1_dropdown.main = player1_dropdown.options[player1_option]

    player2_option = player2_dropdown.update(event_list)
    if player2_option >= 0:
        player2_dropdown.main = player2_dropdown.options[player2_option]

    if play_button.update(event_list):
        return 1

    screen.fill(background_color)

    # Draw heading
    heading_text = heading_font.render("Connect 4", True, BLACK)
    screen.blit(heading_text, heading_text.get_rect(center=(width // 2, 100)))

    # Draw player selection dropdowns
    player1_dropdown.draw(screen)
    player2_dropdown.draw(screen)

    # Draw vs. text
    vs_text = font.render("VS", True, BLACK)
    screen.blit(vs_text, vs_text.get_rect(center=(width // 2, height // 2)))

    # Draw play button
    play_button.draw(screen) 

    return -1
