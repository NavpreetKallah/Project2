import pygame
import sys


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
        self.main_menu_option = None
        self.map_option = None
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
            Renderer.clearLayer("menu")
            self.main_menu_option = Menu.runMenu("main", Renderer.getLayer("menu"))
        elif self.main_menu_option == "quit":
            pygame.quit()
            sys.exit()
        elif self.main_menu_option == "play":
            Renderer.clearLayer("menu")
            self.map_option = Menu.runMenu("map", Renderer.getLayer("menu"))
        # floor = Map.drawMap(Renderer.getLayer("map"))
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

