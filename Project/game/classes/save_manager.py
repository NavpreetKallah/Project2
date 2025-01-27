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
        self.others = self.other_users()
    def other_users(self):
        with open(f"{json_path}", "r") as file:
            data = json.load(file)
        return data

    def loadSave(self, username):
        with open(f"{json_path}", "r") as file:
            data = json.load(file)
            if username in data:
                return data[username]


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

    def saveToFile(self, username):
        self.others[username] = self.createDictionary()
        output = json.dumps(self.others, indent=4)
        with open(f"{json_path}", "w") as file:
            file.write(output)

    def resetSave(self, username):
        self.others[username] = {}
        output = json.dumps(self.others, indent=4)
        with open(f"{json_path}", "w") as file:
            file.write(output)
