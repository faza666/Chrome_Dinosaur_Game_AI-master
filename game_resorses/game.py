import random
import pygame
from .cloud import Cloud
from .constants import BG, SCREEN, BLACK, WHITE, SMALL_CACTUS, LARGE_CACTUS, BIRD
from neat_AI.neat_ import NEAT
from .obstacles import SmallCactus, LargeCactus, Bird


class GameMechanics:
    def __init__(self, neat_object, game_handler):
        self.game_speed = 14
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.points = 0
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.x_pos_bg = 0
        self.fitness = 0

        self.dinosaurs = []
        self.obstacles = []

        self.passed_bird = False
        self.passed_cactus = False

        self.neat_object = neat_object
        self.game_handler = game_handler

    def main_loop(self):
        clock = pygame.time.Clock()
        fps = 30
        cloud = Cloud()

        obstacle_type = None
        run_game = True
        while run_game:
            clock.tick(fps)
            current_fitness = []

            # Quit if 'QUIT' button is pressed
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run_game = False
                    pygame.quit()
                    quit()

            # Draw white screen
            SCREEN.fill(WHITE)

            # Create obstacle
            if len(self.obstacles) == 0:
                obstacle_type = random.randint(0, 2)
                if obstacle_type == 0:
                    self.obstacles.append(SmallCactus(SMALL_CACTUS))
                elif obstacle_type == 1:
                    self.obstacles.append(LargeCactus(LARGE_CACTUS))
                elif obstacle_type == 2:
                    self.obstacles.append(Bird(BIRD))

            # Draw and update dinosaurs' state
            for dinosaur in self.dinosaurs:
                dinosaur.draw(SCREEN, self)
                dinosaur.update()

            for i, dinosaur in enumerate(self.dinosaurs):
                # List of output nodes values (see config.txt, parameter 'num_outputs')
                output = NEAT.nets[i].activate(
                    # Tuple of input nodes values (see config.txt, parameter 'num_inputs')
                    (
                        dinosaur.dino_run,
                        self.obstacles[0].rect.x,
                        obstacle_type,
                        self.game_speed
                    )
                )
                # if values of output[0] and output[1] both less 0.5:
                # Run
                if output[0] < 0.5 > output[1] and not dinosaur.dino_jump:
                    dinosaur.dino_run = True
                    dinosaur.dino_jump = False
                    dinosaur.dino_duck = False

                # if value of output[0] less 0.5 and output[1] higher 0.5:
                # Jump
                if output[0] < 0.5 < output[1] and dinosaur.dino_rect.y == dinosaur.y_pos:
                    dinosaur.dino_run = False
                    dinosaur.dino_jump = True
                    dinosaur.dino_duck = False

                # if value of output[0] higher 0.5 and output[1] less 0.5:
                # Duck
                if output[0] > 0.5 > output[1] and not dinosaur.dino_jump:
                    dinosaur.dino_run = False
                    dinosaur.dino_jump = False
                    dinosaur.dino_duck = True

            for obstacle in self.obstacles:
                obstacle.draw(SCREEN)
                obstacle.update(self)

                for i, dinosaur in enumerate(self.dinosaurs):
                    if dinosaur.passed_obstacle(obstacle):
                        NEAT.genome_list[i].fitness += self.add_fitness(dinosaur, obstacle)
                        current_fitness.append(NEAT.genome_list[i].fitness)
                        self.fitness = max(current_fitness)

                    if NEAT.genome_list[i].fitness == self.neat_object.fitness_threshold:
                        run_game = False

                    # If collision or jump over Bird:
                    if self.get_collided(dinosaur, obstacle) or \
                            (
                                isinstance(obstacle, Bird) and
                                dinosaur.dino_rect.y < obstacle.rect.y and
                                dinosaur.x_pos >= obstacle.rect.x
                            ):
                        self.dinosaurs.pop(i)
                        self.neat_object.nets.pop(i)
                        NEAT.genome_list.pop(i)

            if len(self.dinosaurs) == 0:
                self.obstacles.clear()
                run_game = False

            cloud.draw(SCREEN)
            cloud.update(self)
            self.background()
            self.game_statistics()
            self.game_handler.show_statistics(self.neat_object.population.generation, self.points, self.fitness)

            pygame.display.update()

    def game_statistics(self):
        self.points += 1
        if self.points % 100 == 0 and self.game_speed < 70:
            self.game_speed += 1
            if self.game_speed == 70:
                self.game_speed = 20
        text = self.font.render(f'Score: {self.points}', True, BLACK)
        SCREEN.blit(text, (1000, 50))
        text_1 = self.font.render(f'Dinosaurs Alive:  {(len(self.dinosaurs))}', True, BLACK)
        text_2 = self.font.render(f'Game Speed:  {self.game_speed}', True, BLACK)

        SCREEN.blit(text_1, (50, 450))
        SCREEN.blit(text_2, (50, 510))

    def background(self):
        image_width = BG.get_width()
        SCREEN.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        SCREEN.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    @classmethod
    def get_collided(cls, dinosaur, obstacle):
        dino_mask = dinosaur.get_mask()
        obstacle_mask = obstacle.get_mask()
        offset = (dinosaur.dino_rect.x - obstacle.rect.x, dinosaur.dino_rect.y - obstacle.rect.y)
        collision_point = dino_mask.overlap(obstacle_mask, offset)
        if collision_point:
            return True
        return False

    def add_fitness(self, dino, obstacle):
        if dino.passed_obstacle(obstacle):
            if isinstance(obstacle, SmallCactus) or isinstance(obstacle, LargeCactus):
                self.passed_cactus = True
            elif isinstance(obstacle, Bird):
                self.passed_bird = True
        if self.passed_cactus and self.passed_bird:
            self.passed_cactus = False
            self.passed_bird = False
            return 1
        return 0
