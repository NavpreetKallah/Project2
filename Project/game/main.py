import time
import pygame
import sys
import copy
from game.classes.sql_class import Sql
from game.classes.enemy_class import EnemyManager
from game.classes.save_manager import SaveManager
from game.classes.hud_class import Hud
from game.classes.map_class import Map
from game.classes.renderer_class import Renderer
from game.classes.round_class import Round
from game.classes.menu_class import Menu
from game.classes.tower_class import TowerManager, ProjectileManager
from game.config import SCALE
from typing import Optional

pygame.init()

WIDTH, HEIGHT = 160 * SCALE, 120 * SCALE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
Sql = Sql()
# Sql.create()
Renderer = Renderer(WIDTH, HEIGHT)
Renderer.clearLayers()
Menu = Menu()
Map = Map()
Round = Round()
Hud = Hud()
EnemyManager = EnemyManager()
TowerManager = TowerManager()
SaveManager = SaveManager()


class Game:
    def __init__(self, screen: pygame.Surface) -> None:
        self.temp: float = time.perf_counter()
        self.screen: pygame.Surface = screen
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.hud_initialise: bool = False
        self.map_initialise: bool = False
        self.round_started: bool = False
        self.clicked: bool = False
        self.fast_forward: bool = False
        self.loaded_game: bool = False
        self.username: Optional[str] = None
        self.main_menu_option: Optional[str] = None
        self.map_option: Optional[str] = None
        self.win_option: Optional[str] = None
        self.difficulty_option: Optional[str] = None
        self.user_validated: bool = False
        self.user_created: Optional[tuple] = None
        self.user_login: Optional[tuple] = None
        self.beaten: bool = False
        self.dead: bool = False
        self.pause: bool = False
        self.difficulties: list[str] = ["easy", "medium", "hard"]
        self.fps_counter: int = 0
        self.fps: int = 60
        self.continue_game: Optional[bool] = None
        self.fps_timer: float = time.perf_counter()
        self.timer: float = time.perf_counter()
        self.running: bool = True
        self.round: int = 0
        self.health: int = 100
        self.money: int = 650
        self.autoplay: bool = False

        title: str = "Balloons"
        pygame.init()
        pygame.display.set_caption(title)

    def reset_display(self) -> None:
        self.screen.fill((0, 0, 0))

    def game(self) -> None:
        if not self.loaded_game:
            if self.main_menu_option not in ["play", "towers", "quit"]:
                self.main_menu_option = Menu.runMenu("main", Renderer.getLayer("menu"))
            elif self.main_menu_option == "quit":
                pygame.quit()
                sys.exit()
            elif self.main_menu_option == "play":
                if self.continue_game not in [True, False]:
                    self.continue_game = Menu.runMenu("continue", Renderer.getLayer("menu"))
                elif self.continue_game:
                    if not self.user_login:
                        self.user_login = Menu.runMenu("login", Renderer.getLayer("menu"), events=self.events)
                    else:
                        if Sql.validate(self.user_login[0], self.user_login[1]):
                            self.username = self.user_login[0]
                            data = SaveManager.loadSave(self.user_login[0])
                            if "health" in data:
                                self.health = data["health"]
                                self.money = data["money"]
                                self.round = data["round"]
                                self.beaten = data["beaten"]
                                self.difficulty_option = data["difficulty"]
                                self.map_option = data["map"]
                                self.difficulty_multiplier = 1 + 0.15 * self.difficulties.index(self.difficulty_option)
                                TowerManager.difficulty_multiplier = self.difficulty_multiplier
                                SaveManager.updateSave(self.health, self.money, Round.current_round,
                                                       self.difficulty_option, self.map_option,
                                                       TowerManager.getSprites(), self.beaten)
                                SaveManager.saveToFile(self.username)
                                TowerManager.loadSave(data["towers"])
                                self.loaded_game = True

                            elif "beaten" in data:
                                self.beaten = data["beaten"]
                                self.continue_game = False
                                self.user_created = True
                                self.user_validated = True

                            else:
                                self.continue_game = False
                                self.user_created = True
                                self.user_validated = True

                        else:
                            Menu.clearFields()
                            Menu.error_message = "password"
                            self.continue_game = None
                            self.user_login = False
                elif not self.continue_game:
                    if not self.user_created:
                        self.user_created = Menu.runMenu("create", Renderer.getLayer("menu"), events=self.events)
                    else:
                        if not self.user_validated and self.user_created:
                            valid = Sql.createUser(self.user_created[0], self.user_created[1])
                            if valid is True:
                                self.username = self.user_created[0]
                                self.user_validated = True
                                Menu.clearFields()
                            else:
                                self.continue_game = None
                                self.user_created = False
                                Menu.error_message = valid
                                Menu.clearFields()

                        if self.user_validated == True:
                            if (self.map_option == "meadows" and not self.beaten) or (
                                    self.map_option == "locked") or self.map_option is None:
                                self.map_option = Menu.runMenu("map", Renderer.getLayer("menu"), beaten=self.beaten)
                            elif self.map_option == "cornfield" or (self.map_option == "meadows" and self.beaten):
                                if self.difficulty_option not in ["easy", "medium", "hard"]:
                                    self.difficulty_option = Menu.runMenu("difficulty", Renderer.getLayer("menu"))
                                else:
                                    SaveManager.updateSave(self.health, self.money, Round.current_round,
                                                           self.difficulty_option, self.map_option,
                                                           TowerManager.getSprites(), self.beaten)
                                    SaveManager.saveToFile(self.username)
                                    self.loaded_game = True
        elif self.loaded_game:

            if self.map_option and self.difficulty_option and not self.map_initialise:
                Renderer.clearLayer("menu")
                Map.initialiseMap(self.map_option, Renderer.getLayer("map"))
                self.path = Map.pathfind()
                self.map_initialise = True

            if not self.hud_initialise and self.difficulty_option and self.map_option:
                Hud.initialiseHud(Renderer.getLayer("HUD"))
                Hud.setDifficulty(self.difficulty_option)
                Hud.updateMoney(round(self.money))
                Hud.updateRound(self.round)
                Round.forceRound(self.round)
                Hud.updateHealth(self.health)
                Hud.updateHud(Renderer.getLayer("HUD"))
                self.difficulty_multiplier = 1 + 0.15 * self.difficulties.index(self.difficulty_option)
                TowerManager.difficulty_multiplier = self.difficulty_multiplier
                self.hud_initialise = True

            if not self.dead and ((pygame.mouse.get_pressed()[0] or self.autoplay) and (
                    Hud.play() or self.autoplay) and not EnemyManager.getEnemies() and not EnemyManager.getSprites()):
                if not self.round_started:
                    self.autoplay = True
                    self.round_started = True
                    Round.startRound(EnemyManager)
                    self.round += 1
                    Hud.updateRound(1)
                    Hud.disableSpeed(Renderer.getLayer("HUD"))
                    Hud.updateHud(Renderer.getLayer("HUD"))

            if 41 + self.difficulties.index(self.difficulty_option) * 20 == self.round and not self.win_option:
                self.beaten = True
                self.win_option = Menu.runMenu("win", Renderer.getLayer("menu"))
                self.pause = True
                if self.win_option == "continue":
                    Renderer.clearLayer("menu")
                    self.pause = False
                elif self.win_option == "quit":
                    SaveManager.resetSave(self.username)
                    Menu.clearFields()
                    self.pause = False
                    self.loaded_game = False
                    self.win_option = None
                    self.difficulty_option = None
                    self.map_option = None
                    self.continue_game = None
                    self.username = None
                    self.user_validated = None
                    self.main_menu_option = None
                    self.user_login = None
                    self.health = 100
                    self.money = 650

            # print(1/(time.perf_counter() - self.temp))
            # self.temp = time.perf_counter()
            # print(self.clock.get_fps())
            self.fps_counter += self.clock.get_fps()
            if time.perf_counter() - self.fps_timer > 5:
                # print(self.fps_counter/ (60*5))
                self.fps_timer = time.perf_counter()
                self.fps_counter = 0

            if pygame.mouse.get_pressed()[0] and not self.clicked and not self.dead and not self.pause:
                self.clicked = True
                tower_chosen = Hud.tower_chosen()
                tower_upgrading = TowerManager.getTowerClicked()
                sell_active = Hud.sellClicked() or Hud.getSell()
                if Hud.fastForward():
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
                TowerManager.place(Renderer.getLayer("tower"), Map.getRects(), Map.getMasks(),
                                   TowerManager.getPlacingTower())

            health_change = EnemyManager.getKilled()
            if health_change:
                if self.health - health_change < 0:
                    self.health = 0

                else:
                    self.health = self.health - health_change
                Hud.updateHealth(self.health)
                Hud.updateHud(Renderer.getLayer("HUD"))

            if self.health == 0:
                SaveManager.resetSave(self.username)
                self.dead = True
                self.death_option = Menu.runMenu("death", Renderer.getLayer("menu"))
                if self.death_option == "quit":
                    Menu.clearFields()
                    self.dead = False
                    self.loaded_game = False
                    self.death_option = None
                    self.difficulty_option = None
                    self.map_option = None
                    self.continue_game = None
                    self.username = None
                    self.user_validated = None
                    self.main_menu_option = None
                    self.user_login = None
                    self.health = 100
                    self.money = 650
                elif self.death_option == "restart":
                    Renderer.clearLayer("menu")
                    self.round = 0
                    Round.reset()
                    self.dead = False
                    self.health = 100
                    self.money = 650
                    TowerManager.reset()
                    Hud.updateRound(0, "set")
                    Hud.updateMoney(round(self.money))
                    Hud.updateHealth(self.health)

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

            if not self.dead:
                TowerManager.aim(EnemyManager.getSprites(), self.fast_forward)

            if self.round_started and not self.pause:
                EnemyManager.update(Renderer.getLayer("enemy"), copy.deepcopy(self.path))

            if not EnemyManager.getSprites() and self.round_started and not EnemyManager.getEnemies():
                self.round_started = False
                Hud.enableSpeed(Renderer.getLayer("HUD"))
                Hud.updateHud(Renderer.getLayer("HUD"))
                SaveManager.updateSave(self.health, self.money, Round.current_round, self.difficulty_option,
                                       self.map_option, TowerManager.getSprites(), self.beaten)
                SaveManager.saveToFile(self.username)

            if not self.pause:
                ProjectileManager.update(EnemyManager.getSprites(), TowerManager.getSprites())
            ProjectileManager.getSprites().draw(Renderer.getLayer("projectile"))
            TowerManager.getSprites().draw(Renderer.getLayer("tower"))

        for surface in Renderer.getLayers():
            self.screen.blit(surface, (0, 0))

        if self.loaded_game:
            Renderer.clearLayer("enemy")
            Renderer.clearLayer("tower")
            Renderer.clearLayer("projectile")

    def quit(self) -> None:
        for event in self.events:
            if event.type == pygame.QUIT:
                self.running = False

    def update(self) -> None:
        self.clock.tick(self.fps)
        self.events = pygame.event.get()
        self.quit()
        self.game()
        pygame.display.update()

    def run(self) -> None:
        while self.running:
            self.update()
        pygame.quit()


if __name__ == "__main__":
    game = Game(screen)
    game.run()
