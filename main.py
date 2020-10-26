from ship import *
from asteroid import *

width = 600
height = 600

#Initializing pygame and setting the screen
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Asteroids')

clock = pygame.time.Clock()
FPS = 60

def generateAsteroids(n):
    asteroids = []

    for i in range(n):
        asteroid = Asteroid(width, height)
        asteroids.append(asteroid)

    return asteroids

def update(surface):
    global running

    n = 2
    ship = Ship(width, height)
    asteroids = generateAsteroids(n)
    running = True

    def redraw():
        global running

        surface.fill((0, 0, 0))

        #Moving and showing the asteroids
        for asteroid in asteroids:
            asteroid.move()
            asteroid.edges()
            asteroid.show(surface)

        #Moving and showing the ship
        ship.update()
        ship.move()
        ship.edges()
        ship.show(surface, asteroids)

        #If it collides with an asteroid the game is over
        #So running will now become false
        if ship.collides(asteroids):
            running = False

        pygame.display.update()

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    #Shooting if the space key is pressed
                    ship.shoot()

        #Redrawing the window everytime
        redraw()

        #If there are no asteroids add the double amount of asteroids to the game
        if len(asteroids) == 0:
            n *= 2
            asteroids = generateAsteroids(n)

def menu(surface):
    font = pygame.font.SysFont('comicsans', 50)
    label = font.render('Press any key to play', 1, (255, 255, 255))
    cx = width//2 - label.get_width()//2
    cy = height//2 - label.get_height()//2

    while True:
        surface.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                #If any key is pressed then start the game
                update(surface)

        #Render the text on the screen
        surface.blit(label, (cx, cy))

        pygame.display.update()

#Calling the menu function
menu(screen)
