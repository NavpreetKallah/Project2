import json
import os
import abc
import copy
import time
from abc import ABCMeta
from math import atan2, degrees, pi, sin, cos
from typing import List, Dict, Optional, Tuple, Union

import pygame
import random

from config import SCALE
from game.classes.projectile_class import ProjectileManager

ProjectileManager = ProjectileManager()


class DefaultTower(pygame.sprite.Sprite):
    __metaclass__ = abc.ABCMeta

    def __init__(self, data: Dict[str, Union[str, int, Dict]], pos: Tuple[int, int],
                 difficulty_multiplier: float) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.difficulty_multiplier = difficulty_multiplier
        self.data = data
        image = data["icon"]
        self.buffs: Dict[str, Dict[str, Union[int, bool]]] = {"Village": {}, "Alchemist": {}}
        self.data["icon"] = None
        self.unbuffed_data = copy.deepcopy(self.data)
        self.image = image
        self.upgrades: Dict[str, int] = {"path_one": 0, "path_two": 0}
        self._total_cost = data["cost"]
        self.pos = pos
        self.rect = self.image.get_rect(center=self.pos)
        self.image_copy = self.image
        self.timers: Dict[str, float] = {"main": time.perf_counter(), "secondary": time.perf_counter()}
        self.images: List[pygame.Surface] = [pygame.transform.rotate(self.image, i) for i in range(1, 361)]

    def action(self, enemies: List['Enemy'], fast_forward: bool) -> int:
        for type in ["main", "secondary"]:
            if self.data[type]["speed"] == 0:
                return 0
            enemy_info = [enemy for enemy in enemies if int(pygame.Vector2(self.rect.center).distance_to(
                pygame.Vector2(enemy.rect.center)) // SCALE) < self.data["range"] and (
                                  not enemy.camo or self.data["camo"])]
            if enemy_info:
                angle = round(self.getAngle(enemy_info[0].rect.center))
                self.attack(fast_forward, angle, type)
                self.image = self.images[angle % 360]
                self.rect = self.image.get_rect(center=self.pos)
        return 0

    @abc.abstractmethod
    def abilityUpgrades(self, upgrade_name: str) -> None:
        return

    @property
    def total_cost(self) -> int:
        return self._total_cost

    def attack(self, fast_forward: bool, angle: int, type: str) -> None:
        if time.perf_counter() - self.timers[type] > (
                (self.data[type]["speed"] if not fast_forward else self.data[type]["speed"] / 3) * random.uniform(0.9,
                                                                                                                  1.1)):
            self.timers[type] = time.perf_counter()
            ProjectileManager.create(self.data[type], self.data["camo"], self.data["range"], angle, self.rect.center,
                                     fast_forward)

    def buff(self, buffs: Dict[str, Union[int, bool]], tower: str) -> None:
        for key, value in buffs.items():
            if key == "speed":
                self.buffs[tower][key] = self.buffs[tower][key] if key in self.buffs[tower] and value > \
                                                                   self.buffs[tower][key] else value
            elif key == "camo":
                self.buffs[tower][key] = value
            elif key == "targets":
                self.buffs[tower][key] = self.buffs[tower][key] if key in self.buffs[tower] and len(value) < len(
                    self.buffs[tower][key]) else value
            else:
                self.buffs[tower][key] = self.buffs[tower][key] if key in self.buffs[tower] and value < \
                                                                   self.buffs[tower][key] else value

    def updateBuffs(self) -> None:
        buff_names: set = set()
        buffs: Dict[str, Union[int, bool]] = {}
        alchemist = self.buffs["Alchemist"]
        village = self.buffs["Village"]

        for tower_buffs in self.buffs.values():
            for key in tower_buffs.keys():
                buff_names.add(key)

        for buff in buff_names:
            if buff in ["range", "speed"]:
                buffs[buff] = (alchemist[buff] if buff in alchemist else 1) * (village[buff] if buff in village else 1)
            elif buff == "camo":
                buffs["camo"] = True
            elif buff == "targets":
                buffs["targets"] = []
            else:
                buffs[buff] = alchemist[buff] if buff in alchemist else 0 + village[buff] if buff in village else 0

        for key, value in buffs.items():
            if key == "range":
                self.data[key] = value * self.unbuffed_data[key]
            elif key == "camo":
                self.data[key] = value
            else:
                for attack in ["main", "secondary"]:
                    if key == "speed":
                        self.data[attack][key] = value * self.unbuffed_data[attack][key]
                    elif key in ["damage", "pierce"]:
                        self.data[attack][key] = value + self.unbuffed_data[attack][key]
                    elif key == "targets":
                        self.data[attack][key] = value

    def removeBuffs(self, buffs: Dict[str, Union[int, bool]], tower: str) -> None:
        for stat in ["main", "secondary"]:
            if stat in self.unbuffed_data:
                for key in buffs.keys():
                    if key not in ["range", "camo"]:
                        self.data[stat][key] = self.unbuffed_data[stat][key]
                    else:
                        self.data[key] = self.unbuffed_data[key]
        self.buffs[tower] = {}

    def sell(self) -> int:
        total_cost = round(self.total_cost * 0.7)
        self.kill()
        return total_cost

    def getAngle(self, target: Union[pygame.Rect, Tuple[int, int]]) -> float:
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

    def upgrade(self, path: str, money: int) -> Union[int, float]:
        if self.upgrades[path] == 4:
            return 0

        other_path = list(self.upgrades)[(list(self.upgrades).index(path) + 1) % 2]
        if self.upgrades[path] == 2 and self.upgrades[other_path] > 2:
            return 0

        upgrade_info = self.data[path][str(self.upgrades[path] + 1)]
        if round(upgrade_info["cost"] * self.difficulty_multiplier) > money:
            return 0

        if upgrade_info["stat_change"] is not None:
            for change in upgrade_info["stat_change"]:
                attack = change["attack"]
                stat = change["stat"]
                value = change["value"]

                if attack == "buff":
                    self.data["buffs"][stat] = value
                elif change["stat"] == "range":
                    self.data[stat] += value
                    self.unbuffed_data[stat] += value
                elif change["stat"] == "camo":
                    self.data[stat] = value
                    self.unbuffed_data[stat] = value
                elif change["type"] == "add":
                    self.data[attack][stat] += value
                    self.unbuffed_data[attack][stat] += value
                elif change["type"] == "set":
                    self.data[attack][stat] = value
                    self.unbuffed_data[attack][stat] = value
                else:
                    self.data[attack][stat] *= value
                    self.unbuffed_data[attack][stat] *= value

        if upgrade_info["name"] is not None:
            self.abilityUpgrades(upgrade_info["name"])

        self.upgrades[path] += 1
        self._total_cost += round(upgrade_info["cost"] * self.difficulty_multiplier)
        return round(upgrade_info["cost"] * self.difficulty_multiplier)


class Wizard(DefaultTower, metaclass=ABCMeta):
    def __init__(self, data: Dict[str, Union[str, int, Dict]], pos: Tuple[int, int],
                 difficulty_multiplier: float) -> None:
        super().__init__(data, pos, difficulty_multiplier)
        data["main"]["projectile"] = "wizard_main"
        data["secondary"]["projectile"] = "wizard_fireball"


class Druid(DefaultTower, metaclass=ABCMeta):
    def __init__(self, data: Dict[str, Union[str, int, Dict]], pos: Tuple[int, int],
                 difficulty_multiplier: float) -> None:
        super().__init__(data, pos, difficulty_multiplier)
        data["main"]["projectile"] = "druid_main"
        data["secondary"]["projectile"] = "druid_secondary"


class Dartling(DefaultTower, metaclass=ABCMeta):
    def __init__(self, data: Dict[str, Union[str, int, Dict]], pos: Tuple[int, int],
                 difficulty_multiplier: float) -> None:
        super().__init__(data, pos, difficulty_multiplier)
        data["main"]["projectile"] = "default"

    def action(self, enemies: List['Enemy'], fast_forward: bool) -> int:
        angle = round(self.getAngle(pygame.mouse.get_pos()))
        self.image = self.images[angle % 360]
        self.rect = self.image.get_rect(center=self.pos)
        angle += random.randint(-self.data["main"]["deviation"], self.data["main"]["deviation"])
        self.attack(fast_forward, angle, "main")
        return 0

    def attack(self, fast_forward: bool, angle: int, type: str) -> None:
        if time.perf_counter() - self.timers[type] > (
                (self.data[type]["speed"] if not fast_forward else self.data[type]["speed"] / 3) * random.uniform(0.9,
                                                                                                                  1.1)):
            self.timers[type] = time.perf_counter()
            ProjectileManager.create(self.data[type], self.data["camo"], self.data["range"], angle, self.rect.center,
                                     fast_forward)


class Ice(DefaultTower, metaclass=ABCMeta):
    def __init__(self, data: Dict[str, Union[str, int, Dict]], pos: Tuple[int, int],
                 difficulty_multiplier: float) -> None:
        super().__init__(data, pos, difficulty_multiplier)
        data["main"]["projectile"] = "ice_main"
        data["secondary"]["projectile"] = "default"


class Boomerang(DefaultTower, metaclass=ABCMeta):
    def __init__(self, data: Dict[str, Union[str, int, Dict]], pos: Tuple[int, int],
                 difficulty_multiplier: float) -> None:
        super().__init__(data, pos, difficulty_multiplier)
        data["main"]["projectile"] = "boomerang_main"
        data["secondary"]["projectile"] = "default"


class Ninja(DefaultTower, metaclass=ABCMeta):
    def __init__(self, data: Dict[str, Union[str, int, Dict]], pos: Tuple[int, int],
                 difficulty_multiplier: float) -> None:
        super().__init__(data, pos, difficulty_multiplier)
        data["main"]["projectile"] = "ninja_main"
        data["secondary"]["projectile"] = "ninja_secondary"


class Alchemist(DefaultTower, metaclass=ABCMeta):
    def __init__(self, data: Dict[str, Union[str, int, Dict]], pos: Tuple[int, int],
                 difficulty_multiplier: float) -> None:
        super().__init__(data, pos, difficulty_multiplier)
        data["main"]["projectile"] = "alchemist_main"
        data["secondary"]["projectile"] = "alchemist_main"
        self.buff_timer: float = time.perf_counter()
        self.buffed: Dict[pygame.sprite.Sprite, float] = {}

    def action(self, enemies: List['Enemy'], fast_forward: bool) -> int:
        enemy_info = [enemy for enemy in enemies if int(pygame.Vector2(self.rect.center).distance_to(
            pygame.Vector2(enemy.rect.center)) // SCALE) < self.data["range"] and (
                              not enemy.camo or self.data["camo"])]
        if enemy_info:
            angle = round(self.getAngle(enemy_info[0].rect.center))
            self.attack(fast_forward, angle, "main")
            self.image = self.images[angle % 360]
            self.rect = self.image.get_rect(center=self.pos)
        self.unbuff()
        if self.data["buffs"] and time.perf_counter() - self.timers["secondary"] > ((self.data["secondary"][
            "speed"] if not fast_forward else self.data["secondary"]["speed"] / 3) * random.uniform(0.9, 1.1)):
            self.timers["secondary"] = time.perf_counter()
            tower_buffed = self.getClosestInRangeUnBuffed()
            if tower_buffed:
                angle = round(self.getAngle(tower_buffed.rect.center))
                ProjectileManager.create(self.data["secondary"], self.data["camo"], self.data["range"], angle,
                                         self.rect.center, fast_forward)
                tower_buffed.buff(self.data["buffs"], "Alchemist")
                tower_buffed.updateBuffs()
                self.image = self.images[angle % 360]
                self.rect = self.image.get_rect(center=self.pos)
        return 0

    def unbuff(self) -> None:
        delete_list: List[pygame.sprite.Sprite] = []
        for tower, timer in self.buffed.items():
            if time.perf_counter() - timer > self.data["secondary"]["duration"]:
                tower.removeBuffs(self.data["buffs"], "Alchemist")
                delete_list.append(tower)

        for tower in delete_list:
            del (self.buffed[tower])

    def sell(self) -> int:
        total_cost = round(self.total_cost * 0.7)
        for tower in self.buffed.keys():
            tower.removeBuffs(self.data["buffs"], "Alchemist")
        self.kill()
        return total_cost

    def quickSort(self, list: list, value_list: list) -> list:
        if len(list) <= 1:
            return list

        elif len(list) != len(value_list):
            return []

        middle_item = list[len(list) // 2]
        middle_value = value_list[list.index(middle_item)]

        left = [element for element in list if value_list[list.index(element)] < middle_value]
        middle = [element for element in list if value_list[list.index(element)] == middle_value]
        right = [element for element in list if value_list[list.index(element)] > middle_value]
        return self.quickSort(left, value_list) + middle + self.quickSort(right, value_list)

    def distanceCalculate(self, target: 'DefaultTower') -> float:
        x1, y1 = self.rect.center
        x2, y2 = target.rect.center
        distance = ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** 0.5
        return distance

    def distanceTo(self, targets: list) -> list:
        if isinstance(targets, list):
            return [self.distanceCalculate(target) for target in targets]
        else:
            return [self.distanceCalculate(targets)]

    def getClosestInRangeUnBuffed(self) -> Union['DefaultTower', None]:
        tower_group = self.groups()[0]

        towers = [tower for tower in tower_group if
                  tower != self and tower.__class__.__name__ not in ["Village", "Farm"] and int(
                      pygame.Vector2(self.rect.center).distance_to(
                          pygame.Vector2(tower.rect.center)) // SCALE) < self.data[
                      "range"] and tower not in self.buffed]
        if towers:
            tower = self.quickSort(towers, self.distanceTo(towers))[0]
            self.buffed[tower] = time.perf_counter()
            return tower
        return None


class Super(DefaultTower, metaclass=ABCMeta):
    def __init__(self, data: Dict[str, dict], pos: tuple[int, int], difficulty_multiplier: float) -> None:
        super().__init__(data, pos, difficulty_multiplier)
        data["main"]["projectile"] = "default"
        data["secondary"]["projectile"] = "default"


class Farm(DefaultTower, metaclass=ABCMeta):
    def __init__(self, data: Dict[str, dict], pos: tuple[int, int], difficulty_multiplier: float) -> None:
        super().__init__(data, pos, difficulty_multiplier)
        data["main"]["projectile"] = "banana"
        self.bannana_cooldown: float = time.perf_counter()

    def action(self, enemies: List[object], fast_forward: bool) -> int:
        if time.perf_counter() - self.bannana_cooldown > (self.data["main"]["speed"] if not fast_forward else self.data["main"]["speed"] / 3):
            angle = self.getAngle(pygame.mouse.get_pos())
            angle += random.randint(-90,90)
            self.bannana_cooldown = time.perf_counter()
            ProjectileManager.create(self.data["main"], self.data["camo"], self.data["range"], angle, self.rect.center, fast_forward)

        return ProjectileManager.updateBanana()


class Village(DefaultTower, metaclass=ABCMeta):
    def __init__(self, data: Dict[str, dict], pos: tuple[int, int], difficulty_multiplier: float) -> None:
        super().__init__(data, pos, difficulty_multiplier)
        self.buff_cooldown: float = time.perf_counter()

    def action(self, enemies: List[object], fast_forward: bool) -> int:
        if time.perf_counter() - self.buff_cooldown > 1 if not fast_forward else 1 / 3:
            self.buff_cooldown = time.perf_counter()
            towers_in_range = self.getTowersInRange()
            for tower in towers_in_range:
                tower.buff(self.data["buffs"], "Village")
                tower.updateBuffs()
        return 0

    def getTowersInRange(self) -> List[object]:
        tower_group = self.groups()[0]
        towers = [tower for tower in tower_group if
                  tower != self and tower.__class__.__name__ not in ["Village", "Farm"] and int(
                      pygame.Vector2(self.rect.center).distance_to(
                          pygame.Vector2(tower.rect.center)) // SCALE) < self.data["range"]]
        return towers

    def sell(self) -> int:
        total_cost = round(self.total_cost * 0.7)
        for tower in self.getTowersInRange():
            tower.removeBuffs(self.data["buffs"], "Village")
        self.kill()
        return total_cost


class Dart(DefaultTower):
    def __init__(self, data: Dict[str, dict], pos: tuple[int, int], difficulty_multiplier: float) -> None:
        super().__init__(data, pos, difficulty_multiplier)
        data["main"]["projectile"] = "default"
        data["secondary"]["projectile"] = "default"


class Sniper(DefaultTower):
    def __init__(self, data: Dict[str, dict], pos: tuple[int, int], difficulty_multiplier: float) -> None:
        super().__init__(data, pos, difficulty_multiplier)
        data["main"]["projectile"] = "sniper_main"

    def action(self, enemies: List[object], fast_forward: bool) -> int:
        enemies = sorted([enemy for enemy in enemies if (not enemy.camo or self.data["camo"])],
                         key=lambda enemy: (enemy.value, enemy.distance_travelled_total), reverse=True)
        if not enemies:
            return 0
        angle = round(self.getAngle(enemies[0].rect.center))
        self.image = self.images[angle % 360]
        self.rect = self.image.get_rect(center=self.pos)
        if time.perf_counter() - self.timers["main"] > (
                self.data["main"]["speed"] if not fast_forward else self.data["main"]["speed"] / 3):
            fake_projectile_data = copy.deepcopy(self.data["main"])
            fake_projectile_data["damage"] = 0
            ProjectileManager.create(fake_projectile_data, self.data["camo"], self.data["range"], angle,
                                     self.rect.center, fast_forward)
            self.timers["main"] = time.perf_counter() + random.uniform(-0.01, 0.01)
            return enemies[0].take_damage(self.data["main"]["damage"], self.data["main"]["extra_damage"],
                                          self.data["main"]["targets"], self.data["camo"])
        return 0


json_path: str = os.path.dirname(os.getcwd()) + "/game/data/tower_data.json"
path: str = os.path.dirname(os.getcwd()) + "/textures/HUD"


class TowerManager:
    def __init__(self) -> None:
        with open(f"{json_path}", "r") as file:
            data = json.load(file)
        tower_icons = self.seperate_sheet(
            pygame.transform.scale_by(pygame.image.load_extended(f"{path}/spritesheet2.png").convert_alpha(),
                                      SCALE), 8 * SCALE)
        tower_icons = {tower_name: tower_icons[i] for i, tower_name in enumerate(data)}
        for tower_name, tower_info in data.items():
            data[tower_name]["icon"] = tower_icons[tower_name]
        self.tower_dict: Dict[str, dict] = data
        self.tower_class_dict: Dict[str, type[DefaultTower]] = {"Dart": Dart, "Sniper": Sniper, "Wizard": Wizard,
                                                                "Druid": Druid, "Ninja": Ninja, "Farm": Farm,
                                                                "Village": Village, "Super": Super,
                                                                "Boomerang": Boomerang, "Dartling": Dartling,"Dartling gunner": Dartling,
                                                                "Alchemist": Alchemist, "Ice": Ice}
        self.money: int = 0
        self.placing: bool = False
        self.placing_tower: Optional[str] = None
        self.tower_pos: Optional[tuple[int, int]] = None
        self.tower_mask: Optional[pygame.mask.Mask] = None
        self.sprites: pygame.sprite.Group = pygame.sprite.Group()
        self.images: List[pygame.Surface] = []

    def create(self) -> None:
        if self.placing_tower and self.tower_pos:
            tower_data: Dict[str, object] = {
                info: (value if isinstance(value, pygame.Surface) else copy.deepcopy(value)) for info, value in
                self.tower_dict[self.placing_tower].items()}
            self.sprites.add(
                self.tower_class_dict[self.placing_tower](tower_data, self.tower_pos, self.difficulty_multiplier))
            self.images.append(self.tower_dict[self.placing_tower]["icon"])
            self.placing_tower = None
            self.placing = False
            self.tower_pos = None

    def reset(self) -> None:
        self.sprites.empty()

    def place(self, layer: pygame.Surface, paths: List[pygame.Rect], path_masks: List[pygame.mask.Mask],
              tower: str) -> None:
        mouse = pygame.mouse.get_pos()
        corrected_mouse = ((mouse[0] // SCALE) * SCALE, (mouse[1] // SCALE) * SCALE)
        rect = pygame.Rect(1 * SCALE, 11 * SCALE, 126 * SCALE, 108 * SCALE)
        valid: bool = True
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
            if self.tower_dict[tower]["icon"].get_rect(center=corrected_mouse).collidelist(
                    [sprite.rect for sprite in self.sprites]) != -1:
                for i, sprite in enumerate(self.sprites):
                    rect_x, rect_y = (sprite.rect.center[0] // SCALE) * SCALE, (sprite.rect.center[1] // SCALE) * SCALE
                    offset = (corrected_mouse[0] - rect_x, corrected_mouse[1] - rect_y)
                    if pygame.mask.from_surface(self.images[i]).overlap(self.tower_mask, offset):
                        valid = False
                        break
        else:
            valid = False

        pygame.draw.circle(layer, (50, 50, 50, 20) if valid else (200, 50, 50, 120), corrected_mouse,
                           self.tower_dict[tower]["range"] * SCALE)
        layer.blit(self.tower_dict[tower]["icon"], self.tower_dict[tower]["icon"].get_rect(center=corrected_mouse))
        self.tower_pos = corrected_mouse if valid else None

    def getCost(self) -> int:
        return round(self.tower_dict[self.placing_tower]["cost"] * self.difficulty_multiplier)

    def resetPlacing(self) -> None:
        self.placing_tower = None
        self.placing = False
        self.tower_pos = None
        self.tower_mask = None

    def getTowerPos(self) -> Optional[tuple[int, int]]:
        return self.tower_pos

    def aim(self, enemies: List[object], fast_forward: bool) -> None:
        enemies = sorted(enemies, key=lambda enemy: enemy.distance_travelled_total, reverse=True)
        enemies = [enemy for enemy in enemies if enemy.distance_travelled_total > 10 * SCALE]
        if enemies and self.sprites:
            for tower in self.sprites:
                self.money += tower.action(enemies, fast_forward)

    def attack(self) -> None:
        for tower in self.sprites:
            tower.attack()

    def getPlacing(self) -> bool:
        return self.placing

    def getSprites(self) -> pygame.sprite.Group:
        return self.sprites

    def getMoneyMade(self) -> int:
        temp: int = self.money
        self.money = 0
        return temp

    def getPlacingTower(self) -> Optional[str]:
        return self.placing_tower

    def seperate_sheet(self, sheet: pygame.Surface, width: int) -> List[pygame.Surface]:
        images: List[pygame.Surface] = []
        amount = sheet.get_width() // width
        for i in range(amount):
            image = pygame.Surface((width, width), pygame.SRCALPHA).convert_alpha()
            image.blit(sheet, (0, 0), (width * i, 0, width, width))
            images.append(image)
        return images

    def loadSave(self, save: List[Dict]) -> None:
        for tower in save:
            tower_data: Dict[str, object] = {
                info: (value if isinstance(value, pygame.Surface) else copy.deepcopy(value)) for info, value in
                self.tower_dict[tower["name"]].items()}
            tower_created = self.tower_class_dict[tower["name"]](tower_data, tower["pos"], self.difficulty_multiplier)
            if tower["name"] == "Dartling":
                tower["name"] = "Dartling gunner"
            self.images.append(self.tower_dict[tower["name"]]["icon"])
            for path in ["path_one", "path_two"]:
                for _ in range(tower["upgrades"][path]):
                    tower_created.upgrade(path, 99999999)
            self.sprites.add(tower_created)

    def getUpgradingTower(self) -> Optional['Tower']:
        return self.upgrading_tower

    def getTowerClicked(self) -> Union['Tower', bool]:
        mouse = pygame.mouse.get_pos()
        for tower in self.sprites:
            if tower.rect.collidepoint(mouse):
                self.upgrading_tower = tower
                return tower
        return False
