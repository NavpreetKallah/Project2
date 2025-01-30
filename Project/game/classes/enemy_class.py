import time
import copy
from builtins import range

import pygame
import random
import os
from game.classes.linked_list import LinkedList
from game.config import SCALE
from typing import Optional, List, Dict, Any

LinkedList = LinkedList()

path = os.path.dirname(os.getcwd()) + "/textures/enemies"


class Enemy(pygame.sprite.Sprite):
    def __init__(self, node: Any, spawn_delay: float, properties: Dict[str, Any], cash_per_layer: float,
                 enemy_number: int, fast_forward: bool, dupe_values: Optional[Dict[str, Any]] = None) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.spawn_delay: float = spawn_delay
        self.node: Any = node
        data: Dict[str, Any] = self.node.data
        self.fast_forward: bool = fast_forward
        self.number: int = enemy_number
        self.cash_per_layer: float = cash_per_layer
        self.dupe: bool = False
        self.frozen: bool = False
        self.properties: Dict[str, Any] = properties
        self.camo: bool = properties["camo"]
        self.regen: bool = properties["regen"]
        self.cooldown_timer: float = -10
        self.freeze_timer: Optional[float] = None
        self.freeze_duration: float = 1 if not self.fast_forward else 1 / 3
        self.regen_timer: float = time.perf_counter()
        self.name: str = data["name"]
        self.speed: float = data["speed"]
        self.value: int = data["value"]
        self.colour: Any = data["colour"]
        self.health: int = data["health"]
        self.directions: List[str] = ["D", "R", "U", "L"]

        if dupe_values:
            self.duped_enemy(dupe_values)
        else:
            self.distance_travelled: float = 0
            self.distance_travelled_total: float = 0
            self.initialised: bool = False
            self.set_position()

        self.image: pygame.Surface = self.colourIn()

        self.image_list: List[pygame.Surface] = [pygame.transform.rotate(self.image, i * 90) for i in range(4)]
        if dupe_values and self.name in ["moab", "bfb", "zomg"]:
            self.image = self.image_list[self.directions.index(self.current)]

        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.topleft = (self.pos.x, self.pos.y)

    def duped_enemy(self, dupe_values: Dict[str, Any]) -> None:
        self.initialised = True
        self.distance_travelled_total = dupe_values["distance_travelled_total"]
        self.path: Any = dupe_values["path"]
        self.distance_travelled = dupe_values["distance_travelled"]
        self.current: str = dupe_values["current"]
        self.pos: pygame.Vector2 = dupe_values["pos"]
        self.image = self.colourIn()
        if self.name in ["moab", "bfb", "zomg"]:
            self.image_list = [pygame.transform.rotate(self.image, i * 90) for i in range(4)]
            self.image = self.image_list[self.directions.index(self.current)]

    def heal(self) -> None:
        if self.node.prev:
            self.node = self.node.prev
            self.new_node()

    def set_position(self) -> None:
        if not self.name in ["moab", "bfb", "zomg"] and not self.regen:
            self.pos = pygame.Vector2(SCALE * (12 + [-1, 0, 1, 0][self.number % 4]), SCALE * (-4))
        elif self.regen:
            self.pos = pygame.Vector2(SCALE * (11 + [-1, 0, 1, 0][self.number % 4]), SCALE * (-5))
        elif self.name == "moab":
            self.pos = pygame.Vector2(SCALE * (10 + [-1, 0, 1, 0][self.number % 4]), SCALE * (-5))
        elif self.name == "bfb":
            self.pos = pygame.Vector2(SCALE * (8 + [-1, 0, 1, 0][self.number % 4]), SCALE * (-10))
        elif self.name == "zomg":
            self.pos = pygame.Vector2(SCALE * (8 + [-1, 0, 1, 0][self.number % 4]), SCALE * (-8))

    def check_freeze(self) -> bool:
        if self.freeze_timer and time.perf_counter() - self.freeze_timer > self.freeze_duration:
            self.freeze_timer = None
            self.frozen = False
            self.cooldown_timer = time.perf_counter()
        elif self.frozen:
            return True
        return False

    def move(self, direction: Any) -> Optional[str]:
        if self.check_freeze():
            return

        distance: float = 9 * SCALE
        distance_moved: float = (distance / self.speed)
        self.distance_travelled += distance_moved
        self.distance_travelled_total += distance_moved

        if not self.initialised:
            self.initialised = True
            self.path = direction
            self.current = self.path.remove()

        if len(self.path) == 0:
            return "delete"

        if self.distance_travelled >= distance:
            old: str = copy.deepcopy(self.current)
            self.current = self.path.remove()
            self.distance_travelled = distance - self.distance_travelled
            self.distance_travelled = 0
            if old != self.current and self.name in ["moab", "bfb", "zomg"]:
                self.pos.x, self.pos.y = (self.pos.x // SCALE) * SCALE, (self.pos.y // SCALE) * SCALE
                self.image = self.image_list[self.directions.index(self.current)]
            elif old != self.current:
                self.pos.y = (self.pos.y // SCALE) * SCALE

        if self.current == "D":
            self.pos.y += distance_moved
        elif self.current == "U":
            self.pos.y -= distance_moved
        elif self.current == "L":
            self.pos.x -= distance_moved
        elif self.current == "R":
            self.pos.x += distance_moved
        self.rect.topleft = (self.pos.x, self.pos.y)

    def colourIn(self) -> pygame.Surface:

        if self.name in ["moab", "bfb", "zomg"]:
            image = pygame.transform.scale_by(pygame.image.load_extended(f"{path}/{self.name}.png").convert_alpha(),SCALE)
            return image

        if self.regen:
            image = pygame.Surface((7 * SCALE, 7 * SCALE), pygame.SRCALPHA)
            if self.camo:
                image.fill((0, 210, 0), (0, SCALE, 7*SCALE, SCALE))
                image.fill((0, 210, 0), (0, SCALE*3, 7*SCALE, SCALE))
                image.fill((0, 230, 0), (0, SCALE*2, 7*SCALE, SCALE))
                image.fill((0, 150, 0), (3*SCALE, SCALE, SCALE, 6 * SCALE))
                image.fill((0, 170, 0), (2*SCALE, 0, SCALE, 6 * SCALE))
                image.fill((0, 170, 0), (4*SCALE, 0, SCALE, 6 * SCALE))
                image.fill((0, 190, 0), (SCALE, 0, SCALE, 5 * SCALE))
                image.fill((0, 190, 0), (5*SCALE, 0, SCALE, 5 * SCALE))
            else:
                image.fill((0, 0, 0), (0, SCALE, 7 * SCALE, 3 * SCALE))
                image.fill((0, 0, 0), (SCALE, 0, 2 * SCALE, 5 * SCALE))
                image.fill((0, 0, 0), (SCALE*4, 0, 2 * SCALE, 5 * SCALE))
                image.fill((0, 0, 0), (2*SCALE, 5*SCALE, 3 * SCALE, 1 * SCALE))
                image.fill((0, 0, 0), (3*SCALE, 6*SCALE, SCALE, SCALE))
            if self.name == "rainbow":
                image.fill((255,0,0), (SCALE,SCALE,SCALE*2,SCALE))
                image.fill((255,0,0), (SCALE*4,SCALE,SCALE*2,SCALE))
                image.fill((255,122,0), (SCALE,SCALE*2,SCALE*5,SCALE))
                image.fill((255,255,0), (SCALE,SCALE*3,SCALE*5,SCALE))
                image.fill((0,255,0), (SCALE*2,SCALE*4,SCALE*3,SCALE))
                image.fill((0,0,255), (SCALE*3,SCALE*5,SCALE,SCALE))
                return image
            elif self.name == "zebra":
                image.fill((255,255,255), (SCALE,SCALE,SCALE*2,SCALE))
                image.fill((255,255,255), (SCALE*4,SCALE,SCALE*2,SCALE))
                image.fill((50,50,50), (SCALE,SCALE*2,SCALE*5,SCALE))
                image.fill((255,255,255), (SCALE,SCALE*3,SCALE*5,SCALE))
                image.fill((50,50,50), (SCALE*2,SCALE*4,SCALE*3,SCALE))
                image.fill((255,255,255), (SCALE*3,SCALE*5,SCALE,SCALE))
                return image
            else:
                image.fill(self.colour, (SCALE, SCALE,2 * SCALE, 3 * SCALE))
                image.fill(self.colour, (SCALE*4, SCALE,2 * SCALE, 3 * SCALE))
                image.fill(self.colour, (3 * SCALE, SCALE * 2, SCALE, SCALE*4))
                image.fill(self.colour, (SCALE*2, SCALE*4,3 * SCALE, 1 * SCALE))
                return image

        else:
            image = pygame.Surface((5 * SCALE, 6 * SCALE), pygame.SRCALPHA)
            if self.camo:
                image.fill((0, 210, 0), (0, SCALE*2, 5*SCALE, SCALE))
                image.fill((0, 150, 0), (2*SCALE, 0, SCALE, 6 * SCALE))
                image.fill((0, 170, 0), (SCALE, 0, SCALE, 5 * SCALE))
                image.fill((0, 170, 0), (3*SCALE, 0, SCALE, 5 * SCALE))
                image.fill((0, 190, 0), (0, SCALE, 5*SCALE, SCALE))
                image.fill((0, 190, 0), (0, SCALE*3, 5*SCALE, SCALE))
            else:
                image.fill((0, 0, 0), (0, SCALE, 5 * SCALE, 3 * SCALE))
                image.fill((0, 0, 0), (SCALE, 0, 3 * SCALE, 5 * SCALE))
                image.fill((0, 0, 0), (2 * SCALE, SCALE * 5, SCALE, SCALE))

            if self.name == "rainbow":
                image.fill((255,0,0), (SCALE,SCALE,SCALE*3,SCALE))
                image.fill((255,122,0), (SCALE,SCALE*2,SCALE*3,SCALE))
                image.fill((255,255,0), (SCALE,SCALE*3,SCALE*3,SCALE))
                image.fill((0,255,0), (SCALE*2,SCALE*4,SCALE,SCALE))
                return image
            elif self.name == "zebra":
                image.fill((255,255,255), (SCALE,SCALE,SCALE*3,SCALE))
                image.fill((50,50,50), (SCALE,SCALE*2,SCALE*3,SCALE))
                image.fill((255,255,255), (SCALE,SCALE*3,SCALE*3,SCALE))
                image.fill((50,50,50), (SCALE*2,SCALE*4,SCALE,SCALE))
                return image
            else:
                image.fill(self.colour, (SCALE, SCALE, 3 * SCALE, 3 * SCALE))
                image.fill(self.colour, (2 * SCALE, SCALE * 4, SCALE, SCALE))
                return image

    def freeze(self, projectile: Any) -> None:
        cooldown_duration: float = projectile.data["cooldown"] * 3 if self.fast_forward else projectile.data["cooldown"]
        self.freeze_duration: float = projectile.data["freeze"] / 3 if self.fast_forward else projectile.data["freeze"]

        if self.name not in ["moab", "bfb", "zomg"]:
            if time.perf_counter() - self.cooldown_timer > cooldown_duration and self.name != "white":
                self.frozen = True
            if self.frozen:
                if not self.freeze_timer:
                    self.freeze_timer = time.perf_counter()

    def take_damage(self, damage: int, extra: int, targets: List[str], camo: bool, money_modifier: float = 1) -> int:
        money: int = 0
        if self.name in targets or (self.frozen and "frozen" in targets) or (self.camo and not camo):
            return 0

        if self.name in ["moab", "bfb", "zomg"]:
            damage += extra
        for _ in range(damage):
            self.health -= 1
            if self.health == 0:
                money += self.cash_per_layer * money_modifier
                if not self.node.next:
                    self.kill()
                    return money
                original_name: str = copy.deepcopy(self.name)

                if self.name == "rainbow":
                    self.node = self.node.next.next.next
                elif self.name == "white":
                    self.node = self.node.next.next
                else:
                    self.node = self.node.next
                self.new_node()
                if original_name in ["moab", "bfb", "zomg", "rainbow", "ceramic", "zebra", "black", "white"]:
                    return money

        return money

    def new_node(self) -> None:
        self.children()
        self.fixPositions()
        data: Dict[str, Any] = self.node.data
        self.name: str = data["name"]
        self.speed: float = data["speed"]
        self.value: int = data["value"]
        self.colour: Any = data["colour"]
        self.health: int = data["health"]
        self.image: pygame.Surface = self.colourIn()
        if self.name in ["moab", "bfb", "zomg"]:
            self.image_list = [pygame.transform.rotate(self.image, i * 90) for i in range(4)]
            self.image = self.image_list[self.directions.index(self.current)]

    def fixPositions(self) -> None:
        if self.name in ["moab", "bfb", "zomg"]:
            pos_differences: Dict[str, Dict[str, int]] = {
                "moab": {"x": 2, "y": 2},
                "bfb": {"x": 2, "y": 2},
                "zomg": {"x": 0, "y": -2}
            }
            self.pos.x += pos_differences[self.name]["x"] * SCALE
            self.pos.y += pos_differences[self.name]["y"] * SCALE

    def getValue(self) -> int:
        return self.value

    def children(self) -> None:
        if self.name in ["rainbow", "zebra", "ceramic", "moab", "bfb", "zomg", "black", "white"]:
            self.dupe = True
            self.dupe_amount: int = 1 if self.name in ["rainbow", "zebra", "ceramic", "black", "white"] else 3

    def getSpawnDelay(self) -> float:
        return self.spawn_delay

    def setDupe(self, value: bool) -> None:
        self.dupe = value


class EnemyManager:
    def __init__(self) -> None:
        self.speedup: bool = False
        self.timer: float = time.perf_counter()
        self.kill_list: List[Enemy] = []
        self.enemies: Dict[str, any] = {
            "red": {"name": "red", "speed": 30, "value": 1, "health": 1, "colour": (255, 0, 0)},
            "blue": {"name": "blue", "speed": 25, "value": 2, "health": 1, "colour": (0, 0, 255)},
            "green": {"name": "green", "speed": 24, "value": 3, "health": 1, "colour": (0, 255, 0)},
            "yellow": {"name": "yellow", "speed": 21, "value": 4, "health": 1, "colour": (255, 215, 0)},
            "pink": {"name": "pink", "speed": 18, "value": 5, "health": 1, "colour": (255, 136, 136)},
            "black": {"name": "black", "speed": 14, "value": 7, "health": 1, "colour": (0, 0, 0)},
            "white": {"name": "white", "speed": 14, "value": 7, "health": 1, "colour": (255, 255, 255)},
            "zebra": {"name": "zebra", "speed": 12, "value": 8, "health": 1, "colour": "zebra"},
            "purple": {"name": "purple", "speed": 12, "value": 9, "health": 1, "colour": (255, 0, 255)},
            "lead": {"name": "lead", "speed": 120, "value": 10, "health": 1, "colour": (120, 120, 120)},
            "rainbow": {"name": "rainbow", "speed": 12, "value": 11, "health": 1, "colour": "rainbow"},
            "ceramic": {"name": "ceramic", "speed": 9, "value": 12, "health": 8, "colour": (150, 100, 50)},
            "moab": {"name": "moab", "speed": 120, "value": 13, "health": 200, "colour": "moab"},
            "bfb": {"name": "bfb", "speed": 150, "value": 14, "health": 700, "colour": "bfb"},
            "zomg": {"name": "zomg", "speed": 180, "value": 15, "health": 4000, "colour": "zomg"}
        }

        self.sprites: pygame.sprite.Group = pygame.sprite.Group()
        for data in reversed(self.enemies.values()):
            LinkedList.add(data)

        self.enemy_list: List[Enemy] = []
        self.number: int = 0
        self.count: int = 0
        self.round_number: int = 0

    def create(self, data: str, delay: float, properties: Dict[str, any], round_number: int) -> None:
        self.round_number = round_number
        cash_per_layer: float = self.calculateCash(round_number)
        current_node: LinkedList.Node = LinkedList.head
        while current_node.data != data:
            current_node = current_node.next
        current_node.prev = None
        self.enemy_list.append(Enemy(current_node, delay, properties, cash_per_layer, self.number, self.speedup))
        self.number -= 1

    def calculateCash(self, round_number: int) -> float:
        if round_number > 85:
            return 0.1
        elif round_number > 60:
            return 0.2
        elif round_number > 50:
            return 0.5
        else:
            return 1.0

    def duplicate(self, original_enemy: Enemy) -> Enemy:
        self.number -= 1
        pos: pygame.Vector2 = copy.deepcopy(pygame.Vector2(original_enemy.pos.x, original_enemy.pos.y))
        pos.x += -[-1, 0, 1, 0][original_enemy.number % 4] + random.randint(-1, 1) * SCALE
        pos.y += random.randint(-1, 1) * SCALE
        path: List[pygame.Vector2] = copy.deepcopy(original_enemy.path)
        current: Optional[pygame.Vector2] = copy.deepcopy(original_enemy.current)
        distance_travelled: float = copy.deepcopy(original_enemy.distance_travelled)
        distance_travelled_total: float = copy.deepcopy(original_enemy.distance_travelled_total)
        dupe_values: Dict[str, any] = {"pos": pos, "path": path, "current": current,
                                       "distance_travelled": distance_travelled,
                                       "distance_travelled_total": distance_travelled_total}
        properties: Dict[str, any] = copy.deepcopy(original_enemy.properties)
        duplicate = Enemy(original_enemy.node, 0, properties, self.calculateCash(self.round_number), self.number,
                          self.speedup, dupe_values=dupe_values)
        return duplicate

    def getEnemyStats(self) -> Dict[str, Dict[str, any]]:
        return self.enemies

    def getSpeedState(self) -> bool:
        return self.speedup

    def speedChange(self) -> None:
        speed: float = 3 if self.speedup else 1 / 3
        self.speedup = not self.speedup
        for info in self.enemies.values():
            info["speed"] = round(info["speed"] * speed)

    def slowDown(self) -> None:
        for info in self.enemies.values():
            info["speed"] = info["speed"] * 3

    def move(self, path: List[pygame.Vector2]) -> None:
        for enemy in self.sprites:
            if enemy.move(path) == "delete":
                self.kill_list.append(enemy)

    def load(self) -> None:
        if self.enemy_list and time.perf_counter() - self.timer > self.enemy_list[0].getSpawnDelay():
            self.timer = time.perf_counter()
            enemy = self.enemy_list.pop(0)
            self.sprites.add(enemy)

    def getKilled(self) -> int:
        health: int = 0
        for enemy in self.kill_list:
            health += enemy.getValue()
            self.kill_list.remove(enemy)
            enemy.kill()
        return health

    def updateEnemies(self, path: List[pygame.Vector2]) -> None:
        for enemy in self.sprites:
            if enemy.move(path) == "delete":
                self.kill_list.append(enemy)

            if enemy.dupe:
                for _ in range(enemy.dupe_amount):
                    self.sprites.add(self.duplicate(enemy))
                enemy.setDupe(False)

            if enemy.regen:
                if time.perf_counter() - enemy.regen_timer > 1 / (3 if self.speedup else 1):
                    enemy.regen_timer = time.perf_counter()
                    enemy.heal()

    def update(self, layer: pygame.Surface, Map: List[pygame.Vector2]) -> None:
        self.load()
        self.updateEnemies(Map)
        for sprite in sorted(self.sprites, key=lambda sprite: (sprite.value, sprite.number)):
            layer.blit(sprite.image, sprite.rect)

    def getEnemies(self) -> List[Enemy]:
        return self.enemy_list

    def getSprites(self) -> pygame.sprite.Group:
        return self.sprites

    def towersInRange(self, radius: int) -> Optional[List[Enemy]]:
        return None

    def reset(self):
        self.sprites.empty()

    def enemiesInRange(self, radius: int) -> Optional[List[Enemy]]:
        return None

    def stun(self, towers_in_range: List[Enemy], delta_time: float) -> None:
        return None

    def speedBoost(self, enemies_in_range: List[Enemy], delta_time: float) -> None:
        return None
