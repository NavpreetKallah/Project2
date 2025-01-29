import random
import os
from builtins import property
from typing import Dict, Any


class Round:
    def __init__(self) -> None:
        self.current_round: int = 0
        self.roundValue: int = 30 * self.current_round
        self.valueLeft: int = self.roundValue
        self.enemies: Dict[str, Any] = None
        min_delay: float = 0.1
        change: float = 0.01
        max_delay: float = 0.2
        self.enemy_creator: Dict[str, Dict[str, float]] = {
            "red": {"cost": 1, "weight": 1, "min_delay": min_delay + change * 9, "max_delay": max_delay + change * 9},
            "blue": {"cost": 2, "weight": 2, "min_delay": min_delay + change * 8, "max_delay": max_delay + change * 8},
            "green": {"cost": 3, "weight": 6, "min_delay": min_delay + change * 7, "max_delay": max_delay + change * 7},
            "yellow": {"cost": 4, "weight": 12, "min_delay": min_delay + change * 6,
                       "max_delay": max_delay + change * 6},
            "pink": {"cost": 5, "weight": 24, "min_delay": min_delay + change * 5, "max_delay": max_delay + change * 5},
            "black": {"cost": 6, "weight": 48, "min_delay": min_delay + change * 4,
                      "max_delay": max_delay + change * 4},
            "white": {"cost": 6, "weight": 48, "min_delay": min_delay + change * 3,
                      "max_delay": max_delay + change * 3},
            "zebra": {"cost": 15, "weight": 96, "min_delay": min_delay + change * 1,
                      "max_delay": max_delay + change * 1},
            "purple": {"cost": 16, "weight": 96, "min_delay": min_delay + change * 2,
                       "max_delay": max_delay + change * 2},
            "lead": {"cost": 20, "weight": 48, "min_delay": min_delay + change * 1,
                     "max_delay": max_delay + change * 1},
            "rainbow": {"cost": 30, "weight": 96, "min_delay": min_delay + change * 1,
                        "max_delay": max_delay + change * 1},
            "ceramic": {"cost": 60, "weight": 200, "min_delay": min_delay, "max_delay": max_delay},
            "moab": {"cost": 240, "weight": 40, "min_delay": min_delay, "max_delay": max_delay},
            "bfb": {"cost": 500, "weight": 40, "min_delay": min_delay, "max_delay": max_delay},
            "zomg": {"cost": 2000, "weight": 20, "min_delay": min_delay * 7, "max_delay": max_delay * 7},
        }

        self.enemy_spawn_rounds: list[int] = [1, 2, 6, 11, 15, 20, 22, 25, 26, 28, 35, 38, 50, 70, 90]
        self.round_started: bool = False
        self.speedup: bool = False

    def getCurrent(self) -> int:
        return self.current_round

    def speedChange(self) -> None:
        speed: float = 3 if self.speedup else 1 / 3
        self.speedup = not self.speedup
        for info in self.enemy_creator.values():
            info["min_delay"] *= speed
            info["max_delay"] *= speed

    def calculateValue(self) -> int:
        if self.current_round < 40:
            return 35
        elif self.current_round < 60:
            return 70
        elif self.current_round < 70:
            return 100
        elif self.current_round < 80:
            return 250
        elif self.current_round < 100:
            return 500
        else:
            return 2000

    def forceRound(self, round_number: int) -> None:
        for _ in range(round_number):
            self.current_round += 1
            self.increaseDifficulty()

    def roundWin(self, manager: Any) -> None:
        for _ in range(1):
            self.current_round += 1
            self.increaseDifficulty()
            self.valueLeft = self.current_round * self.calculateValue()
        self.generateEnemies(manager)

    def reset(self) -> None:
        self.current_round = 0

    def increaseDifficulty(self) -> None:
        max_enemies: int = len([i for i in self.enemy_spawn_rounds if i <= self.current_round])
        enemy_names: list[str] = list(self.enemy_creator.keys())[:max_enemies]
        self.enemy_creator[enemy_names[-1]]["weight"] *= 1.1

    def calculateProbabilities(self, value: int) -> str:
        max_enemies: int = len([i for i in self.enemy_spawn_rounds if i <= self.current_round])
        enemy_data = list(self.enemy_creator.values())[:max_enemies + value]
        enemy_names: list[str] = list(self.enemy_creator.keys())[:max_enemies + value]
        total_weight: float = sum(enemy["weight"] for enemy in enemy_data)
        probabilities: list[float] = [data["weight"] / total_weight for data in enemy_data]
        return random.choices(list(enemy_names), probabilities, k=1)[0]

    def generateEnemies(self, manager: Any) -> None:
        if self.current_round in [40, 60, 80]:
            if self.current_round == 40:
                colour: str = "moab"
            elif self.current_round == 60:
                colour: str = "bfb"
            elif self.current_round == 80:
                colour: str = "zomg"
            manager.create(self.enemies[colour], self.generateDelay(colour), self.generateProperties(colour),
                           self.current_round)
        else:
            for i in range(0, -len([i for i in self.enemy_spawn_rounds if i <= self.current_round]), -1):
                colour: str = self.calculateProbabilities(i)
                enemy: int = self.enemy_creator[colour]["cost"]
                if self.valueLeft - enemy >= 0:
                    self.valueLeft -= enemy
                    manager.create(self.enemies[colour], self.generateDelay(colour), self.generateProperties(colour),
                                   self.current_round)
                    self.generateEnemies(manager)
                    break

    def generateDelay(self, colour: str) -> float:
        return random.uniform(self.enemy_creator[colour]["min_delay"], self.enemy_creator[colour]["max_delay"])

    def generateProperties(self, colour: str) -> Dict[str, bool]:
        properties: Dict[str, bool] = {"camo": False, "regen": False}
        if colour not in ["moab", "bfb", "zomg"]:
            if self.current_round >= 24:
                if random.randint(self.current_round, max(75, self.current_round)) == max(75, self.current_round):
                    properties["camo"] = True
            if self.current_round >= 17:
                if random.randint(self.current_round, max(75, self.current_round)) == max(75, self.current_round):
                    properties["regen"] = True
        return properties

    @property
    def getStarted(self) -> bool:
        return self.round_started

    def startRound(self, manager: Any) -> None:
        self.enemies = manager.getEnemyStats()
        self.round_started = True
        self.roundWin(manager)
