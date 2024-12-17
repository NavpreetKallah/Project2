from builtins import int
import json
import pygame
import os

path = os.path.dirname(os.getcwd())+"/textures/HUD"

from game.config import SCALE

# , lives: int, cash: int, round_number: int, total_rounds: int
json_path = os.path.dirname(os.getcwd()) + "/game/data/tower_data.json"
class Hud:
    def __init__(self):
        with open(f"{json_path}", "r") as file:
            data = json.load(file)
        self.lives = 0
        self.cash = 0
        self.round_number = 0
        self.total_rounds = 0
        self.tower_names = ["Engineer", "Sniper", "Druid", "Wizard", "Ninja", "Alchemist", "Ice", "Mortar", "Dartling", "Village", "Farm", "Super"]
        self.locked_list = [True, False, False, False, False, False, False, False, False, False, False, False]

        tower_icons = self.seperate_sheet(pygame.transform.scale_by(pygame.image.load_extended(f"{path}/tower_icon_spritesheet.png").convert_alpha(), SCALE), 10*SCALE)
        tower_icons = {tower_name: tower_icons[i] for i, tower_name in enumerate(data)}
        tower_pos = [(2 * SCALE, 3 * SCALE), (17 * SCALE, 3 * SCALE), (2 * SCALE, 18 * SCALE), (17 * SCALE, 18 * SCALE), (2 * SCALE, 33 * SCALE), (17 * SCALE, 33 * SCALE), (2 * SCALE, 48 * SCALE), (17 * SCALE, 48 * SCALE), (2 * SCALE, 63 * SCALE), (17 * SCALE, 63 * SCALE), (2 * SCALE, 78 * SCALE), (17 * SCALE, 78 * SCALE)]
        tower_pos = {tower_name: tower_pos[i] for i, tower_name in enumerate(dict(sorted(data.items(), key=lambda x: x[1]["cost"])))}
        for tower_name in data:
            data[tower_name]["icon"] = tower_icons[tower_name]
            data[tower_name]["pos"] = tower_pos[tower_name]
        # self.tower_dict = {self.tower_names[i]: {"icon_red": self.tower_icons[i],
        #                                          "icon_green": self.colour_swap(self.tower_icons[i], (255, 0, 0), (0, 255, 0)),
        #                                          "pos": self.pos[i],
        #                                          "cost": 108,
        #                                          "locked": self.locked_list[i],
        #                                          "rect": pygame.Rect(self.pos[i][0], self.pos[i][1],10*SCALE,10*SCALE)}
        #                    for i in range(12)}

        self.tower_dict = {tower_name: {"icon_red": tower_icons[tower_name],
                                        "icon_green": self.colour_swap(tower_icons[tower_name], (255, 0, 0), (0, 255, 0)),
                                        "pos": tower_pos[tower_name],
                                        "cost": tower_name["cost"],
                                        "locked": tower_name["locked"],
                                        "rect": pygame.Rect(tower_pos[tower_name][0], tower_pos[tower_name][1],10*SCALE,10*SCALE)
                                        }
                           for tower_name in data}
        self.locked = pygame.transform.scale_by(pygame.image.load_extended(f"{path}/locked.png").convert_alpha(), SCALE)
        self.HUD_white = pygame.transform.scale_by(pygame.image.load_extended(f"{path}/HUD_white.png").convert_alpha(), SCALE)
        self.HUD_black = pygame.transform.scale_by(pygame.image.load_extended(f"{path}/HUD_black.png").convert_alpha(), SCALE)
        self.HUD_icons = pygame.transform.scale_by(pygame.image.load_extended(f"{path}/HUD_icons.png").convert_alpha(), SCALE)
        self.spritesheet = pygame.transform.scale_by(pygame.image.load_extended(f"{path}/numbers.png").convert_alpha(), SCALE)
        self.numbers = [self.get_image(self.spritesheet,(4)*SCALE,5*SCALE,i*4*SCALE-SCALE) for i in range(1,11)]
        self.numbers.insert(1, self.get_image(self.spritesheet, (3) * SCALE, 5 * SCALE, 0))
        self.counter = 1
        self.money = 100
        self.health = 100
        self.round = 0
        self.round_text = self.createNumber(self.round, 0)
        self.money_text = self.createNumber(self.money, 0)
        self.health_text = self.createNumber(self.health, 3)
        #self.rgb = [(250,i*5,0) for i in range (1,50)] + [(250-i*5,250,0) for i in range (1,50)] + [(0,250,i*5) for i in range (1,50)] + [(0,250-i*5,250) for i in range (1,50)] + [(i*5,0,250) for i in range (1,50)] + [(250,0,250-i*5) for i in range (1,50)]
        #self.rgb_colours = [self.colour_swap(self.HUD_white, (255,255,255), self.rgb[i%294]) for i in range(0,294)]

    def colour_swap(self, image, old_colour, new_colour):
        color_mask = pygame.mask.from_threshold(image, old_colour, threshold=(1, 1, 1, 255))
        color_change_surf = color_mask.to_surface(setcolor=new_colour, unsetcolor=(0, 0, 0, 0))
        img_copy = image.copy()
        img_copy.blit(color_change_surf, (0, 0))
        return img_copy

    def seperate_sheet(self, sheet, width):
        images = []
        amount = sheet.get_width()//width
        for i in range(amount):
            image = pygame.Surface((width,width), pygame.SRCALPHA).convert_alpha()
            image.blit(sheet, (0, 0), (width*i, 0, width, width))
            images.append(image)
        return images

    def get_image(self, surface, width, height,start):
        image = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
        image.blit(surface, (0,0), (start,0, width, height))
        return image


    def initialiseHud(self, layer):
        layer.blit(self.HUD_black, (0,0))
        layer.blit(self.HUD_white, (0,0))
        layer.blit(self.HUD_icons, (0,0))

    def updateHealth(self, health):
        self.health = health
        self.health_text = self.createNumber(self.health,3)

    def updateMoney(self, money):
        self.money = money
        self.money_text = self.createNumber(self.money, 0)

    def updateRound(self, round):
        self.round += round
        self.round_text = self.createNumber(self.round, 0)

    def createTowerSelect(self):
        surface = pygame.Surface((31*SCALE, 93*SCALE), pygame.SRCALPHA).convert_alpha()
        for tower in self.tower_dict.values():
            if tower["locked"]:
                if tower["cost"] >= self.money:
                    surface.blit(tower["icon_red"], tower["pos"])
                else:
                    surface.blit(tower["icon_green"], tower["pos"])
            else:
                surface.blit(self.locked, tower["pos"])
        return surface

    def updateHud(self, layer):
        #layer.blit(self.rgb_colours[round(self.counter/3) % 294], (0, 0))
        layer.blit(self.createTowerSelect(), (129 * SCALE, 12 * SCALE))
        layer.blit(self.HUD_white, (0, 0))
        layer.blit(self.round_text, (116*SCALE - self.round_text.get_width(), 3*SCALE))
        layer.blit(self.health_text,(12*SCALE, 3*SCALE))
        layer.blit(self.money_text, (39*SCALE, 3*SCALE))

    def createNumber(self, number, length):
        padded_number = ("0"*(length-len(str(number))) if length-len(str(number)) >= 0 else "") + str(number)
        sizes = [5*SCALE if i != "1" else 4*SCALE for i in padded_number]
        image_size = sum(sizes)
        surface = pygame.Surface((image_size,5*SCALE), pygame.SRCALPHA).convert_alpha()
        for i, number in enumerate(padded_number):
            surface.blit(self.numbers[int(number)],(sum(sizes[0:i]),0))
        return surface

    def play(self, layer):
        mouse = pygame.mouse.get_pos()
        play = pygame.Rect(128 * SCALE, 105 * SCALE, 15 * SCALE, 14 * SCALE)
        if play.collidepoint(mouse):
            return True







