from laser import *
import pygame
import math

class Ship:
    def __init__(self, width, height):
        #Setting the position to the middle of the screen in the beginning with no velocity
        self.pos = pygame.math.Vector2(width/2, height/2)
        self.vel = pygame.math.Vector2()

        self.r = 20
        #self.n is the number of points the ship will have
        self.n = 3
        self.angle = -math.pi/2
        self.lasers = []

        self.S_WIDTH = width
        self.S_HEIGHT = height

        #Calculation the position of each point
        self.re_calculate_points()

    def create_points(self):
        a = self.angle
        points = []

        for i in range(self.n):
            v = pygame.math.Vector2(math.cos(a), math.sin(a))

            if i == 0:
                #Making the first point a little longer to show the beginning of the ship
                v *= self.r * 4/3
            else:
                v *= self.r

            #Shifting the vector according to own position
            v += self.pos

            points.append(v)

            a += math.radians(360 / self.n)

        return points

    def re_calculate_points(self):
        #Just calculation the points again
        self.points = self.create_points()

    def show(self, surface, asteroids):
        pygame.draw.polygon(surface, (255, 255, 255), self.points, 1)

        #Running all the functions of the lasers shot
        self.run_lasers(surface, asteroids)

    def move(self):
        self.pos += self.vel

        #Slowing down the ship slowly
        self.vel *= 0.99

    def forward_velocity(self):
        #Making the magnitude of the vector less
        return (self.points[0] - self.pos) / 5

    def boost(self):
        #Setting the velocity pointing forward
        self.vel = self.forward_velocity()

    def update(self):
        keys = pygame.key.get_pressed()

        #Turning the ship
        if keys[pygame.K_RIGHT]:
            self.angle += 0.1
        elif keys[pygame.K_LEFT]:
            self.angle -= 0.1

        #Mocing the ship forwards
        if keys[pygame.K_UP]:
            self.boost()

        #Calculating all the points of the ship again
        self.re_calculate_points()

    def edges(self):
        #Checking for the whether the ship is within the screen
        if self.pos.x - self.r > self.S_WIDTH:
            self.pos.x = -self.r
        elif self.pos.x + self.r < 0:
            self.pos.x = self.S_WIDTH + self.r

        if self.pos.y - self.r > self.S_HEIGHT:
            self.pos.y = -self.r
        elif self.pos.y + self.r < 0:
            self.pos.y = self.S_HEIGHT + self.r

        #Calculating the points again
        self.re_calculate_points()

    def new_laser(self):
        velocity = self.forward_velocity()
        laser = Laser(self.points[0], velocity)

        self.lasers.append(laser)

    def shoot(self):
        #Shooting new lasers
        self.new_laser()

    def run_lasers(self, surface, asteroids):
        for laser in self.lasers[:]:
            laser.move()
            laser.show(surface)

            #Removing the laser if it is offscreen
            if laser.offscreen(self.S_WIDTH, self.S_HEIGHT):
                self.lasers.remove(laser)
            else:
                #Breaking the asteroid into small parts if it is shot by the laser
                for asteroid in asteroids[:]:
                    if asteroid.is_hit(laser.pos, True):
                        broken_pieces = asteroid.break_up()
                        asteroids.extend(broken_pieces)
                        asteroids.remove(asteroid)
                        self.lasers.remove(laser)
                        break

    def collides(self, asteroids):
        #Checking if the ship is colliding with the asteroid
        for point in self.points:
            for asteroid in asteroids:
                if asteroid.is_hit(point):
                    return True

        return False
