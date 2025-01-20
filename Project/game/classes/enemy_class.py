import time
import copy
from builtins import range

import pygame
import random, os
from game.classes.linked_list import LinkedList
from game.config import SCALE

# , rect: pygame.Vector2, angle: int, state: str, frame: int, range: int,
#                  distance_travelled: int, health: int, immunities: list, speed: int, value: int,
LinkedList = LinkedList()

path = os.path.dirname(os.getcwd()) + "/textures/enemies"
class Enemy(pygame.sprite.Sprite):
    def __init__(self, node, spawn_delay, properties,enemy_number, dupe_values=None):
        pygame.sprite.Sprite.__init__(self)
        self.spawn_delay = spawn_delay
        self.node = node
        data = self.node.data
        self.number = enemy_number
        self.dupe = False
        self.frozen = False
        self.properties = properties
        self.camo = properties["camo"]
        self.regen = properties["regen"]
        self.cooldown_timer = time.perf_counter()
        self.cooldown_duration = 3
        self.freezable = True
        self.freeze_timer = time.perf_counter()
        self.frozen = False
        self.freeze_duration = 1
        self.regen_timer = time.perf_counter()
        self.name = data["name"]
        self.speed = data["speed"]
        self.value = data["value"]
        self.colour = data["colour"]
        self.health = data["health"]
        self.directions = ["D","R","U","L"]

        if dupe_values:
            self.duped_enemy(dupe_values)
        else:
            self.distance_travelled = 0
            self.distance_travelled_total = 0
            self.initialised = False
            self.set_position()

        self.image = self.colourIn()

        self.image_list = [pygame.transform.rotate(self.image, i*90) for i in range(4)]
        if dupe_values and self.name in ["moab", "bfb", "zomg"]:
            self.image = self.image_list[self.directions.index(self.current)]

        self.rect = self.image.get_rect()
        self.rect.topleft = (self.pos.x, self.pos.y)

    def duped_enemy(self, dupe_values):
        self.initialised = True
        self.distance_travelled_total = dupe_values["distance_travelled_total"]
        self.path = dupe_values["path"]
        self.distance_travelled = dupe_values["distance_travelled"]
        self.current = dupe_values["current"]
        self.pos = dupe_values["pos"]
        self.image = self.colourIn()
        if self.name in ["moab", "bfb", "zomg"]:
            self.image_list = [pygame.transform.rotate(self.image, i * 90) for i in range(4)]
            self.image = self.image_list[self.directions.index(self.current)]

    def heal(self):
        if self.node.prev:
            self.node = self.node.prev
            self.new_node()

    def set_position(self):
        if not self.name in ["moab","bfb","zomg"] and not self.regen:
            self.pos = pygame.Vector2(SCALE * (12 + [-1, 0, 1, 0][self.number % 4]),SCALE * (-4 - [0, 1][self.number % 2]))
        elif self.regen:
            self.pos = pygame.Vector2(SCALE * (11 + [-1, 0, 1, 0][self.number % 4]),SCALE * (-5 - [0, 1][self.number % 2]))
        elif self.name == "moab":
            self.pos = pygame.Vector2(SCALE * (10 + [-1, 0, 1, 0][self.number % 4]),SCALE * (-7 - [0, 1][self.number % 2]))
        elif self.name == "bfb":
            self.pos = pygame.Vector2(SCALE * (8 + [-1, 0, 1, 0][self.number % 4]),SCALE * (-10 - [0, 1][self.number % 2]))
        elif self.name == "zomg":
            self.pos = pygame.Vector2(SCALE * (8 + [-1, 0, 1, 0][self.number % 4]),SCALE * (-8 - [0, 1][self.number % 2]))


    def move(self, direction):
        if self.name not in ["moab", "bfb", "zomg"]:
            if time.perf_counter() - self.cooldown_timer > self.cooldown_duration:
                self.freezable = True

            if self.frozen and self.freezable:
                self.freeze_timer = time.perf_counter()
                if time.perf_counter() - self.freeze_timer > self.freeze_duration:
                    self.freezable = False
                    self.frozen = False
                    self.cooldown_timer = time.perf_counter() - self.freeze_duration
                else:
                    return
        distance = 9 * SCALE
        distance_moved = (distance / self.speed)
        self.distance_travelled += distance_moved
        self.distance_travelled_total += distance_moved

        if not self.initialised:
            self.initialised = True
            self.path = direction
            self.current = self.path.pop(0)

        if len(self.path) == 0:
            return "delete"

        if self.distance_travelled >= distance:

            old = copy.deepcopy(self.current)
            self.current = self.path.pop(0)
            if self.name != "blue":
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

    def colourIn(self):

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

    def take_damage(self, damage, extra, targets, camo):
        money = 0
        if self.name in targets or (self.frozen and "frozen" in targets) or (self.camo and not camo):
            return 0

        self.frozen = True
        if self.name in ["moab","bfb","zomg"]:
            damage += extra
        for _ in range(damage):
            self.health -= 1
            if self.health == 0:
                money += 1
                if not self.node.next:
                    self.kill()
                    return money
                original_name = copy.deepcopy(self.name)

                self.node = self.node.next if self.name != "rainbow" else self.node.next.next.next
                self.new_node()
                if original_name in ["moab","bfb","zomg","rainbow","ceramic"]:
                    return money

        return money

    def new_node(self):
        self.children()
        data = self.node.data
        self.name = data["name"]
        self.speed = data["speed"]
        self.value = data["value"]
        self.colour = data["colour"]
        self.health = data["health"]

        if self.name in ["moab", "bfb", "zomg"]:
            self.image = self.image_list[self.directions.index(self.current)]
        else:
            self.image = self.colourIn()

    def getValue(self):
        return self.value

    def children(self):
        if self.name in ["rainbow", "zebra","ceramic","moab","bfb","zomg"]:
            self.duper = copy.deepcopy(self.name)
            self.dupe = True
            self.dupe_amount = 1 if self.name in ["rainbow", "zebra", "ceramic"] else 3

    def getSpawnDelay(self):
        return self.spawn_delay

    def setDupe(self, value):
        self.dupe = value


class EnemyManager:
    def __init__(self):
        # super().__init__(rect, angle, state, frame, range)
        # self.distance_travelled = distance_travelled
        # self.health = health
        # self.immunities = immunities
        # self.value = value
        self.speedup = False
        self.timer = time.perf_counter()
        self.queue = []
        self.kill_list = []
        self.enemies = {"red": {"name": "red", "speed": 30, "value": 1, "health": 1, "colour": (255, 0, 0)},
                        "blue": {"name": "blue", "speed": 25, "value": 2, "health": 1, "colour": (0, 0, 255)},
                        "green": {"name": "green", "speed": 24, "value": 3, "health": 1, "colour": (0, 255, 0)},
                        "yellow": {"name": "yellow", "speed": 21, "value": 4, "health": 1, "colour": (255, 215, 0)},
                        "pink": {"name": "pink", "speed": 18, "value": 5, "health": 1, "colour": (255, 136, 136)},
                        "black": {"name": "black", "speed": 15, "value": 7, "health": 1, "colour": (0, 0, 0)},
                        "white": {"name": "white", "speed": 15, "value": 7, "health": 1, "colour": (255, 255, 255)},
                        "zebra": {"name": "zebra", "speed": 12, "value": 8, "health": 1, "colour": "zebra"},
                        "purple": {"name": "purple", "speed": 15, "value": 9, "health": 1, "colour": (255, 0, 255)},
                        "lead": {"name": "lead", "speed": 120, "value": 10, "health": 1, "colour": (120, 120, 120)},
                        "rainbow": {"name": "rainbow", "speed": 12, "value": 11, "health": 1, "colour": "rainbow"},
                        "ceramic": {"name": "ceramic", "speed": 9, "value": 12, "health": 8, "colour": (150, 100, 50)},
                        "moab": {"name": "moab", "speed": 120, "value": 13, "health": 200, "colour": "moab"},
                        "bfb": {"name": "bfb", "speed": 150, "value": 14, "health": 700, "colour": "bfb"},
                        "zomg": {"name": "zomg", "speed": 180, "value": 15, "health": 4000, "colour": "zomg"}}

        self.sprites = pygame.sprite.Group()
        for data in reversed(self.enemies.values()):
            LinkedList.add(data)

        self.enemy_list = []
        self.number = 0
        self.count = 0
        self.current = None
        self.initialised = False

    def create(self, data, delay, properties):
        current_node = LinkedList.head
        while current_node.data != data:
            current_node = current_node.next
        current_node.prev = None
        self.enemy_list.append(Enemy(current_node, delay, properties, self.number))
        self.number += 1

    def duplicate(self, original_enemy):
        self.number += 1
        pos = copy.deepcopy(pygame.Vector2(original_enemy.pos.x, original_enemy.pos.y))
        pos.x += random.randint(-1,1) * SCALE
        pos.y += random.randint(-1,1) * SCALE
        path = copy.deepcopy(original_enemy.path)
        current = copy.deepcopy(original_enemy.current)
        distance_travelled = copy.deepcopy(original_enemy.distance_travelled)
        distance_travelled_total = copy.deepcopy(original_enemy.distance_travelled_total)
        dupe_values = {"pos":pos, "path": path, "current": current, "distance_travelled": distance_travelled, "distance_travelled_total": distance_travelled_total}
        properties = copy.deepcopy(original_enemy.properties)
        duplicate = Enemy(original_enemy.node, 0, properties, self.number, dupe_values=dupe_values)
        return duplicate


    def getEnemyStats(self):
        return self.enemies

    def getSpeedState(self):
        return self.speedup

    def speedChange(self):
        speed = 3 if self.speedup else 1 / 3
        self.speedup = not self.speedup
        for info in self.enemies.values():
            info["speed"] = round(info["speed"] * speed)

    def slowDown(self):
        for info in self.enemies.values():
            info["speed"] = info["speed"] * 3

    def move(self, path):
        for enemy in self.sprites:
            if enemy.move(path) == "delete":
                self.kill_list.append(enemy)

    def load(self):
        if self.enemy_list and time.perf_counter() - self.timer > self.enemy_list[0].getSpawnDelay():
            self.timer = time.perf_counter()
            enemy = self.enemy_list.pop(0)
            self.sprites.add(enemy)

    def getKilled(self):
        health = 0
        for enemy in self.kill_list:
            health += enemy.getValue()
            self.kill_list.remove(enemy)
            enemy.kill()
        return health

    def updateEnemies(self, path):
        for enemy in self.sprites:
            if enemy.move(path) == "delete":
                self.kill_list.append(enemy)

            if enemy.dupe:
                for _ in range(enemy.dupe_amount):
                    self.sprites.add(self.duplicate(enemy))
                enemy.setDupe(False)

            if enemy.regen:
                if time.perf_counter() - enemy.regen_timer > 1/(3 if self.speedup else 1):
                    enemy.regen_timer = time.perf_counter()
                    enemy.heal()
    def update(self, layer, Map):
        self.load()
        self.updateEnemies(Map)
        for sprite in sorted(self.sprites, key=lambda sprite: (sprite.value, sprite.number), reverse=True):
            layer.blit(sprite.image, sprite.rect)

    def getEnemies(self):
        return self.enemy_list

    def getSprites(self):
        return self.sprites

    def towersInRange(self, int):
        return None

    def enemiesInRange(self, int):
        return None

    def stun(self, towers_in_range, delta_time):
        return None

    def speedBoost(self, enemies_in_range, delta_time):
        return None