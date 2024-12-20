from builtins import int, list, super, str
import time
import pygame

from game.classes.entity_class import Entity
from game.classes.linked_list import LinkedList
from game.config import SCALE

# , rect: pygame.Vector2, angle: int, state: str, frame: int, range: int,
#                  distance_travelled: int, health: int, immunities: list, speed: int, value: int,
LinkedList = LinkedList()
class Enemy(pygame.sprite.Sprite):
    def __init__(self, node, spawn_delay):
        pygame.sprite.Sprite.__init__(self)
        self.spawn_delay = spawn_delay
        self.node = node
        data = self.node.data
        self.speed = data["speed"]
        self.value = data["value"]
        self.colour = data["colour"]
        self.initialised = False
        self.count = 0
        self.pos = pygame.Vector2(SCALE*12, SCALE*-5)
        # self.rect = pygame.rect.Rect((self.pos.x, self.pos.y, 5*SCALE,5*SCALE))
        self.image = pygame.Surface((5*SCALE, 5*SCALE))
        self.image.fill(self.colour)
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

    def take_damage(self, damage):
        for _ in range(damage):
            if not self.node.next:
                return "delete"
            self.node = self.node.next
        data = self.node.data
        self.speed = data["speed"]
        self.value = data["value"]
        self.colour = data["colour"]
        self.image.fill(self.colour)

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
        self.enemies = {"1red": {"speed": 30, "value": 1, "colour": (255, 0, 0)},
                        "2blue": {"speed": 27, "value": 2, "colour": (0, 0, 255)},
                        "3green": {"speed": 24, "value": 3, "colour": (0, 255, 0)},
                        "4yellow": {"speed": 21, "value": 4, "colour": (255, 215, 0)},
                        "5pink": {"speed": 18, "value": 5, "colour": (255, 136, 136)},
                        "6black": {"speed": 15, "value": 6, "colour": (0, 0, 0)},
                        "7white": {"speed": 12, "value": 7, "colour": (255, 255, 255)},
                        "8purple": {"speed": 9, "value": 8, "colour": (255, 0, 255)},
                        "9lead": {"speed": 6, "value": 9, "colour": (120, 120, 120)},
                        "10zebra": {"speed": 3, "value": 10, "colour": (0, 0, 0)}}

        self.sprites = pygame.sprite.Group()

        for data in reversed(self.enemies.values()):
            LinkedList.add(data)

        self.enemy_list = []
        # self.spawn_list = []
        self.count = 0
        self.current = None
        self.initialised = False

    def create(self, data, delay):
        current_node = LinkedList.head
        while current_node.data != data:
            current_node = current_node.next
        self.enemy_list.append(Enemy(current_node,delay))

    def getEnemyStats(self):
        return self.enemies

    def getSpeedState(self):
        return self.speedup

    def speedChange(self):
        speed = 3 if self.speedup else 1/3
        self.speedup = not self.speedup
        for info in self.enemies.values():
            info["speed"] = round(info["speed"]*speed)

    def slowDown(self):
        for info in self.enemies.values():
            info["speed"] = info["speed"]*3

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

    def update(self, layer, Map):

        self.load()
        self.move(Map)
        # self.draw(layer)
        self.sprites.draw(layer)

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
