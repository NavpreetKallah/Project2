import pygame
import sys

class Button:
    def __init__(self, position: pygame.Vector2, width: int, height: int, borderWidth: int, borderColour: int, image: pygame.Surface):
        self.position = position
        self.width = width
        self.height = height
        self.borderWidth = borderWidth
        self.borderColour = borderColour
        self.image = image

    def onClick(self, deltaTime):
        return None
