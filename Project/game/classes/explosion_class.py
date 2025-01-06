from builtins import int

import pygame


class Explosion:
    def __init__(self, position: pygame.Vector2, radius: int, explosion_damage: int):
        self.position = position
        self.radius = radius
        self.explosion_damage = explosion_damage

    def debuff(self, delta_time):
        return None
