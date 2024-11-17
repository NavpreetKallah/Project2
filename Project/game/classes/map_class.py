from builtins import tuple, list, int, range
import pygame
import json
import os
SCALE = 5

json_path = os.path.dirname(os.getcwd()) + "/map/"
path = os.path.dirname(os.getcwd())+"/textures"
print(path)

#current_map_path: list, current_map_start: tuple, current_map_end: tuple, current_map_textures: list, path_length: int
class Map:
    def __init__(self):
        # self.current_map_path = current_map_path
        # self.current_map_start = current_map_start
        # self.current_map_end = current_map_end
        # self.current_map_textures = current_map_textures
        # self.path_length = path_length
        self.map = None
        self.connector_head = pygame.transform.scale_by(pygame.image.load_extended(f"{path}/connector_head.png"), SCALE)
        self.connector_heads = [pygame.transform.rotate(self.connector_head, theta*90) for theta in range(4)]
        self.connector = pygame.transform.scale_by(pygame.image.load_extended(f"{path}/connector.png"), SCALE)
        self.straight_path = pygame.transform.scale_by(pygame.image.load_extended(f"{path}/straight_path.png"), SCALE)

    def getCoordinate(self,x ,y):
        return None

    def initialiseMap(self, map, layer):
        with open(f"{json_path}{map}.json", "r") as file:
            self.map = json.load(file)["map"]
        for i, row in enumerate(self.map):
            for j, cell in enumerate(row):
                if cell == [92]:
                    layer.blit(self.orientation(self.adjacent_cells(i, j),[91]), (j*9*SCALE, i*9*SCALE))
                elif cell == [91]:
                    layer.blit(self.connector, (j*9*SCALE, i*9*SCALE))
                elif 0 < cell[0] < 90:
                    temp = self.adjacent_cells(i, j)
                    temp = [temp[0] if type(temp) == list and 0 < temp[0] < 90 else None for temp in temp]
                    first = temp.index(None)
                    second = temp.index(None, first+1)
                    if second - first == 2:
                        if first != 0:
                            layer.blit(self.straight_path, (j*9*SCALE, i*9*SCALE))
                        else:
                            layer.blit(pygame.transform.rotate(self.straight_path, 90), (j*9*SCALE, i*9*SCALE))


    def adjacent_cells(self, j, i):
        up = self.map[j-1][i] if j != 0 else None
        down = self.map[j+1][i] if j != 11 else None
        left = self.map[j][i-1] if i != 0 else None
        right = self.map[j][i+1] if i != 13 else None
        return [down, left, up, right]

    def orientation(self, directions, touching):

        return self.connector_heads[directions.index(touching)]



    def createMap(self, map_layer):
        pass

    def print_map(self):
        for row in self.map:
            print(row)

    def print_cell(self, i , j):
        print(self.map[i][j])
