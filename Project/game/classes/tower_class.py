from builtins import int, super, str

import pygame

from classes.entity_class import Entity
# Entity
# , position: pygame.Vector2, angle: int, state: str, frame: int,
#                  range: int, size: int, attack_speed: int
#
# super().__init__(position, angle, state, frame, range)
# self.size = size
# self.attack_speed = attack_speed

class Tower:
    def __init__(self):
        pass
    
    def attack(self, delta_time):
        return None

    def aim(self, position):
        return None

class TowerManager:
    def __init__(self):
        tower_icons = []
        pass