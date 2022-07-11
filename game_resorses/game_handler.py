import pygame
from .constants import SCREEN, BLACK


class GameHandler:
    def __init__(self):
        self.death_count = 0
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.current_generation = 0
        self.high_score = 0
        self.high_score_generation = 0

        self.training_mode = True

    def show_statistics(self, neat_obj, game):
        if game.points > self.high_score:
            self.high_score_generation = neat_obj.population.generation
            self.high_score = game.points

        record_text = self.font.render(f'Record:  {self.high_score}', True, BLACK)

        text_1 = self.font.render(f'Generation:  {neat_obj.population.generation}', True, BLACK)
        text_2 = self.font.render(f'With generation:  {self.high_score_generation}', True, BLACK)

        SCREEN.blit(text_1, (50, 480))
        SCREEN.blit(text_2, (300, 70))
        SCREEN.blit(record_text, (300, 50))
