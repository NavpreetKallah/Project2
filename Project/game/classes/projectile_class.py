import time
from builtins import int

import pygame

from config import SCALE
from math import sin,cos, radians, degrees
import os

# self.position = position
# self.angle = angle
# self.damage = damage
# self.pierce = pierce
# self.expire = expire
# self.velocity = velocity
# self.projectile_image = projectile_image
path = os.path.dirname(os.getcwd()) + "/textures/projectiles"
class Projectile(pygame.sprite.Sprite):
    def __init__(self, data, angle, pos, fast_forward):
        pygame.sprite.Sprite.__init__(self)
        # TODO fix this

        self.type = data["type"]
        self.damage = data["damage"] if self.type != "sniper" else 0
        self.pierce = data["pierce"]
        self.targets = data["targets"]
        self.camo = data["camo"]
        self.extra_damage = data["extra_damage"]
        self.life_time = data["lifespan"] if not fast_forward else data["lifespan"]/3
        self.speed = SCALE * 1 if self.type != "sniper" else 20 * SCALE
        self.speed = self.speed * 3 if fast_forward else self.speed

        self.money = 0
        self.angle = radians(angle)
        # self.image = pygame.Surface((SCALE, SCALE*5))
        # self.image.fill((0,0,0))
        self.image = pygame.transform.scale_by(pygame.image.load_extended(f"{path}/{data['projectile']}.png"),SCALE)
        self.image = pygame.transform.rotate(self.image, degrees(self.angle)+90)
        self.rect = self.image.get_rect(center=pos)
        self.collided = []
        self.life_timer = time.perf_counter()


    def onHit(self):
        return None

    def hit(self, enemies):
        for enemy in enemies:
            if enemy not in self.collided:
                self.collided.append(enemy)
                self.pierce -= 1
                if self.pierce == 0:
                    self.kill()
                self.money += enemy.take_damage(self.damage, self.extra_damage, self.targets, self.camo)
        return self.money

    def move(self):
        if time.perf_counter() - self.life_timer > self.life_time:
            self.kill()
        self.rect.x += sin(self.angle) * self.speed
        self.rect.y += cos(self.angle) * self.speed

class ProjectileManager:
    def __init__(self):
        self.sprites = pygame.sprite.Group()
        self.money = 0

    def create(self, data, angle, pos, fast_forward):
        self.sprites.add(Projectile(data, angle, pos, fast_forward))

    def getSprites(self):
        return self.sprites

    def getMoneyMade(self):
        temp = self.money
        self.money = 0
        return temp

    def update(self, enemies):
        for projectile in self.sprites:
            projectile.move()
        collided = pygame.sprite.groupcollide(self.sprites,enemies,False,False)
        if collided:
            for projectile, enemies in collided.items():
                self.money += projectile.hit(enemies)
