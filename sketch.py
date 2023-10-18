import os
import pickle
import random
import time

import neat
import pygame
import visualize

pygame.font.init()  # init font

WIN_WIDTH = 600
WIN_HEIGHT = 800

pipe_img = pygame.transform.scale2x(
    pygame.image.load(os.path.join("resources/imgs", "pipe.png")).convert_alpha()
)
bg_img = pygame.transform.scale(
    pygame.image.load(os.path.join("resources/imgs", "bg.png")).convert_alpha(),
    (600, 900),
)
bird_images = [
    pygame.transform.scale2x(
        pygame.image.load(os.path.join("resources/imgs", "bird" + str(x) + ".png"))
    )
    for x in range(1, 4)
]

base_img = pygame.transform.scale2x(
    pygame.image.load(os.path.join("resources/imgs", "base.png")).convert_alpha()
)

gen = 0


class Bird:
    IMGS = bird_images
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        # starting position
        self.x = x
        self.y = y
        self.tilt = 0  # rotation of the bird
        self.tick_count = 0  # for the physics
        self.vel = 0  # vertical velocity
        self.height = y  # for the physics
        self.img_count = 0  # to select images
        self.img = bird_images[0]

    def jump(self):
        self.vel = -10.5  # like in p5 the top-left corner = (0,0)
        self.height = self.y
        self.tick_count = 0

    def move(self):
        self.tick_count += 1  # acts like the time
        d = self.vel * self.tick_count + 1.5 * (self.tick_count) ** 2
        # tick = 0 >-10.5 + 1.5 = -9 (go up)
        # tick = 1 >-10.5(2) + 1.5(4) = -15 (go up)
        # tick = 6 >-10.5(6) + 1.5(36) = - 9 (go up)
        # tick = 7 >-10.5(7) + 1.5(49) = 0 (go up)
        # tick = 8 >-10.5(8) + 1.5(64) = 9 (go down)
        # nice function, it jumps and then starts to fall
        d = min(d, 16)  # cap the velocity
        if d < 0:
            d -= 2  # extrapower for jumping
        self.y = self.y + d


bird = Bird(25, 200)
while True:
    bird.move()
