from builtins import int
import pygame
import os

path = os.path.dirname(os.getcwd())+"/textures/HUD"

from Project.game.config import SCALE

# , lives: int, cash: int, round_number: int, total_rounds: int
class Hud:
    def __init__(self):
        self.lives = 0
        self.cash = 0
        self.round_number = 0
        self.total_rounds = 0
        self.HUD_white = pygame.transform.scale_by(pygame.image.load_extended(f"{path}/HUD_white.png").convert_alpha(), SCALE)
        self.HUD_black = pygame.transform.scale_by(pygame.image.load_extended(f"{path}/HUD_black.png").convert_alpha(), SCALE)
        self.HUD_icons = pygame.transform.scale_by(pygame.image.load_extended(f"{path}/HUD_icons.png").convert_alpha(), SCALE)
        self.spritesheet = pygame.transform.scale_by(pygame.image.load_extended(f"{path}/numbers.png").convert_alpha(), SCALE)
        self.numbers = [self.get_image(self.spritesheet,(4)*SCALE,5*SCALE,i*4*SCALE-SCALE) for i in range(1,11)]
        self.numbers.insert(1, self.get_image(self.spritesheet, (3) * SCALE, 5 * SCALE, 0))
        self.counter = 1
        self.rgb = [(250,i*5,0) for i in range (1,50)] + [(250-i*5,250,0) for i in range (1,50)] + [(0,250,i*5) for i in range (1,50)] + [(0,250-i*5,250) for i in range (1,50)] + [(i*5,0,250) for i in range (1,50)] + [(250,0,250-i*5) for i in range (1,50)]
        self.rgb_colours = [self.colour_swap(self.HUD_white, (255,255,255), self.rgb[i%294]) for i in range(0,294)]

    def colour_swap(self, image, old_colour, new_colour):
        color_mask = pygame.mask.from_threshold(image, old_colour, threshold=(1, 1, 1, 255))
        color_change_surf = color_mask.to_surface(setcolor=new_colour, unsetcolor=(0, 0, 0, 0))
        img_copy = image.copy()
        img_copy.blit(color_change_surf, (0, 0))
        return img_copy

    def get_image(self, surface, width, height,start):
        image = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
        image.blit(surface, (0,0), (start,0, width, height))
        return image
    def initialiseHud(self, difficulty, layer):
        layer.blit(self.HUD_black, (0,0))
        layer.blit(self.HUD_white, (0,0))
        layer.blit(self.HUD_icons, (0,0))

    def updateHud(self, layer):
        self.counter += 1
        layer.blit(self.rgb_colours[round(self.counter/3) % 294], (0, 0))
        health = self.createNumber(self.counter % 1000,3)
        money = self.createNumber(self.counter % 9999999, 0)
        layer.blit(health,(12*SCALE, 3*SCALE))
        layer.blit(money, (39*SCALE, 3*SCALE))

    def createNumber(self, number, length):
        padded_number = ("0"*(length-len(str(number))) if length-len(str(number)) >= 0 else "") + str(number)
        sizes = [5*SCALE if i != "1" else 4*SCALE for i in padded_number]
        image_size = sum(sizes)
        surface = pygame.Surface((image_size,5*SCALE), pygame.SRCALPHA).convert_alpha()
        for i, number in enumerate(padded_number):
            surface.blit(self.numbers[int(number)],(sum(sizes[0:i]),0))
        return surface







