import pygame


class Round:
    def __init__(self, current_round: int, enemy_value: int, enemy_weightings: dict):
        self.current_round = current_round
        self.enemy_value = enemy_value
        self.enemy_weightings = enemy_weightings

    def increaseDifficulty(self):
        return None
