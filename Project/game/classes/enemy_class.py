import time

import pygame
import random
from game.classes.linked_list import LinkedList
from game.config import SCALE

# , rect: pygame.Vector2, angle: int, state: str, frame: int, range: int,
#                  distance_travelled: int, health: int, immunities: list, speed: int, value: int,
LinkedList = LinkedList()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, node, spawn_delay, enemy_number, pos=None, count=0, path=None):
        pygame.sprite.Sprite.__init__(self)
        self.spawn_delay = spawn_delay
        self.node = node
        data = self.node.data
        self.number = enemy_number
        self.speed = data["speed"]
        self.value = data["value"]
        self.colour = data["colour"]
        self.health = data["health"]
        self.initialised = False
        self.count = count
        if path:
            self.path = path
        if not pos:
            self.pos = pygame.Vector2(SCALE * (12 + [-1,0,1,0][enemy_number%4]), SCALE * (-5- [0,1][enemy_number%2]))
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
            if self.current == "U":
                self.pos.y -= distance_moved
            if self.current == "L":
                self.pos.x -= distance_moved
            if self.current == "R":
                self.pos.x += distance_moved
            self.rect.topleft = (self.pos.x, self.pos.y)
        self.count -= 1

    def colourIn(self):
        image = pygame.Surface((5 * SCALE, 6 * SCALE), pygame.SRCALPHA)
        image.fill((0,0,0),(0,SCALE,5*SCALE,3*SCALE))
        image.fill((0,0,0),(SCALE,0,3*SCALE,5*SCALE))
        image.fill((0,0,0),(2*SCALE,SCALE*5,SCALE,SCALE))
        image.fill(self.colour,(SCALE,SCALE,3*SCALE,3*SCALE))
        image.fill(self.colour,(2*SCALE,SCALE*4,SCALE,SCALE))
        return image

    def take_damage(self, damage):
        money = 0
        for _ in range(damage):
            self.health -= 1
            if self.health == 0:
                money += 1
                if not self.node.next:
                    self.kill()
                    return money
                self.node = self.node.next
                data = self.node.data
                self.speed = data["speed"]
                self.value = data["value"]
                self.colour = data["colour"]
                self.health = data["health"]
                self.image = self.colourIn()
        return money

    def getValue(self):
        return self.value

    def getSpawnDelay(self):
        return self.spawn_delay

    #
    # def draw(self, layer):
    #     pygame.draw.rect(layer, self.colour, (self.rect.x, self.rect.y, 5 * SCALE, 5 * SCALE))


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
        self.enemies = {"1red": {"speed": 30, "value": 1, "health": 1, "colour": (255, 0, 0)},
                        "2blue": {"speed": 27, "value": 2,"health": 2, "colour": (0, 0, 255)},
                        "3green": {"speed": 24, "value": 3, "health": 3,"colour": (0, 255, 0)},
                        "4yellow": {"speed": 21, "value": 4, "health": 4,"colour": (255, 215, 0)},
                        "5pink": {"speed": 18, "value": 5, "health": 5,"colour": (255, 136, 136)},
                        "6black": {"speed": 15, "value": 7, "health": 6,"colour": (0, 0, 0)},
                        "7white": {"speed": 15, "value": 7, "health": 7,"colour": (255, 255, 255)},
                        "8purple": {"speed": 15, "value": 8, "health": 8,"colour": (255, 0, 255)},
                        "9lead": {"speed": 18, "value": 10, "health": 9,"colour": (120, 120, 120)},
                        "10ceramic": {"speed": 12, "value": 20, "health": 10,"colour": (0, 0, 0)}}

        self.sprites = pygame.sprite.Group()

        for data in reversed(self.enemies.values()):
            LinkedList.add(data)

        self.enemy_list = []
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
    def update(self, layer, Map):

        self.load()
        self.move(Map)
        # self.draw(layer)
        for sprite in sorted(self.sprites, key=lambda sprite: (sprite.speed, sprite.number), reverse=True):
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
