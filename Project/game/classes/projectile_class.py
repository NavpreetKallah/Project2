import time
from builtins import int
import pygame
from math import pi, atan2, radians
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

class DefaultProjectile(pygame.sprite.Sprite):
    def __init__(self, data, camo, angle, pos, fast_forward):
        pygame.sprite.Sprite.__init__(self)
        self.type = data["type"]
        self.damage = data["damage"]
        self.pierce = data["pierce"]
        self.targets = data["targets"]
        self.camo = camo
        self.extra_damage = data["extra_damage"]
        self.life_time = data["lifespan"] if not fast_forward else data["lifespan"]/3
        self.speed = data["projectile_speed"] * SCALE
        self.speed = self.speed * 3 if fast_forward else self.speed
        self.money = 0
        self.angle = radians(angle)
        self.original_image = pygame.transform.scale_by(pygame.image.load_extended(f"{path}/{data['projectile']}.png"), SCALE)
        self.image = pygame.transform.rotate(self.original_image, degrees(self.angle)+90)

        self.rect = self.image.get_rect(center=pos)
        self.collided = []
        self.life_timer = time.perf_counter()

    def hit(self, enemies):
        self.money = 0
        for enemy in enemies:
            if enemy not in self.collided and (not enemy.camo or self.camo):
                self.collided.append(enemy)
                self.pierce -= 1
                if self.pierce == 0:
                    self.kill()
                self.money += enemy.take_damage(self.damage, self.extra_damage, self.targets, self.camo)
        return self.money

    def move(self, enemies):
        if time.perf_counter() - self.life_timer > self.life_time:
            self.kill()
        self.rect.x += sin(self.angle) * self.speed
        self.rect.y += cos(self.angle) * self.speed

    def getAngle(self, target):
        x1, y1 = self.rect.center
        if isinstance(target, type(self.rect)):
            x2, y2 = target.center
        else:
            x2, y2 = target
        dx = x2 - x1
        dy = y2 - y1
        rads = atan2(-dy, dx)
        rads %= 2 * pi
        return degrees(rads) + 90

class ProjectileManager:
    def __init__(self):
        self.sprites = pygame.sprite.Group()
        self.projectile_types = {
            "default": DefaultProjectile,
            "homing": Homing,
            "explosion": Explosion
        }
        self.money = 0

    def create(self, data, camo,angle, pos, fast_forward):
        if "burst" in data:
            for i in range(-data["burst"], data["burst"] + 1):
                self.sprites.add(self.projectile_types[data["type"]](data, camo, angle + i * 10, pos, fast_forward))
        else:
            self.sprites.add(self.projectile_types[data["type"]](data, camo, angle, pos, fast_forward))

    def getSprites(self):
        return self.sprites

    def getMoneyMade(self):
        temp = self.money
        self.money = 0
        return temp

    def update(self, enemy_group):
        for projectile in self.sprites:
            projectile.move(enemy_group)
        collided = pygame.sprite.groupcollide(self.sprites,enemy_group,False,False)
        if collided:
            for projectile, enemies in collided.items():
                if projectile.type == "explosion":
                    self.money += projectile.hit(enemy_group)
                else:
                    self.money += projectile.hit(enemies)


class Homing(DefaultProjectile):
    def __init__(self, data, camo, angle, pos, fast_forward):
        super().__init__(data, camo, angle, pos, fast_forward)
        self.image_list = [pygame.transform.rotate(self.original_image, i) for i in range(360)]
    def homeIn(self, enemies):
        enemy_list = [enemy for enemy in enemies if enemy not in self.collided and (not enemy.camo or self.camo)]
        if enemy_list:
            enemy_targeted = min(enemy_list, key=lambda enemy: pygame.Vector2(self.rect.center).distance_to(pygame.Vector2(enemy.rect.center)))
            self.angle = radians(self.getAngle(enemy_targeted.rect))
            self.image = self.image_list[round(degrees(self.angle) + 90)%360]
            self.rect = self.image.get_rect(center=self.rect.center)

    def move(self, enemies):
        if time.perf_counter() - self.life_timer > self.life_time/5:
            self.homeIn(enemies)
        if time.perf_counter() - self.life_timer > self.life_time:
            self.kill()
        self.rect.x += sin(self.angle) * self.speed
        self.rect.y += cos(self.angle) * self.speed



class Explosion(DefaultProjectile):
    def __init__(self, data, camo, angle, pos, fast_forward):
        super().__init__(data, camo, angle, pos, fast_forward)
        self.explosion_image = pygame.transform.scale_by(pygame.image.load_extended(f"{path}/explosion.png"), SCALE)

    def hit(self, enemies):
        self.speed = 0
        self.angle = 0
        self.image = self.explosion_image
        self.rect = self.image.get_rect(center=self.rect.center)
        collided = pygame.sprite.spritecollide(self, enemies,False)
        if collided:
            self.money += self.explosion_hit(collided)
        return self.money

    def explosion_hit(self, enemies):
        self.money = 0
        for enemy in enemies:
            if enemy not in self.collided and (not enemy.camo or self.camo):
                self.collided.append(enemy)
                self.pierce -= 1
                if self.pierce == 0:
                    self.kill()
                self.money += enemy.take_damage(self.damage, self.extra_damage, self.targets, self.camo)
        return self.money


