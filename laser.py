import pygame

class Laser:
    def __init__(self, pos, vel):
        #Setting position and the velocity
        self.pos = pygame.math.Vector2(pos.x, pos.y)
        self.vel = vel
        self.r = 2

    def show(self, surface):
        #Drawing a circle representing the laser
        pygame.draw.circle(surface, (255, 255, 255), (int(self.pos.x), int(self.pos.y)), self.r)

    def move(self):
        #Updating position according to the velocity
        self.pos += self.vel

    def offscreen(self, width, height):
        #Checking if the laser is offscreen
        return (self.pos.x + self.r > width or
                self.pos.x - self.r < 0 or
                self.pos.y + self.r > height or
                self.pos.y - self.r < 0)
