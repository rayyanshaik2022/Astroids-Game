from pygame.math import Vector2 as Vector
import math
import random
import pygame
from settings import *

class Game():

    def __init__(self, rockets : list, total_asteroids : int ):
        
        self.rockets = rockets
        self.total_asteroids = total_asteroids
        self.asteroids = []

    def update_collisions(self):
        for rocket in self.rockets:
            for asteroid in self.asteroids:
                if math.hypot(rocket.pos.x-asteroid.pos.x, rocket.pos.y-asteroid.pos.y) < asteroid.size + Rocket.RADIUS*0.8:
                    rocket.alive = False
                    self.asteroids.remove(asteroid)
                    continue

    def update_astroids(self):

        # Spawn new asteroids
        SPAWN_RAD = WIDTH//2
        while len(self.asteroids) < self.total_asteroids:
            spawn_angle = random.random()*2 * math.pi*2
            self.asteroids.append(
                # make it so that they spawn properly in a circlurar area and have a target that a is apoint on a smaller circle somewhere      
                Asteroid(
                    (SPAWN_RAD*math.cos(spawn_angle)+WIDTH//2,SPAWN_RAD*math.sin(spawn_angle)+WIDTH//2), random.randint(5,60), random.randint(6,11),
                    random.random()*2 +1
                )
            )
        
        for asteroid in self.asteroids:
            asteroid.pos.x += asteroid.speed * math.cos(asteroid.direction)
            asteroid.pos.y += asteroid.speed * math.sin(asteroid.direction)

            if asteroid.pos.x < 0-asteroid.size or asteroid.pos.y-asteroid.size < 0 or \
                asteroid.pos.x >= WIDTH+asteroid.size or asteroid.pos.y >= HEIGHT+asteroid.size:

                self.asteroids.remove(asteroid)
                continue

    def update_rockets(self):

        for rocket in self.rockets:
            
            rocket.pos += rocket.velocity

            # Teleport across if out of bounds
            if rocket.pos.x >= WIDTH:
                rocket.pos.x = 0
            if rocket.pos.x < 0:
                rocket.pos.x = WIDTH
            if rocket.pos.y >= HEIGHT:
                rocket.pos.y = 0 
            if rocket.pos.y < 0:
                rocket.pos.y = HEIGHT

            rocket.velocity.x += rocket.acceleration * math.cos(rocket.direction)
            rocket.velocity.y += rocket.acceleration * math.sin(rocket.direction)
            
            if rocket.velocity.magnitude() > Rocket.MAX_SPEED:
                rocket.velocity.scale_to_length(Rocket.MAX_SPEED)

class Asteroid():

    def __init__(self, pos, size, sides, speed, point_error=0.3):

        self.pos = Vector(*pos)
        self.speed = speed
        self.acceleration = 0
        self.direction = (random.random()*2 -1) * math.pi 

        self.size = size
        self.point_error = point_error

        self.polygon = self.generate_polygon(size, sides)
    
    def generate_polygon(self, size, n):

        points = []
        
        current_rotation = 0

        for i in range(n):
            angle = current_rotation + (random.random()*2-1)*self.point_error
            points.append( [self.size * math.cos(angle), self.size * math.sin(angle)] )
            current_rotation += 2*math.pi/n
        
        return points

    def current_polygon(self):

        points = []

        for p in self.polygon:
            new_p = [p[0]*math.cos(self.direction) - p[1]*math.sin(self.direction), p[0]*math.sin(self.direction)+p[1]*math.cos(self.direction)]
            new_p[0] += self.pos.x; new_p[1] += self.pos.y
            points.append(new_p)
        
        return points
    
    def draw(self, screen):

        pygame.gfxdraw.aapolygon(screen, self.current_polygon(), COLORS['white'])
        
class Rocket():

    MAX_SPEED = 4
    ACCELERATION = 0.15

    RADIUS = 25
    ANGLE_A = 2.2
    ANGLE_B = 2.5
    ROTATION_RATE = 50

    def __init__(self, pos : tuple):

        self.pos = Vector(*pos)
        self.velocity = Vector(0,0)
        self.acceleration = 0
        self.direction = math.pi

        self.alive = True
    
    def calculate_polygon(self):

        point1 = [0,Rocket.RADIUS]

        point2 = [Rocket.RADIUS*math.cos(Rocket.ANGLE_A), Rocket.RADIUS*math.sin(-Rocket.ANGLE_B)]

        point3 = [0, -Rocket.RADIUS/4]

        point4 = [-Rocket.RADIUS*math.cos(Rocket.ANGLE_A), Rocket.RADIUS*math.sin(-Rocket.ANGLE_B)]

        points = [point1, point2, point3, point4]
        translated_points = []


        for p in points:
            a = [p[0]*math.cos(self.direction-math.pi/2) - p[1]*math.sin(self.direction-math.pi/2), p[0]*math.sin(self.direction-math.pi/2)+p[1]*math.cos(self.direction-math.pi/2)]
            a[0] += self.pos.x; a[1] += self.pos.y
            translated_points.append(a)

        return translated_points
    
    def draw(self, screen):
        pygame.draw.polygon(screen, COLORS['background'], self.calculate_polygon())
        pygame.gfxdraw.aapolygon(screen, self.calculate_polygon(), COLORS['white'])

    # Draw method

class Bullet():

    SPEED = 5
    SIZE = 3

    def __init__(self, pos, direction):

        self.pos = Vector(*pos)
        self.speed = Bullet.SPEED
        self.direction = direction

        self.size = size

    def draw(self, screen):
        pass