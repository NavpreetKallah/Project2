import json
import os
from typing import List, Optional, Tuple, Dict

import pygame

from game.config import SCALE

json_path: str = os.path.dirname(os.getcwd()) + "/map/"
path: str = os.path.dirname(os.getcwd()) + "/textures"

from game.classes.linked_list import Queue


class Map:
    def __init__(self) -> None:
        self.map: Optional[list] = None
        self.scenery: pygame.Surface = pygame.transform.scale_by(
            pygame.image.load_extended(f"{path}/scenery.png").convert_alpha(), SCALE)
        self.straight_path: pygame.Surface = pygame.transform.scale_by(
            pygame.image.load_extended(f"{path}/straight_path.png").convert_alpha(), SCALE)
        self.connector_path: pygame.Surface = pygame.transform.scale_by(
            pygame.image.load_extended(f"{path}/connector_path.png").convert_alpha(), SCALE)
        self.connector_paths: List[pygame.Surface] = [pygame.transform.rotate(self.connector_path, -theta * 90) for
                                                      theta in range(4)]
        self.image_list: List[pygame.Surface] = []
        self.rect_list: List[pygame.Rect] = []
        self.mask_list: List[pygame.Mask] = []

    def getRects(self) -> List[pygame.Rect]:
        return self.rect_list

    def getMasks(self) -> List[pygame.Mask]:
        for image in self.image_list:
            image.set_colorkey((169, 173, 16))
            image = pygame.mask.from_surface(image)
            self.mask_list.append(image)
        return self.mask_list

    def getImages(self) -> List[pygame.Surface]:
        return self.image_list

    def initialiseMap(self, map: str, layer: pygame.Surface) -> None:
        layer.blit(self.scenery, (SCALE, SCALE * 11))
        with open(f"{json_path}{map}.json", "r") as file:
            self.map = json.load(file)["map"]
        for i, row in enumerate(self.map):
            for j, cell in enumerate(row):
                pos: Tuple[int, int] = ((j * 9 + 1) * SCALE, (i * 9 + 11) * SCALE)
                if 0 < cell[0] < 90:
                    adjacent_cells: List[Optional[int]] = self.adjacent_cells(i, j)
                    self.rect_list.append(pygame.Rect(pos[0], pos[1], SCALE * 9, SCALE * 9))
                    if adjacent_cells.count(0) == 3:
                        layer.blit(self.straight_path, pos)
                        self.image_list.append(self.straight_path)
                        continue

                    first_touching: int = adjacent_cells.index(1)
                    second_touching: int = adjacent_cells.index(1, first_touching + 1)

                    if second_touching - first_touching == 2:
                        if first_touching != 1:
                            layer.blit(self.straight_path, pos)
                            self.image_list.append(self.straight_path)
                        else:
                            layer.blit(pygame.transform.rotate(self.straight_path, 90), pos)
                            self.image_list.append(pygame.transform.rotate(self.straight_path, 90))

                    elif second_touching - first_touching != 2:
                        layer.blit(
                            self.connector_paths[second_touching if (second_touching - first_touching) == 1 else 0],
                            pos)
                        self.image_list.append(self.connector_paths[((
                            second_touching if (second_touching - first_touching) == 1 else 0)) % 4])

        self.pathfind()

    def pathfind(self) -> Queue:
        dict: Dict[int, Tuple[int, int]] = {}
        path: Queue = Queue()
        first: Optional[str] = None
        for i, row in enumerate(self.map):
            for j, cell in enumerate(row):
                if 0 < cell[0] < 90:
                    dict[cell[0]] = (i, j)

        for i in range(1, 42):
            if dict[i][1] + 1 == dict[i + 1][1]:
                direction: str = "R"
            elif dict[i][1] - 1 == dict[i + 1][1]:
                direction = "L"
            elif dict[i][0] + 1 == dict[i + 1][0]:
                direction = "D"
            elif dict[i][0] - 1 == dict[i + 1][0]:
                direction = "U"
            path.add(direction)
            if not first:
                path.add(direction)
                path.add(direction)
                first = "Done"

        path.add(path.look(-1))
        path.add(path.look(-1))

        return path

    def adjacent_cells(self, j: int, i: int) -> List[int]:
        up: Optional[int] = self.map[j - 1][i] if j != 0 else None
        down: Optional[int] = self.map[j + 1][i] if j != 11 else None
        left: Optional[int] = self.map[j][i - 1] if i != 0 else None
        right: Optional[int] = self.map[j][i + 1] if i != 13 else None
        adjacent_cells: List[Optional[int]] = [down, left, up, right]
        return [1 if type(adjacent_cells) == list and 0 < adjacent_cells[0] < 90 else 0 for adjacent_cells in
                adjacent_cells]

    def print_map(self) -> None:
        for row in self.map:
            print(row)

    def print_cell(self, i: int, j: int) -> None:
        print(self.map[i][j])
