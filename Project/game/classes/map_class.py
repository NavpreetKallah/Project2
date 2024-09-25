from builtins import tuple, list, int, range
import pygame

#current_map_path: list, current_map_start: tuple, current_map_end: tuple, current_map_textures: list, path_length: int
class Map:
    def __init__(self):
        # self.current_map_path = current_map_path
        # self.current_map_start = current_map_start
        # self.current_map_end = current_map_end
        # self.current_map_textures = current_map_textures
        # self.path_length = path_length
        pass

    def getCoordinate(self,x ,y):
        return None

    def drawMap(self, map_layer):
        tile = pygame.image.load_extended("//BA-SRV-FS-01/18nkallah$/Computer Science/Project/textures/tile.png")
        for i in range(13):
            for j in range(12):
                map_layer.blit(tile, ((i*10)+1, (j*10)+1))
        return map_layer

