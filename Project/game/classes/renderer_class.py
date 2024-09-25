from builtins import dict, list, int

import pygame

#layers_to_update: list, top_surface: pygame.Surface

class Renderer:
    def __init__(self, WIDTH: int, HEIGHT: int):
        self.layers = {
            "map":pygame.Surface((WIDTH,HEIGHT))
            #"path":pygame.Surface((WIDTH,HEIGHT)),
            #"entities":pygame.Surface((WIDTH,HEIGHT)),
            #"HUD":pygame.Surface((WIDTH,HEIGHT))
        }

    def getLayer(self, layer):
        return self.layers[layer]

    def getLayers(self):
        return self.layers.values()

    def updateLayer(self, new_layer, old_layer):
        self.layers[old_layer] = new_layer

    def drawLayers(self):
        return None