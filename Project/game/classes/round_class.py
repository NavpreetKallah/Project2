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
        self.enemies = None
        self.enemy_creator = {"1red":{"weight":1,"min_delay":0.3,"max_delay":0.6},
                              "2blue": {"weight": 2, "min_delay": 0.26, "max_delay": 0.72},
                              "3green": {"weight": 3, "min_delay": 0.42, "max_delay": 0.84},
                              "4yellow": {"weight": 4, "min_delay": 0.48, "max_delay": 0.96},
                              "5pink": {"weight": 5, "min_delay": 0.54, "max_delay": 1.08},
                              "6black": {"weight": 6, "min_delay": 0.6, "max_delay": 1.2},
                              "7white": {"weight": 7, "min_delay": 0.66, "max_delay": 1.32},
                              "8purple": {"weight": 8, "min_delay": 0.72, "max_delay": 1.44},
                              "9lead": {"weight": 9, "min_delay": 0.78, "max_delay": 1.56},
                              "10zebra": {"weight": 10, "min_delay": 0.84, "max_delay": 1.68}
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
        return random.uniform(self.enemy_creator[colour]["min_delay"],self.enemy_creator[colour]["max_delay"])
        #return 0.1

    @property
    def getStarted(self):
        return self.round_started

    def startRound(self, manager):
        self.enemies = manager.getEnemyStats()
        self.round_started = True
        self.roundWin(manager)
