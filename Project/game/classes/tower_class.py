import json
import os
import time

import pygame, random

from config import SCALE
from math import atan2, degrees, pi
from game.classes.projectile_class import ProjectileManager
ProjectileManager = ProjectileManager()


# Entity
# , position: pygame.Vector2, angle: int, state: str, frame: int,
#                  range: int, size: int, attack_speed: int
#
# super().__init__(position, angle, state, frame, range)

# self.size = size
# self.attack_speed = attack_speed
class Tower(pygame.sprite.Sprite):
    def __init__(self, data, pos):
        pygame.sprite.Sprite.__init__(self)
        self.data = data
        self.image = data["icon"]
        self.range = data["range"]
        self.main_atk = data["main_atk"]
        self.main_atk_targets = data["main_atk_targets"]
        self.camo = data["camo"]
        self.atk_speed = data["atk_speed"]
        self.spread = data["spread"]
        self.pos = pos
        self.rect = self.image.get_rect(center=self.pos)
        self.image_copy = self.image
        self.timer = time.perf_counter()
        self.images = [pygame.transform.rotate(self.image, i) for i in range(1,361)]

    def attack(self, fast_forward, angle):
        if time.perf_counter() - self.timer > (self.atk_speed if not fast_forward else self.atk_speed/3):
            self.timer = time.perf_counter()
            ProjectileManager.create(self.data, angle, self.rect.center, fast_forward)

    def action(self, enemies, fast_forward):
        if self.main_atk == "normal":
            self.normal_aim(enemies, fast_forward)
        if self.main_atk == "mouse":
            self.mouse_aim(fast_forward)

    def mouse_aim(self, fast_forward):
        angle = round(self.getAngle(pygame.mouse.get_pos()))
        self.image = self.images[angle % 360]
        self.rect = self.image.get_rect(center=self.pos)
        angle += random.randint(-self.spread,self.spread)
        self.attack(fast_forward, angle)


    def normal_aim(self, enemies, fast_forward):
        if self.atk_speed == 0:
            return
        enemy_info = sorted([(number,int(pygame.Vector2(self.rect.center).distance_to(pygame.Vector2(enemy.center))//SCALE),enemy) for number, enemy in enemies if int(pygame.Vector2(self.rect.center).distance_to(pygame.Vector2(enemy.center))//SCALE) < self.range])
        if enemy_info:
            angle = round(self.getAngle(enemy_info[0][2]))
            self.attack(fast_forward, angle)
            self.image = self.images[angle%360]
            self.rect = self.image.get_rect(center=self.pos)

    def getAngle(self, target):
        x1,y1 = self.rect.center
        if isinstance(target, type(self.rect)):
            x2,y2 = target.center
        else:
            x2,y2 = target
        dx = x2 - x1
        dy = y2 - y1
        rads = atan2(-dy, dx)
        rads %= 2 * pi
        return degrees(rads)+90


json_path = os.path.dirname(os.getcwd()) + "/game/data/tower_data.json"
path = os.path.dirname(os.getcwd()) + "/textures/HUD"


class TowerManager:
    def __init__(self):

        with open(f"{json_path}", "r") as file:
            data = json.load(file)
        tower_icons = self.seperate_sheet(
            pygame.transform.scale_by(pygame.image.load_extended(f"{path}/spritesheet2.png").convert_alpha(),
                                      SCALE), 8 * SCALE)
        tower_icons = {tower_name: tower_icons[i] for i, tower_name in enumerate(data)}
        self.tower_dict = {tower_name: {
            "main_atk": tower_info["main_atk"],
            "main_atk_targets": tower_info["main_atk_targets"],
            "spread": tower_info["spread"],
            "camo": tower_info["camo"],
            "icon": tower_icons[tower_name],
            "range": tower_info["range"],
            "cost": tower_info["cost"],
            "damage": tower_info["damage"],
            "pierce": tower_info["pierce"],
            "atk_speed": tower_info["atk_speed"]

        }
                           for tower_name, tower_info in data.items()}
        self.placing = False
        self.placing_tower = None
        self.tower_pos = None
        self.tower_mask = None
        self.sprites = pygame.sprite.Group()
        self.rects = []
        self.images = []

    def create(self):
        if self.placing_tower and self.tower_pos:
            self.sprites.add(Tower(self.tower_dict[self.placing_tower], self.tower_pos))
            self.rects.append(self.tower_dict[self.placing_tower]["icon"].get_rect(center=self.tower_pos))
            self.images.append(self.tower_dict[self.placing_tower]["icon"])
            self.placing_tower = None
            self.placing = False
            self.tower_pos = None

    def place(self, layer, paths, path_masks, tower):
        mouse = pygame.mouse.get_pos()
        corrected_mouse = ((mouse[0] // SCALE) * SCALE, (mouse[1] // SCALE) * SCALE)
        rect = pygame.Rect(1 * SCALE, 11 * SCALE, 126 * SCALE, 108 * SCALE)
        valid = True
        if not self.tower_mask:
            self.tower_mask = pygame.mask.from_surface(self.tower_dict[tower]["icon"])
        if rect.contains(self.tower_dict[tower]["icon"].get_rect(center=corrected_mouse)):
            if self.tower_dict[tower]["icon"].get_rect(center=corrected_mouse).collidelist(paths) != -1:
                for i, path in enumerate(paths):
                    path_x, path_y = (path.center[0]//SCALE)*SCALE, (path.center[1]//SCALE)*SCALE
                    layer.blit(path_masks[i].to_surface(), (corrected_mouse[0]-path.center[0]+SCALE,corrected_mouse[1]-path.center[1]))
                    if self.tower_mask.overlap(path_masks[i], (corrected_mouse[0]-path_x-SCALE,corrected_mouse[1]-path_y-SCALE)):
                        valid = False

            else:
                if self.tower_dict[tower]["icon"].get_rect(center=corrected_mouse).collidelist(self.rects) != -1:
                    for i, rect in enumerate(self.rects):
                        if self.tower_mask.overlap(pygame.mask.from_surface(self.images[i]), (corrected_mouse[0]-rect.center[0],corrected_mouse[1]-rect.center[1])):
                            valid = False

        else:
            valid = False

        pygame.draw.circle(layer,(50,50,50,20) if valid else (200,50,50,120), corrected_mouse, self.tower_dict[tower]["range"]*SCALE)
        layer.blit(self.tower_dict[tower]["icon"], self.tower_dict[tower]["icon"].get_rect(center=corrected_mouse))
        self.tower_pos = corrected_mouse if valid else None

    def getCost(self):
        return self.tower_dict[self.placing_tower]["cost"]

    def resetPlacing(self):
        self.placing_tower = None
        self.placing = False
        self.tower_pos = None
        self.tower_mask = None

    def getTowerPos(self):
        return self.tower_pos

    def aim(self, enemies, fast_forward):
        if enemies and self.sprites:
            enemy_positions = [(sprite.number, sprite.rect) for sprite in enemies]
            for tower in self.sprites:
                tower.action(enemy_positions, fast_forward)

    def attack(self):
        for tower in self.sprites:
            tower.attack()

    def getPlacing(self):
        return self.placing

    def getSprites(self):
        return self.sprites
    def getPlacingTower(self):
        return self.placing_tower

    def seperate_sheet(self, sheet, width):
        images = []
        amount = sheet.get_width() // width
        for i in range(amount):
            image = pygame.Surface((width, width), pygame.SRCALPHA).convert_alpha()
            image.blit(sheet, (0, 0), (width * i, 0, width, width))
            images.append(image)
        return images
