import random
import pygame
from .constants import SCREEN_WIDTH


class Obstacle:
    def __init__(self, image, type_):
        self.image = image
        self.type = type_
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self, game):
        self.rect.x -= game.game_speed
        if self.rect.x < -self.rect.width:
            game.obstacles.pop()

    def draw(self, screen):
        screen.blit(self.image[self.type], self.rect)
        # pygame.draw.rect(screen, BLACK, (self.rect.x, self.rect.y, self.rect.width, self.rect.height), 2)

    def get_mask(self):
        return pygame.mask.from_surface(self.image[self.type])


class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325


class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300


class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0

    def draw(self, screen):
        if self.index >= 9:
            self.index = 0
        screen.blit(self.image[self.index // 5], self.rect)
        # pygame.draw.rect(screen, BLACK, (self.rect.x, self.rect.y, self.rect.width, self.rect.height), 2)
        self.index += 1
