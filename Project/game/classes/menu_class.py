import pygame

from game.classes.renderer_class import Renderer


class Menu:
    def __init__(self):
        self.information = False
        self.pause = False
        self.map_select = False
        self.difficulty_select = False
        self.victory = False
        self.game_over = False
        self.main_menu = False

    def resetMenu(self):

        self.information = False
        self.pause = False
        self.map_select = False
        self.difficulty_select = False
        self.victory = False
        self.game_over = False
        self.main_menu = False

    def runMenu(self, menu, layer):
        if menu == "main":
            self.runMainMenu(layer)

    def runMainMenu(self, layer):
        self.resetMenu()
        self.main_menu = True
        layer.fill(pygame.Color(125,125,125))
