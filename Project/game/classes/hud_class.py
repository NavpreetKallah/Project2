import json
import os
from typing import Dict, List, Tuple, Optional, Union, Any

import pygame

path: str = os.path.dirname(os.getcwd()) + "/textures/HUD"
json_path: str = os.path.dirname(os.getcwd()) + "/game/data/tower_data.json"

from game.config import SCALE


class Hud:
    def __init__(self) -> None:
        with open(f"{json_path}", "r") as file:
            data: Dict[str, Dict[str, Optional[int]]] = json.load(file)
        self.round_number: int = 0
        self.total_rounds: int = 0
        tower_icons: Dict[str, pygame.Surface] = self.seperate_sheet(
            pygame.transform.scale_by(pygame.image.load_extended(f"{path}/tower_icon_spritesheet.png").convert_alpha(),
                                      SCALE), 10 * SCALE)
        tower_icons = {tower_name: tower_icons[i] for i, tower_name in enumerate(data)}
        tower_pos: Union[list, dict] = [(2 * SCALE, 3 * SCALE), (17 * SCALE, 3 * SCALE), (2 * SCALE, 18 * SCALE),
                                        (17 * SCALE, 18 * SCALE),
                                        (2 * SCALE, 33 * SCALE), (17 * SCALE, 33 * SCALE), (2 * SCALE, 48 * SCALE),
                                        (17 * SCALE, 48 * SCALE), (2 * SCALE, 63 * SCALE), (17 * SCALE, 63 * SCALE),
                                        (2 * SCALE, 78 * SCALE), (17 * SCALE, 78 * SCALE)]
        tower_pos = {tower_name: tower_pos[i] for i, tower_name in
                     enumerate(dict(sorted(data.items(), key=lambda x: x[1]["cost"])))}
        for tower_name in data:
            data[tower_name]["icon"] = tower_icons[tower_name]
            data[tower_name]["pos"] = tower_pos[tower_name]

        self.speedup: bool = False
        self.tower_layer: Optional[pygame.Surface] = None
        self.upgrade: bool = False
        self.tower_dict: Dict[str, Dict[str, Any]] = {tower_name: {"icon_red": tower_icons[tower_name],
                                                                   "icon_green": self.colour_swap(
                                                                       tower_icons[tower_name], (255, 0, 0),
                                                                       (0, 255, 0)),
                                                                   "pos": tower_pos[tower_name],
                                                                   "cost": tower_info["cost"],
                                                                   "locked": tower_info["locked"],
                                                                   "rect": pygame.Rect(tower_pos[tower_name][0],
                                                                                       tower_pos[tower_name][1],
                                                                                       10 * SCALE, 10 * SCALE)
                                                                   }
                                                      for tower_name, tower_info in data.items()}

        self.upgrade_icons: Dict[str, pygame.Surface] = {"range": pygame.transform.scale_by(
            pygame.image.load_extended(f"{path}/upgrade_icons/range.png").convert_alpha(), SCALE),
            "damage": pygame.transform.scale_by(pygame.image.load_extended(
                f"{path}/upgrade_icons/damage.png").convert_alpha(),
                                                SCALE),
            "burst": pygame.transform.scale_by(pygame.image.load_extended(
                f"{path}/upgrade_icons/burst.png").convert_alpha(), SCALE),
            "stun": pygame.transform.scale_by(pygame.image.load_extended(
                f"{path}/upgrade_icons/stun.png").convert_alpha(), SCALE),
            "speed": pygame.transform.scale_by(pygame.image.load_extended(
                f"{path}/upgrade_icons/atk_speed.png").convert_alpha(),
                                               SCALE),
            "camo": pygame.transform.scale_by(pygame.image.load_extended(
                f"{path}/upgrade_icons/camo.png").convert_alpha(), SCALE),
            "pierce": pygame.transform.scale_by(pygame.image.load_extended(
                f"{path}/upgrade_icons/pierce.png").convert_alpha(),
                                                SCALE),
            "max": pygame.transform.scale_by(pygame.image.load_extended(
                f"{path}/upgrade_icons/max.png").convert_alpha(), SCALE),
            "ability": pygame.transform.scale_by(
                pygame.image.load_extended(
                    f"{path}/upgrade_icons/ability.png").convert_alpha(),
                SCALE)}
        self.locked: pygame.Surface = pygame.transform.scale_by(
            pygame.image.load_extended(f"{path}/locked.png").convert_alpha(), SCALE)

        self.HUD_upgrading: pygame.Surface = pygame.transform.scale_by(
            pygame.image.load_extended(f"{path}/HUD_upgrading.png").convert_alpha(),
            SCALE)
        self.HUD_white: pygame.Surface = pygame.transform.scale_by(
            pygame.image.load_extended(f"{path}/HUD_white.png").convert_alpha(),
            SCALE)
        self.HUD_black: pygame.Surface = pygame.transform.scale_by(
            pygame.image.load_extended(f"{path}/HUD_black.png").convert_alpha(),
            SCALE)
        self.HUD_icons: pygame.Surface = pygame.transform.scale_by(
            pygame.image.load_extended(f"{path}/HUD_icons.png").convert_alpha(),
            SCALE)
        self.spritesheet: pygame.Surface = pygame.transform.scale_by(
            pygame.image.load_extended(f"{path}/numbers.png").convert_alpha(),
            SCALE)
        self.fast_forward_indicator: pygame.Surface = pygame.transform.scale_by(
            pygame.image.load_extended(f"{path}/fast_forward.png").convert_alpha(),
            SCALE)
        self.sell_screen: pygame.Surface = pygame.transform.scale_by(
            pygame.image.load_extended(f"{path}/sell.png").convert_alpha(),
            SCALE)
        self.upgrade_background_3: pygame.Surface = self.createBackground(
            pygame.Surface((17 * SCALE, 7 * SCALE), pygame.SRCALPHA).convert_alpha(), (255, 205, 0))
        self.upgrade_background_4: pygame.Surface = self.createBackground(
            pygame.Surface((22 * SCALE, 7 * SCALE), pygame.SRCALPHA).convert_alpha(), (255, 205, 0))
        self.upgrade_background_5: pygame.Surface = self.createBackground(
            pygame.Surface((27 * SCALE, 7 * SCALE), pygame.SRCALPHA).convert_alpha(), (255, 205, 0))
        self.upgrade_backgrounds: List[pygame.Surface] = [self.upgrade_background_3, self.upgrade_background_4,
                                                          self.upgrade_background_5]
        self.upgrade_cost_positions: List[float] = [7, 4.5, 2]
        self.upgrade_sell: pygame.Surface = self.createBackground(
            pygame.Surface((23 * SCALE, 9 * SCALE), pygame.SRCALPHA).convert_alpha(), (255, 205, 0))
        self.numbers: List[pygame.Surface] = [
            self.get_image(self.spritesheet, (4) * SCALE, 5 * SCALE, i * 4 * SCALE - SCALE) for i in
            range(1, 11)]
        self.numbers.insert(1, self.get_image(self.spritesheet, (3) * SCALE, 5 * SCALE, 0))
        self.counter: int = 1
        self.money: int = 0
        self.health: int = 0
        self.round: int = 0
        self.sell: bool = False
        self.round_text: pygame.Surface = self.createNumber(self.round, 0)
        self.money_text: pygame.Surface = self.createNumber(self.money, 0)
        self.health_text: pygame.Surface = self.createNumber(self.health, 3)

    def colour_swap(self, image: pygame.Surface, old_colour: Tuple[int, int, int],
                    new_colour: Tuple[int, int, int]) -> pygame.Surface:
        color_mask: pygame.mask.Mask = pygame.mask.from_threshold(image, old_colour, threshold=(1, 1, 1, 255))
        color_change_surf: pygame.Surface = color_mask.to_surface(setcolor=new_colour, unsetcolor=(0, 0, 0, 0))
        img_copy: pygame.Surface = image.copy()
        img_copy.blit(color_change_surf, (0, 0))
        return img_copy

    def setDifficulty(self, difficulty: str) -> None:
        if difficulty == "easy":
            self.difficulty_multiplier: float = 1
        elif difficulty == "medium":
            self.difficulty_multiplier = 1.15
        else:
            self.difficulty_multiplier = 1.3

    def seperate_sheet(self, sheet: pygame.Surface, width: int) -> List[pygame.Surface]:
        images: List[pygame.Surface] = []
        amount: int = sheet.get_width() // width
        for i in range(amount):
            image: pygame.Surface = pygame.Surface((width, width), pygame.SRCALPHA).convert_alpha()
            image.blit(sheet, (0, 0), (width * i, 0, width, width))
            images.append(image)
        return images

    def get_image(self, surface: pygame.Surface, width: int, height: int, start: int) -> pygame.Surface:
        image: pygame.Surface = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
        image.blit(surface, (0, 0), (start, 0, width, height))
        return image

    def initialiseHud(self, layer: pygame.Surface) -> None:
        layer.blit(self.HUD_black, (0, 0))
        layer.blit(self.HUD_white, (0, 0))
        layer.blit(self.HUD_icons, (0, 0))

    def updateHealth(self, health: int) -> None:
        self.health = health
        self.health_text = self.createNumber(self.health, 3)

    def updateMoney(self, money: int) -> None:
        self.money = money
        self.money_text = self.createNumber(self.money, 0)

    def updateRound(self, round: int, set: bool = False) -> None:
        if not set:
            self.round += round
        else:
            self.round = round
        self.round_text = self.createNumber(self.round, 0)

    def createBackground(self, surface: pygame.Surface, color: Tuple[int, int, int]) -> pygame.Surface:
        surface.fill(color)
        surface.fill((0, 0, 0), (0, 0, SCALE, SCALE))
        surface.fill((0, 0, 0), (surface.get_width() - SCALE, 0, SCALE, SCALE))
        surface.fill((0, 0, 0), (surface.get_width() - SCALE, surface.get_height() - SCALE, SCALE, SCALE))
        surface.fill((0, 0, 0), (0, surface.get_height() - SCALE, SCALE, SCALE))
        surface.set_colorkey((0, 0, 0))
        return surface

    def createTowerSelect(self) -> pygame.Surface:
        surface = pygame.Surface((31 * SCALE, 93 * SCALE), pygame.SRCALPHA).convert_alpha()
        for tower in self.tower_dict.values():
            if not tower["locked"]:
                if round(tower["cost"] * self.difficulty_multiplier) > self.money:
                    surface.blit(tower["icon_red"], tower["pos"])
                else:
                    surface.blit(tower["icon_green"], tower["pos"])
            else:
                surface.blit(self.locked, tower["pos"])
        return surface

    def createTowerUpgrade(self, Tower: 'Tower') -> pygame.Surface:
        self.Tower = Tower
        surface = pygame.Surface((self.HUD_upgrading.get_width(), self.HUD_upgrading.get_height()))
        surface.blit(self.HUD_upgrading, (0, 0))
        path_one = self.Tower.upgrades["path_one"]
        path_two = self.Tower.upgrades["path_two"]
        for path_name, upgrade, y_pos in [("path_one", path_one, 11), ("path_two", path_two, 45)]:
            icon_position = (6 * SCALE, 20 * SCALE) if path_name == "path_one" else (6 * SCALE, 54 * SCALE)

            other_path = ["path_one", "path_two"][(["path_one", "path_two"].index(path_name) + 1) % 2]
            if upgrade == 4 or (upgrade == 2 and self.Tower.upgrades[other_path] > 2):
                surface.blit(self.upgrade_icons["max"], icon_position)
            else:
                upgrade_info = self.Tower.data[path_name][str(upgrade + 1)]
                cost = round(upgrade_info["cost"] * self.difficulty_multiplier)
                text = self.createNumber(cost, 0)
                length = len(str(cost))
                surface.blit(self.upgrade_backgrounds[length - 3],
                             (round(self.upgrade_cost_positions[length - 3] * SCALE), y_pos * SCALE))
                surface.blit(text, (self.upgrade_cost_positions[length - 3] * SCALE + 2 * SCALE, (y_pos + 1) * SCALE))
                if upgrade_info["name"]:
                    surface.blit(self.upgrade_icons["ability"], icon_position)
                else:
                    surface.blit(self.upgrade_icons[upgrade_info["stat_change"][0]["stat"]], icon_position)

        return surface

    def drawRange(self, layer: pygame.Surface) -> None:
        pygame.draw.circle(layer, (50, 50, 50, 20), self.Tower.rect.center, self.Tower.data["range"] * SCALE)

    def setSell(self, value: bool) -> None:
        self.sell = value

    def sellMenu(self) -> Union[int, str]:
        mouse = pygame.mouse.get_pos()
        main_box = pygame.Rect(127 * SCALE, 10 * SCALE, 33 * SCALE, 110 * SCALE)
        sell = pygame.Rect(131 * SCALE, 77 * SCALE, 25 * SCALE, 11 * SCALE)
        if main_box.collidepoint(mouse):
            if sell.collidepoint(mouse):
                self.sell = False
                total_cost = self.Tower.sell()
                self.Tower = None
                self.upgrade = False
                return total_cost
        else:
            self.upgrade = False
            self.sell = False
            return "main"

    def createSell(self) -> pygame.Surface:
        cost = round(self.Tower.total_cost * 0.7)
        surface = self.sell_screen
        text = self.createNumber(cost, 0)
        length = len(str(cost))
        surface.blit(self.upgrade_backgrounds[length - 3],
                     (round(self.upgrade_cost_positions[length - 3] * SCALE), 40 * SCALE))
        surface.blit(text, (self.upgrade_cost_positions[length - 3] * SCALE + 2 * SCALE, (40 + 1) * SCALE))
        return surface

    def updateHud(self, layer: pygame.Surface) -> None:
        layer.fill((255, 255, 255, 0))
        if self.upgrade and self.Tower:
            self.drawRange(layer)
        self.initialiseHud(layer)
        self.counter += 1

        if self.sell:
            layer.blit(self.createSell(), (128 * SCALE, 11 * SCALE))
        elif not self.upgrade:
            layer.blit(self.HUD_black, (0, 0))
            layer.blit(self.createTowerSelect(), (129 * SCALE, 12 * SCALE))
        else:
            layer.blit(self.createTowerUpgrade(self.Tower), (128 * SCALE, 11 * SCALE))
        if self.speedup:
            layer.blit(self.fast_forward_indicator, (145 * SCALE, 106 * SCALE))
        layer.blit(self.round_text, (116 * SCALE - self.round_text.get_width(), 3 * SCALE))
        layer.blit(self.health_text, (12 * SCALE, 3 * SCALE))
        layer.blit(self.money_text, (39 * SCALE, 3 * SCALE))

    def getUpgrading(self) -> bool:
        return self.upgrade

    def createNumber(self, number: int, length: int) -> pygame.Surface:
        padded_number = ("0" * (length - len(str(number))) if length - len(str(number)) >= 0 else "") + str(number)
        sizes = [5 * SCALE if i != "1" else 4 * SCALE for i in padded_number]
        image_size = sum(sizes)
        surface = pygame.Surface((image_size, 5 * SCALE), pygame.SRCALPHA).convert_alpha()
        for i, number in enumerate(padded_number):
            surface.blit(self.numbers[int(number)], (sum(sizes[0:i]), 0))
        return surface

    def sellClicked(self) -> Optional[str]:
        mouse = pygame.mouse.get_pos()
        sell = pygame.Rect(131 * SCALE, 90 * SCALE, 25 * SCALE, 11 * SCALE)
        if sell.collidepoint(mouse) and self.upgrade:
            self.sell = True
            return "sell"

    def getSell(self) -> bool:
        return self.sell

    def upgradeChosen(self, layer: pygame.Surface) -> Union[str, None]:
        mouse = pygame.mouse.get_pos()
        main_box = pygame.Rect(127 * SCALE, 10 * SCALE, 33 * SCALE, 110 * SCALE)
        path_one = pygame.Rect(132 * SCALE, 29 * SCALE, 23 * SCALE, 23 * SCALE)
        path_two = pygame.Rect(132 * SCALE, 63 * SCALE, 23 * SCALE, 23 * SCALE)
        if main_box.collidepoint(mouse):
            if path_one.collidepoint(mouse):
                return "path_one"
            elif path_two.collidepoint(mouse):
                return "path_two"
            return "main"

    def play(self) -> bool:
        mouse = pygame.mouse.get_pos()
        play = pygame.Rect(128 * SCALE, 105 * SCALE, 15 * SCALE, 14 * SCALE)
        if play.collidepoint(mouse):
            return True

    def setUpgrading(self, value: bool) -> None:
        self.upgrade = value

    def tower_chosen(self) -> Optional[str]:
        mouse = pygame.mouse.get_pos()
        for tower, info in self.tower_dict.items():
            if not info["locked"] and info["rect"].collidepoint(
                    (mouse[0] - 129 * SCALE, mouse[1] - 12 * SCALE)) and not self.upgrade:
                if self.money >= round(info["cost"] * self.difficulty_multiplier):
                    return tower

    def disableSpeed(self, layer: pygame.Surface) -> None:
        self.HUD_icons = self.colour_swap(self.HUD_icons, (120, 195, 0), (60, 60, 60))
        self.HUD_icons = self.colour_swap(self.HUD_icons, (180, 255, 0), (180, 180, 180))
        self.HUD_icons = self.colour_swap(self.HUD_icons, (150, 225, 0), (120, 120, 120))
        self.fast_forward_indicator = self.colour_swap(self.fast_forward_indicator, (180, 255, 0), (180, 180, 180))
        layer.blit(self.HUD_icons, (0, 0))

    def enableSpeed(self, layer: pygame.Surface) -> None:
        self.HUD_icons = self.colour_swap(self.HUD_icons, (60, 60, 60), (120, 195, 0))
        self.HUD_icons = self.colour_swap(self.HUD_icons, (180, 180, 180), (180, 255, 0))
        self.HUD_icons = self.colour_swap(self.HUD_icons, (120, 120, 120), (150, 225, 0))
        self.fast_forward_indicator = self.colour_swap(self.fast_forward_indicator, (180, 180, 180), (180, 255, 0))
        layer.blit(self.HUD_icons, (0, 0))

    def fastForward(self) -> bool:
        mouse = pygame.mouse.get_pos()
        fast_forward = pygame.Rect(144 * SCALE, 105 * SCALE, 15 * SCALE, 14 * SCALE)
        if fast_forward.collidepoint(mouse):
            self.speedup = not self.speedup
            return True
