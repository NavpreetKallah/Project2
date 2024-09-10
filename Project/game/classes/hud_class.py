from builtins import round

import pygame


class Hud:
    def __init__(self, lives: int, cash: int, round_number: int, total_rounds: int):
        self.lives = lives
        self.cash = cash
        self.round_number = round_number
        self.total_rounds = total_rounds
