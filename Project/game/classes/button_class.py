from builtins import int

import pygame


class Button:
    def __init__(self, position: pygame.Vector2, width: int, height: int, border_width: int, border_colour: int,
                 image: pygame.Surface):
        self.position = position
        self.width = width
        self.height = height
        self.border_width = border_width
        self.border_colour = border_colour
        self.image = image

    def onClick(self, delta_time):
        return None
