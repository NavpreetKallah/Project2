from builtins import dict, list, int

import pygame

#layers_to_update: list, top_surface: pygame.Surface

class Renderer:
    def __init__(self, width: int, height: int):
        DIMENSIONS = (width, height)
        self.layers = {
            "map":pygame.Surface(DIMENSIONS),
            "menu":pygame.Surface(DIMENSIONS)
            #"path":pygame.Surface(DIMENSIONS),
            #"entities":pygame.Surface(DIMENSIONS),
            #"HUD":pygame.Surface(DIMENSIONS)
        }

    def getLayer(self, layer):
        return self.layers[layer]

    def getLayers(self):
        return self.layers.values()

    def updateLayer(self, new_layer, old_layer):
        self.layers[old_layer] = new_layer

    def drawLayers(self):
        return None

    def clearLayer(self, layer):
        self.layers[layer].fill(pygame.Color(0,0,0,0))

    def clearLayers(self):
        for key in self.layers:
            self.layers[key].fill(pygame.Color(0, 0, 0))

    def deleteLayer(self, layer):
        del(self.layers[layer])