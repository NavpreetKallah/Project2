from builtins import property
import random
import pygame
#, current_round: int, enemy_value: int, enemy_weightings: dict

from game.classes.enemy_class import Enemy

class Round:
    def __init__(self):
        self.spawnList = []
        self.current_round = 0
        self.roundValue = 30 * self.current_round
        self.valueLeft = self.roundValue
        self.enemy_weightings = {"1red":1,
                                 "2blue":2,
                                 "3green":3,
                                 "4yellow":4}
        self.probabilities = [100, 0, 0, 0]
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

    def roundWin(self):
        self.current_round += 1
        self.spawnList = []
        self.valueLeft = self.current_round * 10
        for i in range(1):
            self.increaseDifficulty()
        self.generateEnemies()

    def generateEnemies(self):
        colour = random.choices(list(self.enemy_weightings.keys()), self.probabilities, k=1)[0]
        enemy = self.enemy_weightings[colour]
        if self.valueLeft - enemy >= 0:
            self.valueLeft -= enemy
            self.spawnList.append(Enemy(colour))
            self.generateEnemies()
        else:
            return self.spawnList

    @property
    def getStarted(self):
        return self.round_started

    def startRound(self):
        self.round_started = True
        self.roundWin()
        return self.spawnList
