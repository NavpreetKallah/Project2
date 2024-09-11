from builtins import int

import pygame


class Projectile:
    def __init__(self, position: pygame.Vector2, angle: int, damage: int, pierce: int, expire: int, velocity: int, projectile_image: pygame.image):
        self.position = position
        self.angle = angle
        self.damage = damage
        self.pierce = pierce
        self.expire = expire
        self.velocity = velocity
        self.projectile_image = projectile_image

    def onHit(self, delta_time):
        return None

    def collisionDetect(self):
        return None

    def move(self):
        return None

