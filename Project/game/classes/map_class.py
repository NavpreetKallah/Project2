import pygame


class Map:
    def __init__(self, current_map_path: array, current_map_start: tuple, current_map_end: tuple, current_map_textures: array, path_length: int):
        self.current_map_path = current_map_path
        self.current_map_start = current_map_start
        self.current_map_end = current_map_end
        self.current_map_textures = current_map_textures
        self.path_length = path_length
