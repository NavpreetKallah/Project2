from builtins import int, str

import pygame


class Entity:
    def __init__(self, position: pygame.Vector2, angle: int, state: str, frame: int, range: int):
        self.position = position
        self.angle = angle
        self.state = state
        self.frame = frame
        self.range = range

    def stateChange(self, new_state):
        return None

    def debuff(self, delta_time):
        return None

