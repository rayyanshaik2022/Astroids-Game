from pygame.math import Vector2 as Vector
import pygame
import random
import math

class ParticleManager:
    def __init__(self, colors):

        self.particles = []
        self.colors = colors
    
    def update(self):
        for p in self.particles:
            p.update()
    
    def draw(self, screen):
        for p in self.particles:
            p.draw(screen)

    def add(self, particle):
        if self.colors:
            particle.color = random.choice(self.colors)
        self.particles.append(particle)



class Particle:
    def __init__(self, pos : tuple, color="#FFFFFF", size=4, shape='square', direction=0, speed=5, decay=0.05):

        self.pos = Vector(*pos)

        self.color = color
        self.size = size
        self.shape = shape
        self.direction = direction
        self.speed = 5
        self.decay = decay
        self.alive = True

        self.direction_error = 1.1
        self.direction = self.direction + (random.random()*2-1)*self.direction_error
    
    def update(self):

        if not self.alive:
            return

        if self.speed <= 0:
            self.alive = False
            return

        self.speed -= self.decay
        
        self.pos.x += self.speed * math.cos(self.direction)
        self.pos.y += self.speed * math.sin(self.direction)
    
    def draw(self, screen):

        if not self.alive:
            return

        if self.shape == "square":
            pygame.draw.rect(
                screen, 
                self.color,
                (self.pos.x - self.size//2, self.pos.y - self.size//2, self.size, self.size)
            )