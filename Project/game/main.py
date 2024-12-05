import time
from builtins import print

import pygame
import sys
import os

from pygame import K_KP_0, K_PLUS

from game.classes.button_class import Button
from game.classes.enemy_class import Enemy
from game.classes.entity_class import Entity
from game.classes.explosion_class import Explosion
from game.classes.hud_class import Hud
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
Round = Round()
Hud = Hud()

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.hud_initialise = False
        self.map_initialise = False
        self.round_started = False
        self.main_menu_option = "play"
        self.map_option = "cornfield"
        self.difficulty_option = "easy"
        self.fps = 60
        self.fps_timer = time.perf_counter()
        self.timer = time.perf_counter()
        self.running = True
        self.surfaces = []
        self.spawn_list = []
        self.spawn_queue = []
        self.health = 100
        self.money = 100
        self.round_number = 0
        self.total_rounds = 0
        self.done = True

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
        mouse = pygame.mouse.get_pos()
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

        if pygame.mouse.get_pressed()[0]  and Hud.play(Renderer.getLayer("HUD")):
            if not self.round_started:
                self.round_started = True
                self.spawn_queue += Round.startRound()
                Hud.updateRound(1)
            # else:
            #     self.round_paused = True
            #     Round.pauseRound()



        Renderer.clearLayer("enemy")
        if self.spawn_queue and time.perf_counter() - self.timer > 0.2:
            self.timer = time.perf_counter()
            self.spawn_list.append(self.spawn_queue.pop())

        if self.round_started:
            for enemy in self.spawn_list:
                if enemy.move(Map.pathfind(), Renderer.getLayer("enemy")) == "delete":
                    self.spawn_list.remove(enemy)
                    Hud.updateMoney(enemy.value)

        if self.spawn_list:
            for enemy in self.spawn_list:
                enemy.draw(Renderer.getLayer("enemy"))

        if not self.spawn_list and self.round_started:
            self.round_started = False


        #Enemy.move(Map.pathfind(), Renderer.getLayer("enemy"))
        for surface in Renderer.getLayers():
            self.screen.blit(surface, (0, 0))



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
