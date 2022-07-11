import pygame
import random
from .constants import DUCKING, RUNNING, JUMPING, SCREEN


class Dinosaur:
    x_pos = 80
    y_pos = 310
    y_pos_duck = 340
    start_jump_velocity = 8.0

    def __init__(self):
        # Images
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        # Dino states
        self.dino_run = True
        self.dino_jump = False
        self.dino_duck = False

        self.step_index = 0
        self.image = self.run_img[0]
        self.current_jump_vel = self.start_jump_velocity

        self.dino_rect = self.image.get_rect()
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        self.dino_rect.x = self.x_pos
        self.dino_rect.y = self.y_pos
        self.eye = self.dino_rect.x + 54, self.dino_rect.y + 12

    def update(self):
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()
        if self.dino_duck:
            self.duck()

        if self.step_index >= 9:
            self.step_index = 0

        # Keyboard control
        # if user_input[pygame.K_UP] or user_input[pygame.K_SPACE] and not self.dino_jump:
        #     self.dino_duck = False
        #     self.dino_run = False
        #     self.dino_jump = True
        # elif user_input[pygame.K_DOWN] and not self.dino_jump:
        #     self.dino_duck = True
        #     self.dino_run = False
        #     self.dino_jump = False
        # elif not (self.dino_jump or user_input[pygame.K_DOWN]):
        #     self.dino_duck = False
        #     self.dino_run = True
        #     self.dino_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.x_pos
        self.dino_rect.y = self.y_pos_duck
        self.step_index += 1
        self.eye = self.dino_rect.x + 85, self.dino_rect.y + 12

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.x_pos
        self.dino_rect.y = self.y_pos
        self.step_index += 1
        self.eye = self.dino_rect.x + 54, self.dino_rect.y + 12

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump and self.current_jump_vel <= self.start_jump_velocity:
            self.dino_rect.y -= self.current_jump_vel * 4
            self.current_jump_vel -= self.start_jump_velocity / 10
            self.eye = self.dino_rect.x + 54, self.dino_rect.y + 12
        if self.current_jump_vel <= - self.start_jump_velocity:
            self.dino_jump = False
            self.dino_run = True
            self.current_jump_vel = self.start_jump_velocity
            self.dino_rect.y = self.y_pos
            self.eye = self.dino_rect.x + 54, self.dino_rect.y + 12

    def draw(self, screen, game_):
        screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))
        pygame.draw.rect(
            screen, self.color, (self.dino_rect.x, self.dino_rect.y, self.dino_rect.width, self.dino_rect.height), 2
        )
        for obstacle in game_.obstacles:
            pygame.draw.line(
                SCREEN, self.color, self.eye, obstacle.rect.center, 2
            )

    def get_mask(self):
        return pygame.mask.from_surface(self.image)

    def passed_obstacle(self, obstacle):
        if self.x_pos > obstacle.rect.x + obstacle.rect.width:
            return True
