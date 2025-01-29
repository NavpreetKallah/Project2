import copy
import random
import time
import pygame
from math import pi, atan2, radians, sin, cos, degrees
from config import SCALE
from typing import List, Dict, Optional, Tuple, Union
import os

path = os.path.dirname(os.getcwd()) + "/textures/projectiles"


class DefaultProjectile(pygame.sprite.Sprite):
    def __init__(self, data: Dict[str, Union[int, float, str]], camo: bool, angle: float, range: float,
                 pos: Tuple[float, float], fast_forward: bool) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.data = data
        self.type: str = data["type"]
        self.damage: int = data["damage"]
        self.pierce: int = data["pierce"]
        self.targets: List[str] = data["targets"]
        self.camo: bool = camo
        self.range: float = range
        self.extra_damage: int = data["extra_damage"]
        self.life_time: float = data["lifespan"] if not fast_forward else data["lifespan"] / 3
        self.speed: float = data["projectile_speed"] * SCALE
        self.speed = self.speed * 3 if fast_forward else self.speed
        self.money: int = 0
        self.angle: float = radians(angle)
        self.original_image: pygame.Surface = pygame.transform.scale_by(
            pygame.image.load_extended(f"{path}/{data['projectile']}.png"), SCALE)
        self.image: pygame.Surface = pygame.transform.rotate(self.original_image, degrees(self.angle) + 90)
        self.rect: pygame.Rect = self.image.get_rect(center=pos)
        self.rect.x += sin(self.angle) * self.image.get_width() // 4
        self.rect.y += cos(self.angle) * self.image.get_height() // 4
        self.collided: List[pygame.sprite.Sprite] = []
        self.life_timer: float = time.perf_counter()

    def hit(self, enemies: List[pygame.sprite.Sprite]) -> int:
        self.money = 0
        for enemy in enemies:
            if enemy not in self.collided and (not enemy.camo or self.camo):
                self.collided.append(enemy)
                self.pierce -= 1
                if self.pierce == 0:
                    self.kill()
                self.money += enemy.take_damage(self.damage, self.extra_damage, self.targets, self.camo)
        return self.money

    def move(self, enemies: List[pygame.sprite.Sprite]) -> None:
        if time.perf_counter() - self.life_timer > self.life_time:
            self.kill()
        self.rect.x += sin(self.angle) * self.speed
        self.rect.y += cos(self.angle) * self.speed

    def getAngle(self, target: Union[pygame.Rect, Tuple[float, float]]) -> float:
        x1, y1 = self.rect.center
        if isinstance(target, pygame.Rect):
            x2, y2 = target.center
        else:
            x2, y2 = target
        dx = x2 - x1
        dy = y2 - y1
        rads = atan2(-dy, dx)
        rads %= 2 * pi
        return degrees(rads) + 90


class ProjectileManager:
    def __init__(self) -> None:
        self.sprites: pygame.sprite.Group = pygame.sprite.Group()
        self.projectile_types: Dict[str, type] = {
            "default": DefaultProjectile,
            "homing": Homing,
            "explosion": Explosion,
            "freeze": Freeze,
            "buff": Buff,
            "lead": LeadPotion,
            "gold": MoneyPotion,
            "boomerang": Boomerang,
            "banana": Banana
        }
        self.money: int = 0

    def create(self, data: Dict[str, Union[int, float, str]], camo: bool, ranges: float, angle: float,
               pos: Tuple[float, float], fast_forward: bool) -> None:
        if "burst" in data:
            for i in range(-data["burst"], data["burst"] + 1):
                self.sprites.add(
                    self.projectile_types[data["type"]](data, camo, angle + i * 10, ranges, pos, fast_forward))
        else:
            self.sprites.add(self.projectile_types[data["type"]](data, camo, angle, ranges, pos, fast_forward))

    def getSprites(self) -> pygame.sprite.Group:
        return self.sprites

    def getMoneyMade(self) -> int:
        temp = self.money
        self.money = 0
        return temp

    def updateBanana(self):
        total = 0
        for projectile in self.sprites:
            if projectile.type == "banana":
                total += projectile.nearby()
        return total

    def update(self, enemy_group: pygame.sprite.Group, tower_group: pygame.sprite.Group) -> None:
        for projectile in self.sprites:
            projectile.move(enemy_group)
        collided = pygame.sprite.groupcollide(self.sprites, enemy_group, False, False)
        collided_towers = pygame.sprite.groupcollide(self.sprites, tower_group, False, False)
        if collided:
            for projectile, enemies in collided.items():
                if projectile.type == "explosion":
                    self.money += projectile.hit(enemy_group)
                elif projectile.type != "buff":
                    self.money += projectile.hit(enemies)
        if collided_towers:
            for projectile, towers in collided_towers.items():
                if projectile.type == "buff":
                    projectile.kill()


class Homing(DefaultProjectile):
    def __init__(self, data: Dict[str, Union[int, float, str]], camo: bool, angle: float, ranges: float,
                 pos: Tuple[float, float], fast_forward: bool) -> None:
        super().__init__(data, camo, angle, ranges, pos, fast_forward)
        self.image_list: List[pygame.Surface] = [pygame.transform.rotate(self.original_image, i) for i in range(360)]

    def homeIn(self, enemies: List[pygame.sprite.Sprite]) -> None:
        enemy_list = [enemy for enemy in enemies if enemy not in self.collided and (not enemy.camo or self.camo)]
        if enemy_list:
            enemy_targeted = min(enemy_list, key=lambda enemy: pygame.Vector2(self.rect.center).distance_to(
                pygame.Vector2(enemy.rect.center)))
            self.angle = radians(self.getAngle(enemy_targeted.rect))
            self.image = self.image_list[round(degrees(self.angle) + 90) % 360]
            self.rect = self.image.get_rect(center=self.rect.center)

    def move(self, enemies: List[pygame.sprite.Sprite]) -> None:
        if time.perf_counter() - self.life_timer > self.life_time / 10:
            self.homeIn(enemies)
        if time.perf_counter() - self.life_timer > self.life_time:
            self.kill()
        self.rect.x += sin(self.angle) * self.speed
        self.rect.y += cos(self.angle) * self.speed


class Explosion(DefaultProjectile):
    def __init__(self, data: Dict[str, Union[int, float, str]], camo: bool, angle: float, range: float,
                 pos: Tuple[float, float], fast_forward: bool) -> None:
        super().__init__(data, camo, angle, range, pos, fast_forward)
        self.explosion_image: pygame.Surface = pygame.transform.scale_by(
            pygame.image.load_extended(f"{path}/explosion.png"), SCALE)

    def hit(self, enemies: List[pygame.sprite.Sprite]) -> int:
        self.speed = 0
        self.angle = 0
        self.image = self.explosion_image
        self.rect = self.image.get_rect(center=self.rect.center)
        collided = pygame.sprite.spritecollide(self, enemies, False)
        if collided:
            self.money += self.explosion_hit(collided)
        return self.money

    def explosion_hit(self, enemies: List[pygame.sprite.Sprite]) -> int:
        self.money = 0
        for enemy in enemies:
            if enemy not in self.collided and (not enemy.camo or self.camo):
                self.collided.append(enemy)
                self.pierce -= 1
                if self.pierce == 0:
                    self.kill()
                self.money += enemy.take_damage(self.damage, self.extra_damage, self.targets, self.camo)
        return self.money


class Freeze(DefaultProjectile):
    def __init__(self, data: Dict[str, Union[int, float, str]], camo: bool, angle: float, range: float,
                 pos: Tuple[float, float], fast_forward: bool) -> None:
        super().__init__(data, camo, angle, range, pos, fast_forward)

    def hit(self, enemies: List[pygame.sprite.Sprite]) -> int:
        self.money = 0
        for enemy in enemies:
            if enemy not in self.collided and (not enemy.camo or self.camo):
                self.collided.append(enemy)
                self.pierce -= 1
                if self.pierce == 0:
                    self.kill()
                enemy.freeze(self)
                self.money += enemy.take_damage(self.damage, self.extra_damage, self.targets, self.camo)
        return self.money


class Buff(DefaultProjectile):
    def __init__(self, data: Dict[str, Union[int, float, str]], camo: bool, angle: float, range: float,
                 pos: Tuple[float, float], fast_forward: bool) -> None:
        super().__init__(data, camo, angle, range, pos, fast_forward)
        self.rect.x += sin(self.angle) * self.image.get_width()
        self.rect.y += cos(self.angle) * self.image.get_height()


class LeadPotion(DefaultProjectile):
    def __init__(self, data: Dict[str, Union[int, float, str]], camo: bool, angle: float, range: float,
                 pos: Tuple[float, float], fast_forward: bool) -> None:
        super().__init__(data, camo, angle, range, pos, fast_forward)

    def hit(self, enemies: List[pygame.sprite.Sprite]) -> int:
        self.money = 0
        for enemy in enemies:
            if enemy not in self.collided and (not enemy.camo or self.camo):
                self.collided.append(enemy)
                if enemy.name == "lead":
                    self.kill()
                    enemy.take_damage(999, self.extra_damage, self.targets, self.camo)
                    self.money += 50
                else:
                    self.pierce -= 1
                    if self.pierce == 0:
                        self.kill()
                    self.money += enemy.take_damage(self.damage, self.extra_damage, self.targets, self.camo)
        return self.money


class MoneyPotion(DefaultProjectile):
    def __init__(self, data: Dict[str, Union[int, float, str]], camo: bool, angle: float, range: float,
                 pos: Tuple[float, float], fast_forward: bool) -> None:
        super().__init__(data, camo, angle, range, pos, fast_forward)

    def hit(self, enemies: List[pygame.sprite.Sprite]) -> int:
        for enemy in enemies:
            if enemy not in self.collided and (not enemy.camo or self.camo):
                self.collided.append(enemy)
                self.pierce -= 1
                if self.pierce == 0:
                    self.kill()
                self.money += enemy.take_damage(self.damage, self.extra_damage, self.targets, self.camo,
                                                money_modifier=2)
        return self.money


class Boomerang(DefaultProjectile):
    def __init__(self, data: Dict[str, Union[int, float, str]], camo: bool, angle: float, ranges: float,
                 pos: Tuple[float, float], fast_forward: bool) -> None:
        super().__init__(data, camo, angle, ranges, pos, fast_forward)
        self.distance_travelled: pygame.Vector2 = pygame.Vector2(self.rect.center)
        self.old_distance: float = 1000
        self.original_x: float = copy.deepcopy(self.rect.x)
        self.returning: bool = False
        self.original_y: float = copy.deepcopy(self.rect.y)
        self.counter: int = 0
        self.image_list: List[pygame.Surface] = [pygame.transform.rotate(self.image, 10 * i) for i in range(36)]

    def move(self, enemies: List[pygame.sprite.Sprite]) -> None:
        self.counter += 10
        self.image = self.image_list[round(self.counter) % 36]
        self.rect = self.image.get_rect(center=self.rect.center)
        distance = ((self.distance_travelled.x - self.original_x) ** 2 + (
                    self.distance_travelled.y - self.original_y) ** 2) ** 0.5 / SCALE
        if distance < self.range and not self.returning:
            offset = (-8 / (3 * self.range)) * (0.75 * distance - (3 * self.range) / 8) ** 2 + (3 * self.range) / 8
            self.distance_travelled.x += sin(self.angle) * self.speed
            self.distance_travelled.y += cos(self.angle) * self.speed

        elif distance < 2 * self.range and distance < self.old_distance:
            self.old_distance = distance
            self.returning = True
            offset = (8 / (3 * self.range)) * (0.75 * distance - (3 * self.range) / 8) ** 2 - (3 * self.range) / 8
            self.distance_travelled.x -= sin(self.angle) * self.speed
            self.distance_travelled.y -= cos(self.angle) * self.speed

        else:
            offset = 0
            self.kill()

        self.rect.x = self.distance_travelled.x + offset * SCALE * cos(self.angle)
        self.rect.y = self.distance_travelled.y + offset * SCALE * sin(self.angle)


class Banana(DefaultProjectile):
    def __init__(self, data: Dict[str, Union[int, float, str]], camo: bool, angle: float, ranges: float,
                 pos: Tuple[float, float], fast_forward: bool) -> None:
        super().__init__(data, camo, angle, ranges, pos, fast_forward)
        self.money_earned = data["money"]


        self.rect.x += sin(self.angle)
        self.rect.y += cos(self.angle)

    def move(self, enemies: List[pygame.sprite.Sprite]) -> None:
        if time.perf_counter() - self.life_timer > self.life_time:
            self.kill()
        self.rect.x += sin(self.angle) * self.speed
        self.rect.y += cos(self.angle) * self.speed
        self.speed *= (0.8 + random.uniform(-0.1,0.1))

    def nearby(self):
        mouse = pygame.mouse.get_pos()
        if pygame.Vector2(self.rect.center).distance_to(pygame.Vector2(mouse)) < self.range*SCALE:
            self.angle = radians(self.getAngle(mouse))
            self.speed = SCALE

        if self.rect.collidepoint(mouse):
            self.kill()
            return self.money_earned

        if self.data["autocollect"]:
            self.kill()
            return self.money_earned

        return 0
