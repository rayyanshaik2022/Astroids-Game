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
        self.game = Game([Rocket((400,400))], 0.2, 25)
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
        self.game.update_bullets()
        effects = self.game.update_collisions()

        for p in effects['particles']:
            for i in range(7):
                self.particles.add(
                    Particle(p, direction=(random.random() * 2*math.pi), decay=0.4, speed=(random.random()*3))
                    )

        self.particles.update()

    def draw(self):
        self.screen.fill(COLORS['background'])

        
        r = self.game.rockets[0]
        
        # Adds new particles if accerating
        if r.acceleration != 0: 
            self.particles.add(
                Particle(r.pos, direction=(math.pi+r.direction), decay=0.9, speed=3)
            )

        # Draws all particles
        self.particles.draw(self.screen)

        # Draws the rocket
        r.draw(self.screen)

        # Draws all astroids
        for a in self.game.asteroids:
            a.draw(self.screen)

        # Draw all of the rocket's bullets
        for b in r.bullets:
            b.draw(self.screen)

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
        if keys_pressed[pygame.K_SPACE]:
            if r.shoot_countdown < 0 and len(r.bullets) < Rocket.MAX_BULLETS:
                r.shoot_countdown = Rocket.SHOOTER_DELAY
                r.bullets.append(
                    Bullet([r.pos.x, r.pos.y], r.direction)
                )


# create the game object
g = Gui()
g.new()
g.run()