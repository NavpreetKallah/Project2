import os, json
from typing import Dict, List, Any, Optional

json_path = os.path.dirname(os.getcwd()) + "/game/data/save_data.json"


class SaveManager:
    def __init__(self):
        self.health: int = 0
        self.money: int = 0
        self.round: int = 0
        self.difficulty: Optional[str] = None
        self.map: Optional[str] = None
        self.towers: List[Any] = []
        self.beaten: bool = False
        self.others: Dict[str, Any] = self.other_users()

    def other_users(self) -> Dict[str, Any]:
        with open(f"{json_path}", "r") as file:
            data: Dict[str, Any] = json.load(file)
        return data

    def loadSave(self, username: str) -> Optional[Dict[str, Any]]:
        with open(f"{json_path}", "r") as file:
            data: Dict[str, Any] = json.load(file)
            if username in data:
                return data[username]
        return None

    def createDictionary(self) -> Dict[str, Any]:
        tower_data = []
        for tower in self.towers:
            tower_data.append({
                "name": tower.__class__.__name__,
                "pos": tower.pos,
                "upgrades": tower.upgrades
            })
        dict: Dict[str, Any] = {
            "health": self.health,
            "money": self.money,
            "round": self.round,
            "difficulty": self.difficulty,
            "map": self.map,
            "beaten": self.beaten,
            "towers": tower_data
        }
        return dict

    def updateSave(self, health: int, money: int, round: int, difficulty: Optional[str], map: Optional[str],
                   towers: List[Any], beaten: bool):
        self.health = health
        self.money = money
        self.round = round
        self.difficulty = difficulty
        self.map = map
        self.towers = towers
        self.beaten = beaten

    def saveToFile(self, username: str):
        self.others[username] = self.createDictionary()
        output: str = json.dumps(self.others, indent=4)
        with open(f"{json_path}", "w") as file:
            file.write(output)

    def resetSave(self, username: str):
        self.others[username] = {"beaten": self.beaten}
        output: str = json.dumps(self.others, indent=4)
        with open(f"{json_path}", "w") as file:
            file.write(output)
