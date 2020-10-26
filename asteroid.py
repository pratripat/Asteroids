import pygame
import math
import random
from collinear import *

class Asteroid:
    def __init__(self, width, height, pos=None, r=50):
        self.pos = pos

        #Setting random direction vector
        self.vel = pygame.math.Vector2(random.uniform(0, 1), random.uniform(0, 1)).rotate(random.randrange(360))

        self.r = r
        self.total_points = 10
        self.maxoffset = self.r * 2//3
        self.offsets = []

        self.S_WIDTH = width
        self.S_HEIGHT = height

        self.position(pos)
        self.set_random_offsets()
        self.re_calculate_points()

    def position(self, pos):
        if self.pos != None:
            #Copying the position given
            self.pos = pygame.math.Vector2(pos.x, pos.y)
            return

        #If there is no initial position, create a random one
        self.pos = pygame.math.Vector2(random.randrange(self.S_WIDTH), random.randrange(self.S_HEIGHT))

    def set_random_offsets(self):
        for i in range(self.total_points):
            #Calculating the random offsets
            v = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
            v *= random.randrange(0, self.maxoffset)

            self.offsets.append(v)

    def create_points(self):
        a = 0
        points = []

        for i in range(self.total_points):
            #Calculating all the points with the offset
            v = pygame.math.Vector2(math.cos(a), math.sin(a))
            v *= self.r
            v += self.offsets[i]
            v += self.pos

            points.append(v)

            a += math.radians(360 / self.total_points)

        return points

    def re_calculate_points(self):
        #Just calculating the points
        self.points = self.create_points()

    def show(self, surface):
        #Drawing the polygon
        pygame.draw.polygon(surface, (255, 255, 255), self.points, 1)

    def move(self):
        self.pos += self.vel
        self.re_calculate_points()

    def edges(self):
        #Making the asteroid stay in the screen
        sum_r = self.r + self.maxoffset

        if self.pos.x -sum_r > self.S_WIDTH:
            self.pos.x = -sum_r
        elif self.pos.x + sum_r < 0:
            self.pos.x = self.S_WIDTH + sum_r

        if self.pos.y -sum_r > self.S_HEIGHT:
            self.pos.y = -sum_r
        elif self.pos.y + sum_r < 0:
            self.pos.y = self.S_HEIGHT + sum_r

    def is_hit(self, object_pos, is_laser=False):
        #Checking if the object is hitting the asteroid
        for i in range(len(self.points)):
            point1 = self.points[i]
            point2 = self.points[(i+1) % len(self.points)]

            distance = self.pos.distance_to(object_pos)

            r = self.r - self.offsets[i].magnitude()
            if is_laser:
                r = self.r + self.offsets[i].magnitude()

            condition1 = is_collinear(point1, point2, object_pos)
            condition2 = distance < r

            if condition1 or condition2:
                return True

        return False

    def break_up(self):
        new_asteroids = []

        for i in range(2):
            #Making smaller asteroids on breaking but only if the new radius is not very small
            if self.r // 2 > 5:
                asteroid = Asteroid(self.S_WIDTH, self.S_HEIGHT, self.pos, self.r//2)
                new_asteroids.append(asteroid)

        return new_asteroids
