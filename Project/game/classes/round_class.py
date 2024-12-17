from builtins import property
import random
import pygame

from classes.enemy_class import Enemy
#, current_round: int, enemy_value: int, enemy_weightings: dict


class Round:
    def __init__(self):
        self.current_round = 0
        self.roundValue = 30 * self.current_round
        self.valueLeft = self.roundValue
        self.enemies = {"1red": {"speed": 10, "value": 1, "colour": (255, 0, 0)},
                        "2blue": {"speed": 9, "value": 2, "colour": (0, 0, 255)},
                        "3green": {"speed": 8, "value": 3, "colour": (0, 255, 0)},
                        "4yellow": {"speed": 7, "value": 4, "colour": (255, 215, 0)},
                        "5pink": {"speed": 6, "value": 5, "colour": (255, 136, 136)},
                        "6black": {"speed": 5, "value": 6, "colour": (0, 0, 0)},
                        "7white": {"speed": 4, "value": 7, "colour": (255, 255, 255)},
                        "8purple": {"speed": 3, "value": 8, "colour": (255, 0, 255)},
                        "9lead": {"speed": 2, "value": 9, "colour": (120, 120, 120)},
                        "10zebra": {"speed": 1, "value": 10, "colour": (0, 0, 0)}}
        self.enemy_creator = {"1red":{"weight":1,"min_delay":0.02,"max_delay":0.3},
                              "2blue": {"weight": 2, "min_delay": 1, "max_delay": 2},
                              "3green": {"weight": 3, "min_delay": 2, "max_delay": 3},
                              "4yellow": {"weight": 4, "min_delay": 3, "max_delay": 4},
                              "5pink": {"weight": 1, "min_delay": 4, "max_delay": 5},
                              "6black": {"weight": 1, "min_delay": 5, "max_delay": 6},
                              "7white": {"weight": 1, "min_delay": 6, "max_delay": 7},
                              "8purple": {"weight": 1, "min_delay": 7, "max_delay": 8},
                              "9lead": {"weight": 1, "min_delay": 8, "max_delay": 9},
                              "10zebra": {"weight": 1, "min_delay": 0, "max_delay": 1}
                              }

        self.probabilities = [100, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.round_started = False
        self.weighting = [-20,18,2]
        self.base_probabilities = [100,0,0]

    def increaseDifficulty(self):

        rangeStop = min(3, len(self.probabilities))

        for i in range(rangeStop):
            self.probabilities[i] += self.weighting[i]

        if self.probabilities[0] == 0:
            self.probabilities.pop(0)
            del self.enemy_creator[list(self.enemy_creator.keys())[0]]
            rangeStop = min(3, len(self.probabilities))

            if rangeStop == 2:
                self.base_probabilities = [100, 0]
                self.weighting = [-10, 10]

            if rangeStop == 1:
                self.base_probabilities = [100]
                self.weighting = [0]

            for i in range(rangeStop):
                self.probabilities[i] = self.base_probabilities[i]

    def roundWin(self, manager):
        for _ in range(1):
            self.current_round += 1
            self.valueLeft = self.current_round * 10
            self.increaseDifficulty()
        self.generateEnemies(manager)

    def generateEnemies(self, manager):
        colour = random.choices(list(self.enemy_creator.keys()), self.probabilities, k=1)[0]
        enemy = self.enemy_creator[colour]["weight"]
        if self.valueLeft - enemy >= 0:
            self.valueLeft -= enemy
            manager.create(self.enemies[colour],self.generateDelay(colour))
            self.generateEnemies(manager)

    def generateDelay(self, colour):
        print(random.uniform(self.enemy_creator[colour]["min_delay"],self.enemy_creator[colour]["max_delay"]))
        #return random.uniform(self.enemy_creator[colour]["min_delay"],self.enemy_creator[colour]["max_delay"])
        return 0.1

    @property
    def getStarted(self):
        return self.round_started

    def startRound(self, manager):
        self.round_started = True
        self.roundWin(manager)
