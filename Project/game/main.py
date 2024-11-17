from builtins import print

import pygame
import sys
import os


from Project.game.classes.button_class import Button
from Project.game.classes.enemy_class import Enemy
from Project.game.classes.entity_class import Entity
from Project.game.classes.explosion_class import Explosion
from Project.game.classes.hud_class import Hud
from Project.game.classes.map_class import Map
from Project.game.classes.projectile_class import Projectile
from Project.game.classes.renderer_class import Renderer
from Project.game.classes.round_class import Round
from Project.game.classes.menu_class import Menu
from Project.game.classes.textbox_class import Textbox
from Project.game.classes.tower_class import Tower

SCALE = 5
WIDTH, HEIGHT = 160*SCALE,120*SCALE

Renderer = Renderer(WIDTH, HEIGHT)
Menu = Menu()
Map = Map()


class Game:
    def __init__(self, screen_size):
        self.screen_size = screen_size
        self.screen = pygame.display.set_mode(self.screen_size)
        self.clock = pygame.time.Clock()
        self.main_menu_option = "play"
        self.map_option = "cornfield"
        self.difficulty_option = "easy"
        self.fps = 60
        self.running = True
        self.surfaces = []

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
            if self.map_option not in ["meadows","cornfield"]:
                self.map_option = Menu.runMenu("map", Renderer.getLayer("menu"))
            elif self.map_option in ["meadows","cornfield"]:
                if self.difficulty_option not in ["easy","medium","hard"]:
                    self.difficulty_option = Menu.runMenu("difficulty", Renderer.getLayer("menu"))

        if self.map_option and self.difficulty_option:
            Map.initialiseMap(self.map_option, Renderer.getLayer("menu"))
            print(True)


        for surface in Renderer.getLayers():
            self.screen.blit(surface, (0, 0))

    def update(self):
        self.quit()
        Renderer.clearLayers()
        self.game()
        pygame.display.update()
        self.clock.tick(self.fps)

    def run(self):
        while self.running:
            self.update()
        pygame.quit()

if __name__ == "__main__":
    game = Game((WIDTH, HEIGHT))
    game.run()

