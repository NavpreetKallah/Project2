from builtins import int, list

import pygame


class Enemy:
    def __init__(self, distanceTravelled: int, health: int, immunities: list, speed: int, value: int):
        self.distanceTravelled = distanceTravelled
        self.health = health
        self.immunities = immunities
        self.speed = speed
        self.value = value

    def pathfind(self, end_coordinate):
        return None

    def takeDamage(self, damage):
        return None

    def move(self, magnitude, direction, deltaTime):
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
