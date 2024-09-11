from builtins import dict, list

import pygame


class Renderer:
    def __init__(self, layers: dict, layers_to_update: list, top_surface: pygame.Surface):
        self.layers = layers
        self.layers_to_update = layers_to_update
        self.top_surface = top_surface

    def updateLayer(self):
        return None

    def drawLayers(self):
        return None