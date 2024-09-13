import pygame

from game.classes.button_class import Button
from game.classes.enemy_class import Enemy
from game.classes.entity_class import Entity
from game.classes.explosion_class import Explosion
from game.classes.hud_class import Hud
from game.classes.map_class import Map
from game.classes.projectile_class import Projectile
from game.classes.renderer_class import Renderer
from game.classes.round_class import Round
from game.classes.textbox_class import Textbox
from game.classes.tower_class import Tower

WIDTH, HEIGHT = 1000,1280

class Game:
    def __init__(self, screen_size):
        self.screen_size = screen_size
        self.screen = pygame.display.set_mode(self.screen_size)
        self.clock = pygame.time.Clock()
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
        pass

    def update(self):
        self.quit()
        self.reset_display()
        self.game()
        for surface in self.surfaces:
            self.screen.blit(surface, (0, 0))
        pygame.display.update()
        self.clock.tick(self.fps)

    def run(self):
        while self.running:
            self.update()
        pygame.quit()

if __name__ == "__main__":
    game = Game((WIDTH, HEIGHT))
    game.run()

