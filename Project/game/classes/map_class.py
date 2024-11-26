from builtins import tuple, list, int, range
import pygame
import json
import os
from game.config import SCALE

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
        self.scenery = pygame.transform.scale_by(pygame.image.load_extended(f"{path}/scenery.png").convert_alpha(), SCALE)
        self.straight_path = pygame.transform.scale_by(pygame.image.load_extended(f"{path}/straight_path.png").convert_alpha(), SCALE)
        self.connector_path = pygame.transform.scale_by(pygame.image.load_extended(f"{path}/connector_path.png").convert_alpha(), SCALE)
        self.connector_paths = [pygame.transform.rotate(self.connector_path, -theta*90) for theta in range(4)]

    def getCoordinate(self,x ,y):
        return None

    def initialiseMap(self, map, layer):
        layer.blit(self.scenery, (SCALE,SCALE*11))
        with open(f"{json_path}{map}.json", "r") as file:
            self.map = json.load(file)["map"]
        for i, row in enumerate(self.map):
            for j, cell in enumerate(row):
                pos = ((j*9+1)*SCALE, (i*9+11)*SCALE)
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

        self.pathfind()

    def pathfind(self):
        dict = {}
        direction = []
        for i, row in enumerate(self.map):
            for j, cell in enumerate(row):
                if 0 < cell[0] < 90:
                    dict[cell[0]] = (i,j)
        for i in range(1,42):
            if dict[i][1] + 1 == dict[i+1][1]:
                direction.append("R")
            elif dict[i][1] - 1 == dict[i+1][1]:
                direction.append("L")
            elif dict[i][0] + 1 == dict[i+1][0]:
                direction.append("D")
            elif dict[i][0] - 1 == dict[i+1][0]:
                direction.append("U")
        direction.append("U")
        return direction


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
