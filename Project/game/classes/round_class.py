import random
from builtins import property


# , current_round: int, enemy_value: int, enemy_weightings: dict


class Round:
    def __init__(self):
        self.current_round = 1
        self.roundValue = 30 * self.current_round
        self.valueLeft = self.roundValue
        self.enemies = None
        min_delay = 0.1
        change = 0.01
        max_delay = 0.2
        self.enemy_creator = {"red": {"weight": 1, "min_delay": min_delay + change*9, "max_delay": max_delay + change*9},
                              "blue": {"weight": 2, "min_delay": min_delay + change*8, "max_delay": max_delay + change*8},
                              "green": {"weight": 3, "min_delay": min_delay + change*7, "max_delay": max_delay + change*7},
                              "yellow": {"weight": 4, "min_delay": min_delay + change*6, "max_delay": max_delay + change*6},
                              "pink": {"weight": 5, "min_delay": min_delay + change*5, "max_delay": max_delay + change*5},
                              "black": {"weight": 10, "min_delay": min_delay + change*4, "max_delay": max_delay + change*4},
                              "white": {"weight": 10, "min_delay": min_delay + change*3, "max_delay": max_delay + change*3},
                              "zebra": {"weight": 20, "min_delay": min_delay + change*1, "max_delay": max_delay + change*1},
                              "purple": {"weight": 10, "min_delay": min_delay + change*2, "max_delay": max_delay + change*2},
                              "lead": {"weight": 12, "min_delay": min_delay + change*1, "max_delay": max_delay + change*1},
                              "rainbow": {"weight": 40, "min_delay": min_delay + change*1, "max_delay": max_delay + change*1},
                              "ceramic": {"weight": 80, "min_delay": min_delay, "max_delay": max_delay},
                              "moab": {"weight": 80, "min_delay": min_delay*10, "max_delay": max_delay*10},
                              "bfb": {"weight": 80, "min_delay": min_delay*10, "max_delay": max_delay*10},
                              "zomg": {"weight": 80, "min_delay": min_delay*10, "max_delay": max_delay*10},
                              }

        self.probabilities = [100, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.round_started = False
        self.speedup = False
        self.weighting = [-20, 18, 2]
        self.base_probabilities = [100, 0, 0]

    def getCurrent(self):
        return self.current_round

    def increaseDifficulty(self):

        rangeStop = min(3, len(self.probabilities))

        for i in range(rangeStop):
            self.probabilities[i] += self.weighting[i]

        if self.probabilities[0] == 0:
            self.probabilities.pop(0)
            del self.enemy_creator[list(self.enemy_creator.keys())[0]]
            rangeStop = min(3, len(self.probabilities))

            if rangeStop == 2:
                self.base_probabilities = [100, 0]
                self.weighting = [-10, 10]

            if rangeStop == 1:
                self.base_probabilities = [100]
                self.weighting = [0]

            for i in range(rangeStop):
                self.probabilities[i] = self.base_probabilities[i]

    def speedChange(self):
        speed = 3 if self.speedup else 1 / 3
        self.speedup = not self.speedup
        for info in self.enemy_creator.values():
            info["min_delay"] = info["min_delay"] * speed
            info["max_delay"] = info["max_delay"] * speed

    def roundWin(self, manager):
        for _ in range(5):
            self.current_round += 1
            self.valueLeft = self.current_round * 30
            self.increaseDifficulty()
        self.generateEnemies(manager)

    def generateEnemies(self, manager):
        colour = random.choices(list(self.enemy_creator.keys()), self.probabilities, k=1)[0]
        enemy = self.enemy_creator[colour]["weight"]
        if self.valueLeft - enemy >= 0:
            self.valueLeft -= enemy
            manager.create(self.enemies[colour], self.generateDelay(colour))
            self.generateEnemies(manager)

    def generateDelay(self, colour):
        return random.uniform(self.enemy_creator[colour]["min_delay"], self.enemy_creator[colour]["max_delay"])
        # return 0.1

    @property
    def getStarted(self):
        return self.round_started

    def startRound(self, manager):
        self.enemies = manager.getEnemyStats()
        self.round_started = True
        self.roundWin(manager)
