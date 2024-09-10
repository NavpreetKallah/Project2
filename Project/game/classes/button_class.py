from builtins import int

import pygame
import sys

class Button:
    def __init__(self, position: pygame.Vector2, width: int, height: int, border_width: int, border_colour: int, image: pygame.Surface):
        self.position = position
        self.width = width
        self.height = height
        self.borderWidth = border_width
        self.borderColour = border_colour
        self.image = image

    def onClick(self, delta_time):
        return None
