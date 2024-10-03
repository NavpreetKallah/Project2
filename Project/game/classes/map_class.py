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
        self.tile = pygame.image.load_extended("//BA-SRV-FS-01/18nkallah$/Computer Science/Project/textures/tile.png")
        self.tile = pygame.transform.scale_by(self.tile, 5)
        pass

    def getCoordinate(self,x ,y):
        return None

    def drawMap(self, map_layer):
        for i in range(12):
            for j in range(12):
                map_layer.blit(self.tile, ((i*50), (j*50)))

