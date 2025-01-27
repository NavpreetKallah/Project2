import os
import time

import pygame
from pygame import K_RIGHT, K_LEFT, K_DOWN, K_UP, K_SPACE, K_RETURN
path = os.path.dirname(os.getcwd()) + "/textures"
from game.config import SCALE
from game.classes.textbox_class import TextInput
from game.classes.sql_class import Sql


Sql = Sql()
TextInputUsername = TextInput()
TextInputPassword = TextInput()

class Menu:
    def __init__(self):
        self.time_since_loaded = time.perf_counter()
        self.font = pygame.font.Font(f"{path}/slkscr.ttf", round(17.5*SCALE))
        self.main_menu_selector_locations = []
        self.main_menu_selector_selected = []
        self.main_menu_selector_index = None
        self.main_menu_selector_location = None
        self.selector_images = []
        self.user_name_completed = False
        self.password_completed = False
        self.error_message = None

        self.start_time = time.perf_counter()
        self.time_since_selector = time.perf_counter()
        self.direction = 1
        self.chosen = None
        self.initialised = None

        self.main_menu_play = pygame.transform.scale_by(
            pygame.image.load_extended(f"{path}/main_menu/main_menu_play.png"), SCALE)
        self.main_menu_towers = pygame.transform.scale_by(
            pygame.image.load_extended(f"{path}/main_menu/main_menu_towers.png"), SCALE)
        self.main_menu_quit = pygame.transform.scale_by(
            pygame.image.load_extended(f"{path}/main_menu/main_menu_quit.png"), SCALE)
        self.main_menu_selector = pygame.transform.scale_by(
            pygame.image.load_extended(f"{path}/main_menu/main_menu_selector.png"), SCALE)


        self.continue_continue = pygame.transform.scale_by(
            pygame.image.load_extended(f"{path}/continue/continue.png"), SCALE)
        self.continue_new_game = pygame.transform.scale_by(
            pygame.image.load_extended(f"{path}/continue/new_game.png"), SCALE)
        self.continue_username_taken = pygame.transform.scale_by(
            pygame.image.load_extended(f"{path}/continue/username_taken.png"), SCALE)
        self.continue_wrong_password = pygame.transform.scale_by(
            pygame.image.load_extended(f"{path}/continue/wrong_password.png"), SCALE)
        self.continue_empty_fields = pygame.transform.scale_by(
            pygame.image.load_extended(f"{path}/continue/empty_fields.png"), SCALE)

        self.error_messages = {
            "password": self.continue_wrong_password,
            "username": self.continue_username_taken,
            "empty": self.continue_empty_fields
        }

        self.user_username = pygame.transform.scale_by(
            pygame.image.load_extended(f"{path}/user/username.png"), SCALE)
        self.user_password = pygame.transform.scale_by(
            pygame.image.load_extended(f"{path}/user/password.png"), SCALE)
        self.user_textbox = pygame.transform.scale_by(
            pygame.image.load_extended(f"{path}/user/textbox.png"), SCALE)
        self.user_create = pygame.transform.scale_by(
            pygame.image.load_extended(f"{path}/user/create_button.png"), SCALE)
        self.user_login = pygame.transform.scale_by(
            pygame.image.load_extended(f"{path}/user/login_button.png"), SCALE)

        self.map_menu_cornfield = pygame.transform.scale_by(
            pygame.image.load_extended(f"{path}/map_menu/map_menu_cornfield.png"), SCALE)
        self.map_menu_locked = pygame.transform.scale_by(
            pygame.image.load_extended(f"{path}/map_menu/map_menu_locked.png"), SCALE)
        self.map_menu_select_text = pygame.transform.scale_by(
            pygame.image.load_extended(f"{path}/map_menu/map_menu_select_text.png"), SCALE)
        self.map_menu_meadows = pygame.transform.scale_by(
            pygame.image.load_extended(f"{path}/map_menu/map_menu_meadows.png"), SCALE)
        self.map_menu_selector = pygame.transform.scale_by(
            pygame.image.load_extended(f"{path}/map_menu/map_menu_selector.png"), SCALE)

        self.difficulty_menu_select_text = pygame.transform.scale_by(
            pygame.image.load_extended(f"{path}/difficulty_menu/difficulty_menu_select_text.png"), SCALE)
        self.difficulty_menu_easy = pygame.transform.scale_by(
            pygame.image.load_extended(f"{path}/difficulty_menu/difficulty_menu_easy.png"), SCALE)
        self.difficulty_menu_easy_selector = pygame.transform.scale_by(
            pygame.image.load_extended(f"{path}/difficulty_menu/difficulty_menu_easy_selector.png"), SCALE)
        self.difficulty_menu_medium = pygame.transform.scale_by(
            pygame.image.load_extended(f"{path}/difficulty_menu/difficulty_menu_medium.png"), SCALE)
        self.difficulty_menu_medium_selector = pygame.transform.scale_by(
            pygame.image.load_extended(f"{path}/difficulty_menu/difficulty_menu_medium_selector.png"), SCALE)
        self.difficulty_menu_hard = pygame.transform.scale_by(
            pygame.image.load_extended(f"{path}/difficulty_menu/difficulty_menu_hard.png"), SCALE)
        self.difficulty_menu_hard_selector = pygame.transform.scale_by(
            pygame.image.load_extended(f"{path}/difficulty_menu/difficulty_menu_hard_selector.png"), SCALE)

    def selector(self, keyspressed, move=True, colour_change=False):
        if keyspressed[K_RIGHT] or keyspressed[K_DOWN]:
            if time.perf_counter() - self.time_since_selector > 0.2:
                self.time_since_selector = time.perf_counter()
                self.selector_index += 1
                self.selector_location = self.selector_locations[self.selector_index % len(self.selector_locations)]

        elif keyspressed[K_LEFT] or keyspressed[K_UP]:
            if time.perf_counter() - self.time_since_selector > 0.2:
                self.time_since_selector = time.perf_counter()
                self.selector_index += -1
                self.selector_location = self.selector_locations[self.selector_index % len(self.selector_locations)]

        if colour_change:
            self.selector_image = self.selector_images[self.selector_index % len(self.selector_locations)]

        if keyspressed[K_SPACE] or keyspressed[K_RETURN] and time.perf_counter() - self.time_since_loaded > 0.3:
            return self.selector_selected[self.selector_index % len(self.selector_locations)]

        if time.perf_counter() - self.start_time > 0.5 and move:
            self.start_time = time.perf_counter()
            self.direction = -self.direction
            self.selector_location = (self.selector_location[0] + SCALE * self.direction, self.selector_location[1])

        return None

    def runMenu(self, menu, layer, events=None):
        if menu == "main":
            if self.initialised != "main":
                self.selector_image = self.main_menu_selector
                self.selector_locations = [(64 * SCALE, 12 * SCALE), (90 * SCALE, 30 * SCALE), (62 * SCALE, 48 * SCALE)]
                self.selector_selected = ["play", "towers", "quit"]
                self.selector_index = 0
                self.selector_location = self.selector_locations[0]
                self.initialised = "main"
            return self.runMainMenu(layer)

        elif menu == "map":
            if self.initialised != "map":
                self.time_since_loaded = time.perf_counter()
                self.selector_image = self.map_menu_selector
                self.selector_locations = [(3 * SCALE, 55 * SCALE), (56 * SCALE, 55 * SCALE), (109 * SCALE, 55 * SCALE)]
                self.selector_selected = ["meadows", "cornfield", "locked"]
                self.selector_index = 0
                self.selector_location = self.selector_locations[0]
                self.initialised = "map"
            return self.runMap(layer)

        elif menu == "difficulty":
            if self.initialised != "difficulty":
                self.time_since_loaded = time.perf_counter()
                self.selector_index = 0
                self.selector_images = [self.difficulty_menu_easy_selector, self.difficulty_menu_medium_selector,
                                        self.difficulty_menu_hard_selector]
                self.selector_image = self.selector_images[self.selector_index]
                self.selector_locations = [(54 * SCALE, 47 * SCALE), (76 * SCALE, 61 * SCALE), (52 * SCALE, 75 * SCALE)]
                self.selector_selected = ["easy", "medium", "hard"]
                self.selector_location = self.selector_locations[0]
                self.initialised = "difficulty"
            return self.runDifficultySelect(layer)

        elif menu == "continue":
            if self.initialised != "continue":
                self.time_since_loaded = time.perf_counter()
                self.selector_image = self.main_menu_selector
                self.selector_locations = [(110 * SCALE, 12 * SCALE), (108 * SCALE, 30 * SCALE)]
                self.selector_selected = [True, False]
                self.selector_index = 0
                self.selector_location = self.selector_locations[0]
                self.initialised = "continue"
            return self.runContinueSelect(layer)

        elif menu == "create":
            self.initialised = None
            return self.runCreate(layer, events)

        elif menu == "login":
            self.initialised = None
            return self.runLogin(layer, events)

    def runMainMenu(self, layer):
        keyspressed = pygame.key.get_pressed()
        layer.fill(pygame.Color(70, 70, 70))
        layer.blit(self.main_menu_play, (12 * SCALE, 12 * SCALE))
        layer.blit(self.selector_image, self.selector_location)
        layer.blit(self.main_menu_towers, (12 * SCALE, 30 * SCALE))
        layer.blit(self.main_menu_quit, (12 * SCALE, 48 * SCALE))

        return self.selector(keyspressed)

    def runContinueSelect(self, layer):

        keyspressed = pygame.key.get_pressed()
        layer.fill(pygame.Color(70, 70, 70))
        layer.blit(self.continue_continue, (12 * SCALE, 12 * SCALE))
        layer.blit(self.selector_image, self.selector_location)
        layer.blit(self.continue_new_game, (12 * SCALE, 30 * SCALE))
        if self.error_message:
            layer.blit(self.error_messages[self.error_message], (12 * SCALE, 98 * SCALE))

        return self.selector(keyspressed)

    def runMap(self, layer):
        keyspressed = pygame.key.get_pressed()
        layer.fill(pygame.Color(70, 70, 70))
        layer.blit(self.selector_image, self.selector_location)
        layer.blit(self.map_menu_select_text, (4 * SCALE, 18 * SCALE))
        layer.blit(self.map_menu_cornfield, (57 * SCALE, 49 * SCALE))
        layer.blit(self.map_menu_locked, (110 * SCALE, 49 * SCALE))
        layer.blit(self.map_menu_meadows, (4 * SCALE, 49 * SCALE))

        return self.selector(keyspressed, move=False)

    def runCreate(self, layer, events):
        layer.fill(pygame.Color(70, 70, 70))
        layer.blit(self.user_username, (32 * SCALE, 7 * SCALE))
        layer.blit(self.user_password, (32 * SCALE, 50 * SCALE))
        layer.blit(self.user_textbox, (7 * SCALE, 26 * SCALE))
        layer.blit(self.user_textbox, (7 * SCALE, 70 * SCALE))
        layer.blit(self.user_create, (45 * SCALE, 94 * SCALE))

        if events:
            if not self.user_name_completed:
                self.user_name_completed = TextInputUsername.create(events)
            elif not self.password_completed and self.user_name_completed:
                self.password_completed = TextInputPassword.create(events)
        if not self.user_name_completed:
            self.entered_user_name = self.font.render(TextInputUsername.text, False, (0,0,0))
        elif self.user_name_completed:
            self.entered_password = self.font.render(TextInputPassword.text, True, (0,0,0))

        layer.blit(self.entered_user_name, (12 * SCALE, 25 * SCALE))
        if self.user_name_completed:
            layer.blit(self.entered_password, (12 * SCALE, 69 * SCALE))

        if self.user_name_completed and self.password_completed:
            return (TextInputUsername.text, TextInputPassword.text)

    def clearFields(self):
        self.user_name_completed = False
        self.password_completed = False
        self.entered_user_name = None
        self.entered_password = None
        TextInputPassword.text = ""
        TextInputUsername.text = ""




    def runLogin(self, layer, events):
        layer.fill(pygame.Color(70, 70, 70))
        layer.blit(self.user_username, (32 * SCALE, 7 * SCALE))
        layer.blit(self.user_password, (32 * SCALE, 50 * SCALE))
        layer.blit(self.user_textbox, (7 * SCALE, 26 * SCALE))
        layer.blit(self.user_textbox, (7 * SCALE, 70 * SCALE))
        layer.blit(self.user_login, (52 * SCALE, 94 * SCALE))

        if events:
            if not self.user_name_completed:
                self.user_name_completed = TextInputUsername.create(events)
            elif not self.password_completed and self.user_name_completed:
                self.password_completed = TextInputPassword.create(events)
        if not self.user_name_completed:
            self.entered_user_name = self.font.render(TextInputUsername.text, False, (0,0,0))
        elif self.user_name_completed:
            self.entered_password = self.font.render(TextInputPassword.text, True, (0,0,0))

        layer.blit(self.entered_user_name, (12 * SCALE, 25 * SCALE))
        if self.user_name_completed:
            layer.blit(self.entered_password, (12 * SCALE, 69 * SCALE))

        if self.user_name_completed and self.password_completed:
            return (TextInputUsername.text, TextInputPassword.text)

    def runDifficultySelect(self, layer):
        keyspressed = pygame.key.get_pressed()
        layer.fill(pygame.Color(70, 70, 70))
        layer.blit(self.selector_image, self.selector_location)
        layer.blit(self.difficulty_menu_easy, (4 * SCALE, 47 * SCALE))
        layer.blit(self.difficulty_menu_medium, (4 * SCALE, 61 * SCALE))
        layer.blit(self.difficulty_menu_hard, (4 * SCALE, 75 * SCALE))

        return self.selector(keyspressed, colour_change=True)
