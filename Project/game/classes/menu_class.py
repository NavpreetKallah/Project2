import time

import pygame
from pygame import K_RIGHT

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
        self.main_menu_selector_locations = [(64 * SCALE, 12 * SCALE), (90 * SCALE, 30 * SCALE), (62 * SCALE, 48 * SCALE)]
        self.main_menu_selector_index = 0
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

        self.map_menu_cornfield = pygame.image.load_extended(
            "//BA-SRV-FS-01/18nkallah$/Computer Science/Project/textures/map_menu_cornfield.png")
        self.map_menu_cornfield = pygame.transform.scale_by(self.map_menu_cornfield, SCALE)
        self.map_menu_locked = pygame.image.load_extended(
            "//BA-SRV-FS-01/18nkallah$/Computer Science/Project/textures/map_menu_locked.png")
        self.map_menu_locked = pygame.transform.scale_by(self.map_menu_locked, SCALE)
        self.map_menu_select_text = pygame.image.load_extended(
            "//BA-SRV-FS-01/18nkallah$/Computer Science/Project/textures/map_menu_select_text.png")
        self.map_menu_select_text = pygame.transform.scale_by(self.map_menu_select_text, SCALE)
        self.map_menu_meadows = pygame.image.load_extended(
            "//BA-SRV-FS-01/18nkallah$/Computer Science/Project/textures/map_menu_meadows.png")
        self.map_menu_meadows = pygame.transform.scale_by(self.map_menu_meadows, SCALE)

        self.difficulty_menu_select_text = pygame.image.load_extended(
            "//BA-SRV-FS-01/18nkallah$/Computer Science/Project/textures/difficulty_menu_select_text.png")
        self.difficulty_menu_select_text = pygame.transform.scale_by(self.difficulty_menu_select_text, SCALE)

        self.difficulty_menu_easy = pygame.image.load_extended(
            "//BA-SRV-FS-01/18nkallah$/Computer Science/Project/textures/difficulty_menu_easy.png")
        self.difficulty_menu_easy = pygame.transform.scale_by(self.difficulty_menu_easy, SCALE)
        self.difficulty_menu_easy_selector = pygame.image.load_extended(
            "//BA-SRV-FS-01/18nkallah$/Computer Science/Project/textures/difficulty_menu_easy_selector.png")
        self.map_menu_easy_selector = pygame.transform.scale_by(self.difficulty_menu_easy_selector, SCALE)

        self.difficulty_menu_medium = pygame.image.load_extended(
            "//BA-SRV-FS-01/18nkallah$/Computer Science/Project/textures/difficulty_menu_medium.png")
        self.difficulty_menu_medium = pygame.transform.scale_by(self.difficulty_menu_medium, SCALE)
        self.difficulty_menu_medium_selector = pygame.image.load_extended(
            "//BA-SRV-FS-01/18nkallah$/Computer Science/Project/textures/difficulty_menu_medium_selector.png")
        self.map_menu_medium_selector = pygame.transform.scale_by(self.difficulty_menu_medium_selector, SCALE)

        self.difficulty_menu_hard = pygame.image.load_extended(
            "//BA-SRV-FS-01/18nkallah$/Computer Science/Project/textures/difficulty_menu_hard.png")
        self.difficulty_menu_hard = pygame.transform.scale_by(self.difficulty_menu_hard, SCALE)
        self.difficulty_menu_hard_selector = pygame.image.load_extended(
            "//BA-SRV-FS-01/18nkallah$/Computer Science/Project/textures/difficulty_menu_hard_selector.png")
        self.map_menu_hard_selector = pygame.transform.scale_by(self.difficulty_menu_hard_selector, SCALE)

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
        elif menu ==  "difficulty":
            return self.runDifficultySelect(layer)

    def runMainMenu(self, layer):
        mouse = pygame.mouse.get_pos()
        keyspressed = pygame.key.get_pressed()
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

        if keyspressed[K_RIGHT]:
            self.main_menu_selector_index += 1
            if self.main_menu_selector_index == 3:
                self.main_menu_selector_index = 0
            self.main_menu_selector_location = self.main_menu_selector_locations[self.main_menu_selector_index]

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
        mouse = pygame.mouse.get_pos()
        layer.fill(pygame.Color(70, 70, 70))
        layer.blit(self.map_menu_select_text, (4 * SCALE, 18 * SCALE))
        cornfield = pygame.Rect(57 * SCALE, 49 * SCALE, 46 * SCALE, 47 * SCALE)
        layer.blit(self.map_menu_cornfield, (57 * SCALE, 49 * SCALE))
        locked = pygame.Rect(110 * SCALE, 49 * SCALE, 46 * SCALE, 47 * SCALE)
        layer.blit(self.map_menu_locked, (110 * SCALE, 49 * SCALE))
        meadows = pygame.Rect(4 * SCALE, 49 * SCALE, 46 * SCALE, 47 * SCALE)
        layer.blit(self.map_menu_meadows, (4 * SCALE, 49 * SCALE))

        if meadows.collidepoint(mouse):
            if pygame.mouse.get_pressed()[0]:
                return "meadows"

        elif cornfield.collidepoint(mouse):
            if pygame.mouse.get_pressed()[0]:
                return "cornfield"

        elif locked.collidepoint(mouse):
            if pygame.mouse.get_pressed()[0]:
                return "locked"

        return None

    def runDifficultySelect(self, layer):
        mouse = pygame.mouse.get_pos()
        layer.fill(pygame.Color(70,70,70))
        easy = pygame.Rect(4 * SCALE, 47 * SCALE, 45 * SCALE, 12 * SCALE)
        layer.blit(self.difficulty_menu_easy, (4 * SCALE, 47 * SCALE))
        medium = pygame.Rect(4 * SCALE, 61 * SCALE, 67 * SCALE, 12 * SCALE)
        layer.blit(self.difficulty_menu_medium, (4 * SCALE, 61 * SCALE))
        hard = pygame.Rect(4 * SCALE, 75 * SCALE, 43 * SCALE, 12 * SCALE)
        layer.blit(self.difficulty_menu_hard, (4 * SCALE, 75 * SCALE))

        # pygame.draw.rect(layer, (0, 100, 255), easy, 5)
        # pygame.draw.rect(layer, (0, 100, 255), medium, 5)
        # pygame.draw.rect(layer, (0, 100, 255), hard, 5)

        if easy.collidepoint(mouse):
            if pygame.mouse.get_pressed()[0]:
                return "easy"

        elif medium.collidepoint(mouse):
            if pygame.mouse.get_pressed()[0]:
                return "medium"

        elif hard.collidepoint(mouse):
            if pygame.mouse.get_pressed()[0]:
                return "hard"

        return None


