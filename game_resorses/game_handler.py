import pygame
from .constants import SCREEN, BLACK


class GameHandler:
    def __init__(self):
        self.death_count = 0
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.current_generation = 0
        self.high_score = 0
        self.high_score_generation = 0
        self.high_fitness = 0
        self.high_fitness_generation = 0

    def show_statistics(self, current_generation, points, fitness):
        if points > self.high_score:
            self.high_score_generation = current_generation
            self.high_score = points

        if fitness > self.high_fitness:
            self.high_fitness_generation = current_generation
            self.high_fitness = fitness

        record_score_text = self.font.render(f'Record score:  {self.high_score}', True, BLACK)
        record_generation_text = self.font.render(f'With generation:  {self.high_score_generation}', True, BLACK)

        current_generation_text = self.font.render(f'Current generation:  {current_generation}', True, BLACK)

        current_fitness_text = self.font.render(f'Current fitness:  {fitness}', True, BLACK)
        record_fitness_text = self.font.render(f'Record fitness:  {self.high_fitness}', True, BLACK)
        record_fitness_generation_text = self.font.render(
            f'With generation:  {self.high_fitness_generation}', True, BLACK
        )

        SCREEN.blit(record_score_text, (300, 50))
        SCREEN.blit(record_generation_text, (300, 70))

        SCREEN.blit(current_generation_text, (50, 480))

        SCREEN.blit(current_fitness_text, (1000, 450))
        SCREEN.blit(record_fitness_text, (1000, 480))
        SCREEN.blit(record_fitness_generation_text, (1000, 510))
