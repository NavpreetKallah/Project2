from builtins import int, list, super, str
import pygame

from game.classes.entity_class import Entity
from game.config import SCALE

# , position: pygame.Vector2, angle: int, state: str, frame: int, range: int,
#                  distance_travelled: int, health: int, immunities: list, speed: int, value: int,

class Enemy():
    def __init__(self):
        # super().__init__(position, angle, state, frame, range)
        # self.distance_travelled = distance_travelled
        # self.health = health
        # self.immunities = immunities
        # self.value = value
        self.speed = 1*SCALE
        self.count = 0
        self.current = None
        self.position = pygame.Vector2(SCALE*12,SCALE*13)

    def pathfind(self, end_coordinate):
        return None

    def takeDamage(self, damage):
        return None

    def move(self, direction, layer):
        distance = 9 * SCALE
        distance_moved = distance//self.speed
        if len(direction) == 0:
            print("DONE")
            return False
        if self.count == 0:
            self.current = direction.pop(0)
            self.count = distance_moved
        if self.count > 0:
            if self.current == "D":
                self.position.y += self.speed
            if self.current == "U":
                self.position.y -= self.speed
            if self.current == "L":
                self.position.x -= self.speed
            if self.current == "R":
                self.position.x += self.speed
        self.count -= 1
        self.draw(layer)
        self.move(direction, layer)

    def draw(self, layer):
        pygame.draw.rect(layer, (255,255,255), pygame.Rect(self.position.x, self.position.y, SCALE * 5, SCALE * 5))


    def towersInRange(self, int):
        return None

    def enemiesInRange(self, int):
        return None

    def stun(self, towers_in_range, delta_time):
        return None

    def speedBoost(self, enemies_in_range, delta_time):
        return None

    def regenerate(self, delta_time):
        return None

    def damage(self, health):
        return None
