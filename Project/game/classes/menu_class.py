import pygame

from game.classes.renderer_class import Renderer
SCALE = 5

class Menu:
    def __init__(self):
        self.information = False
        self.pause = False
        self.map_select = False
        self.difficulty_select = False
        self.victory = False
        self.game_over = False
        self.main_menu = False

        self.main_menu_play = pygame.image.load_extended(
            "//BA-SRV-FS-01/18nkallah$/Computer Science/Project/textures/main_menu_play.png")
        self.main_menu_play = pygame.transform.scale_by(self.main_menu_play, 5)
        self.main_menu_towers = pygame.image.load_extended(
            "//BA-SRV-FS-01/18nkallah$/Computer Science/Project/textures/main_menu_towers.png")
        self.main_menu_towers = pygame.transform.scale_by(self.main_menu_towers, 5)
        self.main_menu_quit = pygame.image.load_extended(
            "//BA-SRV-FS-01/18nkallah$/Computer Science/Project/textures/main_menu_quit.png")
        self.main_menu_quit = pygame.transform.scale_by(self.main_menu_quit, 5)

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
        mouse = pygame.mouse.get_pos()
        self.resetMenu()
        self.main_menu = True
        layer.fill(pygame.Color(70,70,70))
        layer.blit(self.main_menu_play,(12 * SCALE,12 * SCALE))
        layer.blit(self.main_menu_towers, (12 * SCALE, 30 * SCALE))
        layer.blit(self.main_menu_quit, (12 * SCALE, 48 * SCALE))
        pygame.draw.rect(layer, (0, 100, 255), (9 * SCALE, 9 * SCALE, 54 * SCALE, 18 * SCALE), 5)
        pygame.draw.rect(layer, (0, 100, 255), (9 * SCALE, 27 * SCALE, 80 * SCALE, 18 * SCALE), 5)
        pygame.draw.rect(layer, (0, 100, 255), (9 * SCALE, 45 * SCALE, 52 * SCALE, 18 * SCALE), 5)
