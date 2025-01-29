import pygame
from typing import List


class TextInput:
    def __init__(self):
        self.text: str = ""

    def create(self, events: List[pygame.event.Event]) -> bool:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif 'unicode' in event.__dict__.keys() and event.unicode.lower() in "abcdefghijklmnopqrstuvwxyz0123456789":
                    self.text += event.unicode
                elif event.key == pygame.K_RETURN:
                    return True
        return False
