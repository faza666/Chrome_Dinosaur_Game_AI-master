import pygame
import os

# Global Constants

# Screen
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1400
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

local_directory = os.path.dirname(__file__)

# Images
RUNNING = [pygame.image.load(os.path.join(local_directory, "../Assets/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join(local_directory, "../Assets/Dino", "DinoRun2.png"))]

JUMPING = pygame.image.load(os.path.join(local_directory, "../Assets/Dino", "DinoJump.png"))

DUCKING = [pygame.image.load(os.path.join(local_directory, "../Assets/Dino", "DinoDuck1.png")),
           pygame.image.load(os.path.join(local_directory, "../Assets/Dino", "DinoDuck2.png"))]

SMALL_CACTUS = [pygame.image.load(os.path.join(local_directory, "../Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join(local_directory, "../Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join(local_directory, "../Assets/Cactus", "SmallCactus3.png"))]

LARGE_CACTUS = [pygame.image.load(os.path.join(local_directory, "../Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join(local_directory, "../Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join(local_directory, "../Assets/Cactus", "LargeCactus3.png"))]

BIRD = [pygame.image.load(os.path.join(local_directory, "../Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join(local_directory, "../Assets/Bird", "Bird2.png"))]

CLOUD = pygame.image.load(os.path.join(local_directory, "../Assets/Other", "Cloud.png"))

BG = pygame.image.load(os.path.join(local_directory, "../Assets/Other", "Track.png"))
