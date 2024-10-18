import time

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
        self.main_menu_selector_location = (64 * SCALE, 12 * SCALE)
        self.main_menu_option = None
        self.start_time = time.perf_counter()
        self.direction = 1
        self.chosen = "play"

        self.main_menu_play = pygame.image.load_extended(
            "//BA-SRV-FS-01/18nkallah$/Computer Science/Project/textures/main_menu_play.png")
        self.main_menu_play = pygame.transform.scale_by(self.main_menu_play, SCALE)
        self.main_menu_towers = pygame.image.load_extended(
            "//BA-SRV-FS-01/18nkallah$/Computer Science/Project/textures/main_menu_towers.png")
        self.main_menu_towers = pygame.transform.scale_by(self.main_menu_towers, SCALE)
        self.main_menu_quit = pygame.image.load_extended(
            "//BA-SRV-FS-01/18nkallah$/Computer Science/Project/textures/main_menu_quit.png")
        self.main_menu_quit = pygame.transform.scale_by(self.main_menu_quit, SCALE)
        self.main_menu_selector = pygame.image.load_extended(
            "//BA-SRV-FS-01/18nkallah$/Computer Science/Project/textures/main_menu_selector.png")
        self.main_menu_selector = pygame.transform.scale_by(self.main_menu_selector, SCALE)

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
            return self.runMainMenu(layer)
        elif menu == "map":
            return self.runMap(layer)

    def runMainMenu(self, layer):
        mouse = pygame.mouse.get_pos()
        keyspressed = pygame.key.get_pressed()[pygame.K_SPACE]
        self.resetMenu()
        self.main_menu = True
        layer.fill(pygame.Color(70,70,70))
        layer.blit(self.main_menu_play,(12 * SCALE,12 * SCALE))
        layer.blit(self.main_menu_selector, self.main_menu_selector_location)
        layer.blit(self.main_menu_towers, (12 * SCALE, 30 * SCALE))
        layer.blit(self.main_menu_quit, (12 * SCALE, 48 * SCALE))
        play = pygame.Rect(9 * SCALE, 9 * SCALE, 54 * SCALE, 18 * SCALE)
        towers = pygame.Rect(9 * SCALE, 27 * SCALE, 80 * SCALE, 18 * SCALE)
        quit = pygame.Rect(9 * SCALE, 45 * SCALE, 52 * SCALE, 18 * SCALE)

        if play.collidepoint(mouse):
            if self.chosen != "play":
                self.main_menu_selector_location = (64 * SCALE, 12 * SCALE)
            self.chosen = "play"
            if pygame.mouse.get_pressed()[0]:
                return "play"

        elif towers.collidepoint(mouse):
            if self.chosen != "towers":
                self.main_menu_selector_location = (90 * SCALE, 30 * SCALE)
            self.chosen = "towers"
            if pygame.mouse.get_pressed()[0]:
                return "towers"

        elif quit.collidepoint(mouse):
            if self.chosen != "quit":
                self.main_menu_selector_location = (62 * SCALE, 48 * SCALE)
            self.chosen = "quit"
            if pygame.mouse.get_pressed()[0]:
                return "quit"

        if time.perf_counter() - self.start_time > 0.5:
            self.start_time = time.perf_counter()
            self.direction = -self.direction
            self.main_menu_selector_location = (self.main_menu_selector_location[0] + SCALE * self.direction, self.main_menu_selector_location[1])
        return None
        # pygame.draw.rect(layer, (0, 100, 255), play, 5)
        # pygame.draw.rect(layer, (0, 100, 255), towers, 5)
        # pygame.draw.rect(layer, (0, 100, 255), quit, 5)

    def runMap(self, layer):
        layer.fill(pygame.Color(70,70,70))

