import pygame
import pygame.gfxdraw
from game import *
from settings import *
import random
from effects import *


class Gui:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

    def new(self):
        self.game = Game([Rocket((400,400))], 10)
        self.particles = ParticleManager(["#FFFACC","#FFEACC","#FFD7CC","#FFCDCC","#FFD5AD"])


    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000 # Controls update speed (FPS per second)
            self.events()
            self.update()
            self.draw()

    def close(self):
        pygame.quit()
        quit()

    def update(self):

        pygame.display.set_caption(f"{TITLE} | FPS {round(self.clock.get_fps(),2)}")
        
        self.game.update_rockets()
        self.game.update_astroids()
        self.game.update_collisions()
        self.particles.update()

    def draw(self):
        self.screen.fill(COLORS['background'])

        # Draw rockets
        r = self.game.rockets[0]
        
        if r.acceleration != 0:
            
            self.particles.add(
                Particle(r.pos, direction=(math.pi+r.direction), decay=0.9, speed=3)
            )

        self.particles.draw(self.screen)
        r.draw(self.screen)
        for a in self.game.asteroids:
            a.draw(self.screen)

        pygame.display.flip()

    def events(self):
        # catch all events here
        keys_pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()
        
        r = self.game.rockets[0]
        if keys_pressed[pygame.K_RIGHT]:
            r.direction += math.pi/Rocket.ROTATION_RATE
        if keys_pressed[pygame.K_LEFT]:
            r.direction -= math.pi/Rocket.ROTATION_RATE
        if keys_pressed[pygame.K_UP]:
            r.acceleration = Rocket.ACCELERATION
        else:
            r.acceleration = 0


# create the game object
g = Gui()
g.new()
g.run()