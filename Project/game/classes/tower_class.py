import json
import os
import abc
import time
from math import atan2, degrees, pi

import pygame
import random

from config import SCALE
from game.classes.projectile_class import ProjectileManager

ProjectileManager = ProjectileManager()


# Entity
# , position: pygame.Vector2, angle: int, state: str, frame: int,
#                  range: int, size: int, attack_speed: int
#
# super().__init__(position, angle, state, frame, range)

# self.size = size
# self.attack_speed = attack_speed

class DefaultTower(pygame.sprite.Sprite):
    __metaclass__ = abc.ABCMeta
    def __init__(self, data, pos):
        pygame.sprite.Sprite.__init__(self)
        self.data = data
        self.upgrades = {"path_one":0,"path_two":0}
        self.image = data["icon"]
        self.pos = pos
        self.rect = self.image.get_rect(center=self.pos)
        self.image_copy = self.image
        self.timer = time.perf_counter()
        self.images = [pygame.transform.rotate(self.image, i) for i in range(1, 361)]

    @abc.abstractmethod
    def action(self, enemies, fast_forward):
        return

    @abc.abstractmethod
    def abilityUpgrades(self, upgrade_name):
        return

    def attack(self, fast_forward, angle):
        if time.perf_counter() - self.timer > (self.data["main_atk_speed"] if not fast_forward else self.data["main_atk_speed"] / 3):
            self.timer = time.perf_counter()
            ProjectileManager.create(self.data, angle, self.rect.center, fast_forward)

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

    def upgrade(self, path, money):

        if self.upgrades[path] == 4:
            return 0

        upgrade_info = self.data[path][str(self.upgrades[path] + 1)]
        if upgrade_info["cost"] > money:
            return 0

        if upgrade_info["stat_change"] is not None:
            for change in upgrade_info["stat_change"]:
                if change["type"] == "add":
                    self.data[change["stat"]] += change["value"]
                elif change["type"] == "set":
                    self.data[change["stat"]] = change["value"]
                else:
                    self.data[change["stat"]] *= change["value"]
        if upgrade_info["name"] is not None:
            self.abilityUpgrades(upgrade_info["name"])

        self.upgrades[path] += 1

        return upgrade_info["cost"]

class Wizard(DefaultTower):
    def __init__(self, data, pos):
        super().__init__(data, pos)
        data["projectile_image"] = "default"
    def action(self, enemies, fast_forward):
        if self.data["main_atk_speed"] == 0:
            return
        enemy_info = [enemy for enemy in enemies if int(pygame.Vector2(self.rect.center).distance_to(pygame.Vector2(enemy.rect.center)) // SCALE) < self.data["range"]]
        if enemy_info:
            angle = round(self.getAngle(enemy_info[0].rect.center))
            self.attack(fast_forward, angle)
            self.image = self.images[angle % 360]
            self.rect = self.image.get_rect(center=self.pos)
        return 0

    def abilityUpgrades(self, upgrade_name):
        print(upgrade_name)

class Dart(DefaultTower):
    def __init__(self, data, pos):
        super().__init__(data, pos)
        data["projectile_image"] = "default"
    def action(self, enemies, fast_forward):
        if self.data["main_atk_speed"] == 0:
            return
        enemy_info = [enemy for enemy in enemies if int(pygame.Vector2(self.rect.center).distance_to(pygame.Vector2(enemy.rect.center)) // SCALE) < self.data["range"]]
        if enemy_info:
            angle = round(self.getAngle(enemy_info[0].rect.center))
            self.attack(fast_forward, angle)
            self.image = self.images[angle % 360]
            self.rect = self.image.get_rect(center=self.pos)
        return 0

    def abilityUpgrades(self, upgrade_name):
        print(upgrade_name)

class Sniper(DefaultTower):
    def __init__(self, data, pos):
        super().__init__(data, pos)
        data["projectile_image"] = "default"

    def action(self, enemies, fast_forward):
        enemies = sorted(enemies, key=lambda enemy: enemy.value, reverse=True)
        angle = round(self.getAngle(enemies[0].rect.center))
        self.image = self.images[angle % 360]
        self.rect = self.image.get_rect(center=self.pos)
        if time.perf_counter() - self.timer > (
        self.data["main_atk_speed"] if not fast_forward else self.data["main_atk_speed"] / 3):
            ProjectileManager.create(self.data, angle, self.rect.center, fast_forward)
            self.timer = time.perf_counter() + random.uniform(-0.01, 0.01)
            return enemies[0].take_damage(self.data["damage"], self.data["main_atk_targets"], self.data["camo"])
        return 0

    def abilityUpgrades(self, upgrade_name):
        print(upgrade_name)

class Tower(pygame.sprite.Sprite):
    def __init__(self, data, pos):
        pygame.sprite.Sprite.__init__(self)
        self.data = data
        self.upgrades = {"path_one":0,"path_two":0}
        self.image = data["icon"]
        self.pos = pos
        self.rect = self.image.get_rect(center=self.pos)
        self.image_copy = self.image
        self.timer = time.perf_counter()
        self.images = [pygame.transform.rotate(self.image, i) for i in range(1, 361)]

    def attack(self, fast_forward, angle):
        if time.perf_counter() - self.timer > (self.data["main_atk_speed"] if not fast_forward else self.data["main_atk_speed"] / 3):
            self.timer = time.perf_counter()
            ProjectileManager.create(self.data, angle, self.rect.center, fast_forward)

    def upgrade(self, path, money):
        upgrade_info = self.data[path][str(self.upgrades[path]+1)]
        if upgrade_info["cost"] > money:
            return 0

        print(self.upgrades[path])
        if upgrade_info["name"] is None:
            for change in upgrade_info["stat_change"]:
                if change["type"] == "add":
                    self.data[change["stat"]] += change["value"]
                elif change["type"] == "set":
                    self.data[change["stat"]] = change["value"]
                else:
                    self.data[change["stat"]] *= change["value"]
        return upgrade_info["cost"]

    def action(self, enemies, fast_forward):
        if self.data["main_atk"] == "normal":
            self.normal_aim(enemies, fast_forward)
            return 0
        if self.data["main_atk"] == "mouse":
            self.mouse_aim(fast_forward)
            return 0
        if self.data["main_atk"] == "sniper":
            return self.sniper(enemies, fast_forward)
    def sniper(self, enemies, fast_forward):
        enemies = sorted(enemies, key=lambda enemy: enemy.value, reverse=True)
        angle = round(self.getAngle(enemies[0].rect.center))
        self.image = self.images[angle % 360]
        self.rect = self.image.get_rect(center=self.pos)
        if time.perf_counter() - self.timer > (self.data["main_atk_speed"] if not fast_forward else self.data["main_atk_speed"] / 3):
            ProjectileManager.create(self.data, angle, self.rect.center, fast_forward)
            self.timer = time.perf_counter() + random.uniform(-0.01,0.01)
            return enemies[0].take_damage(self.data["damage"], self.data["main_atk_targets"], self.data["camo"])
        return 0

    def mouse_aim(self, fast_forward):
        angle = round(self.getAngle(pygame.mouse.get_pos()))
        self.image = self.images[angle % 360]
        self.rect = self.image.get_rect(center=self.pos)
        angle += random.randint(-self.data["spread"], self.data["spread"])
        self.attack(fast_forward, angle)

    def normal_aim(self, enemies, fast_forward):
        if self.data["main_atk_speed"] == 0:
            return
        enemy_info = [enemy for enemy in enemies if int(pygame.Vector2(self.rect.center).distance_to(pygame.Vector2(enemy.rect.center)) // SCALE) < self.data["range"]]
        if enemy_info:
            angle = round(self.getAngle(enemy_info[0].rect.center))
            self.attack(fast_forward, angle)
            self.image = self.images[angle % 360]
            self.rect = self.image.get_rect(center=self.pos)

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


json_path = os.path.dirname(os.getcwd()) + "/game/data/tower_data.json"
path = os.path.dirname(os.getcwd()) + "/textures/HUD"


class TowerManager:
    def __init__(self):

        with open(f"{json_path}", "r") as file:
            data = json.load(file)
        tower_icons = self.seperate_sheet(
            pygame.transform.scale_by(pygame.image.load_extended(f"{path}/spritesheet2.png").convert_alpha(),
                                      SCALE), 8 * SCALE)
        tower_icons = {tower_name: tower_icons[i] for i, tower_name in enumerate(data)}
        for tower_name, tower_info in data.items():
            data[tower_name]["icon"] = tower_icons[tower_name]
        self.tower_dict = data
        self.tower_class_dict = {"Dart": Dart, "Sniper": Sniper, "Wizard": Wizard}
        self.money = 0
        self.placing = False
        self.placing_tower = None
        self.tower_pos = None
        self.tower_mask = None
        self.sprites = pygame.sprite.Group()
        self.images = []

    def create(self):
        if self.placing_tower and self.tower_pos:
            print(self.placing_tower)
            self.sprites.add(self.tower_class_dict[self.placing_tower](self.tower_dict[self.placing_tower], self.tower_pos))
            self.images.append(self.tower_dict[self.placing_tower]["icon"])
            self.placing_tower = None
            self.placing = False
            self.tower_pos = None

    def place(self, layer, paths, path_masks, tower):
        mouse = pygame.mouse.get_pos()
        corrected_mouse = ((mouse[0] // SCALE) * SCALE, (mouse[1] // SCALE) * SCALE)
        rect = pygame.Rect(1 * SCALE, 11 * SCALE, 126 * SCALE, 108 * SCALE)
        valid = True
        if not self.tower_mask:
            self.tower_mask = pygame.mask.from_surface(self.tower_dict[tower]["icon"])
        if rect.contains(self.tower_dict[tower]["icon"].get_rect(center=corrected_mouse)):
            if self.tower_dict[tower]["icon"].get_rect(center=corrected_mouse).collidelist(paths) != -1:
                for i, path in enumerate(paths):
                    path_x, path_y = (path.center[0] // SCALE) * SCALE, (path.center[1] // SCALE) * SCALE
                    offset = corrected_mouse[0] - path_x, corrected_mouse[1] - path_y
                    if path_masks[i].overlap(self.tower_mask, offset):
                        valid = False
                        break
            if self.tower_dict[tower]["icon"].get_rect(center=corrected_mouse).collidelist([sprite.rect for sprite in self.sprites]) != -1:
                for i, sprite in enumerate(self.sprites):
                    rect_x, rect_y = (sprite.rect.center[0] // SCALE) * SCALE, (sprite.rect.center[1] // SCALE) * SCALE
                    offset = (corrected_mouse[0] - rect_x, corrected_mouse[1] - rect_y)
                    if pygame.mask.from_surface(self.images[i]).overlap(self.tower_mask, offset):
                        valid = False
                        break

        else:
            valid = False

        pygame.draw.circle(layer, (50, 50, 50, 20) if valid else (200, 50, 50, 120), corrected_mouse,
                           self.tower_dict[tower]["range"]*SCALE)
        layer.blit(self.tower_dict[tower]["icon"], self.tower_dict[tower]["icon"].get_rect(center=corrected_mouse))
        self.tower_pos = corrected_mouse if valid else None

    def getCost(self):
        return self.tower_dict[self.placing_tower]["cost"]

    def resetPlacing(self):
        self.placing_tower = None
        self.placing = False
        self.tower_pos = None
        self.tower_mask = None

    def getTowerPos(self):
        return self.tower_pos

    def aim(self, enemies, fast_forward):
        enemies = sorted(enemies, key=lambda enemy: enemy.distance_travelled)
        if enemies and self.sprites:
            for tower in self.sprites:
                self.money += tower.action(enemies, fast_forward)

    def attack(self):
        for tower in self.sprites:
            tower.attack()

    def getPlacing(self):
        return self.placing

    def getSprites(self):
        return self.sprites

    def getMoneyMade(self):
        temp = self.money
        self.money = 0
        return temp
    def getPlacingTower(self):
        return self.placing_tower

    def seperate_sheet(self, sheet, width):
        images = []
        amount = sheet.get_width() // width
        for i in range(amount):
            image = pygame.Surface((width, width), pygame.SRCALPHA).convert_alpha()
            image.blit(sheet, (0, 0), (width * i, 0, width, width))
            images.append(image)
        return images

    def getUpgradingTower(self):
        return self.upgrading_tower
    def getTowerClicked(self):
        mouse = pygame.mouse.get_pos()
        for tower in self.sprites:
            if tower.rect.collidepoint(mouse):
                self.upgrading_tower = tower
                return tower
        return False
