import time
import copy

import pygame
import random
from game.classes.linked_list import LinkedList
from game.config import SCALE

# , rect: pygame.Vector2, angle: int, state: str, frame: int, range: int,
#                  distance_travelled: int, health: int, immunities: list, speed: int, value: int,
LinkedList = LinkedList()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, node, spawn_delay, enemy_number, pos=None, count=0, path=None, current=None, initialised=False):
        pygame.sprite.Sprite.__init__(self)
        self.spawn_delay = spawn_delay
        self.node = node
        data = self.node.data
        self.number = enemy_number
        self.dupe = False
        self.frozen = False
        self.camo = False
        self.name = data["name"]
        self.speed = data["speed"]
        self.value = data["value"]
        self.colour = data["colour"]
        self.health = data["health"]
        self.initialised = initialised
        self.count = count
        if current:
            self.current = current
        self.path = path
        if not pos:
            self.pos = pygame.Vector2(SCALE * (12 + [-1, 0, 1, 0][enemy_number % 4]),
                                      SCALE * (-5 - [0, 1][enemy_number % 2]))
        else:
            self.pos = pos
        self.image = self.colourIn()
        # self.rect = pygame.rect.Rect((self.pos.x, self.pos.y, 5*SCALE,5*SCALE))
        # self.image.fill((0,0,0),(SCALE,SCALE,1*SCALE,1*SCALE))
        # self.image.fill((0,0,0),(3*SCALE,SCALE,1*SCALE,1*SCALE))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.pos.x, self.pos.y)

    def move(self, direction):
        distance = 9 * SCALE
        distance_moved = (distance / self.speed)
        if not self.initialised:
            self.initialised = True
            self.path = direction

        if len(self.path) == 0:
            return "delete"

        if self.count == 0:
            self.current = self.path.pop(0)
            self.count = self.speed

        if self.count > 0:
            # I can not update the rect position directly here as it will round the value of distance moved causing the enemies to not follow the path
            if self.current == "D":
                self.pos.y += distance_moved
            elif self.current == "U":
                self.pos.y -= distance_moved
            elif self.current == "L":
                self.pos.x -= distance_moved
            elif self.current == "R":
                self.pos.x += distance_moved
            self.rect.topleft = (self.pos.x, self.pos.y)
        self.count -= 1

    def colourIn(self):
        image = pygame.Surface((5 * SCALE, 6 * SCALE), pygame.SRCALPHA)
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
            image.fill((255,255,255), (SCALE, SCALE, 3 * SCALE, 3 * SCALE))
            image.fill((255,255,255), (2 * SCALE, SCALE * 4, SCALE, SCALE))
            image.fill((0,0,0), (2*SCALE,SCALE,SCALE,SCALE))
            image.fill((0,0,0), (SCALE,2*SCALE,SCALE,SCALE))
            image.fill((0,0,0), (3*SCALE,2*SCALE,SCALE,SCALE))
            image.fill((0,0,0), (2*SCALE,3*SCALE,SCALE,SCALE))
            return image
        else:
            image.fill(self.colour, (SCALE, SCALE, 3 * SCALE, 3 * SCALE))
            image.fill(self.colour, (2 * SCALE, SCALE * 4, SCALE, SCALE))
            return image

    def take_damage(self, damage, targets, camo):
        money = 0
        if self.name in targets or (self.frozen and "frozen" in targets) or (self.camo and not camo):
            return 0
        for _ in range(damage):
            self.health -= 1
            if self.health == 0:
                money += 1
                if not self.node.next:
                    self.kill()
                    return money

                self.new_node()

        return money

    def new_node(self):
        self.children()
        self.node = self.node.next if self.name != "rainbow" else self.node.next.next.next
        data = self.node.data
        self.name = data["name"]
        self.speed = data["speed"]
        self.value = data["value"]
        self.colour = data["colour"]
        self.health = data["health"]
        self.image = self.colourIn()

    def getValue(self):
        return self.value

    def children(self):
        if self.name in ["rainbow", "zebra","ceramic","moab","bfb","zomg"]:
            self.duper = copy.deepcopy(self.name)
            self.dupe = True
            self.dupe_amount = 1 if self.name in ["rainbow", "zebra","ceramic"] else 3

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
                        "blue": {"name": "blue", "speed": 27, "value": 2, "health": 1, "colour": (0, 0, 255)},
                        "green": {"name": "green", "speed": 24, "value": 3, "health": 1, "colour": (0, 255, 0)},
                        "yellow": {"name": "yellow", "speed": 21, "value": 4, "health": 1, "colour": (255, 215, 0)},
                        "pink": {"name": "pink", "speed": 18, "value": 5, "health": 1, "colour": (255, 136, 136)},
                        "black": {"name": "black", "speed": 15, "value": 7, "health": 1, "colour": (0, 0, 0)},
                        "white": {"name": "white", "speed": 15, "value": 7, "health": 1, "colour": (255, 255, 255)},
                        "zebra": {"name": "zebra", "speed": 15, "value": 8, "health": 1, "colour": "zebra"},
                        "purple": {"name": "purple", "speed": 15, "value": 9, "health": 1, "colour": (255, 0, 255)},
                        "lead": {"name": "lead", "speed": 120, "value": 10, "health": 1, "colour": (120, 120, 120)},
                        "rainbow": {"name": "rainbow", "speed": 12, "value": 11, "health": 1, "colour": "rainbow"},
                        "ceramic": {"name": "ceramic", "speed": 120, "value": 12, "health": 200, "colour": (0, 0, 0)},
                        "moab": {"name": "moab", "speed": 120, "value": 12, "health": 200, "colour": "moab"},
                        "bfb": {"name": "bfb", "speed": 120, "value": 13, "health": 700, "colour": "bfb"},
                        "zomg": {"name": "zomg", "speed": 168, "value": 14, "health": 4000, "colour": "zomg"}}

        self.sprites = pygame.sprite.Group()
        self.duped_sprites = pygame.sprite.Group()
        for data in reversed(self.enemies.values()):
            LinkedList.add(data)

        self.enemy_list = []

        self.duped_list = []
        # self.spawn_list = []
        self.number = 0
        self.count = 0
        self.current = None
        self.initialised = False

    def create(self, data, delay):
        current_node = LinkedList.head
        while current_node.data != data:
            current_node = current_node.next
        self.enemy_list.append(Enemy(current_node, delay, self.number))
        self.number += 1

    def duplicate(self, original_enemy):
        self.number += 1
        pos = copy.deepcopy(pygame.Vector2(original_enemy.pos.x, original_enemy.pos.y))
        pos.x += [-1, 1][self.number % 2] * SCALE
        pos.y += [-1, 1][self.number % 2] * SCALE
        path = copy.deepcopy(original_enemy.path)
        count = copy.deepcopy(original_enemy.count)
        current = copy.deepcopy(original_enemy.current)
        duplicate = Enemy(original_enemy.node, 0, self.number, pos=pos, count=count, path=path, current=current, initialised=True)
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
    # def draw(self, layer):
    #     for enemy in self.spawn_list:
    #         enemy.draw(layer)

    def load(self):
        if self.enemy_list and time.perf_counter() - self.timer > self.enemy_list[0].getSpawnDelay():
            self.timer = time.perf_counter()
            enemy = self.enemy_list.pop(0)
            # self.spawn_list.append(enemy)
            self.sprites.add(enemy)

    def getKilled(self):
        health = 0
        for enemy in self.kill_list:
            health += enemy.getValue()
            self.kill_list.remove(enemy)
            enemy.kill()
        return health

    def bySpeed(self, sprite):
        return sprite.speed

    def dupe(self):
        for sprite in self.sprites:
            if sprite.dupe:
                for i in range(sprite.dupe_amount):
                    if sprite.duper == "rainbow":
                        duplicate = self.duplicate(sprite)
                        print(duplicate.name)
                        self.sprites.add(duplicate)
                sprite.setDupe(False)

    def update(self, layer, Map):
        self.load()
        self.move(Map)
        self.dupe()
        for sprite in sorted(self.sprites, key=lambda sprite: (sprite.value, sprite.number), reverse=True):
            layer.blit(sprite.image, sprite.rect)

    def getEnemies(self):
        return self.enemy_list

    # def getSpawnedEnemies(self):
    #     return self.spawn_list

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

    def regenerate(self, delta_time):
        return None

    def damage(self, health):
        return None
