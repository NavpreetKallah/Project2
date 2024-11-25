import time
from builtins import print

import pygame
import sys
import os

from game.classes.button_class import Button
from game.classes.enemy_class import Enemy
from game.classes.entity_class import Entity
from game.classes.explosion_class import Explosion
from game.classes.hud_class import Hud
from game.classes.temp import Temp
from game.classes.map_class import Map
from game.classes.projectile_class import Projectile
from game.classes.renderer_class import Renderer
from game.classes.round_class import Round
from game.classes.menu_class import Menu
from game.classes.textbox_class import Textbox
from game.classes.tower_class import Tower
from game.config import SCALE


WIDTH, HEIGHT = 160 * SCALE, 120 * SCALE


screen = pygame.display.set_mode((WIDTH, HEIGHT), vsync=1)

Renderer = Renderer(WIDTH, HEIGHT)
Renderer.clearLayers()
Menu = Menu()
Map = Map()
Hud = Hud()
Temp = Temp()

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.hud_initialise = False
        self.map_initialise = False
        self.main_menu_option = "play"
        self.map_option = "cornfield"
        self.difficulty_option = "easy"
        self.fps = 60
        self.timer = time.perf_counter()
        self.running = True
        self.surfaces = []
        self.health = 0
        self.money = 0
        self.round_number = 0
        self.total_rounds = 0

        title = "Balloons"
        pygame.init()
        pygame.display.set_caption(title)

    def quit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def reset_display(self):
        self.screen.fill((0, 0, 0))

    def game(self):
        if self.main_menu_option not in ["play", "towers", "quit"]:
            self.main_menu_option = Menu.runMenu("main", Renderer.getLayer("menu"))
        elif self.main_menu_option == "quit":
            pygame.quit()
            sys.exit()
        elif self.main_menu_option == "play":
            if self.map_option not in ["meadows", "cornfield"]:
                self.map_option = Menu.runMenu("map", Renderer.getLayer("menu"))
            elif self.map_option in ["meadows", "cornfield"]:
                if self.difficulty_option not in ["easy", "medium", "hard"]:
                    self.difficulty_option = Menu.runMenu("difficulty", Renderer.getLayer("menu"))

        if self.map_option and self.difficulty_option and not self.map_initialise:
            Renderer.deleteLayer("menu")
            Map.initialiseMap(self.map_option, Renderer.getLayer("map"))
            self.map_initialise = True

        if not self.hud_initialise:
            Hud.initialiseHud(self.difficulty_option, Renderer.getLayer("HUD"))
            self.hud_initialise = True

        for surface in Renderer.getLayers():
            self.screen.blit(surface, (0, 0))

        # print(1/(time.perf_counter() - self.timer))
        # self.timer = time.perf_counter()

    def update(self):
        self.clock.tick(self.fps)
        self.quit()
        self.game()
        Hud.updateHud(Renderer.getLayer("HUD"))
        pygame.display.update()

    def run(self):
        while self.running:
            self.update()
        pygame.quit()


if __name__ == "__main__":
    game = Game(screen)
    game.run()
