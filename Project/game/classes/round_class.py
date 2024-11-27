from builtins import property

import pygame
#, current_round: int, enemy_value: int, enemy_weightings: dict

class Round:
    def __init__(self):
        self.current_round = 0
        self.enemy_value = 30 * self.current_round
        self.enemy_weightings = None
        self.round_started = False

    def increaseDifficulty(self):
        return None

    def generateEnemies(self):
        return None

    @property
    def getStarted(self):
        return self.round_started

    def startRound(self):
        self.round_started = True
