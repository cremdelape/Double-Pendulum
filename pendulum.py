import pygame
import math
from conf import *

vec = pygame.math.Vector2


# noinspection PyArgumentList
class DoublePendulum:
    def __init__(self, screen, trail_screen):
        self.screen = screen
        self.trail_screen = trail_screen
        self.g = g
        # Start is the fixed point to which the first pendulum connected
        self.start = vec(START_POS)
        # Length of the strings
        self.l1 = LENGTH1
        self.l2 = LENGTH2
        # Mass of the bobs
        self.m1 = MASS1
        self.m2 = MASS2
        # The angle of the pendulums(angles are measured in radians)
        self.ang1 = math.pi / 2
        self.ang2 = -math.pi / 3
        # The position of the bobs
        self.pos1 = self.start + vec(self.l1 * math.sin(self.ang1), self.l1 * math.cos(self.ang1))
        self.pos2 = self.pos1 + vec(self.l2 * math.sin(self.ang2), self.l2 * math.cos(self.ang2))
        # Angular Velocity
        self.vel1 = 0
        self.vel2 = 0
        # Angular Accelration
        self.acc1 = 0
        self.acc2 = 0
        self.unstable = False

    def update_values(self, changes):
        self.g = changes[0]
        self.m1 = changes[1]
        self.m2 = changes[2]
        self.l1 = changes[3]
        self.l2 = changes[4]

    def update(self):
        # Calculating the angular acceleration using langrange's equations
        try:
            num1a = -self.g * (2 * self.m1 + self.m2) * math.sin(self.ang1)
            num1b = -self.m2 * self.g * math.sin(self.ang1 - 2 * self.ang2)
            num1c = -2 * math.sin(self.ang1 - self.ang2) * self.m2
            num1d = self.vel1 ** 2 * self.l2 + self.vel2 ** 2 * self.l1 * math.cos(self.ang1 - self.ang2)
            den1 = self.l1 * (2 * self.m2 + self.m2 - self.m2 * math.cos(2 * self.ang1 - 2 * self.ang2))
            num2a = 2 * math.sin(self.ang1 - self.ang2)
            num2b = self.vel1 ** 2 * self.l1 * (self.m1 + self.m2)
            num2c = self.g * (self.m1 + self.m2) * math.cos(self.ang1)
            num2d = self.vel2 ** 2 * self.l2 * self.m2 * math.cos(self.ang1 - self.ang2)
            den2 = self.l2 * (2 * self.m2 + self.m2 - self.m2 * math.cos(2 * self.ang1 - 2 * self.ang2))
            self.acc1 = (num1a + num1b + num1c * num1d) / den1
            self.acc2 = (num2a * (num2b + num2c + num2d)) / den2
            self.unstable = False
        except OverflowError:
            self.acc1 = 0
            self.acc2 = 0
            self.vel1 = 0.001
            self.vel2 = 0.001
            self.unstable = True

        # Adding the acceleration to the velocity
        self.vel1 = (self.vel1 + self.acc1)
        self.vel2 = (self.vel2 + self.acc2)

        # Changing the angles according to the velocity
        self.ang1 += self.vel1
        self.ang2 += self.vel2

    def move_bob(self):
        # Updating the bob positions
        self.pos1 = self.start + vec(self.l1 * math.sin(self.ang1), self.l1 * math.cos(self.ang1))
        self.pos2 = self.pos1 + vec(self.l2 * math.sin(self.ang2), self.l2 * math.cos(self.ang2))

    def draw_trail(self):
        i_pos2 = (int(self.pos2.x), int(self.pos2.y))
        pygame.draw.circle(self.trail_screen, RED, i_pos2, TRAIL_SIZE)

    def draw(self):
        i_pos1 = (int(self.pos1.x), int(self.pos1.y))
        i_pos2 = (int(self.pos2.x), int(self.pos2.y))
        i_pos3 = (int(self.start.x), int(self.start.y))
        pygame.draw.line(self.screen, BLUE, self.start, self.pos1, 5)
        pygame.draw.line(self.screen, BLUE, self.pos1, self.pos2, 5)
        pygame.draw.circle(self.screen, RED, i_pos1, self.m1 // 2)
        pygame.draw.circle(self.screen, RED, i_pos2, self.m2 // 2)
        pygame.draw.circle(self.screen, BLACK, i_pos3, 5)
