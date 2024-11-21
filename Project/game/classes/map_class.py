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
        self.scenery = pygame.transform.scale_by(pygame.image.load_extended(f"{path}/scenery.png"), SCALE)
        self.straight_path = pygame.transform.scale_by(pygame.image.load_extended(f"{path}/straight_path.png"), SCALE)
        self.connector_path = pygame.transform.scale_by(pygame.image.load_extended(f"{path}/connector_path.png"), SCALE)
        self.connector_paths = [pygame.transform.rotate(self.connector_path, -theta*90) for theta in range(4)]

    def getCoordinate(self,x ,y):
        return None

    def initialiseMap(self, map, layer):
        layer.blit(self.scenery, (0,0))
        with open(f"{json_path}{map}.json", "r") as file:
            self.map = json.load(file)["map"]
        for i, row in enumerate(self.map):
            for j, cell in enumerate(row):
                pos = (j*9*SCALE, i*9*SCALE)
                if 0 < cell[0] < 90:
                    adjacent_cells = self.adjacent_cells(i, j)

                    if adjacent_cells.count(0) == 3:
                        layer.blit(self.straight_path, pos)
                        continue

                    first_touching = adjacent_cells.index(1)
                    second_touching = adjacent_cells.index(1, first_touching+1)

                    # This code orientates the path to be the correct direction
                    if second_touching - first_touching == 2:
                        if first_touching != 1:
                            layer.blit(self.straight_path, pos)
                        else:
                            layer.blit(pygame.transform.rotate(self.straight_path, 90), pos)

                    # This code rotates the connectors within the paths to be the correct orientation
                    elif second_touching - first_touching != 2:
                        layer.blit(self.connector_paths[second_touching if (second_touching - first_touching) == 1 else 0], pos)


    def adjacent_cells(self, j, i):
        up = self.map[j-1][i] if j != 0 else None
        down = self.map[j+1][i] if j != 11 else None
        left = self.map[j][i-1] if i != 0 else None
        right = self.map[j][i+1] if i != 13 else None
        adjacent_cells = [down, left, up, right]
        return [1 if type(adjacent_cells) == list and 0 < adjacent_cells[0] < 90 else 0 for adjacent_cells in adjacent_cells]



    def createMap(self, map_layer):
        pass

    def print_map(self):
        for row in self.map:
            print(row)

    def print_cell(self, i , j):
        print(self.map[i][j])
