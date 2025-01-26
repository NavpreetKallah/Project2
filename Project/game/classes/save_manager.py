import pygame, os, json
from game.config import SCALE

json_path = os.path.dirname(os.getcwd()) + "/game/data/save_data.json"
class SaveManager:
    def __init__(self):
        self.health = 0
        self.money = 0
        self.round = 0
        self.difficulty = None
        self.game_mode = None
        self.map = None
        self.towers = []

    def loadSave(self):
        with open(f"{json_path}", "r") as file:
            data = json.load(file)
        return data


    def createDictionary(self):
        dict = {"health": self.health,
                "money": self.money,
                "round": self.round,
                "difficulty": self.difficulty,
                "game_mode": self.game_mode,
                "map": self.map,
                "towers": [{"name": tower.__class__.__name__,
                            "pos": tower.pos,
                            "upgrades": tower.upgrades} for tower in self.towers]}
        return dict

    def updateSave(self, health, money, round, difficulty, game_mode, map, towers):
        self.health = health
        self.money = money
        self.round = round
        self.difficulty = difficulty
        self.game_mode = game_mode
        self.map = map
        self.towers = towers

    def saveToFile(self):
        output = json.dumps(self.createDictionary(), indent=4)
        with open(f"{json_path}", "w") as file:
            file.write(output)

    def resetSave(self):
        with open(f"{json_path}", "w") as file:
            file.write(json.dumps({}, indent=4))
