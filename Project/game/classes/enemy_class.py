from builtins import int, list, super, str
import pygame

from game.classes.entity_class import Entity


class Enemy(Entity):
    def __init__(self, position: pygame.Vector2, angle: int, state: str, frame: int, range: int,
                 distance_travelled: int, health: int, immunities: list, speed: int, value: int,):
        super().__init__(position, angle, state, frame, range)
        self.distance_travelled = distance_travelled
        self.health = health
        self.immunities = immunities
        self.speed = speed
        self.value = value

    def pathfind(self, end_coordinate):
        return None

    def takeDamage(self, damage):
        return None

    def move(self, magnitude, direction, delta_time):
        return None

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
