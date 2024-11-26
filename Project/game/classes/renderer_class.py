from builtins import dict, list, int

import pygame

#layers_to_update: list, top_surface: pygame.Surface

class Renderer:
    def __init__(self, width: int, height: int):
        DIMENSIONS = (width, height)
        self.layers = {
            "map": pygame.Surface(DIMENSIONS, pygame.SRCALPHA),
            "menu": pygame.Surface(DIMENSIONS, pygame.SRCALPHA),
            #"entities":pygame.Surface(DIMENSIONS, pygame.SRCALPHA),
            "HUD": pygame.Surface(DIMENSIONS, pygame.SRCALPHA),
            "enemy": pygame.Surface(DIMENSIONS, pygame.SRCALPHA)
        }

    def getLayer(self, layer):
        return self.layers[layer]

    def getLayers(self):
        layers = []
        if "map" in self.layers:
            layers.append(self.layers["map"])
        if "menu" in self.layers:
            layers.append(self.layers["menu"])
        if "enemy" in self.layers:
            layers.append(self.layers["enemy"])
        if "HUD" in self.layers:
            layers.append(self.layers["HUD"])
        return layers

    def updateLayer(self, new_layer, old_layer):
        self.layers[old_layer] = new_layer

    def drawLayers(self):
        return None

    def clearLayer(self, layer):
        self.layers[layer].fill(pygame.Color(0,0,0,0))

    def clearLayers(self):
        for key in self.layers:
            self.layers[key].fill(pygame.Color(0, 0, 0, 0))

    def deleteLayer(self, layer):
        del(self.layers[layer])