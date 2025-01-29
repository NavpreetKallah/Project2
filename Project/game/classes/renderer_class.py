import pygame
from typing import List, Dict


class Renderer:
    def __init__(self, width: int, height: int) -> None:
        DIMENSIONS = (width, height)
        self.layers: Dict[str, pygame.Surface] = {
            "map": pygame.Surface(DIMENSIONS, pygame.SRCALPHA),
            "menu": pygame.Surface(DIMENSIONS, pygame.SRCALPHA),
            "tower": pygame.Surface(DIMENSIONS, pygame.SRCALPHA),
            "HUD": pygame.Surface(DIMENSIONS, pygame.SRCALPHA),
            "enemy": pygame.Surface(DIMENSIONS, pygame.SRCALPHA),
            "projectile": pygame.Surface(DIMENSIONS, pygame.SRCALPHA)
        }

    def getLayer(self, layer: str) -> pygame.Surface:
        return self.layers[layer]

    def getLayers(self) -> List[pygame.Surface]:
        layers: List[pygame.Surface] = []
        if "map" in self.layers:
            layers.append(self.layers["map"])
        if "enemy" in self.layers:
            layers.append(self.layers["enemy"])
        if "tower" in self.layers:
            layers.append(self.layers["tower"])
        if "projectile" in self.layers:
            layers.append(self.layers["projectile"])
        if "HUD" in self.layers:
            layers.append(self.layers["HUD"])
        if "menu" in self.layers:
            layers.append(self.layers["menu"])
        return layers

    def updateLayer(self, new_layer: pygame.Surface, old_layer: str) -> None:
        self.layers[old_layer] = new_layer

    def drawLayers(self) -> None:
        return None

    def clearLayer(self, layer: str) -> None:
        self.layers[layer].fill(pygame.Color(0, 0, 0, 0))

    def clearLayers(self) -> None:
        for key in self.layers:
            self.layers[key].fill(pygame.Color(0, 0, 0, 0))

    def deleteLayer(self, layer: str) -> None:
        del (self.layers[layer])
