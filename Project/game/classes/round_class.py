import random
import os
from builtins import property


# , current_round: int, enemy_value: int, enemy_weightings: dict
class Round:
    def __init__(self):
        self.current_round = 0
        self.roundValue = 30 * self.current_round
        self.valueLeft = self.roundValue
        self.enemies = None
        min_delay = 0.1
        change = 0.01
        max_delay = 0.2
        self.enemy_creator = {"red": {"cost": 1, "weight":1, "min_delay": min_delay + change*9, "max_delay": max_delay + change*9},
                              "blue": {"cost": 2, "weight":2, "min_delay": min_delay + change*8, "max_delay": max_delay + change*8},
                              "green": {"cost": 3, "weight":6, "min_delay": min_delay + change*7, "max_delay": max_delay + change*7},
                              "yellow": {"cost": 4, "weight":12, "min_delay": min_delay + change*6, "max_delay": max_delay + change*6},
                              "pink": {"cost": 5, "weight":24, "min_delay": min_delay + change*5, "max_delay": max_delay + change*5},
                              "black": {"cost": 6, "weight":48, "min_delay": min_delay + change*4, "max_delay": max_delay + change*4},
                              "white": {"cost": 6, "weight":48, "min_delay": min_delay + change*3, "max_delay": max_delay + change*3},
                              "zebra": {"cost": 15, "weight":96, "min_delay": min_delay + change*1, "max_delay": max_delay + change*1},
                              "purple": {"cost": 16, "weight":96, "min_delay": min_delay + change*2, "max_delay": max_delay + change*2},
                              "lead": {"cost": 20, "weight":48, "min_delay": min_delay + change*1, "max_delay": max_delay + change*1},
                              "rainbow": {"cost": 30, "weight":96, "min_delay": min_delay + change*1, "max_delay": max_delay + change*1},
                              "ceramic": {"cost": 60, "weight":200, "min_delay": min_delay, "max_delay": max_delay},
                              "moab": {"cost": 240, "weight":40, "min_delay": min_delay, "max_delay": max_delay},
                              "bfb": {"cost": 500, "weight":40, "min_delay": min_delay, "max_delay": max_delay},
                              "zomg": {"cost": 2000, "weight":20, "min_delay": min_delay, "max_delay": max_delay},
                              }

        self.enemy_spawn_rounds = [1,2,6,11,15,20,22,25,26,28,35,38,40,60,80]
        self.round_started = False
        self.speedup = False

    def getCurrent(self):
        return self.current_round

    def speedChange(self):
        speed = 3 if self.speedup else 1 / 3
        self.speedup = not self.speedup
        for info in self.enemy_creator.values():
            info["min_delay"] = info["min_delay"] * speed
            info["max_delay"] = info["max_delay"] * speed

    def calculateValue(self):
        if self.current_round < 40:
            return 35
        elif self.current_round < 60:
            return 70
        elif self.current_round < 70:
            return 100
        elif self.current_round < 80:
            return 250
        elif self.current_round < 100:
            return 500
        else:
            return 2000

    def roundWin(self, manager):
        for _ in range(150):
            self.current_round += 1
            self.increaseDifficulty()
            self.valueLeft = self.current_round * self.calculateValue()
        self.generateEnemies(manager)

    def increaseDifficulty(self):
        max_enemies = len([i for i in self.enemy_spawn_rounds if i <= self.current_round])
        enemy_names = list(self.enemy_creator.keys())[:max_enemies]
        self.enemy_creator[enemy_names[-1]]["weight"] *= 1.1

    def calculateProbabilities(self, value):
        max_enemies = len([i for i in self.enemy_spawn_rounds if i <= self.current_round])
        enemy_data = list(self.enemy_creator.values())[:max_enemies+value]
        enemy_names = list(self.enemy_creator.keys())[:max_enemies+value]
        total_weight = 0
        for enemy in enemy_data:
            total_weight += enemy["weight"]
        probabilities = [data["weight"] / total_weight for data in enemy_data]
        return random.choices(list(enemy_names), probabilities, k=1)[0]

    def generateEnemies(self, manager):
        for i in range(0,-len([i for i in self.enemy_spawn_rounds if i <= self.current_round]),-1):
            colour = self.calculateProbabilities(i)
            enemy = self.enemy_creator[colour]["cost"]
            if self.valueLeft - enemy >= 0:
                self.valueLeft -= enemy
                manager.create(self.enemies[colour], self.generateDelay(colour), self.generateProperties(colour), self.current_round)
                self.generateEnemies(manager)
                break

    def generateDelay(self, colour):
        return random.uniform(self.enemy_creator[colour]["min_delay"], self.enemy_creator[colour]["max_delay"])
        # return 0.1

    def generateProperties(self, colour):
        properties = {"camo": False, "regen": False}
        if colour not in ["moab","bfb","zomg"]:
            if self.current_round >= 24:
                if random.randint(self.current_round,max(75,self.current_round)) == max(75,self.current_round):
                    properties["camo"] = True
            if self.current_round >= 17:
                if random.randint(self.current_round,max(75,self.current_round)) == max(75,self.current_round):
                    properties["regen"] = True
        return properties
    @property
    def getStarted(self):
        return self.round_started

    def startRound(self, manager):
        self.enemies = manager.getEnemyStats()
        self.round_started = True
        self.roundWin(manager)
