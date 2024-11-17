from builtins import int, super, str

import pygame

from Project.game.classes.entity_class import Entity


class Tower(Entity):
    def __init__(self, position: pygame.Vector2, angle: int, state: str, frame: int,
                 range: int, size: int, attack_speed: int):
        super().__init__(position, angle, state, frame, range)
        self.size = size
        self.attack_speed = attack_speed

    def attack(self, delta_time):
        return None

    def aim(self, position):
        return None