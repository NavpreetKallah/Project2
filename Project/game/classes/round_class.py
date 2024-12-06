from builtins import property
import random
import pygame

from classes.enemy_class import Enemy
#, current_round: int, enemy_value: int, enemy_weightings: dict

from game.classes.enemy_class import EnemyManager
EnemyManager = EnemyManager()

class Round:
    def __init__(self):
        self.current_round = 0
        self.roundValue = 30 * self.current_round
        self.valueLeft = self.roundValue
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
        self.enemy_weightings = {"1red":1,
                                 "2blue":2,
                                 "3green":3,
                                 "4yellow":4,
                                 "5pink": 5,
                                "6black":6,
                                "7white": 7,
                                "8purple": 8,
                                "9lead": 9,
                                "10zebra": 10}
        self.probabilities = [100, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.round_started = False
        self.weighting = [-10,9,1]
        self.base_probabilities = [90,9,1]

    def increaseDifficulty(self):

        rangeStop = min(3, len(self.probabilities))

        for i in range(rangeStop):
            self.probabilities[i] += self.weighting[i]

        if self.probabilities[0] == 0:
            self.probabilities.pop(0)
            del self.enemy_weightings[list(self.enemy_weightings.keys())[0]]
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
        self.current_round += 1
        self.valueLeft = self.current_round * 10
        for i in range(1):
            self.increaseDifficulty()
        self.generateEnemies(manager)

    def generateEnemies(self, manager):
        colour = random.choices(list(self.enemy_weightings.keys()), self.probabilities, k=1)[0]
        enemy = self.enemy_weightings[colour]
        if self.valueLeft - enemy >= 0:
            self.valueLeft -= enemy
            manager.create(self.enemies[colour])
            self.generateEnemies(manager)

    @property
    def getStarted(self):
        return self.round_started

    def startRound(self, manager):
        self.round_started = True
        self.roundWin(manager)
