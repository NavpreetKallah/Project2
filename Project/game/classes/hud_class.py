import json
import os
from builtins import int

import pygame

path = os.path.dirname(os.getcwd()) + "/textures/HUD"

from game.config import SCALE

# , lives: int, cash: int, round_number: int, total_rounds: int
json_path = os.path.dirname(os.getcwd()) + "/game/data/tower_data.json"


class Hud:
    def __init__(self):
        with open(f"{json_path}", "r") as file:
            data = json.load(file)
        self.round_number = 0
        self.total_rounds = 0
        tower_icons = self.seperate_sheet(
            pygame.transform.scale_by(pygame.image.load_extended(f"{path}/tower_icon_spritesheet.png").convert_alpha(),
                                      SCALE), 10 * SCALE)
        tower_icons = {tower_name: tower_icons[i] for i, tower_name in enumerate(data)}
        tower_pos = [(2 * SCALE, 3 * SCALE), (17 * SCALE, 3 * SCALE), (2 * SCALE, 18 * SCALE), (17 * SCALE, 18 * SCALE),
                     (2 * SCALE, 33 * SCALE), (17 * SCALE, 33 * SCALE), (2 * SCALE, 48 * SCALE),
                     (17 * SCALE, 48 * SCALE), (2 * SCALE, 63 * SCALE), (17 * SCALE, 63 * SCALE),
                     (2 * SCALE, 78 * SCALE), (17 * SCALE, 78 * SCALE)]
        tower_pos = {tower_name: tower_pos[i] for i, tower_name in
                     enumerate(dict(sorted(data.items(), key=lambda x: x[1]["cost"])))}
        for tower_name in data:
            data[tower_name]["icon"] = tower_icons[tower_name]
            data[tower_name]["pos"] = tower_pos[tower_name]

        self.speedup = False
        self.tower_layer = None
        self.upgrade = False
        self.tower_dict = {tower_name: {"icon_red": tower_icons[tower_name],
                                        "icon_green": self.colour_swap(tower_icons[tower_name], (255, 0, 0),
                                                                       (0, 255, 0)),
                                        "pos": tower_pos[tower_name],
                                        "cost": tower_info["cost"],
                                        "locked": tower_info["locked"],
                                        "rect": pygame.Rect(tower_pos[tower_name][0], tower_pos[tower_name][1],
                                                            10 * SCALE, 10 * SCALE)
                                        }
                           for tower_name, tower_info in data.items()}

        self.upgrade_icons = {"range": pygame.transform.scale_by(pygame.image.load_extended(f"{path}/upgrade_icons/range.png").convert_alpha(),SCALE),
                              "damage": pygame.transform.scale_by(pygame.image.load_extended(f"{path}/upgrade_icons/damage.png").convert_alpha(),SCALE),
                              "secondary_damage": pygame.transform.scale_by(pygame.image.load_extended(f"{path}/upgrade_icons/damage.png").convert_alpha(),SCALE),
                              "main_atk_speed": pygame.transform.scale_by(pygame.image.load_extended(f"{path}/upgrade_icons/atk_speed.png").convert_alpha(),SCALE),
                              "secondary_atk_speed": pygame.transform.scale_by(pygame.image.load_extended(f"{path}/upgrade_icons/atk_speed.png").convert_alpha(),SCALE),
                              "camo": pygame.transform.scale_by(pygame.image.load_extended(f"{path}/upgrade_icons/camo.png").convert_alpha(),SCALE),
                              "pierce": pygame.transform.scale_by(pygame.image.load_extended(f"{path}/upgrade_icons/pierce.png").convert_alpha(),SCALE),
                              "max": pygame.transform.scale_by(pygame.image.load_extended(f"{path}/upgrade_icons/max.png").convert_alpha(),SCALE),
                              "ability": pygame.transform.scale_by(pygame.image.load_extended(f"{path}/upgrade_icons/ability.png").convert_alpha(),SCALE)}
        self.locked = pygame.transform.scale_by(pygame.image.load_extended(f"{path}/locked.png").convert_alpha(), SCALE)

        self.HUD_upgrading = pygame.transform.scale_by(pygame.image.load_extended(f"{path}/HUD_upgrading.png").convert_alpha(),
                                                   SCALE)
        self.HUD_white = pygame.transform.scale_by(pygame.image.load_extended(f"{path}/HUD_white.png").convert_alpha(),
                                                   SCALE)
        self.HUD_black = pygame.transform.scale_by(pygame.image.load_extended(f"{path}/HUD_black.png").convert_alpha(),
                                                   SCALE)
        self.HUD_icons = pygame.transform.scale_by(pygame.image.load_extended(f"{path}/HUD_icons.png").convert_alpha(),
                                                   SCALE)
        self.spritesheet = pygame.transform.scale_by(pygame.image.load_extended(f"{path}/numbers.png").convert_alpha(),
                                                     SCALE)
        self.fast_forward_indicator = pygame.transform.scale_by(
            pygame.image.load_extended(f"{path}/fast_forward.png").convert_alpha(),
            SCALE)
        self.upgrade_background_3 = self.createBackground(pygame.Surface((17 * SCALE, 7 * SCALE), pygame.SRCALPHA).convert_alpha(),(255,205,0))
        self.upgrade_background_4 = self.createBackground(pygame.Surface((22 * SCALE, 7 * SCALE), pygame.SRCALPHA).convert_alpha(),(255,205,0))
        self.upgrade_background_5 = self.createBackground(pygame.Surface((27 * SCALE, 7 * SCALE), pygame.SRCALPHA).convert_alpha(),(255,205,0))
        self.upgrade_backgrounds = [self.upgrade_background_3, self.upgrade_background_4, self.upgrade_background_5]
        self.upgrade_cost_positions = [7,4.5,2]
        self.upgrade_sell = self.createBackground(pygame.Surface((23 * SCALE, 9 * SCALE), pygame.SRCALPHA).convert_alpha(),(255,205,0))
        self.numbers = [self.get_image(self.spritesheet, (4) * SCALE, 5 * SCALE, i * 4 * SCALE - SCALE) for i in
                        range(1, 11)]
        self.numbers.insert(1, self.get_image(self.spritesheet, (3) * SCALE, 5 * SCALE, 0))
        self.counter = 1
        self.money = 0
        self.health = 0
        self.round = 0
        self.round_text = self.createNumber(self.round, 0)
        self.money_text = self.createNumber(self.money, 0)
        self.health_text = self.createNumber(self.health, 3)
        # self.rgb = [(250,i*5,0) for i in range (1,50)] + [(250-i*5,250,0) for i in range (1,50)] + [(0,250,i*5) for i in range (1,50)] + [(0,250-i*5,250) for i in range (1,50)] + [(i*5,0,250) for i in range (1,50)] + [(250,0,250-i*5) for i in range (1,50)]
        # self.rgb_colours = [self.colour_swap(self.HUD_white, (255,255,255), self.rgb[i%294]) for i in range(0,294)]

    def colour_swap(self, image, old_colour, new_colour):
        color_mask = pygame.mask.from_threshold(image, old_colour, threshold=(1, 1, 1, 255))
        color_change_surf = color_mask.to_surface(setcolor=new_colour, unsetcolor=(0, 0, 0, 0))
        img_copy = image.copy()
        img_copy.blit(color_change_surf, (0, 0))
        return img_copy

    def seperate_sheet(self, sheet, width):
        images = []
        amount = sheet.get_width() // width
        for i in range(amount):
            image = pygame.Surface((width, width), pygame.SRCALPHA).convert_alpha()
            image.blit(sheet, (0, 0), (width * i, 0, width, width))
            images.append(image)
        return images

    def get_image(self, surface, width, height, start):
        image = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
        image.blit(surface, (0, 0), (start, 0, width, height))
        return image

    def initialiseHud(self, layer):
        layer.blit(self.HUD_black, (0, 0))
        layer.blit(self.HUD_white, (0, 0))
        layer.blit(self.HUD_icons, (0, 0))

    def updateHealth(self, health):
        self.health = health
        self.health_text = self.createNumber(self.health, 3)

    def updateMoney(self, money):
        self.money = money
        self.money_text = self.createNumber(self.money, 0)

    def updateRound(self, round):
        self.round += round
        self.round_text = self.createNumber(self.round, 0)

    def createBackground(self, surface, color):
        surface.fill(color)
        surface.fill((0, 0, 0),(0,0,SCALE,SCALE))
        surface.fill((0, 0, 0),(surface.get_width()-SCALE,0,SCALE,SCALE))
        surface.fill((0, 0, 0),(surface.get_width()-SCALE,surface.get_height()-SCALE,SCALE,SCALE))
        surface.fill((0, 0, 0),(0,surface.get_height()-SCALE,SCALE,SCALE))
        surface.set_colorkey((0,0,0))
        return surface

    def createTowerSelect(self):
        surface = pygame.Surface((31 * SCALE, 93 * SCALE), pygame.SRCALPHA).convert_alpha()
        for tower in self.tower_dict.values():
            if not tower["locked"]:
                if tower["cost"] > self.money:
                    surface.blit(tower["icon_red"], tower["pos"])
                else:
                    surface.blit(tower["icon_green"], tower["pos"])
            else:
                surface.blit(self.locked, tower["pos"])
        return surface

    def createTowerUpgrade(self, Tower):
        self.Tower = Tower
        surface = pygame.surface.Surface((self.HUD_upgrading.get_width(),self.HUD_upgrading.get_height()))
        surface.blit(self.HUD_upgrading, (0,0))
        path_one = self.Tower.upgrades["path_one"]
        path_two = self.Tower.upgrades["path_two"]
        for path_name, upgrade, y_pos in [("path_one",path_one,11),("path_two",path_two,45)]:
            icon_position = (6*SCALE,20*SCALE) if path_name == "path_one" else (6*SCALE, 54*SCALE)
            if upgrade == 4:
                surface.blit(self.upgrade_icons["max"], icon_position)
            else:
                upgrade_info = self.Tower.data[path_name][str(upgrade+1)]
                cost = upgrade_info["cost"]
                text = self.createNumber(cost, 0)
                length = len(str(cost))
                surface.blit(self.upgrade_backgrounds[length-3], (round(self.upgrade_cost_positions[length-3]*SCALE),y_pos*SCALE))
                surface.blit(text, (self.upgrade_cost_positions[length-3]*SCALE+2*SCALE,(y_pos+1)*SCALE))
                if upgrade_info["name"]:
                    surface.blit(self.upgrade_icons["ability"], icon_position)
                else:
                    surface.blit(self.upgrade_icons[upgrade_info["stat_change"][0]["stat"]], icon_position)

        return surface


        # path_two_cost = self.Tower.data[f"path_two"][str(path_two+1)]["cost"]
        # path_two_text = self.createNumber(path_two_cost, 0)
        # path_two_text_length = len(str(path_two_cost))
        # surface.blit(self.upgrade_backgrounds[path_two_text_length-3], (round(self.upgrade_cost_positions[path_two_text_length-3]*SCALE),y_pos*SCALE))
        # surface.blit(path_two_text, (self.upgrade_cost_positions[path_two_text_length-3]*SCALE+2*SCALE,(y_pos+1)*SCALE))

    def drawRange(self, layer):
        pygame.draw.circle(layer, (50, 50, 50, 20), self.Tower.rect.center, self.Tower.data["range"] * SCALE)

    def updateHud(self, layer):
        layer.fill((255,255,255,0))
        if self.upgrade and self.Tower:
            self.drawRange(layer)
        self.initialiseHud(layer)
        self.counter += 1

        # layer.blit(self.rgb_colours[round(self.counter/3) % 294], (0, 0))
        if not self.upgrade:
            layer.blit(self.HUD_black, (0,0))
            layer.blit(self.createTowerSelect(), (129 * SCALE, 12 * SCALE))
        else:
            layer.blit(self.createTowerUpgrade(self.Tower), (128 * SCALE, 11 * SCALE))
        if self.speedup:
            layer.blit(self.fast_forward_indicator, (145 * SCALE, 106 * SCALE))
        layer.blit(self.round_text, (116 * SCALE - self.round_text.get_width(), 3 * SCALE))
        layer.blit(self.health_text, (12 * SCALE, 3 * SCALE))
        layer.blit(self.money_text, (39 * SCALE, 3 * SCALE))

    def getUpgrading(self):
        return self.upgrade

    def createNumber(self, number, length):
        padded_number = ("0" * (length - len(str(number))) if length - len(str(number)) >= 0 else "") + str(number)
        sizes = [5 * SCALE if i != "1" else 4 * SCALE for i in padded_number]
        image_size = sum(sizes)
        surface = pygame.Surface((image_size, 5 * SCALE), pygame.SRCALPHA).convert_alpha()
        for i, number in enumerate(padded_number):
            surface.blit(self.numbers[int(number)], (sum(sizes[0:i]), 0))
        return surface

    def upgradeChosen(self, layer):
        mouse = pygame.mouse.get_pos()
        main_box = pygame.Rect(127*SCALE,10*SCALE,33*SCALE,110*SCALE)
        path_one = pygame.Rect(132*SCALE,29*SCALE,23*SCALE,23*SCALE)
        path_two = pygame.Rect(132*SCALE,63*SCALE,23*SCALE,23*SCALE)
        if main_box.collidepoint(mouse):
            if path_one.collidepoint(mouse):
                return "path_one"
            elif path_two.collidepoint(mouse):
                return "path_two"
            return "main"


    def play(self):
        mouse = pygame.mouse.get_pos()
        play = pygame.Rect(128 * SCALE, 105 * SCALE, 15 * SCALE, 14 * SCALE)
        if play.collidepoint(mouse):
            return True

    def setUpgrading(self, value):
        self.upgrade = value

    def tower_chosen(self):
        mouse = pygame.mouse.get_pos()
        for tower, info in self.tower_dict.items():
            if not info["locked"] and info["rect"].collidepoint(
                    (mouse[0] - 129 * SCALE, mouse[1] - 12 * SCALE)) and not self.upgrade:
                if self.money >= info["cost"]:
                    return tower

    # TODO rename disable and enable speed
    def disableSpeed(self, layer):
        self.HUD_icons = self.colour_swap(self.HUD_icons, (120, 195, 0), (60, 60, 60))
        self.HUD_icons = self.colour_swap(self.HUD_icons, (180, 255, 0), (180, 180, 180))
        self.HUD_icons = self.colour_swap(self.HUD_icons, (150, 225, 0), (120, 120, 120))
        self.fast_forward_indicator = self.colour_swap(self.fast_forward_indicator, (180, 255, 0), (180, 180, 180))
        layer.blit(self.HUD_icons, (0, 0))

    def enableSpeed(self, layer):
        self.HUD_icons = self.colour_swap(self.HUD_icons, (60, 60, 60), (120, 195, 0))
        self.HUD_icons = self.colour_swap(self.HUD_icons, (180, 180, 180), (180, 255, 0))
        self.HUD_icons = self.colour_swap(self.HUD_icons, (120, 120, 120), (150, 225, 0))
        self.fast_forward_indicator = self.colour_swap(self.fast_forward_indicator, (180, 180, 180), (180, 255, 0))
        layer.blit(self.HUD_icons, (0, 0))

    def fastForward(self, layer):
        mouse = pygame.mouse.get_pos()
        fast_forward = pygame.Rect(144 * SCALE, 105 * SCALE, 15 * SCALE, 14 * SCALE)
        # pygame.draw.rect(layer, (50,50,50),fast_forward,SCALE)
        if fast_forward.collidepoint(mouse):
            self.speedup = not self.speedup
            return True
