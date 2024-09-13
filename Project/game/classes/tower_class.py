from builtins import int

import pygame


class Tower:
    def __init__(self, size: int, attack_speed: int):
        self.size = size
        self.attack_speed = attack_speed

    def attack(self, delta_time):
        return None

    def aim(self, position):
        return None