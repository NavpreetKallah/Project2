import time
from builtins import print

import pygame
import sys
import os

from pygame import K_KP_0, K_PLUS
from pygame.mixer_music import queue

from game.classes.enemy_class import EnemyManager
from game.classes.button_class import Button
from game.classes.enemy_class import Enemy
from game.classes.entity_class import Entity
from game.classes.explosion_class import Explosion
from game.classes.hud_class import Hud
from game.classes.map_class import Map
from game.classes.renderer_class import Renderer
from game.classes.round_class import Round
from game.classes.menu_class import Menu
from game.classes.textbox_class import Textbox

from game.classes.tower_class import TowerManager, ProjectileManager
from game.config import SCALE


WIDTH, HEIGHT = 160 * SCALE, 120 * SCALE


screen = pygame.display.set_mode((WIDTH, HEIGHT))

Renderer = Renderer(WIDTH, HEIGHT)
Renderer.clearLayers()
Menu = Menu()
Map = Map()
Round = Round()
Hud = Hud()
EnemyManager = EnemyManager()
TowerManager = TowerManager()

class Game:
    def __init__(self, screen):
        self.temp = time.perf_counter()
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.hud_initialise = False
        self.map_initialise = False
        self.round_started = False
        self.clicked = False
        self.fast_forward = False
        self.main_menu_option = "play"
        self.map_option = "cornfield"
        self.difficulty_option = "hard"
        self.difficulty_multiplier = 1.3
        self.fps_counter = 0
        self.fps = 60
        self.fps_timer = time.perf_counter()
        self.timer = time.perf_counter()
        self.running = True
        self.round = 0
        self.health = 100
        self.money = 75000000

        self.autoplay = False

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
            self.path = Map.pathfind()
            self.map_initialise = True

        if not self.hud_initialise and self.difficulty_option and self.map_option:
            Hud.initialiseHud(Renderer.getLayer("HUD"))
            Hud.setDifficulty(self.difficulty_option)
            Hud.updateMoney(round(self.money))
            Hud.updateRound(self.round)
            Hud.updateHealth(self.health)
            Hud.updateHud(Renderer.getLayer("HUD"))
            self.hud_initialise = True

        if (pygame.mouse.get_pressed()[0] or self.autoplay) and (Hud.play() or self.autoplay) and not EnemyManager.getEnemies() and not EnemyManager.getSprites():
            if not self.round_started:
                self.autoplay = True
                self.round_started = True
                Round.startRound(EnemyManager)
                Hud.updateRound(1)
                Hud.disableSpeed(Renderer.getLayer("HUD"))
                Hud.updateHud(Renderer.getLayer("HUD"))

        # print(1/(time.perf_counter() - self.temp))
        # self.temp = time.perf_counter()
        #print(self.clock.get_fps())
        self.fps_counter += self.clock.get_fps()
        if time.perf_counter() - self.fps_timer > 5:
            #print(self.fps_counter/ (60*5))
            self.fps_timer = time.perf_counter()
            self.fps_counter = 0

        if pygame.mouse.get_pressed()[0] and not self.clicked:
            self.clicked = True
            tower_chosen = Hud.tower_chosen()
            tower_upgrading = TowerManager.getTowerClicked()
            sell_active = Hud.sellClicked() or Hud.getSell()
            #if not self.round_started:
            if Hud.fastForward(Renderer.getLayer("HUD")):
                EnemyManager.speedChange()
                Round.speedChange()
                self.fast_forward = not self.fast_forward
                Hud.updateHud(Renderer.getLayer("HUD"))
            if sell_active:
                sold = Hud.sellMenu()
                if sold != "main" and sold:
                    self.money += sold
                    Hud.updateMoney(round(self.money))
                Hud.updateHud(Renderer.getLayer("HUD"))
            elif tower_chosen:
                TowerManager.placing = True
                TowerManager.placing_tower = tower_chosen
            elif Hud.getUpgrading():
                option_chosen = Hud.upgradeChosen(Renderer.getLayer("HUD"))
                Hud.updateHud(Renderer.getLayer("HUD"))
                if option_chosen:
                    if option_chosen not in ["main", "sell"]:
                        upgrade_cost = TowerManager.getUpgradingTower().upgrade(option_chosen, self.money)
                        self.money -= upgrade_cost
                        Hud.updateMoney(round(self.money))
                        Hud.updateHud(Renderer.getLayer("HUD"))
                else:
                    Hud.setUpgrading(False)
                    Hud.updateHud(Renderer.getLayer("HUD"))

            elif tower_upgrading:
                Hud.createTowerUpgrade(tower_upgrading)
                Hud.setUpgrading(True)
                Hud.updateHud(Renderer.getLayer("HUD"))


        if TowerManager.getPlacing():
            TowerManager.place(Renderer.getLayer("tower"), Map.getRects(), Map.getMasks(),TowerManager.getPlacingTower())

        # if pygame.mouse.get_pressed()[2] and not self.clicked:
        #     self.clicked = True
            # for enemy in EnemyManager.getSprites():
            #     damaged = enemy.take_damage(2)
            #     if damaged == "delete":
            #         enemy.kill()
            #     self.money += 1
            #     Hud.updateMoney(round(self.money))
            #EnemyManager.fastForward()

        #Hud.updateHealth(round(self.clock.get_fps()))
        health_change = EnemyManager.getKilled()
        if health_change:
            if self.health - health_change < 0:
                self.health = 0
            else:
                self.health = self.health - health_change
            Hud.updateHealth(self.health)
            Hud.updateHud(Renderer.getLayer("HUD"))


        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False
            if TowerManager.getPlacing():
                if TowerManager.getTowerPos():
                    self.money -= TowerManager.getCost()
                    TowerManager.create()
                    Hud.updateMoney(round(self.money))
                    Hud.updateHud(Renderer.getLayer("HUD"))
                else:
                    TowerManager.resetPlacing()
            else:
                TowerManager.resetPlacing()


        Renderer.clearLayer("enemy")
        TowerManager.getSprites().draw(Renderer.getLayer("tower"))
        ProjectileManager.update(EnemyManager.getSprites(), TowerManager.getSprites())
        money_made = ProjectileManager.getMoneyMade()
        money_made_two = TowerManager.getMoneyMade()
        if money_made:
            self.money += money_made
            Hud.updateMoney(round(self.money))
            Hud.updateHud(Renderer.getLayer("HUD"))
        if money_made_two:
            self.money += money_made_two
            Hud.updateMoney(round(self.money))
            Hud.updateHud(Renderer.getLayer("HUD"))
        ProjectileManager.getSprites().draw(Renderer.getLayer("projectile"))
        TowerManager.aim(EnemyManager.getSprites(), self.fast_forward)

        if self.round_started:
            EnemyManager.update(Renderer.getLayer("enemy"), self.path[:])

        if not EnemyManager.getSprites() and self.round_started and not EnemyManager.getEnemies():
            #self.money += 100 + Round.getCurrent()
            Hud.updateMoney(round(self.money))
            self.round_started = False
            Hud.enableSpeed(Renderer.getLayer("HUD"))
            Hud.updateHud(Renderer.getLayer("HUD"))

        for surface in Renderer.getLayers():
            self.screen.blit(surface, (0, 0))


        Renderer.clearLayer("tower")
        Renderer.clearLayer("projectile")



    def update(self):
        self.clock.tick(self.fps)
        self.quit()
        self.game()
        pygame.display.update()

    def run(self):
        while self.running:
            self.update()
        pygame.quit()


if __name__ == "__main__":
    game = Game(screen)
    game.run()
