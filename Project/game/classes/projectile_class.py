import time
from builtins import int

import pygame

from config import SCALE
from math import sin,cos, radians

# self.position = position
# self.angle = angle
# self.damage = damage
# self.pierce = pierce
# self.expire = expire
# self.velocity = velocity
# self.projectile_image = projectile_image
class Projectile(pygame.sprite.Sprite):
    def __init__(self, data, angle, pos, fast_forward):
        pygame.sprite.Sprite.__init__(self)
        self.damage = data["damage"]
        self.pierce = data["pierce"]
        self.speed = SCALE*3
        self.money = 0
        self.speed = self.speed* 3 if fast_forward else self.speed
        self.angle = radians(angle)
        self.image = pygame.Surface((SCALE, SCALE))
        self.image.fill((0,0,0))
        self.rect = self.image.get_rect(center=pos)
        self.collided = []
        self.life_time = 2
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
                self.money += enemy.take_damage(self.damage)
        return self.money


    def collisionDetect(self):
        return None

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
