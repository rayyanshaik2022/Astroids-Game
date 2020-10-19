import pygame
import pygame.gfxdraw
from game import *
from settings import *
import random
from effects import *
from network import *

p = Population(pop_size=25, generations=15, lifespan=30, mutation_chance=0.15, mutation_rate=0.2)
p.train()
agent = p.population[0]

key = input("Ready to start visualization? ")

class Gui:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

    def new(self):
        font = '.\Fonts\-Nasalization-Regular.ttf'
        self.font_medium = pygame.font.Font(font, 35)

        self.game = Game(Rocket((400,400)), 0.2, 15)
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

        self.game.controller(
            (agent.get_move(self.game.rocket, self.game.rocket.closest_obstacles(self.game.asteroids)))
        )

        self.game.update()
    
        effects = self.game.update_collisions()

        for p in effects['particles']:
            for i in range(7):
                self.particles.add(
                    Particle(p, direction=(random.random() * 2*math.pi), decay=0.4, speed=(random.random()*3))
                    )

        self.particles.update()

    def draw(self):
        self.screen.fill(COLORS['background'])

        
        r = self.game.rocket
        
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

        # Draw texts
        text = self.font_medium.render(f"Score: {r.score}", True, COLORS['white'])
        self.screen.blit(text, (20,10))

        pygame.display.flip()

    def events(self):
        # catch all events here
        keys_pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    print(agent.get_state(self.game.rocket, self.game.rocket.closest_obstacles(self.game.asteroids)))
        
        r = self.game.rocket
        if keys_pressed[pygame.K_RIGHT]:
            self.game.controller(Game.TURN_RIGHT)
        if keys_pressed[pygame.K_LEFT]:
            self.game.controller(Game.TURN_LEFT)
        if keys_pressed[pygame.K_UP]:
            self.game.controller(Game.THRUST)
        else:
            r.acceleration = 0
        if keys_pressed[pygame.K_SPACE]:
            self.game.controller(Game.SHOOT)


# create the game object
g = Gui()
g.new()
g.run()