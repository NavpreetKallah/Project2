from builtins import int

import pygame


class TextInput:
    def __init__(self):
        self.text = ""

    def create(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.unicode.lower() in "abcdefghijklmnopqrstuvwxyz0123456789":
                    self.text += event.unicode
                elif event.key == pygame.K_RETURN:
                    return True
        return False
