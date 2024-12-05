from builtins import int, list, super, str
import pygame

from game.classes.entity_class import Entity
from game.classes.linked_list import LinkedList
from game.config import SCALE

# , position: pygame.Vector2, angle: int, state: str, frame: int, range: int,
#                  distance_travelled: int, health: int, immunities: list, speed: int, value: int,
LinkedList = LinkedList()
class Enemy:
    def __init__(self, node):
        data = node.data
        self.speed = data["speed"]
        self.value = data["value"]
        self.colour = data["colour"]
        self.count = 0
        self.position = pygame.Vector2(SCALE*12,SCALE*-5)

class EnemyManager():
    def __init__(self):
        # super().__init__(position, angle, state, frame, range)
        # self.distance_travelled = distance_travelled
        # self.health = health
        # self.immunities = immunities
        # self.value = value
        self.enemies = {"1red": {"speed": 10, "value": 1, "colour": (255, 0, 0)},
                        "2blue": {"speed": 9, "value": 2, "colour": (0, 0, 255)},
                        "3green": {"speed": 8, "value": 3, "colour": (0, 255, 0)},
                        "4yellow": {"speed": 7, "value": 4, "colour": (255, 255, 0)},
                        "5pink": {"speed": 6, "value": 5, "colour": (255, 136, 136)},
                        "6black": {"speed": 5, "value": 6, "colour": (0, 0, 0)},
                        "7white": {"speed": 4, "value": 7, "colour": (255, 255, 255)},
                        "8purple": {"speed": 3, "value": 8, "colour": (255, 0, 255)},
                        "9lead": {"speed": 2, "value": 9, "colour": (120, 120, 120)},
                        "10zebra": {"speed": 1, "value": 10, "colour": (0, 0, 0)}}





        for data in self.enemies.values():
            LinkedList.add(data)
        # self.type = type
        # self.speed = self.enemies[type]["speed"]
        # self.value = self.enemies[type]["value"]
        # self.colour = self.enemies[type]["colour"]
        self.enemy_list = []
        self.count = 0
        self.current = None
        self.initialised = False
        # self.position = pygame.Vector2(SCALE*12,SCALE*-5)

    def create(self, type):
        current_node = LinkedList.head
        while current_node.data != type:
            current_node = current_node.next

        self.enemy_list.append(Enemy(current_node))

    def move(self, direction, layer):
        distance = 9 * SCALE
        distance_moved = (distance/self.speed)
        if not self.initialised:
            self.initialised = True
            self.path = direction

        if len(self.path) == 0:
            return "delete"

        if self.count == 0:
            self.current = self.path.pop(0)
            self.count = self.speed

        if self.count > 0:
            if self.current == "D":
                self.position.y += distance_moved
            if self.current == "U":
                self.position.y -= distance_moved
            if self.current == "L":
                self.position.x -= distance_moved
            if self.current == "R":
                self.position.x += distance_moved
        self.count -= 1

    def draw(self, layer):
        pygame.draw.rect(layer, (self.colour), pygame.Rect(self.position.x, self.position.y, SCALE * 5, SCALE * 5))


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
